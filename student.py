from tree_search import SearchTree
import random
import logging

#$ PORT=80 SERVER=pacman-aulas.ws.atnog.av.it.pt python client.py
# to kill server: fuser 8000/tcp

# for debug purposes
debug = True

# logs are written to file logger.log after the client is closed
# possible messages: debug, info, warning, error, critical 
# how to use: logging.typeOfMessage('message')
logger = logging.getLogger('student_logger')
logger_format = '[%(lineno)s - %(funcName)20s() - %(levelname)s]\n %(message)s\n'
#logger_format = '%(levelname)s:\t%(message)' # simpler format

# currently writing over the logger file, change filemode to a to append
logging.basicConfig(format=logger_format, filename='logger.log', filemode='w', level=logging.DEBUG)

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
        logger.warning('\n\n\n ========================== NEW EXECUTION ==========================\n')
        logger.debug('CREATING PACMAN AGENT\n')

        # static info from mapa.py Map
        self.map_ = map_
        self.pathways = self.create_pathways_list()
        self.crossroads = self.create_crossroads_list(self.pathways)
        self.adjacencies, self.cae0ad115ec86ac73b730a6fa08032ebfe40afa71orridors = self.create_static_maps(self.pathways, self.crossroads)
        self.corr_adjacencies =self.create_corridor_adjacencies(self.corridors, self.crossroads)

        logger.debug('CREATED PACMAN AGENT')

    def get_next_move(self, state):
        """Objective of Pacman_agent - calculates the next position using
        multiple auxiliar methods

        Args:
        state: a list of lists with the state of every element in the game

        Returns: the key corresponding to the next move of PACMAN
        """

        #logger.debug(nt("\nEnergy size is : " + str(len(state['energy'])) + "\n")

        #! ##########   STRATEGY   ##########
        #?      -> L
        #*      -> P
        #TODO   -> MJ

        #? criar modes:
            #? counter_mode (pesquisar boost para terminar perseguição)
            #? pursuit_mode (search and destroy dos fantasmas)
            #? eating_mode  (sem perigo, maior preocupacao, comer bolinhas)
            #? flight_mode  (pesquisa por corredores seguros, com ou sem bolinhas, se houver boosts usar)

        #* modes mais importantes: pursuit e flight mode (eating seria por defeito, o COUNTER é relevante?)
        #* implementação : Enum e detecção usando ifs
        #* how to use enums (if I correctly remember)
        #* from enum import Enum
        # class Mode(Enum):
        #   COUNTER = 1
        #   PURSUIT = 2
        #   EATING  = 3
        #   FLIGHT  = 4

        #? calcular distancia a pontos acessiveis
        #? calcular distancia aos meus cruzamentos
        #? calcular distancia a boosts
        #? calcular distancia a fantasmas
        #* basta um método distanceTo(original_pos, dest_pos)
        #* a diferença estará na forma de obter dest_pos, como é óbvio

        #? verificar condicoes do meu corredor

        #* algoritmo
        #* porque não uma simplificação (só se analisam corredores nos cruzamentos e
        #* deixamos de analisar os cruzamentos em si)
        #? corredor SAFE?
            #* continua no corredor até um cruzamento

            #? Cruzamentos VERDE?
                #? EATING_MODE
                    #? ignorar fantasmas...
                    #? ignorar boosts
                    #? pesquisas bolinhas, caminho mais seguro
            #? cruzamentos VERDE e AMARELO
                #? EATING_MODE
                    #? OPCAO 1 - aproveitar para limpar lado amarelo enquanto 'e possivel
                    #? OPCAO 2 - continuar a pesquisar caminho mais seguro
                    #* OPCAO 1 é mais arriscada mas mais adequada para obter mais pontos mais depressa (prefiro)
            #? cruzamentos AMARELO
                #? FLIGHT_MODE
                    #? OPCAO 1 - fugir para um qualquer caminho seguro
                    #? OPCAO 2 - fugir pelo lado que tem mais bolinhas
                    #? OPCAO 3 - fugir pelo caminha mais curto (evitar que mais fantasmas se aproximem no entretanto?)
                    #? OPCAO 4 - sistema de pesos com as anteriores
                #* muito complexo... temos de tentar simplificar
            #? cruzamento AMARELO e VERMELHO
                #? FLIGHT_MODE
                #? fugir pelo lado possivel para o sitio mais seguro (com ou sem bolinhas)
            #? cruzamentos VERMELHOS
                #? FLIGHT_MODE
                #? fugir pelo menos vermelho
                #? morrer com dignidade e apanhar o maximo de bolinhas
                #* simplemesmente evitá-los (voltar para trás)?

        #? corredor NOT SAFE
            #* acho que querias dizer cruzamentos, não corredores :P
            #? corredor livre a AMARELO
                #? FLIGHT_MODE
            #? corredor livre a VERDE
                #? há BOOST?
                    #? pesquisar boost
                #? não há boost
                    #? fantasma nao nos afecta, desde que nao se volte atras. pesquisar bolinhas

            #* se o corredor não for safe: a) evitamo-lo ou b) escolhemos o melhor em termos de pontos (BOOST + energias - ghosts)
            #* ideia: método que, dado um corredor, devolve o seu valor (BOOST + energias - ghosts). 
            #* é um revisit da ideia dos pesos mas não sofre dos mesmo problemas 
            #*(um corredor nunca é muito extenso e a análise seria ocasional)

        #print("\nEnergy size is : " + str(len(state['energy'])) + "\n")
        # create a vector for every element in the game
        # every element points pacman teh next move to get to it
        vectors = []
        #logger.debug(nt(state['energy'])
        
        pac_pos = (state['pacman'][0], state['pacman'][1])
        # if debug:
        #     logger.debug("\t pacman is in position " + str(pac_pos))

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
                logger.warning("There is a problem not solved yet in this line of code!")
        
        if debug:
            logger.debug('The key is: ' + str(key))


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
        #     logger.debug("***********************************************************")
        #     logger.debug('\t get vector was called! ')
        #     logger.debug("***********************************************************")

        # convert list to dictionary with zero weight for each element
        weight_dict = { (x,y):1 for [x,y] in nodes_to_search }

        for (x,y) in nodes_to_search:

            # if debug:
                # logger.debug("#######################################################")
                # logger.debug('\t calculating vector for pos: ' + str((x,y)))
                # logger.debug("#######################################################")
        
            # if debug:
            #     logger.debug("\t cycle  for position " + str((x,y)))

            # search the path
            # if debug:
            #     logger.debug("SearchDomain being called to create")
            domain = Pathways(self.adjacencies)

            # if debug:
            #     logger.debug("SearchProblem " + str(i) + " being called to create")
            my_prob = SearchProblem(domain,(x,y),pac_pos)
            
            # if debug:
            #     logger.debug("SearchTree " + str(i) + " being called to create")
            my_tree = SearchTree(my_prob, weight_dict, self.strategy)
            
            next_result = my_tree.search()

            if next_result != None:
                next_res, next_cost = next_result
                next_pos += [((x,y) , next_res, next_cost)]
            else:
                next_pos += [((x,y), pac_pos, 0)]

            #logger.debug((x,y))
            #logger.debug(next_result)
            
            #logger.debug("\t search " + str(i) + " was completed!")

            # if debug:
            #     logger.debug('\t Calculating next move for position: ' + str((x,y)))

        #logger.debug(next_pos)

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

                logger.debug(str(next_pos[i][0]) + " : vector is: " + str(dir))
            
            # if debug:
            #     logger.debug("#######################################################")
            #     logger.debug('\t Vector is ' + str(dir))
            #     logger.debug("#######################################################")

        #logger.debug(weight_dict)



        # sum all the vectors
        vec_x = 0
        vec_y = 0
        for (x,y) in vectors:
            vec_x += x
            vec_y += y
        
        #logger.debug("\npacman is in position " + str(pac_pos[0], pac_pos[1]))
        #logger.debug('Sum of all vectors is: ' + str(vec_x) + ', ' + str(vec_y) + "\n")

        if debug:
            logger.debug("#######################################################")
            logger.debug('\t Vector is ' + str((vec_x, vec_y)))
            logger.debug("#######################################################")

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
        #logger.debug("#######################################################")
        #logger.debug('\t ' + string + ' is: ')
        #logger.debug("#######################################################")
        #logger.debug(var)


