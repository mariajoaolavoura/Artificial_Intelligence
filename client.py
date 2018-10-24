import random
import sys
import json
import asyncio
import websockets
import os
from mapa import Map
from tree_search import *
import math
from pathways import Pathways
from testTreeSearch import *

async def agent_loop(server_address = "localhost:8000", agent_name="student"):
    async with websockets.connect("ws://{}/player".format(server_address)) as websocket:

        #----------------------------------------------------------------------#
        # Receive information about static game properties 
        await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))
        msg = await websocket.recv()
        game_properties = json.loads(msg)
        #----------------------------------------------------------------------#
        
        
        # get map and pathways info
        mapa = Map(game_properties['map'])
        pathways = mapa.pathways
        energy = mapa.energy
        #print(energy)
        boost = mapa.boost

        # create list of adjacent coordinates (verified!)
        domain = []
        for (x,y) in pathways:
            domain += [ ((x,y),(a,b)) for (a,b) in pathways \
                                if ((a == x+1 and b == y) \
                                or (a == x-1 and b == y) \
                                or (b == y+1 and a == x) \
                                or (b == y-1 and a == x) \
                                or (x == 0 and a == mapa.hor_tiles-1 and b == y) \
                                or (a == 0 and x == mapa.hor_tiles-1 and b == y) \
                                or (y == 0 and b == mapa.ver_tiles-1 and a == x) \
                                or (b == 0 and y == mapa.ver_tiles-1 and a == x))
                                and not domain.__contains__(((a,b),(x,y)))]

        domain.remove(((8,15),(8,16)))
        #domain.remove(((8,16),(8,15)))
        #domain.remove(((8,15),(8,14)))
        domain.remove(((8,14),(8,15)))
        
        #init agent properties 
        key = 'a'
        cur_x, cur_y = None, None
        
        # play!
        while True:
            #------------------------------------------------------------------#
            r = await websocket.recv()
            state = json.loads(r) #receive game state
            #------------------------------------------------------------------#


            # game over (unnecessary for actuak play
            if not state['lives']:
                print("GAME OVER")
                return

            
            # create the vector for every element in the game
            #vectors = []
            vectors = test_search(domain, energy[0:2])
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
            
            
            
            #send new key
            await websocket.send(json.dumps({"cmd": "key", "key": key}))


loop = asyncio.get_event_loop()
SERVER = os.environ.get('SERVER', 'localhost')
PORT = os.environ.get('PORT', '8000')
NAME = os.environ.get('NAME', 'student')
loop.run_until_complete(agent_loop("{}:{}".format(SERVER,PORT), NAME))
