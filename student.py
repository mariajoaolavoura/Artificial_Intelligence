from game_consts import *
from static_analysis import Static_Analysis
from pathways import Pathways
from tree_search import SearchTree, SearchProblem
from corridor import Corridor
from strategy_advisor import Strategy_Advisor
import logging
import sys
import json
import asyncio
import websockets
import os
from mapa import Map





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
        #
        if next_move == None:
            return 'w' # w for win


        # if advice is not specific, adjustments to the strategy may be needed
        if (next_move == False): # correct when methods are implemented
            strategy_adjuster = Strategy_Adjuster()
            mode_handler = strategy_adjuster.adjustStrategy()
            next_move = self.mode(mode_handler, state)
        
        # calculate and return the key
        # if (next_move == [5,23] or next_move == [6,7]):
        #     print("KEY IS " + str(self.calculate_key(state['pacman'], next_move)))

        # logger.debug("KEY IS " + str(self.calculate_key(state['pacman'], next_move)) + "\n\n")
        return self.calculate_key(state['pacman'], next_move)



    def mode(self, mode_handler, advisor, state):
        if mode_handler != MODE.EATING:
            print(mode_handler)
        if mode_handler == MODE.EATING:
            next_move = self.eating_agent(advisor, state)
        elif mode_handler == MODE.FLIGHT:
            next_move = self.flight_agent(advisor)
        elif mode_handler == MODE.PURSUIT:
            next_move = self.pursuit_agent(advisor, state)
        else: # next_move == MODE.COUNTER
            next_move = self.counter_agent(advisor, state)
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



        if nx == px + 1:
            key = 'd'
        elif nx == px -1:
            key = 'a'
        elif ny == py + 1:
            key = 's'
        elif ny == py -1:
            key = 'w'
        elif nx > px:
            key = 'a'
        elif nx < px:
            key = 'd'
        elif ny > py:
            key = 'w'
        else:
            key = 's'
        
        return key



    def eating_agent(self, advisor, state):

        acessible_energies = []
        targets = state['energy'] + state['boost']
        domain = Pathways(self.map_.corr_adjacencies, targets)
        possible_moves = []
        
        for energy in targets:
            
            # create domain to search
            
            # print("Energy #######################################")
            # print(energy)
            # print("#######################################")

            # find this energy corridor
            corridor = None
            for corr in self.map_.corridors:
                if energy in corr.coordinates:
                    corridor = corr

            # print("Corridor #######################################")
            # print(corridor)
            # print("#######################################")
            if (self.debug):
                pass
            
            # create problem and search
            my_prob = SearchProblem(domain, corridor, energy, advisor.pacman_info.corridor, advisor.pacman_info.position)
            my_tree = SearchTree(my_prob, "a*")
            search_results = my_tree.search()
            
            # filter valid results and store them in possible_moves
            if search_results != None:
                acessible_energies += [energy]
                possible_moves += [search_results]

        # if there are no possible moves, everything is eaten
        if len(possible_moves) == 0:
            return None

        # sort possible_moves by cost
        possible_moves = sorted(possible_moves,key=lambda res: res[1])
        # if a path is blocked by a ghost in the next corridor, choose another corridor
        for move in possible_moves:
            if move[2][-3].safe == True:
                return move[0]

        # if this code is reached, then, no path is safe (unblocked) in the next corridor
        return possible_moves[0][0]
    

    def flight_agent(self, advisor):
        '''
        args:
        advisor: instance of Strategy_Advisor
                self.map_ = map_
                self.state = state
                self.unsafe_corridors = self.set_corridors_safety()
                self.pacman_info = Pacman_Info(state['pacman'])
                self.calculate_pacman_corridor()
                self.ghosts_info = self.calculate_ghosts_info()
        '''
                
        pac_info = advisor.pacman_info
        pac_crossroads = pac_info.crossroads

        pac_adj0, pac_safe_corr0 = self.calc_adj_and_safe(pac_info.corridor, pac_crossroads[0])

        pac_adj1, pac_safe_corr1 = self.calc_adj_and_safe(pac_info.corridor, pac_crossroads[1])

        ########################################################################
        ## PAC CORR UNSAFE #####################################################
        ########################################################################

        #corr pacman tem ghost do lado do crossroad0       
        if pac_info.crossroad0_is_safe == CORRIDOR_SAFETY.UNSAFE:

            #pacman esta encurralado (corr do pacman tem ghosts dos 2 lados)
            if pac_info.crossroad1_is_safe == CORRIDOR_SAFETY.UNSAFE:
                
                #escolhe lado com ghost mais afastado
                if pac_info.dist_to_ghost_at_crossroad0 >= pac_info.dist_to_ghost_at_crossroad1:
                    #escolhe crossroad0
                    return self.calc_next_coord(pac_info, pac_info.crossroad0, [])
                else:
                    #escolhe crossroad1
                    return self.calc_next_coord(pac_info, pac_info.crossroad1, [])

            #ghost no corr do pacman apenas do lado do crossroad0 -> crossroad0 is RED
            else:
    
                #pacman consegue fugir pelo crossroad1
                if pac_info.semaphore1 == SEMAPHORE.YELLOW:   

                    #ha corr safe
                    if pac_safe_corr1 != []:
                        #escolhe pac_safe_corr1[0]
                        return self.calc_next_coord(pac_info, pac_info.crossroad1, pac_safe_corr1)
                    
                    #NAO ha corr safe
                    else:
                        #escolhe corr com ghost mais afastado
                        #?return self.calc_corridor_ghost_farther(pac_info, pac_adj1, ghosts_info)
                        return self.calc_next_coord(pac_info, pac_info.crossroad1, pac_adj1)

                #pacman NAO consegue fugir pelo crossroad1 -> crossroad1 is RED
                else:
                    #escolhe crossroad1
                    return self.calc_next_coord(pac_info, pac_info.crossroad1, [])

        #corr do pacman NAO tem ghost do lado crossroad0
        else:

            #corr do pacman tem ghost apenas do lado crossroad1 -> crossroad1 is RED
            if pac_info.crossroad1_is_safe == CORRIDOR_SAFETY.UNSAFE:

                #pacman consegue fugir apenas pelo crossroad0
                if pac_info.semaphore0 == SEMAPHORE.YELLOW:
                    #crossroad0 liga a corr SAFE
                    if pac_safe_corr0 != []:
                        #escolhe pac_safe_corr0[0]
                        return self.calc_next_coord(pac_info, pac_info.crossroad0, pac_safe_corr0)
                    
                    #NAO ha corr SAFE pelo crossroad0
                    else:
                        #escolhe corr com ghost mais afastado
                        #?return self.calc_corridor_ghost_farther(pac_info, pac_adj0, ghosts_info)
                        return self.calc_next_coord(pac_info, pac_info.crossroad0, pac_adj0)

                #pacman NAO consegue fugir por nenhum crossroad -> crossroad0 is RED
                else:
                    #escolhe lado com ghost mais afastado
                    #?return self.calc_corridor_ghost_farther(pac_info, pac_adj0 + pac_adj1, ghosts_info)
                    return self.calc_next_coord(pac_info, pac_info.crossroad0, [])


            ####################################################################
            ## PAC CORR SAFE ###################################################
            ####################################################################

            #corr do pacman NAO tem ghosts -> crossroad[0].SAFE and crossroad[1].SAFE
            else:
                
                #pacman consegue fugir pelo crossroad0
                if pac_info.semaphore0 == SEMAPHORE.YELLOW:
                
                    #pacman consegue fugir por qualquer crossroad
                    if pac_info.semaphore1 == SEMAPHORE.YELLOW:

                        #crossroad0 liga a corr SAFE
                        if pac_safe_corr0 != []:
                            #ambos os crossroads ligam a corr SAFE
                            if pac_safe_corr1 != []:
                                #escolhe o crossroad mais longe
                                #crossroad0 mais longe do pacman
                                if pac_info.dist_to_crossroad0 >= pac_info.dist_to_crossroad1:
                                    #escolhe pac_safe_corr0[0]
                                    return self.calc_next_coord(pac_info, pac_info.crossroad0, pac_safe_corr0)

                                #crossroad1 mais longe do pacman    
                                else:
                                    #escolhe pac_safe_corr1[0]
                                    return self.calc_next_coord(pac_info, pac_info.crossroad1, pac_safe_corr1)

                            #apenas crossroad0 liga a corr SAFE
                            else:
                                #escolhe pac_safe_corr0[0]
                                return self.calc_next_coord(pac_info, pac_info.crossroad0, pac_safe_corr0)
                        
                        #crossroad0 nao liga a corr SAFE
                        else:
                            #apenas crossroad1 liga a corr SAFE
                            if pac_safe_corr1 != []:
                                #escolhe pac_safe_corr1[0]
                                return self.calc_next_coord(pac_info, pac_info.crossroad1, pac_safe_corr1)

                            #NAO ha corr SAFE        
                            else:
                                #escolhe corr com ghost mais afastado
                                #?return self.calc_corridor_ghost_farther(pac_info, pac_adj0 + pac_adj1, ghosts_info)
                                return self.calc_next_coord(pac_info, pac_info.crossroad0, pac_adj0)#, return self.calc_next_coord(pac_info.position, pac_info.crossroad1)
                    
                    #pacman consegue fugir apenas pelo crossroad0
                    else:

                        #crossroad0 liga a corr SAFE
                        if pac_safe_corr0 != []:
                            #escolhe pac_safe_corr0[0]
                            return self.calc_next_coord(pac_info, pac_info.crossroad0, pac_safe_corr0)
                        
                        #NAO ha corr SAFE pelo crossroad0
                        else:
                            #escolhe corr com ghost mais afastado
                            #?return self.calc_corridor_ghost_farther(pac_info, pac_adj0, ghosts_info)
                            return self.calc_next_coord(pac_info, pac_info.crossroad0, pac_adj0)
                
                #pacman NAO consegue fugir pelo crossroad0
                else:

                    #pacman consegue fugir apenas pelo crossroad1
                    if pac_info.semaphore1 == SEMAPHORE.YELLOW:
                        #crossroad1 liga a corr SAFE
                        if pac_safe_corr1 != []:
                            #escolhe pac_safe_corr1[0]
                            return self.calc_next_coord(pac_info, pac_info.crossroad1, pac_safe_corr1)
                        
                        #NAO ha corr SAFE pelo crossroad1
                        else:
                            #escolhe corr com ghost mais afastado
                            #?return self.calc_corridor_ghost_farther(pac_info, pac_adj1, ghosts_info)
                            return self.calc_next_coord(pac_info, pac_info.crossroad1, pac_adj1)

                    #pacman NAO consegue fugir por nenhum crossroad
                    else:
                        #escolhe lado com ghost mais afastado
                        #?return self.calc_corridor_ghost_farther(pac_info, pac_adj0 + pac_adj1, ghosts_info)
                        return self.calc_next_coord(pac_info, pac_info.crossroad0, [])


    def calc_adj_and_safe(self, pac_corr, crossroad):
        adj = [[cA, cB] for [cA, cB] in self.map_.corr_adjacencies\
                                        if crossroad in cA.ends\
                                        or crossroad in cB.ends]
           
        safe = [[cA, cB] for [cA, cB] in adj\
                            if (cA.coordinates == pac_corr.coordinates and cB.safe == CORRIDOR_SAFETY.SAFE)\
                            or (cB.coordinates == pac_corr.coordinates and cA.safe == CORRIDOR_SAFETY.SAFE)]

        return adj, safe
                

    def calc_next_coord(self, pac_info, end, adj_end):
        '''
            Args:
            pac_info:   advisor.pacman_info
            end     :   crossroad do lado escolhido para o pacman fugir
            adj_end :   lista de corredores adjacentes ao end
                        - adj_end == [] é porque o pacman não consegue fugir pelo end
                                        tanto por existir um fantasma no mesmo corredor desse lado
                                        tanto por o end ser RED
        '''

        [px, py] = pac_info.position
        
        next_move_pac_corr = [ coord for coord in pac_info.corridor.coordinates\
                                        if coord == [px-1, py]\
                                        or coord == [px+1, py]\
                                        or coord == [px, py-1]\
                                        or coord == [px, py+1]]

        #pacman esta num crossroad
        if len(next_move_pac_corr) == 1:
            next_moves = [ coord for corridor in adj_end\
                                    for coord in [corridor.get_coord_next_to_end(end)]]

            return next_moves[0]

        #pacman NAO está num crossroad
        else:      

            [ex, ey] = end

            next_coord = next_move_pac_corr[0]
            dx = abs(ex - next_coord[0])
            dy = abs(ey - next_coord[1])

            for i in range(1, len(next_move_pac_corr)):

                [a,b] = next_move_pac_corr[i]
                da = abs(ex-a)
                db = abs(ey-b)

                if py == ey:
                    next_coord, dx, dy = [[a,b], da, db] if da<dx else [next_coord, dx, dy]
                elif px == ex:
                    next_coord, dx, dy = [[a,b], da, db] if db<dy else [next_coord, dx, dy]
                else:
                    next_coord, dx, dy = [[a,b], da, db] if (da==dx and db<dy)\
                                                            or (db==dy and da<dx)\
                                                         else [next_coord, dx, dy]

            return next_coord




    #escolhe corr com ghost mais afastado
    #TODO not done
    def calc_corridor_ghost_farther(self, pac_info, pac_adj, ghosts_info):
        dist = 0
        corr = []
        for adj_corr in pac_adj:
            for g_info in ghosts_info:
                if g_info.corridor == adj_corr and dist < g_info.dist_to_pacman:
                    dist = g_info.dist_to_pacman
                    corr = g_info.corridor                                                   
        
        #TODO devolver prox coord
        pass

    
    def pursuit_agent(self, advisor, state):
        """Calculates the next position of the next move, when in pursuit mode.
        In Counter Mode, Pac-Man is must focus on eating zombie ghosts.
        
        Args:
        advisor
        state

        Returns:
        The [x,y] position of the next_move
        """

        #<pathways.Pathways object at 0x7fc182823208> [[2, 26], [2, 25], [2, 24], [2, 23], [1, 23], [1, 22], [1, 21], [1, 20], [2, 20], [3, 20], [4, 20]] [1, 22] [[14, 15], [15, 15], [16, 15], [17, 15], [18, 15], [0, 15], [1, 15], [2, 15], [3, 15], [4, 15]] [3, 15]
       
        eatable_ghosts = state['ghosts'].copy()
        eatable_ghosts[1][1] = True # FOR TESTING PURPOSES
        
        eatable_ghosts = [ghost[0] for ghost in eatable_ghosts if ghost[1]]    #only get the positions
        
        acessible_ghosts = []
        possible_moves   = []
        safeties         = []

        for ghost in eatable_ghosts:
            domain = Pathways(self.map_.corr_adjacencies.copy(), eatable_ghosts)

            corridor = None
            for corr in self.map_.corridors:
                if ghost in corr.coordinates:
                    corridor = corr
                    safety = corridor.safe
            
            print(domain, corridor, ghost, advisor.pacman_info.corridor, advisor.pacman_info.position)
            my_prob = SearchProblem(domain, corridor, ghost, advisor.pacman_info.corridor, advisor.pacman_info.position)
            my_tree = SearchTree(my_prob, "a*")
            search_results = my_tree.search()
            
            if search_results != None:
                #? avoid repetead boosts
                if ghost not in acessible_ghosts:
                    acessible_ghosts += [ghost]
                    possible_moves   += [(search_results[0], search_results[1])]
                    safeties         += [safety]

        if len([safety for safety in safeties if safety == CORRIDOR_SAFETY.SAFE]): #if any corridor is safe
            #remove unsafe corridors info
            for i in range(0, len(acessible_ghosts)):
                if safeties[i] == CORRIDOR_SAFETY.UNSAFE:
                    del safeties[i]
                    del acessible_ghosts[i]
                    del possible_moves[i]        

        # should not be on this mode (no more zombie ghost)
        if (len(possible_moves) == 0):
            return False
        
        # choose the closest zombie ghost 
        # either there are several ghost in a safe corridor 
        # OR there are only ghost in unsafe corridors)
        possible_moves = sorted(possible_moves,key=lambda elem: elem[1])
        return possible_moves[0][0]


    def counter_agent(self, advisor, state):
        """Calculates the next position of the next move, when in counter mode.
        In Counter Mode, Pac-Man is almost surrounded by ghosts and must focus on eating boosts.
        
        Args:
        advisor
        state

        Returns:
        The [x,y] position of the next_move

        Considerations/Strategy:
        -> For each corridor where the boosts are, check for safe ones
        -> From the safest ones, choose the closest (if no one is safe, choose the closest one)
        
        ghost [[9, 15], False, 0],
        """
        boosts = state['boost'].copy()
        acessible_boosts = []
        possible_moves   = []
        safeties         = []

        for boost in boosts:
            domain = Pathways(self.map_.corr_adjacencies.copy(), boosts)

            corridor = None
            for corr in self.map_.corridors:
                if boost in corr.coordinates:
                    corridor = corr

            my_prob = SearchProblem(domain, corridor, boost, advisor.pacman_info.corridor, advisor.pacman_info.position)
            my_tree = SearchTree(my_prob, "a*")
            search_results = my_tree.search()
            
            if search_results != None:
                #? avoid repetead boosts
                #if boost not in acessible_boosts:
                acessible_boosts += [boost]
                possible_moves   += [(search_results[0], search_results[1])]
                safeties         += [search_results[2][len(search_results[2]) - 3].safe]        #safety of two to last corridor

        # print("BOOSTS"   + str(acessible_boosts) + "\n")
        # print("MOVES"    + str(possible_moves)+ "\n")
        # print("SAFETIES" + str(safeties)+ "\n")
        
        other_choices = []
        blocked = True

        if len([safety for safety in safeties if safety == CORRIDOR_SAFETY.SAFE]): #if any corridor is safe
            blocked = False
            #remove unsafe corridors info
            for i in range(0, len(acessible_boosts)):
                if safeties[i] == CORRIDOR_SAFETY.UNSAFE:
                    other_choices += possible_moves[i]
                    
                    del safeties[i]
                    del acessible_boosts[i]
                    del possible_moves[i]        

        # should not be on this mode (no more boosts)
        if (len(possible_moves) == 0):
            return False
        
        # choose the closest boost 
        # either there are several boosts in a safe corridor 
        # OR there are only boosts in unsafe corridors)
        
        possible_moves = sorted(possible_moves,key=lambda elem: elem[1])
        other_choices += [possible_move[0] for possible_move in possible_moves[1:]]
        #response = ModeResponse(possible_moves[0][0], other_choices, blocked)
        #print(response)
        return possible_moves[0][0]