################################################################################
#####################   STATIC ANALYSIS AUXILIAR METHODS   #####################
################################################################################
    
    #* ##########   TESTED AND VERIFIED   ##########"""
    def create_pathways_list(self):
        """Create a list with all coordinates that are not walls

        Returns:
        Tuple of lists (for efficiency purposes):
        pathways_hor: pathways organized by row
        pathways_ver: pathways organized by column
        """

        # find ghosts den. This area will not be used in any search or strategy
        # and should be avoided by PACMAN
        ghosts_den = self.get_ghosts_den(self.map_)

        pathways_hor = []
        for y in range(self.map_.ver_tiles):
            for x in range(self.map_.hor_tiles):
                
                if not self.map_.is_wall((x,y)): 
                    pathways_hor += [(x,y)]

        pathways_hor = [ p for p in pathways_hor if p not in ghosts_den ]
        pathways_ver = sorted(pathways_hor, key=lambda y: (x,y))

        if True:
            self.print_debug_block('ghosts_den', ghosts_den)
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

    def get_ghosts_den(self, map_):
        """delimit the coordinates that make up the ghosts den

        Args:
        map_       : map of the game

        Returns:
        den_corners: list of coordinates of the points inside the den (including the walls and entrances)
        """

        # get ghots spawn point (which is itself part of the den)
        spawn = map_.ghost_spawn
        logger.debug("Spawn point is: " + str(spawn))
        
        # list of the 4 corners of the den (den is a rectangle)
        den_corners = []

        # possible directions to go from a given point in the map
        # format (dir_x, dir_y)
        # currently init is equivalent to left, right, up, down
        possible_dirs =[(-1,0), (1,0), (0, 1), (0, -1)]    

        # initialize to_visit queue
        # to_visit is a queue with the points to visit
        # each position is a tuple (pos_x, pos_y, list of possible directions)
        to_visit = [(spawn, possible_dirs)]     

        while len(to_visit) > 0:
            # "pop" element from queue to_visit
            current_pos, current_dirs = to_visit[0]
            current_x, current_y = current_pos
            to_visit = to_visit[1:] 
            
            adj_walls = []
            
            logger.debug("Analyzing " + str((current_pos, current_dirs)))

            for current_dir in current_dirs:
                current_dir_x, current_dir_y = current_dir    
                remaining_dirs = [dir_ for dir_ in current_dirs if dir_ != current_dir]
                
                # New position is obtained traveling in the current_direction from the (current_x, current_y)
                new_pos = current_x + current_dir_x, current_y + current_dir_y

                logger.debug("Following direction "   + str(current_dir) + " from " + str((current_x, current_y)))
                logger.debug("Remaining directions: " + str(remaining_dirs))
                logger.debug("New pos to analyze: "   + str(new_pos))

                # if it's a wall, add the new position to the list of the adjacent walls
                if (self.map_.is_wall(new_pos)):
                    logger.debug("Detected wall at " + str(new_pos) + " dir " + str(current_dir))
                    
                    adj_walls += [new_pos]
                  
                # if it's not a wall, add the new position to the positions to visit. 
                else:
                    logger.debug("No Detected wall.\n Adding " +  str(new_pos) + " to visit")

                    # from the new position we can go to the remaning_dirs + the oposite direction of where it came from 
                    # (thus avoiding repetead points, ie going back)
                    possible_dirs = [current_dir] + [dir_ for dir_ in remaining_dirs if dir_ != (current_dir_x * -1, current_dir_y * -1)]
                    to_visit += [(new_pos, possible_dirs)]

                    logger.debug("New to_visit is: " + str(to_visit))
            
            # the current point is a candidate to be a corner (2 adjacent walls)
            if len(adj_walls) == 2: 

                # verify if adjacent walls are valid
                # all corners in a rectangle has 2 adjacent walls
                # but we can have points with 2 adjacent walls 
                # without being a corner (see point (3, 15) of the original map, for example)
                wall1_x, wall1_y = adj_walls[0]
                wall2_x, wall2_y = adj_walls[1]
                logger.debug("Analyzing corner with wall " + str((wall1_x, wall1_y)) + " and " + str((wall2_x, wall2_y)))
                
                if (abs(wall1_x - wall2_x) == 1 and abs(wall1_y - wall2_y) == 1):
                    # we can have repeteaded corners 
                    # we can reach corners from different paths
                    logger.debug("Adding valid corner")
                    logger.debug(den_corners + [(current_x, current_y)])
                    den_corners = list(set(den_corners + [(current_x, current_y)]))
                    
                    # Found all den corners (a rectangular den has 4 corners)
                    # Since the den is rectangular so, we can define the bounds of the den 
                    # and its inside points using the corners
                    if (len(den_corners) == 4):
                        logger.debug("Found all 4 corners")
                        logger.debug("Den corners " + str(den_corners))
                        #print("Den corners are " + str(den_corners))
                        
                        # previously
                        #return den_corners

                        # return all positions of the outer square
                        # 4 corners, two possible values for x and y: the min and max
                        x_values, y_values = set([x for (x, y) in den_corners]), set([y for (x, y) in den_corners])
                        big_x, big_y = max(x_values), max(y_values)
                        small_x, small_y = min(x_values), min(y_values)
                        
                        # include the walls
                        small_x -= 1
                        small_y -= 1
                        big_x   += 1
                        big_y   += 1
                        den = []

                        for i in range(small_x, big_x + 1, 1):
                            for j in range(small_y, big_y + 1, 1):
                                logger.debug("Den point is " + str((i, j)))
                                den += [(i, j)]

                        logger.debug("Returning " + str(den) + " (length " + str(len(den)) + ")")
                        print("Den is (includes walls & entrances) " + str(den) + " (length " + str(len(den)) + ")")

                        return den

                    # clean up to_visit
                    # after finding a corner, we no longer have to
                    # search using the points in that quadrant 
                    # so we can clean up the list based on zones

                    # Note:
                    # visit[0] -> pos
                    # visit[0][0/1] -> pos_x/pos_y
                    if (current_x < spawn[0]):
                        if (current_y > spawn[0]): # left up corner
                            logger.debug("Clean left up area")
                            to_visit = [visit for visit in to_visit if visit[0][0] > spawn[0] or (visit[0][0]  < spawn[0] and visit[0][1] < spawn[1])]
                        if (current_y < spawn[0]): # left down corner
                            logger.debug("Clean left down area")
                            to_visit = [visit for visit in to_visit if visit[0][0] > spawn[0] or (visit[0][0]  < spawn[0] and visit[0][1] > spawn[1])]
                    elif (current_x > spawn[0]):
                        if (current_y > spawn[0]): # right up corner
                            logger.debug("Clean right up area")
                            to_visit = [visit for visit in to_visit if visit[0][0] < spawn[0] or (visit[0][0]  > spawn[0] and visit[0][1] < spawn[1])]
                        if (current_y < spawn[0]): # right down corner
                            logger.debug("Clean right down area")
                            to_visit = [visit for visit in to_visit if visit[0][0] < spawn[0] or (visit[0][0]  > spawn[0] and visit[0][1] > spawn[1])]
                               
        # Should never reach this      
        return []
        
    

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
            corr = corridors.pop()
            
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
        tunnels = self.find_tunnels(corridors, tunnel_points)
        corridors = [ c for c in corridors if c not in tunnels]
        tunnels = self.connect_tunnels(tunnels, crossroads)
        corridors += tunnels

        return [ Corridor(corr) for corr in connected ]

