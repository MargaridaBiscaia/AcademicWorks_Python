import math
import sys
from mpi4py import MPI
import time

start = time.time()

n = int(sys.argv[1])
m = int(math.sqrt(n)) #m: dimensão da grid n = m x m
grid = 2 / m #intervalo entre unidades da grid 

if int(math.sqrt(n) + 0.5) ** 2 == n: #verificar se n é quadrado perfeito para podermos construir a grid
   
    pe = 0 #pontos equidistantes
    
    x = -1 + (grid/2) #a começar a grid em (-1,-1) 
    y = -1 + (grid/2)
  
    #Vai fazer este processo para todos os intervalos da grid, primeiro para a direita e depois para cima
    for i in range(m):
        for j in range(m):
            d = (x ** 2) + (y ** 2) #verificar se os pontos estão dentro do círculo 
            if d <= 1:
                pe += 1 #se sim, adiciona o ponto
                
            x += grid #anda para a direita na grid
            j += 1 #guarda que já andámos um passo para a direita
        
        #depois de terminar a direita, vamos para cima:
        y += grid #anda para cima na grid
        i += 1 #guarda que já andámos um passo para cima
        
        #o ponto em x vai novamente para o início da grid 
        x = -1 + (grid/2)
        j = 0
    
# Calcular um valor aproximado do pi:
     
# S = x * y -> área da grid; neste caso: 2 * 2 = 4
# Por um lado, a área do círculo é: S * (pe/n); por outro lado, sabemos que a área do círculo é (raio ** 2) * pi = 1 * pi = pi
# Logo, pi = S * (pe/n)


    print('pi = ', 4*(pe/n))
    
    r = pe/n
    error = math.sqrt((r*(1-r))/n) 
    print('erro relativo = ', error)
    
    
else:
    print('O número que inseriu não é um quadrado perfeito. Insira outro n.')
    
"função utilizada para medir o tempo de execução"
end = time.time()
print('Time: ',end - start, 's') 
    
"""
O resultado obtido foi:

pi =  3.14159424
erro relativo =  4.1054556622855694e-05
Time:  92.44642782211304 s = 1m32s

Na simulação de Monte Carlo, para n^8, temos:
pi =  3.14181076
erro relativo =  4.105079314358785e-05
Time:  2m0.182s

Comparando os dois resultados, concluímos que o valor obtido neste programa aproxima melhor o valor de pi. 
Isto faz todo o sentido, uma vez que a simulação de Monte Carlo é feita através da geração de números aleatórios.    
"""
