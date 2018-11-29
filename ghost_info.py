class Ghost_Info():

    def __init__(self, ghost, zombie, timeout, corridor, dist_to_pacman, crossroad_to_pacman, dist_to_crossroad):
        self.position = ghost
        self.zombie = zombie
        self.timeout = timeout
        self.corridor = corridor
        self.dist_to_pacman = dist_to_pacman
        self.crossroad_to_pacman = crossroad_to_pacman
        self.dist_to_crossroad = dist_to_crossroad
