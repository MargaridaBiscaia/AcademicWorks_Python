from mpi4py import MPI
from random import randint
import math
import time

start = time.time()

def run_simulations(np):
    D = {}  
    for i in range(2,13):
        D[i] = 0 
        
    for i in range(np):
        v = randint(1, 6)
        w = randint(1,6)
        #print (v)
        D[v+w] += 1
    return D

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

n=1024
P={2:1/36,3:1/18,4:1/12,5:1/9,6:5/36,7:1/6,8:5/36,9:1/9,10:1/12,11:1/18,12:1/36}
R = {}
for i in range(2,13):
    R[i] = 0

np=1
while True:
    if np==0:
        break
    np2 = n//MPI.COMM_WORLD.Get_size()
    np = comm.bcast(np2, root=0)
    Dp =run_simulations(np)
    Dv = comm.gather(Dp, root=0)
    if rank == 0:
        D = {}
        for i in range(2,13):
            D[i] = 0
        for p in range(MPI.COMM_WORLD.Get_size()):
            for i in range(2, 13):
                D[i] += Dv[p][i]
        for i in range(2, 13):
            R[i]+=D[i]
        t=sum(R[i] for i in R)
        somatorio=0
        for i in range(2,13):    
            somatorio += ((R[i]/t-P[i])/P[i])**2
        s=math.sqrt(somatorio)/11
        print (R,'n= ',n,'erro= ',s,'total= ',t)
        if s < pow(10,-3):
            n=0
        else: 
            n=n*2
            
"função utilizada para medir o tempo de execução"
end = time.time()
print('Time: ',end - start, 's')   

"""
O resultado obtido foi:
{2: 31, 3: 57, 4: 89, 5: 129, 6: 131, 7: 186, 8: 121, 9: 122, 10: 82, 11: 55, 12: 21} n=  1024 erro=  0.034104024502754966 total=  1024
{2: 89, 3: 157, 4: 287, 5: 342, 6: 422, 7: 518, 8: 405, 9: 347, 10: 252, 11: 180, 12: 73} n=  2048 erro=  0.020360750873291922 total=  3072
{2: 210, 3: 389, 4: 643, 5: 776, 6: 995, 7: 1205, 8: 975, 9: 800, 10: 580, 11: 406, 12: 189} n=  4096 erro=  0.010891772827990899 total=  7168
{2: 400, 3: 827, 4: 1268, 5: 1744, 6: 2175, 7: 2590, 8: 2097, 9: 1702, 10: 1249, 11: 859, 12: 449} n=  8192 erro=  0.008912712762281113 total=  15360
{2: 897, 3: 1712, 4: 2710, 5: 3532, 6: 4446, 7: 5256, 8: 4381, 9: 3543, 10: 2583, 11: 1790, 12: 894} n=  16384 erro=  0.004894291640905056 total=  31744
{2: 1841, 3: 3588, 4: 5366, 5: 7161, 6: 8972, 7: 10782, 8: 8901, 9: 7148, 10: 5272, 11: 3663, 12: 1818} n=  32768 erro=  0.003946626202679671 total=  64512
{2: 3601, 3: 7368, 4: 10822, 5: 14428, 6: 18117, 7: 21815, 8: 17951, 9: 14327, 10: 10731, 11: 7225, 12: 3663} n=  65536 erro=  0.00266601986674142 total=  130048
{2: 7279, 3: 14591, 4: 21645, 5: 28826, 6: 36199, 7: 43999, 8: 36098, 9: 29027, 10: 21710, 11: 14442, 12: 7304} n=  131072 erro=  0.0016672781874618999 total=  261120
{2: 14593, 3: 29101, 4: 43533, 5: 57821, 6: 72676, 7: 87859, 8: 72586, 9: 57917, 10: 43673, 11: 28880, 12: 14625} n=  262144 erro=  0.0013014550530340782 total=  523264
{2: 28983, 3: 58433, 4: 87254, 5: 115612, 6: 145142, 7: 175698, 8: 145209, 9: 116153, 10: 87629, 11: 58005, 12: 29434} n=  524288 erro=  0.0015481580795064888 total=  1047552
{2: 58046, 3: 116722, 4: 175000, 5: 231891, 6: 290781, 7: 351129, 8: 290812, 9: 232265, 10: 175381, 11: 116033, 12: 58068} n=  1048576 erro=  0.0009518449961814282 total=  2096128
{2: 58046, 3: 116722, 4: 175000, 5: 231891, 6: 290781, 7: 351129, 8: 290812, 9: 232265, 10: 175381, 11: 116033, 12: 58068} n=  0 erro=  0.0009518449961814282 total=  2096128
Time:  0m2.64 s
    
"""

