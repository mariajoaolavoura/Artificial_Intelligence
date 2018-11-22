class Ghost_Info(Object):

    def __init__(self, position, zombie, timeout, dist_to_pacman, crossroad_to_pacman, dist_to_crossroad):
        self.position = position
        self.zombie = zombie
        self.timeout = timeout
        self.dist_to_pacman = dist_to_pacman
        self.crossroad_to_pacman = crossroad_to_pacman
        self.dist_to_crossroad = dist_to_crossroad
