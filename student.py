from game_consts import *
from static_analysis import Static_Analysis
from pathways import Pathways
from tree_search import SearchTree, SearchProblem
from corridor import Corridor
from strategy_advisor import Strategy_Advisor
import logging

#$ PORT=80 SERVER=pacman-aulas.ws.atnog.av.it.pt python client.py
# to kill server: fuser 8000/tcp

# logger
# logs are written to file student.log after the client is closed
# possible messages: debug, info, warning, error, critical 
# how to use: logger.typeOfMessage('message')
logger = setup_logger('student', 'student.log')

# for debug purposes
debug = True


#! ##########   PAC-MAN AGENT GLOBAL STRATEGY   ##########

    #! ###    CONCEPTS    ###

    #! Corridor
        #* A list of path coordinates with only two adjacent coordinates
        #* and two crossroads as ends

    #! Crossroad
        #* A coordinate that joins corridors. The crossroad belong to all
        #* corridors it joins

    #! Corridor SAFE vs UNSAFE
        #* SAFE - Has no ghosts
        #* UNSAFE - Has one or more ghosts

    #! Crossroad GREEN - YELLOW - RED
        #* Refers to the crossroads directly accessible to Pac-Man (the
        #* ends of it's corridor)
        #* GREEN - No ghosts in proximity
        #* YELLOW - There are ghosts at a dangerous distance of the crossroad
        #*          (default = 1). Pac-Man can escape if he goes directly through
        #*          that end
        #* RED - Considering that the ghosts is in pursuit of Pac-Man, it is
        #*       impossible for Pac-Man to escape from that end before the ghost
        #*       gets to it (or the ghost is already inside Pac-Man's Corridor)


    #! Strategy Game Modes
        #* EATING_MODE - Pac-Man is safe. Focus on eating energies. Tries to
        #*               find closest energies through safest paths
        #* COUNTER_MODE - Pac-Man is almost surrounded. Focus on eating boosts.
        #* PURSUIT_MODE - Pac-Man is safe and there are zombie ghosts.
        #*               Focus on eating ghosts.
        #* FLIGHT_MODE - Pac-Man is almost surrounded. There are no boosts
        #*               available. Focus on finding the closest safest Corridor.

    #! Static Analysis of Map provides
        #* pathways
        #* corridors
        #* crossroads
        #* corridor_adjacencies
    
    #! Strategy Guidelines
        #* Pac-Man Agent calls Strategy Advisor
        #*      Strategy Advisor analyses:
        #*          Corridor Safety
        #*          Crossroads Semaphores
        #*          Distance to ghosts
        #*      Strategy Advisor advises a Game Mode
        #* Pac-Man calls Game Mode Agent to get next move
        #*      Game Mode tries to find the next move
        #* Pac-Man analyses next move
        #*      Is it specific (only one solution)
        #*          Pac-Man accepts next move
        #*      It's not specific (strategy was not correct)
        #*          Pac-Man calls Strategy Adjuster
        #*              Strategy Adjuster evaluates new info and advises a new Game Mode
        #*          Pac-Man call Game Mode Agent to get next move
        #*              Game Mode tries to find a solution
        #*          Pac-Man accepts best solution found (if more than one)



