from tree_search import *
import random


#$ PORT=80 SERVER=pacman-aulas.ws.atnog.av.it.pt python client.py
# to kill server: fuser 8000/tcp

debug = True


class Pacman_agent():
    """Creates the PACMAN agent that analyses the given 'Map' and 'state'
    to decide which direction to take and win the game 

    Args:
    map_: instance of Map for the current level

    Attr:
    map_: instance of Map for the current level
    pathways: list of all coordinates that are not walls
    adjacencies: list of pairs of adjacent pathways
    corridors: list of coordinates that create a corridor
    crossroads: list of all coordinates that separate corridors
    """


    def __init__(self, map_): 
        # static info from mapa.py Map
        self.map_ = map_
        self.pathways = self.create_pathways_list()
        self.crossroads = self.create_crossroads_list(self.pathways)
        self.adjacencies, self.corridors = self.create_static_maps(self.pathways, self.crossroads)

        if debug:
            print('CREATED PACMAN AGENT')

        


    def get_next_move(self, state):
        """Objective of Pacman_agent - calculates the next position using
        multiple auxiliar methods

        Args:
        state: a list of lists with the state of every element in the game

        Returns: the key corresponding to the next move of PACMAN
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

        Args:
        nodes_to_search -- 
        pac_pos         -- coordinates of PACMAN position

        Returns:

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
        print('\t ' + string + ' is: ')
        print("#######################################################")
        print(var)


################################################################################
#####################   STATIC ANALYSIS AUXILIAR METHODS   #####################
################################################################################
    
    """##########   TESTED AND VERIFIED   ##########"""
    # TODO how to remove ghosts den from the crossroads (is it needed? see method)
    def create_pathways_list(self):
        """Create a list with all coordinates that are not walls

        Returns:
        Tuple of lists (for efficiency purposes):
        pathways_hor: pathways organized by row
        pathways_ver: pathways organized by column
        """

        pathways_hor = []
        for y in range(self.map_.ver_tiles):
            for x in range(self.map_.hor_tiles):
                
                if not self.map_.is_wall((x,y)): 
                    pathways_hor += [(x,y)]
            
        pathways_ver = sorted(pathways_hor, key=lambda y: (x,y))

        if True:
            self.print_debug_block('pathways_hor', pathways_hor)
            self.print_debug_block('pathways_ver', pathways_ver)

        return pathways_hor, pathways_ver

#------------------------------------------------------------------------------#
    
    def create_crossroads_list(self, pathways):
        """Create a list with all coordinates that are crossroads

        Args:
        pathways: tuple with two list with all coordinates that are not walls

        Returns:
        crossroads: list of all coordinates that are crossroads:
        """

        pathways_hor, _ = pathways
        crossroads = []
        for (x,y) in pathways_hor:
            adj = 0
            if x > 0 and not self.map_.is_wall((x-1,y)):
                adj += 1
            if x < self.map_.hor_tiles-1 and not self.map_.is_wall((x+1,y)):
                adj += 1
            if y > 0 and not self.map_.is_wall((x,y-1)):
                adj += 1
            if y < self.map_.ver_tiles-1 and not self.map_.is_wall((x,y+1)):
                adj += 1
            if adj > 2:
                crossroads += [(x,y)]

        if debug:
            self.print_debug_block('crossroads', crossroads)

        return crossroads

#------------------------------------------------------------------------------#

    def get_ghosts_den(self, map_, den):
        """delimit the coordinates that make up the ghosts den

        Args:
        ghost_spawn: coordinates where ghosts spawn (usually the center of den)

        Returns:
        crossroads: list of coordinates tht make up the ghosts den:
        """

        # TODO - work in progress. before continuing, verify if it will be needed
        # TODO   Using searchTree with corridors, there is no risk of entering the
        # TODO   den during the search.


        buffer = den
        #while 
        if den == []:
            return den

        # get neighbors
        neighbors = []
        count = 0
        for (x,y) in den:

            if not map_.is_wall((x-1,y)):
                neighbors += [(x-1,y)]
                count += 1
            if not map_.is_wall((x+1,y)):
                neighbors += [(x+1,y)]
                count += 1
            if not map_.is_wall((x,y-1)):
                neighbors += [(x,y-1)]
                count += 1
            if not map_.is_wall((x,y+1)):
                neighbors += [(x,y+1)]
                count += 1

        if count < 2:
            return [(x,y)]
        if count == 2:
            pass
            #found entrance
        if count > 2:
            return [den] + get_ghosts_den(map_, neighbors)
        

        return [ghost_spawn] + get_ghosts_den(map_, ...)
    

