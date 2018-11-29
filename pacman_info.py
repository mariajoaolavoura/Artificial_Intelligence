from corridor import Corridor
from game_consts import *

class Pacman_Info():

    def __init__(self, pacman):
        self.position = pacman
        self.corridor = None
        self.crossroads = None
        self.crossroad0 = None
        self.crossroad1 = None
        self.dist_to_crossroad0 = None
        self.dist_to_crossroad1 = None
        self.semaphore0 = None
        self.semaphore1 = None
        self.dist_to_ghost_at_crossroad0 = None
        self.dist_to_ghost_at_crossroad1 = None

        # evaluates if a ghost is inside the corridor, blocking the crossroad
        self.crossroad0_is_blocked = False 
        self.crossroad1_is_blocked = False

        # evaluates if the closest ghost in the direction of crossroad is at safe distance (game_consts.pySAFE_DIST_TO_GHOST)
        self.pursued_from_crossroad0 = False
        self.pursued_from_crossroad1 = False

        self.ghost_at_crossroad0 = None
        self.ghost_at_crossroad1 = None

    def update_corridor(self, corridor):
        self.corridor = corridor
        self.crossroads = corridor.ends
        self.crossroad0 = corridor.ends[0]
        self.crossroad1 = corridor.ends[1]
        self.dist_to_crossroad0 = corridor.dist_end0(self.position)
        self.dist_to_crossroad1 = corridor.dist_end1(self.position)

    def dist_to_crossroad(self, crossroad):
        if crossroad == self.crossroad0:
            return self.crossroad0
        elif crossroad == self.crossroad1:
            return self.crossroad1
        else:
            return None
        