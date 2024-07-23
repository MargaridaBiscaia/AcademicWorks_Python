from random import randint
import time

start = time.time()

n = 10000000
D = {}
for i in range(2,13):
    D[i] = 0
    
for i in range(n):
    v = randint(1,6)
    w = randint(1,6)
    D[v+w] += 1

print (D, sum(D[k] for k in D)) 

"função utilizada para medir o tempo de execução"
end = time.time()
print('Time: ',end - start, 's') 

"""
Pela análise combinatória seria de esperar os seguintes resultados:
    
    1/36 dos resultados fosse 2 ou 12, 
    1/18 dos resultados fosse 3 ou 11, 
    1/12 dos resultados fosse 4 ou 10,
    1/9 dos resultados fosse 5 ou 9,
    5/36 dos resultados fosse 6 ou 8,
    1/6 dos resultados fosse 7.

Os resultados obtidos através do programa foram:
    
{2: 278532, 3: 555302, 4: 832188, 5: 1110056, 6: 1389554, 7: 1664665, 8: 1389553, 9: 1112595, 10: 834634, 11: 555627, 12: 277294} 10000000
Time:  23.965856552124023 s

Concluímos então que os resultados estão de acordo com o esperado.

"""