#------------------------------------------------------------------------------#

    def create_static_maps(self, pathways, crossroads):
        """Creates a list with all adjacencies of coordinates that are not walls
        Uses two cycles for horizontal and vertical adjacencies for efficiency
        purposes

        Args:
        pathways: a tuple of list of the coordinates that are not walls

        Returns: A tuple with 2 lists
        adjacencies: list with pairs of adjacent coordinates
        corridors: list with groups of horizontal and vertical Corridors
        """

        pathways_hor, pathways_ver = pathways
        adjacencies = []
        corridors = []
        tunnel_points = []

        # horizontal search
        (x,y) = pathways_hor[0]
        corridor = [(x,y)]
        i = 0
        for i in range(1,len(pathways_hor)):
            # print()
            # print('horizontal iteration number: ' +)
            (a,b) = pathways_hor[i]

            # check for row change (coordinates are not adjacent)
            if b != y:
                if len(corridor) > 1: # length 1 is a section of a vertical corridor
                    corridors += [corridor]
                corridor = [(a,b)]
                (x,y) = (a,b)
                continue

            # if horizontally adjacent, add to adjacencies, add to current
            # horizontal corridor
            if a == x+1:
                adjacencies += [((x,y),(a,b))]
                corridor += [(a,b)]
                if (a,b) in crossroads:
                    corridors += [corridor]
                    corridor = [(a,b)]
            else:
                if len(corridor) > 1: # length 1 is a section of a vertical corridor
                    corridors += [corridor]
                corridor = [(a,b)]

            # check for spherical map adjacencies
            if a == self.map_.hor_tiles-1:
                (i,j) = [ (i,j) for (i,j) in pathways_hor if i == 0 and j == b ][0]
                adjacencies += [((i,j),(a,b))]
                tunnel_points += [(i,j)]
                tunnel_points += [(a,b)]

            

            (x,y) = (a,b)
        
        # add last horizontal adjacency
        if i == len(pathways_hor) -1:
            adjacencies += [(pathways_hor[len(pathways_hor) -2], pathways_hor[len(pathways_hor) -1])]
        if len(corridor) > 1:
            corridors += [corridor]

        if debug:
            self.print_debug_block('horizontal corridors', corridors)


        # vertical search
        (x,y) = pathways_ver[0]
        corridor = [(x,y)]
        i = 0
        for i in range(1,len(pathways_ver)):

            (a,b) = pathways_ver[i]

            # check for column change (coordinates are not adjacent)
            if a != x:
                if len(corridor) > 1:
                    corridors += [corridor] # length 1 is a section of a horizontal corridor
                corridor = [(a,b)]
                (x,y) = (a,b)
                continue

            # if vertically adjacent, add to adjacencies, add to current
            # vertical corridor
            if b == y+1:
                adjacencies += [((x,y),(a,b))]
                corridor += [(a,b)]
                if (a,b) in crossroads:
                    corridors += [corridor]
                    corridor = [(a,b)]
            else:
                if len(corridor) > 1: # length 1 is a section of a vertical corridor
                    corridors += [corridor]
                corridor = [(a,b)]

            # check for spherical map adjacencies
            if b == self.map_.ver_tiles-1:
                (i,j) = [ (i,j) for (i,j) in pathways_ver if j == 0 and i == a ][0]
                adjacencies += [((i,j),(a,b))]
                tunnel_points += [(i,j)]
                tunnel_points += [(a,b)]

            (x,y) = (a,b)

        if debug:
            self.print_debug_block('horizontal + vertical corridors', corridors)

        # add last vertical adjacency and last vertical corridor
        if i == len(pathways_ver) -1:
            adjacencies += [(pathways_ver[len(pathways_ver) -2], pathways_ver[len(pathways_ver) -1])]
        if len(corridor) > 1:
            corridors += [corridor]        

        # connect corridors
        corridors = self.connect_corridors(corridors, tunnel_points, crossroads)

        if debug:
            self.print_debug_block('adjacencies', adjacencies)
            self.print_debug_block('corridors', corridors)

        return adjacencies, corridors

