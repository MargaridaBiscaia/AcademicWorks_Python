from mpi4py import MPI
import sys
import math
from time import time

def create_grid(y):
    tstart = time() #inicializamos o tempo
    
    pe = 0 #pontos equidistantes
    
    x = 0 + (grid/2) #inicializa a gride em x (em y já foi feito)
    
    #Vai fazer este processo para todos os intervalos da gride, primeiro para a direita e depois para cima
    for i in range(m//MPI.COMM_WORLD.Get_size()):
        for j in range(m):
            d = (x ** 2) + (y ** 2) #verificar se os pontos estão dentro do círculo 
            if d <=1:  
               pe += 1 #se sim, adiciona o ponto
            else:
                break #senão acaba o ciclo
                       
            x = x + grid #anda para a direita na gride
            j += 1 #guarda que já andámos um passo para a direita
            
        #depois de terminar a direita, vamos para cima:
        y += grid #anda para cima na grid
        i += 1 #guarda que já andámos um passo para cima
        
        #o ponto em x vai novamente para o início da grid 
        x = 0 + (grid/2)
        j = 0
        
        tend = time() #terminamos o tempo
        T = tend - tstart
        
    return (pe, T)  #devolve o número de pontos dentro do círculo e o tempo que demorou


n = int(sys.argv[1])

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

m = int(math.sqrt(n)) #m: dimensão da grid n = m x m
grid = 1 / m #intervalo entre unidades da grid 

yp= 1/MPI.COMM_WORLD.Get_size() #divide o eixo Oy pelos diferentes processadores

#guardamos o ymin em que cada processador deve começar
ymin = {}
ymin[0] = 0 + (grid/2)

mp = 0

#o ymin de cada um deve ser o ymin do anterior mais o número de linhas que cada um deve fazer
for mp in range(1, MPI.COMM_WORLD.Get_size()):
    ymin[mp] = ymin[mp -1] + yp
    
if int(math.sqrt(n) + 0.5) ** 2 == n: #verificar se n é quadrado perfeito para podermos construir a grid
   pe = create_grid(ymin[rank]) #cada processador realiza a sua experiência
    
   j = 0
   #Master analisa os resultados
   if rank == 0:
       print ('Number of processes:', MPI.COMM_WORLD.Get_size())
       j = pe[0]
       print('On process', rank, 'result is', pe[0])
       print('On process', rank, 'time is', pe[1])  #imprime o resultado obtido no Master
       
       for p in range(1, MPI.COMM_WORLD.Get_size()):
           pep = comm.recv(source = p) #recebe os resultados dos outros processadores e imprime-os
           print('On process', p, 'result is', pep)
           
           j += pep[0] #soma os resultados de cada processador
           print('On process', p, 'result is', pep[0])
           print('On process', p, 'time is', pep[1])
       
       print('pi = ', 4*(j/n))
       r = j/n
       error = math.sqrt((r*(1-r))/n) 
       print('erro relativo = ', error)

   else:
       comm.send(pe, dest=0) #envia o resultado obtido ao Master

else:
    print('O número que inseriu não é um quadrado perfeito. Insira outro n.')
    
"""
O resultado obtido foi:

Number of processes: 8
On process 0 result is 12467380
On process 0 time is 23.34644103050232
On process 1 result is (12269712, 23.21973490715027)
On process 1 result is 12269712
On process 1 time is 23.21973490715027
On process 2 result is (11864471, 23.14875340461731)
On process 2 result is 11864471
On process 2 time is 23.14875340461731
On process 3 result is (11229029, 22.182560443878174)
On process 3 result is 11229029
On process 3 time is 22.182560443878174
On process 4 result is (10320526, 21.309496641159058)
On process 4 result is 10320526
On process 4 time is 21.309496641159058
On process 5 result is (9055924, 19.329967260360718)
On process 5 result is 9055924
On process 5 time is 19.329967260360718
On process 6 result is (7245140, 15.564546346664429)
On process 6 result is 7245140
On process 6 time is 15.564546346664429
On process 7 result is (4087665, 9.564660549163818)
On process 7 result is 4087665
On process 7 time is 9.564660549163818
pi =  3.14159388
erro relativo =  4.105456287937544e-05

Era de esperar que o tempo diminuísse, tendo em conta que
o ciclo termina mais cedo quanto maior for o ymin (uma vez que o maior ymin corresponde ao processador de maior "grau"), 
e foi o observado

"""
