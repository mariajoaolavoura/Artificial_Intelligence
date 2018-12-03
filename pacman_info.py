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

    # called in strategy_advisor, calculate_pacman_corridor()
    def update_corridor(self, corridor):
        self.corridor = corridor
        self.crossroads = corridor.ends
        self.crossroad0 = corridor.ends[0]
        self.crossroad1 = corridor.ends[1]
        self.dist_to_crossroad0 = corridor.dist_end0(self.position)
        self.dist_to_crossroad1 = corridor.dist_end1(self.position)
        # print("##########################################")
        # print(str(self.dist_to_crossroad0) + ', ' + str(self.dist_to_crossroad1))
        # print("##########################################")

    def dist_to_crossroad(self, crossroad):
        if crossroad == self.crossroad0:
            return self.dist_to_crossroad0
        elif crossroad == self.crossroad1:
            return self.dist_to_crossroad1
        else:
            return None

    def pursued_from_crossroad(self, crossroad):
        if crossroad == self.crossroad0:
            return self.pursued_from_crossroad0
        elif crossroad == self.crossroad1:
            return self.pursued_from_crossroad1
        else:
            return None

    def ghost_at_crossroad(self, crossroad):
        if crossroad == self.crossroad0:
            return self.ghost_at_crossroad0
        elif crossroad == self.crossroad1:
            return self.ghost_at_crossroad1
        else:
            return None

    def dist_to_ghost_at_crossroad(self, crossroad):
        if crossroad == self.crossroad0:
            return self.dist_to_ghost_at_crossroad0
        elif crossroad == self.crossroad1:
            return self.dist_to_ghost_at_crossroad1
        else:
            return None
    
    def __str__(self):
        string = \
        'Pac-Man is in position ' + str(self.position) + '\n'

        if self.ghost_at_crossroad0 != None:
            string += \
            'Ghost ' + str(self.ghost_at_crossroad0.position) + ' is at crossroad ' + str(self.crossroad0) + \
            ' at distance ' + str(self.dist_to_ghost_at_crossroad0) + ' from Pc-Man '
        if (self.dist_to_ghost_at_crossroad0 != None):
            string += \
            ' at distance ' + str(self.dist_to_ghost_at_crossroad0 - self.dist_to_crossroad0) + ' of crossroad \n' + \
            'with the semaphore ' + str(self.semaphore0) + '\n' + \
            'Pac-Man distance to this crossroad0 is ' + str(self.dist_to_crossroad0) + '\n'

        if self.ghost_at_crossroad1 != None:
            string += \
            'Ghost ' + str(self.ghost_at_crossroad1.position) + ' is at crossroad ' + str(self.crossroad1) + \
            ' at distance ' + str(self.dist_to_ghost_at_crossroad1) + ' from Pc-Man'
        if (self.dist_to_ghost_at_crossroad1 != None):
            string += \
            ' at distance ' + str(self.dist_to_ghost_at_crossroad1 - self.dist_to_crossroad1) + ' of crossroad \n' + \
            'with the semaphore ' + str(self.semaphore1) + '\n' \
            'Pac-Man distance to this crossroad1 is ' + str(self.dist_to_crossroad1)

        return string

    def __repr__(self):
        return self.__str__()