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
        v = randint(1,6)
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
    if rank == 0:
        np= n//MPI.COMM_WORLD.Get_size()
        for p in range(1, MPI.COMM_WORLD.Get_size()):
            comm.send(np,dest=p)
        D=run_simulations(np)
        #print ('Number of processes:', MPI.COMM_WORLD.Get_size())
        #print('On process', rank, 'result is', D)
        for p in range(1, MPI.COMM_WORLD.Get_size()):
            Dp = comm.recv(source=p)
            #print('On process', p, 'result is', Dp)
            for i in range(2, 13):
                D[i] += Dp[i]
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
    else:
        np=comm.recv(source=0)
        D=run_simulations(np)
        comm.send(D, dest=0)
        
"função utilizada para medir o tempo de execução"
end = time.time()
print('Time: ',end - start, 's')    

"""
O resultado obtido foi:

{2: 25, 3: 56, 4: 110, 5: 98, 6: 148, 7: 176, 8: 135, 9: 111, 10: 84, 11: 57, 12: 24} n=  1024 erro=  0.03499216057221465 total=  1024
{2: 71, 3: 179, 4: 278, 5: 316, 6: 405, 7: 541, 8: 411, 9: 353, 10: 283, 11: 165, 12: 70} n=  2048 erro=  0.02821237043443184 total=  3072
{2: 175, 3: 381, 4: 633, 5: 801, 6: 955, 7: 1244, 8: 982, 9: 830, 10: 606, 11: 390, 12: 171} n=  4096 erro=  0.019503488087241425 total=  7168
{2: 437, 3: 875, 4: 1328, 5: 1653, 6: 2066, 7: 2571, 8: 2130, 9: 1696, 10: 1353, 11: 839, 12: 412} n=  8192 erro=  0.008813394636035097 total=  15360
{2: 870, 3: 1756, 4: 2673, 5: 3441, 6: 4306, 7: 5354, 8: 4493, 9: 3483, 10: 2765, 11: 1744, 12: 859} n=  16384 erro=  0.006394124978129995 total=  31744
{2: 1775, 3: 3568, 4: 5403, 5: 7071, 6: 8861, 7: 10812, 8: 8991, 9: 7212, 10: 5457, 11: 3587, 12: 1775} n=  32768 erro=  0.0026330031533606506 total=  64512
{2: 3602, 3: 7265, 4: 10848, 5: 14549, 6: 18007, 7: 21819, 8: 17853, 9: 14405, 10: 10956, 11: 7192, 12: 3552} n=  65536 erro=  0.0024144207276827227 total=  130048
{2: 7146, 3: 14553, 4: 21785, 5: 29180, 6: 36313, 7: 43627, 8: 35998, 9: 28838, 10: 21986, 11: 14481, 12: 7213} n=  131072 erro=  0.0020419022016935073 total=  261120
{2: 14535, 3: 29204, 4: 43357, 5: 58466, 6: 72779, 7: 87023, 8: 72341, 9: 58061, 10: 43752, 11: 29130, 12: 14616} n=  262144 erro=  0.0011541924983490227 total=  523264
{2: 29219, 3: 58156, 4: 86874, 5: 116517, 6: 145187, 7: 174032, 8: 145948, 9: 116046, 10: 87866, 11: 58445, 12: 29262} n=  524288 erro=  0.001177582011408559 total=  1047552
{2: 58236, 3: 116202, 4: 174512, 5: 233040, 6: 291253, 7: 347982, 8: 291846, 9: 232549, 10: 175271, 11: 116991, 12: 58246} n=  1048576 erro=  0.0007215326106278648 total=  2096128
{2: 58236, 3: 116202, 4: 174512, 5: 233040, 6: 291253, 7: 347982, 8: 291846, 9: 232549, 10: 175271, 11: 116991, 12: 58246} n=  0 erro=  0.0007215326106278648 total=  2096128
Time:  0m2.194s 

"""
        

