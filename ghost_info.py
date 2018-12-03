class Ghost_Info():

    def __init__(self, ghost, zombie, timeout, corridor, dist_to_pacman, crossroad_to_pacman, dist_to_crossroad, path):
        self.position = ghost
        self.zombie = zombie
        self.timeout = timeout
        self.corridor = corridor
        self.dist_to_pacman = dist_to_pacman
        self.crossroad_to_pacman = crossroad_to_pacman
        self.dist_to_crossroad = dist_to_crossroad
        self.path = path


    def side_interception(self, pacman_path):
        intercept_corr = None
        ghost_intercept_dist = 0
        for corr in self.path:
            if corr.coordinates in pacman_path:
                intercept_corr = corr
                break
            else:
                ghost_intercept_dist += corr.cost

        if intercept_corr == None:
            return None

        pac_intersept_dist = 0
        for corr in pacman_path[::-1]:
            if corr != intercept_corr:
                pac_intercept_dist += corr.cost
            else:
                pac_intercept_dist += corr.cost
                break

        return pac_intersept_dist < ghost_intercept_dist


    def __str__(self):
        return 'ghost('+str(self.position)+')'

    def __repr__(self):
        return self.__str__()

    def print(self):
        string = \
        'Ghost ' + str(self.position) + ' is at distance ' + str(self.dist_to_pacman) + \
        ' from Pac-Man and ' + str(self.dist_to_crossroad) + ' from crossroad ' + str(self.crossroad_to_pacman)

        return string