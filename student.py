from tree_search import *
import random


#$ PORT=80 SERVER=pacman-aulas.ws.atnog.av.it.pt python client.py
# to kill server: fuser 8000/tcp

debug = True


class Pacman_agent():


    def __init__(self, map_, strategy='a*'): 
        # get map and pathways info
        self.map_ = map_
        self.strategy = strategy
        self.pathways = self.create_pathways_list()
        self.adjacencies = self.create_adjacencies_map(self.pathways, map_.ghost_spawn)
        self.energy = map_.energy
        self.boost = map_.boost
        self.ghosts = None
        if debug:
            print('CREATED PACMAN AGENT')
        


    def create_pathways_list(self):
        """Create a list with all coordinates that are not walls

        Keyword arguments:
        map_ -- instance of Map for the current level

        Returns tuple of lists (for efficiency purposes):
        pathways_hor - pathways organized by row
        pathways_ver - pathways organized by column
        """

        pathways_hor = []
        for y in range(self.map_.ver_tiles):
            for x in range(self.map_.hor_tiles):
                
                if not self.map_.is_wall((x,y)): 
                    pathways_hor.extend((x,y))

        pathways_ver = []
        for x in range(self.map_.hor_tiles):
            for y in range(self.map_.ver_tiles):
            
                if not self.map_.is_wall((x,y)): 
                    pathways_ver.extend((x,y))

        return pathways_hor, pathways_ver
    


    def create_adjacencies_map(self, pathways, ghost_spawn):
        """Create a list with all adjacencies of coordinates that are not walls

        Keyword arguments:
        pathways -- a tuple of list of the coordinates that are not walls
        """

        pathways_hor, pathways_ver = pathways
        corridors = []
        # using two cicles for horizontal and vertical adjancencies for
        # efficiency purposes
        (x,y) = pathways_hor[0]
        corridor = [(x,y)]
        for i in range(1,len(pathways_hor)):

            (a,b) = pathways_hor[i]
            
            if b != y:
                (x,y) = (a,b)
                corridors += [corridor]
                corridor = []
                continue

            if a == x+1:
                adjacencies += [((x,y),(a,b))]
                corridor += [(a,b)]
            elif (x == 0 and a == self.map_.hor_tiles-1 and b == y) \
                or (a == 0 and x == self.map_.hor_tiles-1 and b == y):
                adjacencies += [((x,y),(a,b))]

            (x,y) = (a,b)
        corridors + [corridor]

        (x,y) = pathways_ver[0]
        corridor = [(x,y)]
        for i in range(1,len(pathways_ver)):

            (a,b) = pathways_ver[i]
            
            if a != x:
                (x,y) = (a,b)
                corridors += [corridor]
                corridor = []
                continue

            if b == y+1:
                adjacencies += [((x,y),(a,b))]
                corridor += [(a,b)]
            elif (y == 0 and b == self.map_.hor_tiles-1 and a == x) \
                or (b == 0 and y == self.map_.hor_tiles-1 and a == x):
                adjacencies += [((x,y),(a,b))]

            (x,y) = (a,b)
        corridors + [corridor]

        return adjacencies, corridors

        


    def get_next_move(self, state):
        """Objective of Pacman_agent - calculates the next position using
        multiple auxiliar methods

        Keyword arguments:
        state -- a list of lists with the state of every element in the game
        """

        #print("\nEnergy size is : " + str(len(state['energy'])) + "\n")
        # create a vector for every element in the game
        # every element points pacman teh next move to get to it
        vectors = []
        #print(state['energy'])
        
        pac_pos = (state['pacman'][0], state['pacman'][1])
        # if debug:
        #     print("\t pacman is in position " + str(pac_pos))

        ex, ey = self.get_vector(nodes_to_search=state['energy'], pac_pos=pac_pos)
        #(gx, gy) = self.get_vector(state['ghosts'], pac_pos)

        #sum the vectors
        vec_x = ex #+ (-10*gx)
        vec_y = ey #+ (-10*gy)

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
            if vec_x > 0 and vec_y > 0:
                key = random.choice('sd')
            elif vec_x > 0 and vec_y < 0:
                key = random.choice('dw')
            elif vec_x < 0 and vec_y < 0:
                key = random.choice('aw')
            elif vec_x < 0 and vec_y > 0:
                key = random.choice('as')
            elif vec_x == 0:
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


    def get_vector(self, nodes_to_search, pac_pos):
        """Calculates the vector given by an element

        Keyword arguments:
        nodes_to_search -- 
        pac_pos         -- coordinates of PACMAN position
        """
        i = 0
        next_pos = []
        vectors = []
        # if debug:
        #     print("***********************************************************")
        #     print('\t get vector was called! ')
        #     print("***********************************************************")

        # convert list to dictionary with zero weight for each element
        weight_dict = { (x,y):1 for [x,y] in nodes_to_search }

        for (x,y) in nodes_to_search:

            # if debug:
                # print("#######################################################")
                # print('\t calculating vector for pos: ' + str((x,y)))
                # print("#######################################################")
        
            # if debug:
            #     print("\t cycle  for position " + str((x,y)))

            # search the path
            # if debug:
            #     print("SearchDomain being called to create")
            domain = Pathways(self.adjacencies)

            # if debug:
            #     print("SearchProblem " + str(i) + " being called to create")
            my_prob = SearchProblem(domain,(x,y),pac_pos)
            
            # if debug:
            #     print("SearchTree " + str(i) + " being called to create")
            my_tree = SearchTree(my_prob, weight_dict, self.strategy)
            
            next_result = my_tree.search()

            if next_result != None:
                next_res, next_cost = next_result
                next_pos += [((x,y) , next_res, next_cost)]
            else:
                next_pos += [((x,y), pac_pos, 0)]

            #print((x,y))
            #print(next_result)
            
            #print("\t search " + str(i) + " was completed!")

            # if debug:
            #     print('\t Calculating next move for position: ' + str((x,y)))

        #print(next_pos)

        for i in range(len(next_pos)):
            if next_pos[i][1] != pac_pos:
                pac_x, pac_y = pac_pos
                next_x, next_y = (next_pos[i])[1]
                x = pac_x - next_x
                y = pac_y - next_y
                if (x == 1):
                    dir = ( ( -(1/next_pos[i][2])) , 0 )
                elif (x == -1):
                    dir = ( ( (1/next_pos[i][2])) , 0 )
                elif (y == 1):
                    dir = ( 0 , (-(1/next_pos[i][2])) )
                elif (y == -1):
                    dir = ( 0 , ((1/next_pos[i][2])) )
                elif (x > 1):
                    dir = ( ((1/next_pos[i][2])) , 0 )
                elif (x < 1):
                    dir = ( (-(1/next_pos[i][2])) , 0 )
                elif (y > 1):
                    dir = ( 0 , ((1/next_pos[i][2])) )
                elif (y < 1):
                    dir = ( 0 , (-(1/next_pos[i][2])) )
                vectors += [dir]

                print(str(next_pos[i][0]) + " : vector is: " + str(dir))
            
            # if debug:
            #     print("#######################################################")
            #     print('\t Vector is ' + str(dir))
            #     print("#######################################################")

        #print(weight_dict)



        # sum all the vectors
        vec_x = 0
        vec_y = 0
        for (x,y) in vectors:
            vec_x += x
            vec_y += y
        
        #print("\npacman is in position " + str(pac_pos[0], pac_pos[1]))
        #print('Sum of all vectors is: ' + str(vec_x) + ', ' + str(vec_y) + "\n")

        if debug:
            print("#######################################################")
            print('\t Vector is ' + str((vec_x, vec_y)))
            print("#######################################################")

        return [vec_x, vec_y]





    def calculate_key(self, vector):
        """Calculates the 'wasd' key that corresponds to the next move

        Keyword arguments:
        vector -- the vector that represents next PACMAN move
        """



    def calculate_next_move_direction(self, pac_pos, next_pos):
        """Calculates direction of next PACMAN move

        Keyword arguments:
        pac_pos     -- coordinates of PACMAN position
        next_pos    -- coordinates of next PACMAN move
        """



    def sum_vectors(self, vectors):
        """Sums all vectors

        Keyword arguments:
        vectors -- a list of vectors
        """



    def combinations(self, list_, n):
        """Generates all combinations of the elements in a list

        Keyword arguments:
        list_   -- a list
        n       -- number of elements per combination
        """
        if n==0: yield []
        else:
            for i in range(len(list_)):
                for elem in self.combinations(list_[i+1:],n-1):
                    yield [list_[i]] + elem

    

    def print_debug_block(self, string, var):
        """Prints a debug bar

        Keyword arguments:
        list_   -- a list
        n       -- number of elements per combination
        """
        print("#######################################################")
        print('\t ' + string + ': ' + str(var))
        print("#######################################################")



class Corridor():
    """Represents an uninterrupted path of adjacente coordinates with a
    crossroad at each end

    Args:
        coordinates: list of coordinates of the Corridor

    Attributes:
        coordinates: list of coordinates of the Corridor
        length: length of coordinates without crossroad ends

    """
    def __init__(self, coordinates):
        self.coordinates = coordinates
        self.length = len(coordinates) -2
        self.ends = (coordinates[0], coordinates[self.length-1])
        
    def dist_end1(coord):
        return len(coordinates[0:coord])

    def dist_end2(coord):
        return len(coordinates[coord:self.length])

    def dist_end(coord, end):
        if end == ends[0]:
            return self.dist_end1(coord)
        return self.dist_end2(coord)

    def closest_end(coord):
        return self.dist_end1(coord)
            if self.dist_end1(coord) <= self.dist_end2(coord)
            else self.dist_end2(coord)


    def sub_corridor(self, coord):
        index = self.coordinates.index(coord)
        return Corridor(self.coordinates[:index]+[self.coordinates[index]]), Corridor(self.coordinates[index:])