from mpi4py import MPI
from random import randint
import time

start = time.time()

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

n = 10000000//MPI.COMM_WORLD.Get_size()
D = {}
for i in range(2,13):
    D[i] = 0
    
for i in range(n):
    v = randint(1,6)
    w = randint(1,6)
    D[v+w] += 1

if rank == 0:
    print ('Number of processes:', MPI.COMM_WORLD.Get_size())
    print('On process', rank, 'result is', D)
    for p in range(1, MPI.COMM_WORLD.Get_size()):
        Dp = comm.recv(source=p)
        print('On process', p, 'result is', Dp)
        for i in range(2,13):
            D[i] += Dp[i]
    print ('Final result:         ', D)
else:
    comm.send(D, dest=0)

"função utilizada para medir o tempo de execução"
end = time.time()
print('Time: ', end - start, 's') 

"""
Pela análise combinatória seria de esperar os seguintes resultados:
    
    1/36 dos resultados fosse 2 ou 12, 
    1/18 dos resultados fosse 3 ou 11, 
    1/12 dos resultados fosse 4 ou 10,
    1/9 dos resultados fosse 5 ou 9,
    5/36 dos resultados fosse 6 ou 8,
    1/6 dos resultados fosse 7.

Os resultados obtidos através do programa foram:
    
Number of processes: 8
On process 0 result is {2: 34425, 3: 69665, 4: 103578, 5: 138904, 6: 174198, 7: 208658, 8: 173390, 9: 138708, 10: 103995, 11: 69760, 12: 34719}
On process 1 result is {2: 34582, 3: 68871, 4: 104260, 5: 138806, 6: 174110, 7: 208053, 8: 174512, 9: 138765, 10: 104387, 11: 69037, 12: 34617}
On process 2 result is {2: 34551, 3: 69336, 4: 104369, 5: 138664, 6: 173554, 7: 208309, 8: 173862, 9: 139011, 10: 103737, 11: 69896, 12: 34711}
On process 3 result is {2: 34767, 3: 69334, 4: 104254, 5: 138744, 6: 174059, 7: 208655, 8: 172964, 9: 139362, 10: 103717, 11: 69506, 12: 34638}
On process 4 result is {2: 34747, 3: 69200, 4: 104428, 5: 138309, 6: 173570, 7: 208515, 8: 173529, 9: 139327, 10: 103948, 11: 69567, 12: 34860}
On process 5 result is {2: 34880, 3: 69654, 4: 103877, 5: 138806, 6: 173776, 7: 208797, 8: 173432, 9: 139009, 10: 103752, 11: 69252, 12: 34765}
On process 6 result is {2: 34492, 3: 69583, 4: 103865, 5: 139507, 6: 173413, 7: 207704, 8: 173966, 9: 138649, 10: 104192, 11: 69606, 12: 35023}
On process 7 result is {2: 34672, 3: 68956, 4: 104202, 5: 139520, 6: 173703, 7: 208280, 8: 173774, 9: 138762, 10: 103644, 11: 69789, 12: 34698}
Final result:          {2: 277116, 3: 554599, 4: 832833, 5: 1111260, 6: 1390383, 7: 1666971, 8: 1389429, 9: 1111593, 10: 831372, 11: 556413, 12: 278031}
Time:  11.719791889190674 s

Concluímos então que os resultados estão de acordo com o esperado.

Em relação ao primeiro programa podemos concluir que a execução do segundo foi 
mais rápida cerca de 12s, uma vez que foram utilizados 8 processadores.

"""