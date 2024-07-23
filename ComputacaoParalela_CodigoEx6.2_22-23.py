import numpy as np
import sys
from mpi4py import MPI
import math
import time

start = time.time()

n = int(sys.argv[1])

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
mp= MPI.COMM_WORLD.Get_size()
#Número de divisões
nd=int(math.sqrt(mp))
pn = n//nd

a_p = np.empty(pn*n).reshape((pn,n))
b_p = np.empty(pn*n).reshape((pn,n))
ab_p = np.empty(pn**2).reshape((pn,pn))
ab_aux = np.empty(n**2).reshape((mp,pn,pn))

#Master
if rank==0:
    a = np.linspace(1,n**2,n**2).reshape((n,n))
    b = np.linspace(10,10*n**2,n**2).reshape((n,n))
    
    #Verificar cálculos
    #C=np.matmul(A,B)
    #print ('\nC: (usando matmul)\n%s' % C)
    
    ab = np.empty(n**2).reshape((mp,pn,pn))
    print ('a:\n%s' % a)
    print ('b:\n%s' % b)
    a = a.reshape((nd,pn,n))
    b = b.transpose()
    b = b.reshape((nd,pn*n))
    
    for p in range(1,mp):
        comm.Send(a[p%nd], dest=p)
        comm.Send(b[p//nd], dest=p)
    
    #Primeiro bloco
    a_p = a[0]    
    b_p = b.reshape((nd,pn,n))
    b_p = b_p[0]
    b_p = b_p.transpose()
    ab_p=np.matmul(a_p, b_p)
    
else:
    comm.Recv(a_p, source=0)
    comm.Recv(b_p, source=0)
    
    b_p = b_p.transpose()
    ab_p=np.matmul(a_p, b_p)
    
    
#Envia os blocos (AB_p) para o Master
comm.Gather(ab_p,ab_aux,root=0)

if rank==0:
    #Coloca os resultados nas posições corretas
    ab_aux = ab_aux.reshape(mp,pn,pn)
    #Construir a matriz M por blocos
    M = np.empty(n**2).reshape((n,n))
    M = np.block([[ab_aux[0], ab_aux[2]], [ab_aux[1], ab_aux[3]]])
    
    print ('M:\n%s' % M)
    
"função utilizada para medir o tempo de execução"
end = time.time()
print('Time: ',end - start, 's')  


"""
O resultado obtido para n=4 foi:
    
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

M:
[[ 900. 1000. 1100. 1200.]
 [2020. 2280. 2540. 2800.]
 [3140. 3560. 3980. 4400.]
 [4260. 4840. 5420. 6000.]]

Time:  0.015 s
    
"""
    

