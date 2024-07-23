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
        #mete o maior número da coluna na diagonal e guarda o pivot como sendo o que está na linha em que estamos a trabalhar
        pivot = piv
        for p in range(piv,n):
            #descobre o maior elemento da coluna i
            if(abs(a[p,piv])>abs(a[pivot,piv])):
                pivot = p
        
        #se o valor da diagonal não for o maior dessa coluna
        if pivot>piv:
            #troca as linhas de a e b para que o maior fique na diagonal
            auxA = np.empty(n)
            auxB = np.empty(n)
            for j in range(n):
                auxA[j]=a[piv][j]
                a[piv][j] = a[pivot][j]
                a[pivot][j] = auxA[j] 
            auxB = b[piv]
            b[piv] = b[pivot]
            b[pivot] = auxB
        
        #Verifica se o pivot é zero
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
[[0.72678282 0.89533545 0.26863973 0.51615858 0.94741809 0.59442199
  0.57576985 0.75694519 0.31692125 0.25507564 0.53909062 0.97574667
  0.33221377 0.01388494 0.61384043 0.61925897]
 [0.615208   0.88086575 0.37269346 0.63330956 0.03815951 0.8775138
  0.19089474 0.38694089 0.96144469 0.15773441 0.00648467 0.06475308
  0.34722708 0.6871463  0.18197375 0.4727413 ]
 [0.91324696 0.644511   0.21739226 0.21687082 0.16103488 0.51738862
  0.40780492 0.85427941 0.77790098 0.93833277 0.67138901 0.58335613
  0.08550881 0.60426081 0.19504833 0.93874147]
 [0.8452446  0.60915683 0.62770904 0.0122262  0.96780119 0.83101555
  0.9821815  0.63324497 0.62043076 0.07028754 0.98624405 0.9593996
  0.6042671  0.16952303 0.89110608 0.13657909]
 [0.87783952 0.33634291 0.91392205 0.56886424 0.92863784 0.90530317
  0.92479316 0.57427458 0.43290705 0.23938507 0.19619636 0.15301615
  0.98008163 0.75808579 0.33888884 0.04769925]
 [0.80447272 0.10148296 0.50882686 0.50089688 0.08325325 0.35373583
  0.44087639 0.09915971 0.95591593 0.82699288 0.99833707 0.68401976
  0.07445111 0.80041273 0.38790627 0.70256911]
 [0.80156916 0.53842654 0.41698306 0.72298539 0.15101655 0.11847613
  0.73648037 0.78285618 0.50492932 0.75804665 0.87557728 0.04142717
  0.4823769  0.94506552 0.34351704 0.07936729]
 [0.31956221 0.59816417 0.87167227 0.24211149 0.288346   0.47292296
  0.62088537 0.37158283 0.67855672 0.82241813 0.1880111  0.28730928
  0.0935838  0.92303207 0.43965231 0.18499642]
 [0.05662358 0.20716222 0.09304777 0.67229142 0.27961113 0.32623694
  0.99193024 0.61762846 0.59094529 0.55729694 0.69989005 0.7807063
  0.10033111 0.35716411 0.95133189 0.44040221]
 [0.53249742 0.90440989 0.19378195 0.74066613 0.37128986 0.52104801
  0.49648697 0.84440133 0.18811792 0.18282    0.90808532 0.84558353
  0.44190162 0.30162144 0.55822569 0.85683904]
 [0.79196684 0.35497485 0.68600536 0.13078005 0.07453554 0.23093094
  0.25892795 0.76419277 0.14815474 0.82626981 0.12400948 0.92424733
  0.82476584 0.79608264 0.12419512 0.33280777]
 [0.27740854 0.9053251  0.0666634  0.30425038 0.90191481 0.85606465
  0.10740075 0.63544361 0.00693314 0.96581024 0.77241337 0.27173518
  0.85643329 0.55895644 0.5546796  0.97653295]
 [0.81687295 0.82921468 0.06213769 0.64879518 0.92834269 0.27393943
  0.73316323 0.2908465  0.9847547  0.95958731 0.10348623 0.53477433
  0.1815333  0.62172781 0.39646483 0.00182288]
 [0.85985231 0.58833495 0.86809538 0.41922807 0.95955167 0.61312124
  0.45507059 0.05090535 0.13033228 0.63025103 0.8261541  0.97663877
  0.76122645 0.67229126 0.33376991 0.48830156]
 [0.66846945 0.56325207 0.65979082 0.89760447 0.98571112 0.38985789
  0.93582294 0.77621954 0.91184499 0.37385902 0.96977629 0.43902167
  0.52120329 0.55036023 0.18967433 0.5224492 ]
 [0.12740776 0.60409657 0.97882411 0.59213074 0.36775965 0.68883439
  0.93544904 0.24263022 0.46806399 0.48266232 0.81511864 0.96521167
  0.9576391  0.63321698 0.49822357 0.35541456]]
solução X :
[[-2.82041769]
 [-1.68908427]
 [-2.42834881]
 [ 1.61170915]
 [ 1.61258622]
 [ 6.94797941]
 [-3.47699457]
 [ 3.46466242]
 [-0.70096036]
 [ 0.01466959]
 [ 2.99873719]
 [ 3.88900213]
 [-3.76135111]
 [ 3.62454322]
 [-4.54287763]
 [-6.20359515]]
b inicial :
[0.25923904 0.75286234 0.46296722 0.89687366 0.32456838 0.03036704
 0.20279008 0.30748018 0.34870756 0.57399275 0.21267296 0.85651398
 0.52121775 0.77161561 0.6549108  0.26674661]
A*x :
[[0.25923904]
 [0.75286234]
 [0.46296722]
 [0.89687366]
 [0.32456838]
 [0.03036704]
 [0.20279008]
 [0.30748018]
 [0.34870756]
 [0.57399275]
 [0.21267296]
 [0.85651398]
 [0.52121775]
 [0.77161561]
 [0.6549108 ]
 [0.26674661]]
"""