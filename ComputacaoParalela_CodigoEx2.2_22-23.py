import random
import math
import sys
from mpi4py import MPI
import time

start = time.time()

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

n= int (sys.argv [1])
np = n//MPI.COMM_WORLD.Get_size()
m = 0
    
for i in range(np):
    x = random.uniform(-1,1)
    y = random.uniform(-1,1)
    if math.sqrt((x**2)+(y**2))<=1:
        m += 1
        
if rank == 0:
    print ('Number of processes:', MPI.COMM_WORLD.Get_size())
    print('On process', rank, ' m=', m)
    for p in range(1, MPI.COMM_WORLD.Get_size()):
        mp = comm.recv(source=p)
        m += mp
        print('On process', p, ' m=', mp)
    pi = 4*(m/n)
    r = m/n
    e = math.sqrt((r*(1-r))/(n))
    print ("m=",m)
    print ("pi=",pi)
    print ("e=",e)

else:
    comm.send(m, dest=0)
        
"função utilizada para medir o tempo de execução"
end = time.time()
print('Time: ',end - start, 's') 

"""
Seria de esperar um erro de aproximadamente 0.000013 e um delta pi de 0.00005.

O resultado obtido foi:
    
Number of processes: 8
On process 0  m= 98175428
On process 1  m= 98174852
On process 2  m= 98185324
On process 3  m= 98170140
On process 4  m= 98168721
On process 5  m= 98178897
On process 6  m= 98164538
On process 7  m= 98177500
m= 785395400
pi= 3.1415816
e= 1.2982660191919068e-05
Time:  375.6280870437622 s = 6m15s
    
E portanto 
    delta pi: pi-3.1415816 = 0.00001105
    delta r = 0.00001238
    
Concluímos assim que está de acordo com o esperado e que o tempo de execução foi muito menor.

"""











