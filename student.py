from tree_search import *
import math
from pathways import Pathways
from testTreeSearch import *


#$ PORT=80 SERVER=pacman-aulas.ws.atnog.av.it.pt python client.py

class Pacman_agent():

    def __init__(self,mapa, strategy='breadth'): 
        # get map and pathways info
        self.mapa = mapa
        self.pathways = mapa.pathways
        self.domain = self.create_search_domain(self.pathways)
        self.energy = mapa.energy
        self.boost = mapa.boost
        self.ghosts = None
        


    #
    # creates a list of tuples with all adjacent coordinates
    #
    def create_search_domain(self, pathways):
        for (x,y) in pathways:
            domain = [ ((x,y),(a,b)) for (a,b) in pathways \
                                if ((a == x+1 and b == y) \
                                or (a == x-1 and b == y) \
                                or (b == y+1 and a == x) \
                                or (b == y-1 and a == x) \
                                or (x == 0 and a == self.mapa.hor_tiles-1 and b == y) \
                                or (a == 0 and x == self.mapa.hor_tiles-1 and b == y) \
                                or (y == 0 and b == self.mapa.ver_tiles-1 and a == x) \
                                or (b == 0 and y == self.mapa.ver_tiles-1 and a == x))
                                and not domain.__contains__(((a,b),(x,y)))] # How the hell does this work? does it work?!
        return domain

        # TODO this only works to avoid the den in the example map
        # TODO must find a way to eliminate den from domain/pathways 
        domain.remove(((8,15),(8,16)))
        domain.remove(((8,14),(8,15)))


    #
    # calculates and returns the next move of pacman_agent (format 'wasd')
    #
    def get_next_move(self, ghosts):

        # create the vector for every element in the game
        #vectors = []
        vectors = test_search(self.domain, self.energy)
        # for (x,y) in energy:

        #     pac_pos = state['pacman']
            
        #     my_prob = SearchProblem(Pathways(domain),(x,y),pac_pos)
        #     my_tree = SearchTree(my_prob, 'a*')
        #     #path = my_tree.search()
        #     last_pos = my_tree.search()

        #     print("###############\n" + str(last_pos))

        #     goal_pos = pac_pos
        #     #last_pos = path[len(path)-2]

        #     dir = None
        #     if last_pos:
        #         x = goal_pos[0] - last_pos[0]
        #         y = goal_pos[1] - last_pos[1]
        #         if (x > 0):
        #             dir = (-1/my_tree.cost,0)
        #         if (x < 0):
        #             dir = (1/my_tree.cost,0)
        #         if (y > 0):
        #             dir = (0,-1/my_tree.cost)
        #         if (y < 0):
        #             dir = (0,1/my_tree.cost)

        #     vectors += [dir]


        # sum the vector 
        vec_x = 0
        vec_y = 0
        for (x,y) in vectors:
            vec_x += x
            vec_y += y

        # vec_x = [sum(x) for (x,y) in vectors]
        # vec_y = [sum(y) for (x,y) in vectors]


        # calculate the key to send
        print(str(vec_x) + " " + str(vec_y))
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
            key = 'w'
            # preencher esta parte que raramente irá acontecer


        # x, y = state['pacman']
        # if x == cur_x and y == cur_y:
        #     if key in "ad":
        #         key = random.choice("ws")
        #     elif key in "ws":
        #         key = random.choice("ad")
        # cur_x, cur_y = x, y

        return key