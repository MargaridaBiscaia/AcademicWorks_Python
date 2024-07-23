from mpi4py import MPI
import math
import sys
import time

start = time.time()

def create_grid(y):
    pe = 0 #pontos equidistantes
    
    x = -1 + (grid/2) #Inicializa a gride em x (em y já foi feito)
    
    #Vai fazer este processo para todos os intervalos da gride, primeiro para a direita e depois para cima
    for i in range(m//MPI.COMM_WORLD.Get_size()):
        for j in range(m):
            d = (x ** 2) + (y ** 2) #verificar se os pontos estão dentro do círculo 
            if d <=1:  
               pe += 1 #se sim, adiciona o ponto
               
           
            x = x + grid #anda para a direita na gride
            j += 1 #guarda que já andámos um passo para a direita
            
        #depois de terminar a direita, vamos para cima:
        y += grid #anda para cima na grid
        i += 1 #guarda que já andámos um passo para cima
        
        #o ponto em x vai novamente para o início da grid 
        x = -1 + (grid/2)
        j = 0
        
    return pe  #devolve o número de pontos dentro do círculo

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

n = int(sys.argv[1])

m = int(math.sqrt(n)) #m: dimensão da grid n = m x m
grid = 2 / m #intervalo entre unidades da grid 


yp= 2/MPI.COMM_WORLD.Get_size() #divide o eixo Oy pelos diferentes processadores

#guardamos o ymin em que cada processador deve começar
ymin = {}
ymin[0] = -1 + (grid/2)

mp = 0

#o ymin de cada um deve ser o ymin do anterior mais o número de linhas que cada um deve fazer
for mp in range(1, MPI.COMM_WORLD.Get_size()):
    ymin[mp] = ymin[mp -1] + yp
    
if int(math.sqrt(n) + 0.5) ** 2 == n: #verificar se n é quadrado perfeito para podermos construir a grid
   pe = create_grid(ymin[rank]) #cada processador realiza a sua experiência
    
    #Master analisa os resultados
   if rank == 0:
       print ('Number of processes:', MPI.COMM_WORLD.Get_size())
       print('On process', rank, 'result is', pe)  #imprime o resultado obtido no Master
       for p in range(1, MPI.COMM_WORLD.Get_size()):
            pep = comm.recv(source = p) #recebe os resultados dos outros processadores e imprime-os
            print('On process', p, 'result is', pep)
            pe += pep #soma os resultados de cada processador
        
        
       print('pi = ', 4*(pe/n))
       r = pe/n
       error = math.sqrt((r*(1-r))/n) 
       print('erro relativo = ', error)

   else:
       comm.send(pe, dest=0) #envia o resultado obtido ao Master

else:
    print('O número que inseriu não é um quadrado perfeito. Insira outro n.')
    
    
"função utilizada para medir o tempo de execução"
end = time.time()
print('Time: ',end - start, 's')     

"""
O resultado obtido foi:
    
Number of processes: 8
On process 0 result is 5666408
On process 1 result is 9688230
On process 2 result is 11546734
On process 3 result is 12368556
On process 4 result is 12368556
On process 5 result is 11546734
On process 6 result is 9688230
On process 7 result is 5666408
pi =  3.14159424
erro relativo =  4.1054556622855694e-05
Time:  0m27s 

Como era de esperar, este tempo foi inferior ao tempo utilizando o "single core"
"""




