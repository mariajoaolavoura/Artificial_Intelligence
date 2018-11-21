from corridor import Corridor
import logging

debug = True

# logs are written to file logger.log after the client is closed
# possible messages: debug, info, warning, error, critical 
# how to use: logging.typeOfMessage('message')
logger = logging.getLogger('static_analysis_logger')
logger_format = '[%(lineno)s - %(funcName)20s() - %(levelname)s]\n %(message)s\n'
#logger_format = '%(levelname)s:\t%(message)' # simpler format

# currently writing over the logger file, change filemode to a to append
logging.basicConfig(format=logger_format, filename='loggerStaticAnalysis.log', filemode='w', level=logging.DEBUG)

class Static_Analysis():
    """Makes the static analysis of the Map instance for the game. 

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
        self.map_ = map_
        self.pathways = self.create_pathways_list()
        self.crossroads = self.create_crossroads_list(self.pathways)
        self.coord_adjacencies, self.corridors = self.create_static_maps(self.pathways, self.crossroads)
        self.corr_adjacencies =self.create_corridor_adjacencies(self.corridors, self.crossroads)

        self.corridors = [ Corridor(corr) for corr in self.corridors ]


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
                tunnel_points += [(i,j)]
                tunnel_points += [(a,b)]

            (x,y) = (a,b)
        
        # add last horizontal corridor
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
                tunnel_points += [(i,j)]
                tunnel_points += [(a,b)]

            (x,y) = (a,b)

        if debug:
            self.print_debug_block('horizontal + vertical corridors', corridors)

        # add last vertical corridor
        if len(corridor) > 1:
            corridors += [corridor]        

        # connect corridors
        corridors = self.connect_corridors(corridors, tunnel_points, crossroads)

        if debug:
            self.print_debug_block('coord_adjacencies', coord_adjacencies)
            self.print_debug_block('corridors', corridors)

        return corridors

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
        corridors += connected

        return corridors

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