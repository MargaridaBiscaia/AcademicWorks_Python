import numpy as np
import sys
from mpi4py import MPI
import time

start = time.time()

n = int(sys.argv[1])

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
mp= MPI.COMM_WORLD.Get_size()
pn = n//mp  

a_p = np.empty(pn*n).reshape((pn,n))
ab_p = np.empty(pn*n).reshape((pn,n))

if rank==0:
    a = np.linspace(1,n**2,n**2).reshape((n,n))
    b = np.linspace(10,10*n**2,n**2).reshape((n,n))
    c = np.empty(n*n).reshape((n,n))
    print ('a:\n%s' % a)
    print ('b:\n%s' % b)
    a = a.reshape((mp,pn,n))
else:
    a = None
    b = np.empty(n**2).reshape((n,n))
    c = None
    
comm.Bcast(b, root=0)
comm.Scatter(a, a_p, root=0)
ab_p=np.matmul(a_p, b)
comm.Gather(ab_p,c,root=0)

if rank==0:
    print ('c:\n%s' % c)


"função utilizada para medir o tempo de execução"
end = time.time()
print('Time: ',end - start, 's')  

"""
O resultado obtido foi:
    
a:
[[ 1.  2.  3.  4.]
 [ 5.  6.  7.  8.]
 [ 9. 10. 11. 12.]
 [13. 14. 15. 16.]]

b:
[[ 10.  20.  30.  40.]
 [ 50.  60.  70.  80.]
 [ 90. 100. 110. 120.]
 [130. 140. 150. 160.]]

c:
[[ 900. 1000. 1100. 1200.]
 [2020. 2280. 2540. 2800.]
 [3140. 3560. 3980. 4400.]
 [4260. 4840. 5420. 6000.]]

Time:  0.015 s
    
"""