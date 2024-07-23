import sys
import random

nr_games = int(sys.argv[1])

#cada fila tem que ter um número específico de peças
pieces=[1,3,5,7]
lista_jogadas={}
pos=0
for i in pieces:
    for j in range(1,i+1):
        lista_jogadas[str(pos)]=[i,j,0]
        pos+=1
        
percentagem_de_jogos_aleatórios=0.2    
contador1=0
contador2=0
for g in range(nr_games):
  if(g/nr_games<percentagem_de_jogos_aleatórios): 
    fullrandom=1
    contador1+=1
  else:
    fullrandom=0
    contador2+=1
  # moves[player][pos]:
  #   for player 1 and 2:
  #     for each position this player went through:
  #        number of peaces taken at position
  moves = {}
  moves[1] = []
  moves[2] = []
  # start position, player 1 is starting
  pos = {}
  for i in lista_jogadas:
      pos[i]=lista_jogadas[i].copy()
  player = 0
  # perform one game:
  aux={}
  for i in pos:
      aux[pos[i][0]]=pos[i][0]
  while len(pos):
    # switch to other player
    player = 2 if player == 1 else 1
    # get best move for this position so far:
    #   key of highest value in Stat[pos])
    
    if(fullrandom):
        fullrandom_aux={}
        k=0
        for i in pos:
            fullrandom_aux[k]=i
            k+=1
        move=str(random.choice(fullrandom_aux))
    else:
        move=list(pos.keys())[0]
        for i in pos:
            if pos[i][0]==pos[move][0]:
                if pos[move][2]<pos[i][2]:
                    move=i
                if pos[move][2]==pos[i][2]:
                    move=random.choice([i, move])
            
    aux1=pos[move][1]
    aux2=pos[move][0]
    aux[aux2]-=aux1
    list_to_pop=[]
    for i in pos:
        if pos[i][0]==aux2 and pos[i][1]>aux[pos[i][0]]:
            list_to_pop.append(i)
    for i in list_to_pop:
        pos.pop(i)
    moves[player].append(move)
    
  # last player wins, collect statistics:
  for move in moves[player]:
   lista_jogadas[move][2]+= 1
  # switch to other player that lost:
  player = 2 if player == 1 else 1
  for move in moves[player]:
   lista_jogadas[move][2]-= 1

print("Jogos Efetuados Completamente Aleatorios: ",contador1)
print("Jogos Efetuados com Machine Learning: ",contador2)
print("Total de Jogos Efetuados: ",nr_games)
for i in lista_jogadas:
    print ("Estrategia: %s,%s    Eficacia: %s" % (str(lista_jogadas[i][0]),str(lista_jogadas[i][1]), str(lista_jogadas[i][2])))
    
""" 
Só conseguimos implementar de modo a que quem ganhe seja o último jogador.
Para esta implementação não encontrámos uma estratégia vencedora.
"""