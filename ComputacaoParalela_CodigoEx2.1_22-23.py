import random
import math
import sys
import time

start = time.time()

n = int (sys.argv [1])
m = 0
    
for i in range(n):
    x = random.uniform(-1,1)
    y = random.uniform(-1,1)
    if math.sqrt((x**2)+(y**2))<=1:
        m += 1

pi = 4*(m/n)
r = m/n
e = math.sqrt((r*(1-r))/(n))

print ("m=",m)
print ("pi=",pi)
print ("e=",e)

"função utilizada para medir o tempo de execução"
end = time.time()
print('Time: ',end - start, 's') 

"""
Seria de esperar um erro de aproximadamente 0.000013 e um delta pi de 0.00005.

O resultado obtido foi:
m= 785413198
pi= 3.141652792
e= 1.2982268923705624e-05
Time:  1554.4212970733643 s = 25m54s
    
E portanto 
    delta pi: |pi-3.141652792| = 0.00006014
    delta r = 0.00001298
    
Concluímos assim que está de acordo com o esperado.

"""
