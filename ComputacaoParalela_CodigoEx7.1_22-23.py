from mpi4py import MPI
import numpy as np
import sys

import time

start = time.time()

def eliminacao_gauss(piv, piv_A, linhA, piv_B, linhB):
    #Calculo da eliminação de Gauss pela fórmula dada na aula 
    for k in range(piv+1,n):
        linhA[k]=linhA[k]-((linhA[piv]*piv_A[k])/piv_A[piv])
    linhB=linhB-((linhA[piv]*piv_B)/piv_A[piv])
    
    #Colocar zeros debaixo do pivot
    for i in range(piv+1):
        linhA[i]=0
    #Devolve as novas linhas
    return linhA,linhB

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
mp= MPI.COMM_WORLD.Get_size() 

#Recebe a dimensão do x
n = int(sys.argv[1])

if rank==0:
    #Cria o vetor que vai guardar a solução como um vetor vazio
    x=np.empty(n).reshape((n,1))

    #Estabelece as matrizes que se vão resolver
    a=np.random.rand(n**2).reshape((n,n))
    b=np.random.rand(n)
    
    #Criação do espaço para as matrizes que guardam os valores
    A = np.empty([n,n])
    B = np.empty(n)
    
    #Copia-se a matriz a e b para não perder os valores nos cálculos
    for p in range(n):
        B[p] = b[p]
        for q in range(n):
            A[p,q] = a[p,q]
else:
    a = None
    b = None
    A = None
    B = None

#Eliminação de Gauss
for piv in range(n):
    if rank==0:
        #Verifica se o pivot não é zero
        if a[piv,piv] == 0.0:
            sys.exit('ERRO: Pivot igual a zero!')

        #determina e guarda o número de equações a guardar por processador
        #número de equações que falta calcular: n-piv-1, n total, piv equação onde vamos 
        div = (n-piv-1)//mp 
        resto = (n-piv-1)%mp
        n_por_processador = [div for r in range(mp)]
        
        #Variavel que vai guardar a posição da linha onde começar para cada processador 
        linha = np.empty(mp, int) 
        linha[0] = piv+1
        
        #Dividir o possivel resto pelos processadores e estabelecer em que linha cada processador irá começar
        for p in range(1, mp):
            if resto!=0:
                n_por_processador[p] = div+1
                resto = resto-1
            #a linha onde começa será igual à linha do processador anterior mais o número de linhas em que esse trabalhará
            linha[p] = linha[p-1] + n_por_processador[p-1] 
        
        #Informação a enviar a cada processador
        for p in range(1,mp):
            #Envia as linhas principais de a e b para p
            comm.Send(a[piv],dest=p) 
            comm.send(b[piv],dest=p) 
        
            #Envio da linha onde começar e quantas trabalhar
            comm.send(linha[p], dest=p)
            comm.send(n_por_processador[p], dest=p)
            
            #Envio das linhas abaixo da principal de a e b
            for l in range(linha[p], linha[p]+n_por_processador[p]):
                comm.Send(a[l],dest=p) 
                comm.send(b[l],dest=p)
                
        #Master faz a eliminacao de Gauss das linhas a seu cargo
        for l in range(linha[0], linha[0]+n_por_processador[0]):
            a[l], b[l] = eliminacao_gauss(piv, a[piv], a[l], b[piv], b[l])
        
        #Master recebe resultados dos slaves
        for p in range(1,mp):
            for l in range(linha[p], linha[p]+n_por_processador[p]):
                comm.Recv(a[l], source=p)
                b[l] = comm.recv(source=p)
                
    else:
        #p cria espaço e recebe linha principal de a
        piv_A = np.empty(n)
        comm.Recv(piv_A, source=0)
        
        #p recebe a linha principal de b
        piv_B = comm.recv(source=0)
       
        #p recebe informação: indice da linha onde começar e quantas linhas tem de fazer
        linha = comm.recv(source=0)
        n_por_processador= comm.recv(source=0)
       
        #p cria espaço e recebe restantes linhas a serem calculadas de a e b
        linhA = np.empty([n_por_processador,n])
        linhB = np.empty(n_por_processador)
        for l in range(n_por_processador):
            comm.Recv(linhA[l], source=0)
            linhB[l] = comm.recv(source=0)
            
            #p aplica a eliminacao de Gauss
            linhA[l], linhB[l] = eliminacao_gauss(piv, piv_A, linhA[l], piv_B, linhB[l])
            
            #p envia os resultados obtidos para o master
            comm.Send(linhA[l], dest=0)
            comm.send(linhB[l], dest=0)

#Master analisa resultados
if rank==0:
    #Faz o cálculo da solução com a fórmula pretendida
    x[n-1] = b[n-1]/a[n-1][n-1]
    for piv in range(n-2,-1,-1):
        x[piv] = b[piv]
        for j in range(piv+1,n):
            x[piv] = x[piv] - a[piv,j]*x[j]
        x[piv] = x[piv]/a[piv,piv]

    check = np.matmul(A,x) #cálculo de verificação
    
    #Apresenta os resultados
    print ('A :\n%s' % A)
    print ('solução X :\n%s' % x)
    print ('b inicial :\n%s' % B)
    print ('A*x :\n%s' % check)
    
