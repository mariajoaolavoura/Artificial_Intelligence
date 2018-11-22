class Ghost_Info():

    def __init__(self, ghost, corridor, dist_to_pacman, crossroad_to_pacman, dist_to_crossroad):
        self.position = ghost[0]
        self.zombie = ghost[1]
        self.timeout = ghost[2]
        self.corridor = corridor
        self.dist_to_pacman = dist_to_pacman
        self.crossroad_to_pacman = crossroad_to_pacman
        self.dist_to_crossroad = dist_to_crossroad
