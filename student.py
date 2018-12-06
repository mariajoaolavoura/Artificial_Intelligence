from game_consts import *
from static_analysis import Static_Analysis
from pathways import Pathways
from tree_search import SearchTree, SearchProblem
from corridor import Corridor
from strategy_advisor import StrategyAdvisor
from strategy_analyst import StrategyAnalyst
import logging
import sys
import json
import asyncio
import websockets
import os
from mapa import Map
from eating_agent import *
from counter_agent import *
from pursuit_agent import *
from flight_agent import *
from time import time

#$ PORT=80 SERVER=pacman-aulas.ws.atnog.av.it.pt python client.py
# to kill server: fuser 8000/tcp

# logger
# logs are written to file student.log after the client is closed
# possible messages: debug, info, warning, error, critical 
# how to use: logger.typeOfMessage('message')
logger = setup_logger('student', 'student.log')
time_logger = setup_logger('key_times', 'key_times.log', format='%(message)s\n')
time_logger.debug("TIMES IN MILISECONDS (*1000)")

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
        strategy_advisor = StrategyAdvisor(self.map_, state)
        #mode_handler = strategy_advisor.advise()

        # first always try to eat
        strategy_analyst = StrategyAnalyst(strategy_advisor)
        next_move = strategy_analyst.decide()

        # if next_move is None, the the game is finished
        if next_move == None:
            sys.exit(0)

        # logger.debug("KEY IS " + str(self.calculate_key(state['pacman'], next_move)) + "\n\n")
        return self.calculate_key(state['pacman'], next_move)
        



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



#------------------------------------------------------------------------------#
# MAIN METHOD - INTERFACES WITH SERVER TO RECEIVE AND SEND GAME 'WASD' KEYS
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
        lives = 3
        # play!
        while True:
            #------------------------------------------------------------------#
            # for debug purposes : times
            r = await websocket.recv()
            start = time()      # saved on key_times.log
            state = json.loads(r) #receive game state

            # for debug purposes : times
            start = time()      # saved on key_times.log

            # # game over (unnecessary for actual play
            # if not 'lives' in state:
            #     print(state)
            #     print("GAME OVER")
            #     sys.exit(0)

            if state['lives'] != lives:
                lives = state['lives']
                print('\n############\nPACMAN HAS LOST A LIFE\n#############\n')
                stop0 = time()
                print('Last move time: ' + str((stop0-start) * 1000))
                #sys.exit(1)
            
            #------------------------------------------------------------------#
            # for debug purposes (save scores and stress testing)
            
            # create apropriated logger based on ghosts and level
            if game_properties['ghosts'] == []:
                name = 'scores_empty.log'
            else:
                name = 'scores_ghosts_level' + str(game_properties['ghosts_level']) + '.log'

            score_logger = setup_logger('scores', name, mode='a', format='%(message)s\n')

            # game won (ended)
            if state['energy'] == [] and state['boost'] == []:
                sys.stderr.write("\n\033[92mGAME ENDED. SCORE IS " + str(state['score']) + "\033[0m")
                score_logger.debug(str(state['score']))
                return

            # game lost (no more lives)
            if not state['lives']:
                sys.stderr.write("\n\033[91mGAME OVER. SCORE IS " + str(state['score'])  + "\033[0m")
                score_logger.debug(str(state['score']))
                return

            #------------------------------------------------------------------#
            #print(state)
            # get next move from pacman agent
            key = pacman.get_next_move(state)
            stop1 = time()
            print('Last move time: ' + str((stop1-start) * 1000))
            
           

            #-send new key-----------------------------------------------------#
            await websocket.send(json.dumps({"cmd": "key", "key": key}))

            # debug purposes (time)
            stop = time()            
            time_logger.debug(str(state['step']) + " " + str(key) + "-> " + str((stop-start) * 1000))

            #------------------------------------------------------------------#

loop = asyncio.get_event_loop()
SERVER = os.environ.get('SERVER', 'localhost')
PORT = os.environ.get('PORT', '8000')
NAME = os.environ.get('NAME', 'student')
loop.run_until_complete(agent_loop("{}:{}".format(SERVER,PORT), NAME))

#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#