class Pacman_agent():
    """Creates the PACMAN agent that analyses the given 'Map' and 'state'
    to decide which direction to take and win the game 

    Args:
    map_: instance of Map for the current level

    Attr:
    map_: instance of Map for the current level
    static_analysis: instance of Static_Analysis containing:
                - pathways: list of all coordinates that are not walls
                - adjacencies: list of pairs of adjacent pathways
                - corridors: list of coordinates that create a corridor
                - crossroads: list of all coordinates that separate corridors
    """

    def __init__(self, map_,): 
        logger.warning('\n\n\n ========================== NEW EXECUTION ==========================\n')
        logger.debug('CREATING PACMAN AGENT\n')

        self.map_ = Static_Analysis(map_)
        self.debug = False

        logger.debug('CREATED PACMAN AGENT')


    def get_next_move(self, state):
        """Objective of Pacman_agent - calculates the next position using
        multiple auxiliar methods

        Args:
        state: a list of lists with the state of every element in the game

        Returns: the key corresponding to the next move of PACMAN
        """

        #logger.debug(nt("\nEnergy size is : " + str(len(state['energy'])) + "\n")

        

        # get advice on the next move
        strategy_advisor = Strategy_Advisor(self.map_, state)
        mode_handler = strategy_advisor.advise()
        next_move = self.mode(mode_handler, strategy_advisor, state)

        # if advice is not specific, adjustments to the strategy may be needed
        if (next_move == False): # correct when methods are implemented
            strategy_adjuster = Strategy_Adjuster()
            mode_handler = strategy_adjuster.adjustStrategy()
            next_move = self.mode(mode_handler, state)
        
        # calculate and return the key
        if (next_move == [5,23]):
            print("KEY IS " + str(self.calculate_key(state['pacman'], next_move)))

        logger.debug("KEY IS " + str(self.calculate_key(state['pacman'], next_move)) + "\n\n")
        return self.calculate_key(state['pacman'], next_move)



    def mode(self, mode_handler, advisor, state):
        if mode_handler == MODE.EATING:
            next_move = self.eating_agent(advisor, state)
        elif mode_handler == MODE.FLIGHT:
            next_move = self.flight_agent()
        elif mode_handler == MODE.PURSUIT:
            next_move = self.pursuit_agent()
        else: # next_move == MODE.COUNTER
            next_move = self.counter_agent()
        return next_move



    def calculate_key(self, pacman, next_move):
        """Calculates the 'wasd' key that corresponds to the next move

        Args:
        pacman: the coordinates of Pac-Man position
        next_move: the coordinates of the position to go to

        Returns:
        The 'wasd' key for moving from pacman to next_move
        """
        #print("NEXT MOVE: " + str(pacman) + ", " + str(next_move))
        px, py = pacman
        nx, ny = next_move
        if nx > px:
            key = 'd'
        elif nx < px:
            key = 'a'
        elif ny > py:
            key = 's'
        else: # ny < py
            key = 'w'
        
        return key



    def eating_agent(self, advisor, state):

        domain = Pathways(self.map_.corr_adjacencies, state['energy'] + state['boost'])

        acessible_energies = []
        points = state['energy'] + state['boost']
        
        for energy in points:

            domain = Pathways(self.map_.corr_adjacencies.copy(), [state['energy'] + state['boost']])
            # print("Energy #######################################")
            # print(energy)
            # print("#######################################")

            corridor = None
            for corr in self.map_.corridors:
                if energy in corr.coordinates:
                    corridor = corr

            # print("Corridor #######################################")
            # print(corridor)
            # print("#######################################")
            if (self.debug):
                pass
                #print(energy)
            my_prob = SearchProblem(domain, corridor, energy, advisor.pacman_info.corridor, advisor.pacman_info.position)
            my_tree = SearchTree(my_prob, "a*")
            search_results = my_tree.search()
            

            if search_results != None:
                #? avoid repetead energies. 
                if (search_results[0] not in acessible_energies):       
                    acessible_energies += [search_results[0]]

        logger.debug("NEW! PACMAN POS" + str(advisor.pacman_info.position))
        #acessible_energies = [a for a in acessible_energies if a != advisor.pacman_info.position]
        logger.debug("Acessible_Energies #######################################")
        logger.debug(acessible_energies)
        logger.debug("#######################################")
        
        logger.debug("Returning " + str(acessible_energies[0]))
        return acessible_energies[0]
    

    def flight_agent(self, advisor):
        '''
        args:
        advisor: instance of Strategy_Advisor
        '''
        
        pac_crossroads = advisor.pac_corridor.ends

        adj_corridors = [ corr for corr in self.map_.corr_adjacencies \
                                if pac_crossroads[0] in corr.coordinates \
                                or pac_crossroads[1] in corr.coordinates ]

        #crossroads YY, YR, RR -> semaphore.Y or semaphore.R for end[0] and end[1]
        #ghost.distPac
        #corr adj SAFE, UNSAFE 

        #pac corr UNSAFE? (ghost no mesmo corr do pac)
            #crossroad[0].RED and crossroad[1].RED?
                #distGhostPac >= SAFE_DIST_TO_GHOST?
                    #escolhe lado
                #distGhostPac < SAFE_DIST_TO_GHOST?
                    #lado com maior dist
            
            #crossroad[0].YELLOW?
                #próximo corr SAFE?
                    #escolhe saída
                #proximo corr UNSAFE?
                    #ghost do prox corr (crossroad[0]) pode nao estar em perseguiçao, so...
                    #distGhostPac >= SAFE_DIST_TO_GHOST?
                        #escolhe saida
                    #distGhostPac < SAFE_DIST_TO_GHOST?
                        #escolhe o 1º corr
                    

            #else crossroad[1].YELLOW?
                #próximo corr SAFE?
                    #escolhe saída
                #proximo corr UNSAFE?
                    #ghost do prox corr (crossroad[1]) pode nao estar em perseguiçao, so...
                    #distGhostPac >= SAFE_DIST_TO_GHOST?
                        #escolhe saida
                    #distGhostPac < SAFE_DIST_TO_GHOST?
                        #escolhe o 1º corr
                    

        #else pac corr SAFE? (corr do pac nao tem ghost)
            #crossroad[0].YELLOW and crossroad[1].YELLOW?
                #pesquisar todos os prox corredores
                #SAFE?
                    #escolhe saida
                #UNSAFE? 
                    #escolhe o 1º corr do crossroad mais perto

            #crossroad[0].RED?
                #crossroad[1].YELLOW?
                    #próximo corr SAFE?
                        #escolhe saída do ghost mais longe
                    #próximo corr UNSAFE?
                        #ghost do prox corr (crossroad[1]) pode nao estar em perseguiçao, so...
                        #distGhostPac >= SAFE_DIST_TO_GHOST?
                            #escolhe saida
                        #distGhostPac < SAFE_DIST_TO_GHOST?
                            #escolhe o 1º corr
                #else crossroad[1].RED?
                    #morrer com dignidade

            #crossroad[1].RED?
                #crossroad[0].YELLOW?
                    #próximo corr SAFE?
                        #escolhe saída
                    #próximo corr UNSAFE?
                        #ghost do prox corr (crossroad[0]) pode nao estar em perseguiçao, so...
                        #distGhostPac >= SAFE_DIST_TO_GHOST?
                            #escolhe saida
                        #distGhostPac < SAFE_DIST_TO_GHOST?
                            #escolhe o 1º corr
                #else crossroad[0].RED?
                    #morrer com dignidade

        

    
    def pursuit_agent(self, state):
        pass


    def counter_agent(self, state):
        pass