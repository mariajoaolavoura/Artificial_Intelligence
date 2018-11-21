from corridor import Corridor
import logging

#------------------------------------------------------------------------------#
# GLOBAL VARIABLES

# minimum escape margin if racing towards crossroad againt a ghost
SAFE_DIST_TO_CROSSROAD = 1
# distance at which ghost probably isn't in pursuit of pacman
SAFE_DIST_TO_GHOST = 7

# Usage MODE.EATING
class MODE(Enum):
    EATING  = 1
    FLIGHT  = 2
    PURSUIT = 3
    COUNTER = 4

class CORRIDOR_SAFETY(Enum):
    SAFE   = 1
    UNSAFE = 2

class CROSSROAD_SAFETY(Enum):
    GREEN  = 1
    YELLOW = 2
    RED    = 3

class Strategy_Advisor():
    """Analyses corridors safety (if contains ghost or not) and crossroads
    semaphores. Advises on a strategy for the given conditions

    Args:
    map_: instance of Map for the current level

    Attr:
    map_: instance of Map for the current level
    pathways: list of all coordinates that are not walls
    adjacencies: list of pairs of adjacent pathways
    corridors: list of coordinates that create a corridor
    crossroads: list of all coordinates that separate corridors
    """

    def __init__():
        self.map_ = map_
        
        self.state = state
    

    def advise(self, map_, state):
        
        pac_corridor, semaphores = compute_situation(state)

        # There is at least on crossroad with a ghost at a safe distance
        ghosts_dists = [semaphores[cross][0] for cross in semaphores]
        any_safe_dist = any([ dist >= SAFE_DIST_TO_GHOST for dist in ghosts_dists] )
        
        if any_safe_dist:
            return EATING

        # There are no safe crossroads
        colors = [semaphores[cross][1] for cross in semaphores]

        if any([color == GREEN for color in colors]):
            return EATING
        elif any([color == YELLOW for color in colors]):
            if len(state['boosts']) > 0:
                return COUNTER
            return FLIGHT
        else:
            return EATING
        
        




    def compute_situation(self, state):
        """

        Args:
        state: a list of lists with the state of every element in the game

        Returns: the key corresponding to the next move of PACMAN
        """

        # verify corridors safety
        ghosts = state['ghosts']
        unsafe_corridors = self.set_corridors_safety(ghosts)

        # Pac-Man position and corridor or list of corridors if Pac-Man is in crossroad
        pacman = state['pacman']
        pac_corridor = [ corr for corr in self.map_.corridors if pacman in corr ][0]

        #Pac-Man might be at a crossroad. Choose most dangerous corridor.
        for corr in self.map_.corridors:
            if corr.safe == False:
                pac_corridor = [corr]
                break
        pac_corridor = pac_corridor[0]

        # Evaluate Pac-Man escape crossroads as GREEN, YELLOW OR RED
        semaphores = get_crossroads_semaphores()

        logger.debug()

        return pac_corridor, semaphores    

        



    #* COMPLETE - NOT TESTED
    def set_corridors_safety(self, ghosts):
        """Verifies if a corridor is safe and sets a flag

        Args:
        state: a list of lists with the state of every element in the game

        Returns:
        A list of tuples of ghost and the corridor the ghost is in
        """

        unsafe_corridors = []
        for [ghost, zombie] in ghosts:
            for (cA, cB) in self.map_.corr_adjacencies:
                if zombie == False: # ghost is not zombie
                    if ghost in cA.coordinates: # pode dar erro: pesquisar [x,y] em (x,y)
                        cA.safe = False
                        #TODO consider changing to cA.safe = CORRIDOR_SAFETY.UNSAFE
                        unsafe_corridors += [(cA, ghost[0]]
                    elif ghost in cB.coordinates:
                        cB.safe = False
                        #TODO consider changing to cb.safe = CORRIDOR_SAFETY.UNSAFE
                        unsafe_corridors += [(cB, ghost[0])]
                    else:
                        cA.safe = True
                        cB.safe = True
                        #TODO consider changing to ca.safe = CORRIDOR_SAFETY.SAFE and cb.safe = CORRIDOR_SAFETY.UNSAFE
        
        return unsafe_corridors
            


    def calculate_crossroads_semaphores(self, unsafe_corridors, pac_corridor, pacman):
        """Objective of Pacman_agent - calculates the next position using
        multiple auxiliar methods

        Args:
        state: a list of lists with the state of every element in the game

        Returns: the key corresponding to the next move of PACMAN
        """

        # get ends of Pac-Man corridor
        pac_crossroads = pac_corridor.ends
        pac_dist_end0 = pac_corridor.dist_end0(pacman)
        pac_dist_end1 = pac_corridor.dist_end1(pacman)


        # verify crossroads semaphores
        semaphores = {}
        domain = Pathways(self.map_.corr_adjacencies)
        for (ghost, corr) in unsafe_corridors:

            # calculate trajectory of every ghost towards Pac-Man
            my_prob = SearchProblem(domain, corr, ghost, pac_corridor, pacman)
            my_tree = SearchTree(my_prob, "a*")
            _, cost, path = my_tree.search()

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
        semaphores = { crossroad : (min(costs),min(dists)) for crossroad in semaphores }

        # compare distance of Pac-Man and ghosts to crossroads and
        # attribute a semaphore color
        for cross in semaphores:

            if cross == pac_corridor.ends[0]:
                end = pac_dist_end0
            else:
                end = pac_dist_end1
                
            if semaphores[cross][1] > end + 1:
                semaphores[cross] = (semaphores[cross][0], CROSSROAD_SAFETY.GREEN)
            elif semaphores[cross][1] == end + 1:
                semaphores[cross] = (semaphores[cross][0], CROSSROAD_SAFETY.YELLOW)
            else:
                semaphores[cross] = (semaphores[cross][0], CROSSROAD_SAFETY.RED)

        return semaphores

        


    def boosts_analyser(self):
        """Objective of Pacman_agent - calculates the next position using
        multiple auxiliar methods

        Args:
        state: a list of lists with the state of every element in the game

        Returns: the key corresponding to the next move of PACMAN
        """
        pass
