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


    def is_coord_in_path(self, coord):
        for c in [c for corr in self.path for c in corr.coordinates]:
            if c == coord:
                return True
        return False

    def side_interception(self, pacman_path, flight=False):
        intercept_coord = None
        path = [c for c in self.path[-2].coordinates]
        pacman_path_coords = [c for corr in pacman_path for c in corr.coordinates]

        for c in path:
            if c in pacman_path_coords:
                found_interception = True
                intercept_coord = c
                break
        if intercept_coord == None:
            return False
        ghost_intercept_dist = self.path[-2].dist_to_end(self.position, intercept_coord)    

        pac_intercept_dist = 0
        if flight == False:
            for corr in pacman_path[::-1]:
                if intercept_coord in corr.coordinates:
                    pac_intercept_dist += corr.cost
                    break
                else:
                    pac_intercept_dist += corr.cost
        else:
            for corr in pacman_path:
                if intercept_coord in corr.coordinates:
                    pac_intercept_dist += corr.cost
                    break
                else:
                    pac_intercept_dist += corr.cost

        return pac_intercept_dist >= ghost_intercept_dist


    def __str__(self):
        return 'ghost('+str(self.position)+', '+str(self.dist_to_pacman)+')'

    def __repr__(self):
        return self.__str__()

    def print(self):
        string = \
        'Ghost ' + str(self.position) + ' is at distance ' + str(self.dist_to_pacman) + \
        ' from Pac-Man and ' + str(self.dist_to_crossroad) + ' from crossroad ' + str(self.crossroad_to_pacman)

        return string