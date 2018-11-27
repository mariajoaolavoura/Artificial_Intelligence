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
        self.dist_to_ghost_at_crossroad0 = None #
        self.dist_to_ghost_at_crossroad1 = None #
        self.crossroad0_is_safe = None #
        self.crossroad1_is_safe = None #

    def update_corridor(self, corridor):
        self.corridor = corridor
        self.crossroads = corridor.ends
        self.crossroad0 = corridor.ends[0]
        self.crossroad1 = corridor.ends[1]
        self.dist_to_crossroad0 = corridor.dist_end0(self.position)
        self.dist_to_crossroad1 = corridor.dist_end1(self.position)
        