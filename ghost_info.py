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
        intercept_coord = None
        ghost_intercept_dist = 0
        path = [c for c in self.path[1].coordinates]
        pacman_path = [c for corr in pacman_path for c in corr.coordinates]
        for c in path:
            if c in pacman_path:
                print('SIDE INTERCEPT FOUND A CORRIDOR')
                intercept_coord = c
                ghost_intercept_dist += 1
                break
            else:
                ghost_intercept_dist += 1

        if intercept_coord == None:
            return None

        pac_intercept_dist = 0
        for c in pacman_path[::-1]:
            if c != intercept_coord:
                pac_intercept_dist += 1
            else:
                break
        print('pac dist to intersept: ' + str(pac_intercept_dist) + 'ghost dist to intercept: ' + str(ghost_intercept_dist))
        return pac_intercept_dist < ghost_intercept_dist


    def __str__(self):
        return 'ghost('+str(self.position)+')'

    def __repr__(self):
        return self.__str__()

    def print(self):
        string = \
        'Ghost ' + str(self.position) + ' is at distance ' + str(self.dist_to_pacman) + \
        ' from Pac-Man and ' + str(self.dist_to_crossroad) + ' from crossroad ' + str(self.crossroad_to_pacman)

        return string