#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#
async def agent_loop(server_address = "localhost:8000", agent_name="student"):
    async with websockets.connect("ws://{}/player".format(server_address)) as websocket:

        #----------------------------------------------------------------------#
        # Receive information about static game properties 
        await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))
        msg = await websocket.recv()
        game_properties = json.loads(msg)
        #----------------------------------------------------------------------#
        
        
        # Create the pacman agent
        pacman = Pacman_agent(Map(game_properties['map']))

        # play!
        while True:
            #------------------------------------------------------------------#
            r = await websocket.recv()
            state = json.loads(r) #receive game state

            # game over (unnecessary for actual play
            if not state['lives']:
                print("GAME OVER")
                return
            #------------------------------------------------------------------#

            
            #print(state)
            # get next move from pacman agent
            key = pacman.get_next_move(state)

            
            #-send new key-----------------------------------------------------#
            await websocket.send(json.dumps({"cmd": "key", "key": key}))
            #------------------------------------------------------------------#

loop = asyncio.get_event_loop()
SERVER = os.environ.get('SERVER', 'localhost')
PORT = os.environ.get('PORT', '8000')
NAME = os.environ.get('NAME', 'student')
loop.run_until_complete(agent_loop("{}:{}".format(SERVER,PORT), NAME))
if __name__ == "__main__":
    agent_loop()
#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#