import sys
import math
from random import randint
import time

start = time.time()

n = int(sys.argv[1])

if int(math.sqrt(n) + 0.5) ** 2 == n: #verificar se é quadrado perfeito para podermos construir a grid
    m = int(math.sqrt(n)) #m: dimensão da grid n = m x m
    grid = 1 / m #intervalo entre unidades da grid 
    
    pe = 0 #pontos equidistantes
    
    x = 0 + (grid/2) #a começar a grid em (0,0)
    y = 0 + (grid/2)
  
    
    #Vai fazer este processo para todos os intervalos da gride, primeiro para a direita e depois para cima
    for i in range(m):
        for j in range(m):
            d = (x ** 2) + (y ** 2) #verificar se os pontos estão dentro do cí­rculo 
            if d <= 1:
                pe += 1 #se sim, adiciona o ponto
                
                x += grid #anda para a direita na grid
                j += 1 #guarda que já andámos um passo para a direita
        
        #depois de terminar a direita, vamos para cima:
        y += grid #anda para cima na grid
        i += 1 #guarda que já andámos um passo para cima
        
        #o ponto em x vai novamente para o início da grid 
        x = 0 + (grid/2)
        j = 0

        
# Calcular um valor aproximado do pi:
    print('pi = ', 4*(pe/n))
    
    r = pe/n
    error = math.sqrt((r*(1-r))/n) 
    print('erro relativo = ', error)
    
    
else:
    print('O número que inseriu não é um quadrado perfeito. Insira outro n.')


end = time.time()
print('Time: ',end - start, 's') 

"função utilizada para medir o tempo de execução"
end = time.time()
print('Time: ',end - start, 's') 

"""
pi =  3.14159388
erro relativo =  4.105456287937544e-05
Time:  109.67546939849854 s = 1m49s

Concluímos que o tempo de execução foi menor e a precião do resultado também, uma vez que o valor de pi está com uma melhor aproximação.

"""