"função utilizada para medir o tempo de execução"
end = time.time()
print('Time: ',end - start, 's')  

"""
Resultado obtido:
    
A :
[[0.1249328  0.11233403 0.21958717 0.21395581 0.64734816 0.85388862
  0.72448911 0.21089919 0.2637745  0.42825091 0.05769101 0.24439531
  0.94114489 0.9683729  0.22844093 0.64998044]
 [0.47392961 0.40842128 0.08849044 0.94118454 0.88079484 0.14159801
  0.51631048 0.04406856 0.10311412 0.93568249 0.30572956 0.41363997
  0.99422438 0.17793364 0.08014464 0.19701529]
 [0.00265635 0.82312047 0.78355357 0.67611784 0.70678089 0.64420611
  0.18739693 0.7303203  0.62590545 0.42224649 0.12509139 0.60714004
  0.56560334 0.67010707 0.62326741 0.89553205]
 [0.49892049 0.84991833 0.99111859 0.1995061  0.89776324 0.36340433
  0.96787779 0.22461099 0.06310015 0.33342337 0.06877967 0.65365935
  0.73147544 0.30461491 0.12740834 0.45903349]
 [0.76299831 0.77578269 0.28311545 0.32428896 0.987099   0.82025992
  0.93574345 0.70272663 0.91555315 0.69454895 0.56770135 0.07694336
  0.14713212 0.65435125 0.01772136 0.18663259]
 [0.98541626 0.56979766 0.19759369 0.58114674 0.09161142 0.74582808
  0.65681302 0.78206695 0.87583062 0.36039137 0.26603294 0.31245687
  0.3539808  0.41286164 0.41853329 0.01585211]
 [0.09033849 0.83836998 0.10704451 0.6909345  0.56342423 0.0690017
  0.59561812 0.33761936 0.24174223 0.17045741 0.46686486 0.86244988
  0.07091113 0.40945209 0.9188601  0.85563888]
 [0.24849426 0.99350869 0.24342794 0.35910233 0.14238866 0.68910779
  0.88540278 0.44514478 0.65933262 0.05453367 0.68556578 0.01930097
  0.54042995 0.41858891 0.30307038 0.05530348]
 [0.32461203 0.14373615 0.53987316 0.07396813 0.85267307 0.68440731
  0.880453   0.0737537  0.87311422 0.27338869 0.70183512 0.58905245
  0.48431847 0.62769089 0.1793001  0.29276341]
 [0.88792197 0.75578626 0.0754439  0.06284612 0.8904725  0.33809067
  0.37312366 0.75724689 0.21075634 0.06930831 0.44330162 0.0495308
  0.19752009 0.15136638 0.42083159 0.41220335]
 [0.3788749  0.76357603 0.25754901 0.71792281 0.70983395 0.07413643
  0.21853786 0.08056595 0.73613601 0.19164241 0.06937843 0.28521052
  0.18729789 0.87337883 0.85918313 0.37873624]
 [0.47141659 0.02003511 0.01783762 0.07786637 0.53075429 0.74990466
  0.59931195 0.25971195 0.41272502 0.67802721 0.76992618 0.50229464
  0.15914883 0.06102    0.48949886 0.12643012]
 [0.40717007 0.93724791 0.19266594 0.98173569 0.66162774 0.06031183
  0.99731696 0.53693191 0.56617456 0.77085524 0.59133678 0.24888171
  0.65864836 0.91909603 0.5838693  0.53910403]
 [0.42692379 0.22532111 0.26528688 0.68636028 0.22764289 0.25721079
  0.43652013 0.51096081 0.57535425 0.72635066 0.88157186 0.13313662
  0.88578039 0.7698118  0.09420118 0.72781886]
 [0.16164088 0.3651714  0.98963744 0.08264152 0.1082724  0.21367943
  0.71064386 0.40812265 0.89748761 0.63097796 0.32722344 0.15164527
  0.64646978 0.90536798 0.37404588 0.34528449]
 [0.39149317 0.62485261 0.16416631 0.41857689 0.76329352 0.41867518
  0.42724272 0.86894644 0.43030463 0.05720089 0.55531679 0.9008025
  0.373272   0.40260913 0.48665301 0.17891766]]
solução X :
[[ 0.23340021]
 [-1.27377373]
 [ 1.35413415]
 [ 0.68602028]
 [ 0.58127235]
 [-0.14107104]
 [ 0.29563929]
 [ 0.29374854]
 [-0.15533565]
 [-0.55718155]
 [ 0.78143322]
 [-1.1634002 ]
 [ 0.15534243]
 [-0.75911272]
 [ 1.32461001]
 [ 0.23699322]]
b inicial :
[0.21106179 0.40601293 0.74281073 0.59316478 0.15561426 0.34965048
 0.51420073 0.30777109 0.83634162 0.98081521 0.54271042 0.85041483
 0.62509408 0.90832058 0.9108892  0.29771239]
A*x :
[[0.21106179]
 [0.40601293]
 [0.74281073]
 [0.59316478]
 [0.15561426]
 [0.34965048]
 [0.51420073]
 [0.30777109]
 [0.83634162]
 [0.98081521]
 [0.54271042]
 [0.85041483]
 [0.62509408]
 [0.90832058]
 [0.9108892 ]
 [0.29771239]]
Time:  0.0312 s
"""