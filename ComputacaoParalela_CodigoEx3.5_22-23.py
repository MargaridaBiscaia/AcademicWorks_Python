from mpi4py import MPI
import sys
import math
from time import time

def create_grid(y, y2):
    tstart = time() #inicializamos o tempo
    
    pe = 0 #pontos equidistantes
    
    x = 0 + (grid/2) #inicializa a gride em x (em y já foi feito)
    
    while(y < y2): #enquanto o y for menor que o y do outro processador, fazemos
        for j in range(m):
            d = (x ** 2) + (y ** 2) #verificar se os pontos estão dentro do círculo 
            if d <= 1:  
               pe += 1 #se sim, adiciona o ponto
            else:
                break
                       
            x = x + grid #anda para a direita na gride
            j += 1 #guarda que já andámos um passo para a direita
            
        #depois de terminar a direita, vamos para cima:
        y += grid #anda para cima na grid
        
        #o ponto em x vai novamente para o início da grid 
        x = 0 + (grid/2)
        j = 0
        
        tend = time() #terminamos o tempo
        T = tstart - tend
        
    return (pe, T)  #devolve o número de pontos dentro do círculo e o tempo que demorou


n = int(sys.argv[1])

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

m = int(math.sqrt(n)) #m: dimensão da grid n = m x m
grid = 1 / m #intervalo entre unidades da grid 

yp= 1/MPI.COMM_WORLD.Get_size() #divide o eixo Oy pelos diferentes processadores

#guardamos o ymin em que cada processador deve começar
ymin = {} 

ymin=[(grid/2)+0,(grid/2)+0.201, (grid/2)+0.412, (grid/2)+0.609, (grid/2)+1]


if int(math.sqrt(n) + 0.5) ** 2 == n: #verificar se n é quadrado perfeito para podermos construir a grid
   pe = create_grid(ymin[rank], ymin[rank+1]-(grid/2)) #cada processador realiza a sua experiência
    
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
Este programa não funciona mas foi a nossa tentativa.

Para minimizar o tempo total de execução podemos dividir as tarefas de modo a que todos os processadores tenham o mesmo tempo de execução, origininando 
um tempo total mínimo.

"""