#------------------------------------------------------------------------------#

    def find_tunnels(self, corridors, tunnel_points):
        return [ corr for corr in corridors \
                            if corr[0] in tunnel_points \
                            or corr[1] in tunnel_points ]

#------------------------------------------------------------------------------#

    def connect_tunnels(self, tunnels, crossroads):

        connected = []
        while tunnels != []:

            tun = tunnels.pop()

            found = True
            while found:
                found = False
                #self.print_debug_block('tun', tun)
                end0 = tun[0]
                end1 = tun[len(tun)-1]
                for t in tunnels[:]: # copy of list to allow removals while iterating

                    #if end0 == (0,_)

                    if end0 == t[len(t)-1] and end0 not in crossroads:
                        tun = t + tun[1:]
                        self.print_debug_block('removed t', t)
                        tunnels.remove(t)
                        found = True
                        break
                    elif end1 == t[0] and end1 not in crossroads:
                        tun = tun + t[1:]
                        self.print_debug_block('removed t', t)
                        tunnels.remove(t)
                        found = True
                        break

            connected += [tun]
        
        return connected

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

            corr = buffer.pop()
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

    def sub_corridors(self, coord):
        index = self.coordinates.index(coord)
        return Corridor(self.coordinates[:index+1]), Corridor(self.coordinates[index:])

    def __str__(self):
        return str(self.coordinates)

    def __repr__(self):
        return self.__str__()
        