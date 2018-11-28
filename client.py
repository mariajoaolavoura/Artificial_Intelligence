import random
import sys
import json
import asyncio
import websockets
import os
from mapa import Map
from student import Pacman_agent


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