#------------------------------------------------------------------------------#

    def connect_corridors(self, corridors, tunnel_points, crossroads):
        """connects horizontal and vertical subcorridors that make up the
        same corridor

        Args:
        corridors: a list of horizontal and vertical subcorridors

        Returns:
        a list of complete corridors
        """

        # TODO turn this into a function to be utilized to sort corridors and to sort tunnels
        # connect vertical and horizontal adjacent corridors
        connected = []
        while corridors != []:
            self.print_debug_block('corridors', corridors)
            corr = corridors.pop(len(corridors)-1)
            
            found = True
            while found:
                found = False
                self.print_debug_block('corr', corr)
                end0 = corr[0]
                end1 = corr[len(corr)-1]
                for c in corridors[:]: # copy of list to allow removals while iterating

                    #if end0 == (0,_)

                    if end0 == c[0] and end0 not in crossroads:
                        corr = corr[::-1] + c[1:]
                        self.print_debug_block('removed c', c)
                        corridors.remove(c)
                        found = True
                        break
                    elif end0 == c[len(c)-1] and end0 not in crossroads:
                        corr = c + corr[1:]
                        self.print_debug_block('removed c', c)
                        corridors.remove(c)
                        found = True
                        break
                    elif end1 == c[0] and end1 not in crossroads:
                        corr = corr + c[1:]
                        self.print_debug_block('removed c', c)
                        corridors.remove(c)
                        found = True
                        break
                    elif end1 == c[len(c)-1] and end1 not in crossroads:
                        corr = c[0:len(c)-1] + corr[::-1]
                        self.print_debug_block('removed c', c)
                        corridors.remove(c)
                        found = True
                        break

            connected += [corr]


        # TODO complete this part
        # connect corridors that form a tunnel (spherical map)
        tunnels = [ corr for corr in connected \
                            if corr[0] in tunnel_points \
                            or corr[1] in tunnel_points ]





        return [ Corridor(corr) for corr in connected ]

#------------------------------------------------------------------------------#

    def create_corridor_adjacencies(self, corridors, crossroads):
        """Creates pairs of adjacent corridors

        Args:
        corridors: a list of corridors

        Returns:
        a list of sorted tuples of adjacent corridors (with adjacency in the middle)
        """

        # connect vertical and horizontal adjacent corridors
        buffer = corridors
        corridors = []
        while buffer != []:

            corr = buffer.pop(len(buffer)-1)
            found = True
            while found:
                found = False
                end0 = corr[0]
                end1 = corr[len(corr)-1]
                for c in buffer[:]: # copy of list to allow removals while iterating
                    if end0 == c[0] and end0 not in crossroads:
                        corr = corr[::-1] + c[1:]
                        buffer.remove(c)
                        found = True
                        break
                    elif end0 == c[len(c)-1] and end0 not in crossroads:
                        corr = c[1:] + corr
                        buffer.remove(c)
                        found = True
                        break
                    elif end1 == c[0] and end1 not in crossroads:
                        corr = corr + c[1:]
                        buffer.remove(c)
                        found = True
                        break
                    elif end1 == c[len(c)-1] and end1 not in crossroads:
                        corr = c[1:len(c)-1] + corr[::-1]
                        buffer.remove(c)
                        found = True
                        break

            corridors += [corr]

        corridors = [ Corridor(corr) for corr in corridors ]

        if debug:
            self.print_debug_block('corridors', corridors)

        return corridors


################################################################################
#############################   AUXILIAR CLASSES   #############################
################################################################################

class Corridor():
    """Represents an uninterrupted path of adjacente coordinates with a
    crossroad at each end

    Args:
        coordinates: list of coordinates of the Corridor

    Attr:
        coordinates: list of coordinates of the Corridor
        length: length of coordinates without crossroad ends

    """
    def __init__(self, coordinates):
        self.coordinates = coordinates
        self.length = len(coordinates) -2
        self.ends = (coordinates[0], coordinates[len(coordinates)-1])
        
    def dist_end0(self, coord):
        return len(self.coordinates[0:coord])

    def dist_end1(self, coord):
        return len(self.coordinates[coord:self.length])

    def dist_end(self, coord, end):
        if end == self.ends[0]:
            return self.dist_end0(coord)
        return self.dist_end1(coord)

    def closest_end(self, coord):
        return self.dist_end0(coord) \
            if self.dist_end0(coord) <= self.dist_end1(coord) \
            else self.dist_end1(coord)

    def __str__(self):
        return str(self.coordinates)

    def __repr__(self):
        return self.__str__()