from game_consts import *
from tree_search import SearchProblem, SearchTree
from pathways import Pathways
from corridor import Corridor


# logger
# logs are written to file strategy_advisor.log after the client is closed
# possible messages: debug, info, warning, error, critical 
# how to use: logger.typeOfMessage('message')
logger = setup_logger('strategy_advisor', 'strategy_advisor.log')

class Strategy_Advisor():
    """Analyses corridors safety (if contains ghost or not) and crossroads
    semaphores. Advises on a strategy for the given conditions.

    Args:
    map_: instance of Map for the current level
    state: the game state given by the server

    Attr:
    ghosts: A set of quadruples with (ghost_position, zombie, timeout, distance_to_pacman)
    """

    def __init__(self, map_, state):
        self.map_ = map_
        self.state = state
        self.ghosts = {}
        self.pac_corridor = []
    

    def advise(self):
        """Given the safety of corridors and crossroads, advises a MODe of play

        Returns: the advised MODE of play
        """
        
        semaphores = self.compute_situation()

        # There is at least on crossroad with a ghost at a safe distance
        ghosts_dists = [semaphores[cross][0] for cross in semaphores]
        any_safe_dist = any([ dist >= SAFE_DIST_TO_GHOST for dist in ghosts_dists] )
        
        if any_safe_dist:
            return MODE.EATING

        # There are no safe crossroads
        colors = [semaphores[cross][1] for cross in semaphores]

        if any([color == MODE.GREEN for color in colors]):
            return MODE.EATING
        elif any([color == MODE.YELLOW for color in colors]):
            if len(self.state['boosts']) > 0:
                return MODE.COUNTER
            return MODE.FLIGHT
        else:
            return MODE.EATING
        
        

    def compute_situation(self):
        """Organizes state info and calls needed methods to analise Pac-Man
        current scenario

        Returns:
        A tuple with the updated corridor where Pac-Man is and the semaphores
        of it's crossroads
        """

        # verify corridors safety
        ghosts = self.state['ghosts']
        unsafe_corridors = self.set_corridors_safety(ghosts)

        # Pac-Man position and corridor or list of corridors if Pac-Man is in crossroad
        pacman = (self.state['pacman'][0],self.state['pacman'][1])
        self.pac_corridor = [ corr for corr in self.map_.corridors if pacman in corr.coordinates ]

        #Pac-Man might be at a crossroad. Choose most dangerous corridor.
        for corr in self.pac_corridor:
            if corr.safe == CORRIDOR_SAFETY.UNSAFE:
                self.pac_corridor = [corr]
                break
        self.pac_corridor = self.pac_corridor[0]

        # Evaluate Pac-Man escape crossroads as GREEN, YELLOW OR RED
        semaphores = self.calculate_crossroads_semaphores(unsafe_corridors, self.pac_corridor, pacman)

        return semaphores    

        

    #* COMPLETE - NOT TESTED
    def set_corridors_safety(self, ghosts):
        """Sets the corridors safety flag according to the existence of ghosts

        Args:
        ghots: a list with the position of all non zombie ghosts

        Returns:
        A list of tuples with the unsafe corridors and the position of the ghost
        in that corridor. If more than one ghost is in a given corridors, the
        corridor is returned multiple times tupled with each ghost 
        """

        unsafe_corridors = []
        for ghost in [ghost for ghost in ghosts if ghost[1] == False]: # non zombie ghosts
            for (cA, cB) in self.map_.corr_adjacencies:
                if ghost[0] in cA.coordinates:     # pode dar erro: pesquisar [x,y] em (x,y)
                    cA.safe = CORRIDOR_SAFETY.UNSAFE
                    unsafe_corridors += [cA]
                elif ghost[0] in cB.coordinates:
                    cB.safe = CORRIDOR_SAFETY.UNSAFE
                    unsafe_corridors += [cB]
                else:
                    cA.safe = CORRIDOR_SAFETY.SAFE
                    cA.safe = CORRIDOR_SAFETY.SAFE

        return unsafe_corridors
            


    def calculate_crossroads_semaphores(self, unsafe_corridors, pac_corridor, pacman):
        """Attributes a SEMAPHORE color for each crossroad in Pac-Man's corridor
        by comparingthe distance of Pac-Man and the closest ghost to that
        crossroad

        Args:
        unsafe_corridors: list of corridors that have a ghost
        pac_corridor: the corridor Pac-Man is in
        pacman: the coordinates of Pac-Man position

        Returns:
        A dictionary with key = crossroad and value of a tuple with the distance
        of the ghost to Pac-Man and the distance of the ghost to the crossroad
        """

        # get ends of Pac-Man corridor
        pac_crossroads = pac_corridor.ends
        pac_dist_end0 = pac_corridor.dist_end0(pacman)
        pac_dist_end1 = pac_corridor.dist_end1(pacman)

        # verify crossroads semaphores
        semaphores = {}
        domain = Pathways(self.map_.corr_adjacencies, self.state['energy'])
        for ghost in [ghost for ghost in self.state['ghosts'] if ghost[1] == False]: # non zombie ghosts

            # get the corridor the ghost is in
            ghost_corr = None
            if ghost[0] not in self.map_.ghosts_den:
                for corr in unsafe_corridors:
                    print(str(ghost[0]) + "---" + str(corr.coordinates))
                    if ghost[0] in corr.coordinates:
                        ghost_corr = corr
                        break

            # calculate trajectory of every ghost towards Pac-Man
            if not ghost_corr == None:
                my_prob = SearchProblem(domain, ghost_corr, ghost, pac_corridor, pacman)
                my_tree = SearchTree(my_prob, "a*")
                _, cost, path = my_tree.search()
            else:
                continue

            # update sel.ghosts with new attribute of distance_to_pacman
            self.ghosts += (ghost[0], ghost[1], ghost[2], cost)

            # the crossroad that the ghost will use to get to Pac-Man
            crossroad = path[-2].ends[0] if path[-2].ends[0] != pacman else path[-2].ends[1]

            # calculate distance of every ghost to Pac-Man crossroads
            ghost_dist = cost - pac_corridor.dist_end(pacman, crossroad)

            if crossroad in semaphores:
                costs, dists = semaphores[crossroad]
                costs += [cost]
                dists += [ghost_dist]
                semaphores[crossroad] = (costs, dists)
            else:
                semaphores[crossroad] = [(cost, ghost_dist)]
        
        # select most dangerous ghost distancies
        if len(semaphores) > 0:
            semaphores = { crossroad : (min(costs),min(dists)) for crossroad in semaphores }
        else: #TODO temporary solution for when ghosts are in the den
            semaphores = {}
            semaphores[pac_crossroads[0]] = (self.map_.map_.ver_tiles, self.map_.map_.ver_tiles)
            semaphores[pac_crossroads[1]] = (self.map_.map_.ver_tiles, self.map_.map_.ver_tiles)

        # compare distance of Pac-Man and ghosts to crossroads and
        # attribute a semaphore color
        for cross in semaphores:

            if cross == pac_corridor.ends[0]:
                end = pac_dist_end0
            else:
                end = pac_dist_end1
                
            if semaphores[cross][1] > end + 1:
                semaphores[cross] = (semaphores[cross][0], SEMAPHORE.GREEN)
            elif semaphores[cross][1] == end + 1:
                semaphores[cross] = (semaphores[cross][0], SEMAPHORE.YELLOW)
            else:
                semaphores[cross] = (semaphores[cross][0], SEMAPHORE.RED)

        return semaphores

        


    def boosts_analyser(self):
        """

        Args:

        Returns:
        """
        pass
