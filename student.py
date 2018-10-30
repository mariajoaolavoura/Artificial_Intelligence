from tree_search import *
import math
from pathways import Pathways


#$ PORT=80 SERVER=pacman-aulas.ws.atnog.av.it.pt python client.py

debug = True


class Pacman_agent():

    def __init__(self, mapa, strategy='a*'): 
        # get map and pathways info
        self.mapa = mapa
        self.pathways = mapa.pathways
        self.domain = self.create_search_domain(self.pathways)
        self.energy = mapa.energy
        self.boost = mapa.boost
        self.ghosts = None
        if debug:
            print('CREATED PACMAN AGENT')
        

    #
    # creates a list of tuples with all adjacent coordinates
    #
    def create_search_domain(self, pathways):
        domain = [ ((x,y),(a,b)) for ((x,y),(a,b)) in self.combinations(pathways, 2) \
                        if ((a == x+1 and b == y) \
                        or (a == x-1 and b == y) \
                        or (b == y+1 and a == x) \
                        or (b == y-1 and a == x) \
                        or (x == 0 and a == self.mapa.hor_tiles-1 and b == y) \
                        or (a == 0 and x == self.mapa.hor_tiles-1 and b == y) \
                        or (y == 0 and b == self.mapa.ver_tiles-1 and a == x) \
                        or (b == 0 and y == self.mapa.ver_tiles-1 and a == x)) ]

        return domain

        # TODO this only works to avoid the den in the example map
        # TODO must find a way to eliminate den from domain/pathways 
        # not needed for pacman, as no vector will point that way
        # only needed as a more to make calculations more efficient
        domain.remove(((8,15),(8,16)))
        domain.remove(((8,14),(8,15)))


    #
    # calculates and returns the next move of pacman_agent (format 'wasd')
    #
    def get_next_move(self, state):

        # create a vector for every element in the game
        # every element points pacman teh next move to get to it
        vectors = []
        #vectors = test_search(self.domain, self.energy)
        for (x,y) in state['energy']:

            if debug:
                print("\t cycling for position " + str((x,y)))

            pac_pos = state['pacman']
            
            # search the path
            my_prob = SearchProblem(Pathways(self.domain),(x,y),pac_pos)
            my_tree = SearchTree(my_prob, 'a*')
            next_pos = my_tree.search()

            if debug:
                print('\t Searching path for energy ' + str((x,y)))

            #print("###############\n" + str(next_pos))

            # calculate vector for every element
            dir = None
            if next_pos:
                pac_x, pac_y = pac_pos
                next_x, next_y = next_pos
                x = pac_x - next_x
                y = pac_y - next_y
                if (x > 0):
                    dir = (-1/my_tree.cost,0)
                elif (x < 0):
                    dir = (1/my_tree.cost,0)
                elif (y > 0):
                    dir = (0,-1/my_tree.cost)
                elif (y < 0):
                    dir = (0,1/my_tree.cost)
                vectors += [dir]
            
            if debug:
                print('\t Vector is ' + str(dir))


        # sum all the vectors
        vec_x = 0
        vec_y = 0
        for (x,y) in vectors:
            vec_x += x
            vec_y += y
        
        if debug:
            print('Sum of all vectors is: ' + str(vec_x) + ', ' + vec_y)


        # calculate the key to send
        if abs(vec_x) > abs(vec_y):
            if vec_x > 0:
                key = 'd'
            else:
                key = 'a'
        elif abs(vec_x) < abs(vec_y):
            if vec_y > 0:
                key = 's'
            else:
                key = 'w'
        elif abs(vec_x) == abs(vec_y):
            if x > 0 and y > 0:
                key = random.choice('sd')
            elif x > 0 and y < 0:
                key = random.choice('dw')
            elif x < 0 and y > 0:
                key = random.choice('aw')
            elif x < 0 and y > 0:
                key = random.choice('as')
            elif x == 0:
                print("There is a problem not solved yet in this line of code!")
        
        if debug:
            print('The key is: ' + str(key))


        # x, y = state['pacman']
        # if x == cur_x and y == cur_y:
        #     if key in "ad":
        #         key = random.choice("ws")
        #     elif key in "ws":
        #         key = random.choice("ad")
        # cur_x, cur_y = x, y

        return key



    def combinations(self, list_, n):
        if n==0: yield []
        else:
            for i in range(len(list_)):
                for elem in self.combinations(list_[i+1:],n-1):
                    yield [list_[i]] + elem