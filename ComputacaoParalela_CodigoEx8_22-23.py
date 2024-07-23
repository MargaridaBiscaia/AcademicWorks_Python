from mpi4py import MPI
import numpy as np
from sys import argv
import time

start = time.time()

def run_simulation(v,vp):
    rp=np.empty(len(vp),dtype=int)
    for i in range(len(vp)):
        x = 0
        for j in range(n):
            if vp[i] > v[j]:
                x += 1
        rp[i] = x
    return (rp)

n = int(argv[1])

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
mp= MPI.COMM_WORLD.Get_size()

rT = [0 for i in range(n)]

vT = np.random.rand(n)

if rank==0:
    print ('vp :\n%s\n' %vT)
    vaux = np.array_split(vT,mp)
else:
    vaux=None

v = comm.bcast(vT, root=0)
vp = comm.scatter(vaux, root=0)
r = run_simulation(v,vp)
rM = comm.gather(r, root=0)

if rank==0:
    k=0
    for i in range(mp):
        for j in range(n//mp):
            rT[k] = rM[i][j]
            k=k+1
    for i in range(n):
        for j in range(n):
            if (rT[i]==rT[j] and i!=j):
                rT[j]=rT[j]+1
    b = np.empty(n, dtype=float)
    for i in range(n):
        b[rT[i]] = vT[i]
    print ('b :\n%s\n' %b)

        
"função utilizada para medir o tempo de execução"
end = time.time()
print('Time: ',end - start, 's')  

"""
Resultado obtido para n=16:
vp :
[0.58071762 0.72365033 0.57593234 0.5235645  0.92730516 0.53479784
 0.46323722 0.17900295 0.62057178 0.65189591 0.35646332 0.96588204
 0.54430251 0.00799217 0.38337127 0.98836973]

b :
[0.00799217 0.17900295 0.35646332 0.38337127 0.46323722 0.5235645
 0.53479784 0.54430251 0.57593234 0.58071762 0.62057178 0.65189591
 0.72365033 0.92730516 0.96588204 0.98836973]

Time:  0.0 s
"""
        
