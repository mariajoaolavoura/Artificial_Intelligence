from game_consts import *


class MoveRiskAssessor():

    def __init__(self, advisor, ghosts_in_pursuit):
        self.advisor = advisor
        self.ghosts_in_pursuit = ghosts_in_pursuit


    def analyse_best_move(self, possible_moves, flight=False, surrounded_eating=False, counter=False):
        """ Auxiliary method whose objective is to verify if the best move given
        by an Agent (Pursuit, Eating and Counter) is valid and does no lead
        Pac-Man to suicide or entrapment

        Args:
        possible_moves: the ordered list of possible_moves of the Agent

        Returns:
        True if the best move is safe
        """

        if possible_moves == []:
            return False

        move = possible_moves[0]
        #print('ANALYSE: move is ' + str(move))
        cost = move[1]
        path = move[2]
        #print('ANALYSE: path is ' + str(path))
        path_coords = [c for corr in path for c in corr.coordinates]
        aux = []
        for c in path_coords:
            if c not in aux:
                aux += [c]
        path_coords = aux
        pacman = self.advisor.pacman_info
        
        sub_corr0, sub_corr1 = pacman.corridor.sub_corridors(pacman.position)
        sub_corr0 = sub_corr0.coordinates[:-1]
        sub_corr1 = sub_corr1.coordinates[1:]
        print('subcorridor0 is: ' + str(sub_corr0))
        print('subcorridor1 is: ' + str(sub_corr1))
        print('path_coords is: ' + str(path_coords))
        crossroad = None
        semaphore = None
        ghost = None

        # verify which side of path pacman wants to go
        if any([c in path_coords for c in sub_corr0]):
            print('IN SUB CORR 0')
            crossroad = pacman.crossroad0
            semaphore = pacman.semaphore0
            ghost = pacman.ghost_at_crossroad0
        elif any([c in path_coords for c in sub_corr1]):
            print('IN SUB CORR 1')
            crossroad = pacman.crossroad1
            semaphore = pacman.semaphore1
            ghost = pacman.ghost_at_crossroad1
        else:
            print('IN ELSE')
            crossroad = pacman.position
            semaphore = pacman.semaphore(crossroad)
            ghost = pacman.ghost_at_crossroad(crossroad)
            

        print()
        print(pacman)
        print('Pac-Man distance to target ' + str(move[2][0].coordinates[0]) + '(fligh is: ' + str(move[2][-1].coordinates[0]) + ') is: ' + str(move[1]))
        print('Pac-Man corridor is :' + str(pacman.corridor))
        print('crossroad: ' + str(crossroad))
        print('ghost at crossroad is: ' + str(ghost))
        for g in self.advisor.ghosts_info:
            pass
            print(g.print())
        

        # There is no ghost reaching pacman at the crossroad
        if ghost == None:
            print('valid: no ghost')
            return True
        
        # The ghost and pacman are in opposite sides of the target
        print('---> verify if ghost just after the target')
        tx,ty = move[0]
        gx,gy = ghost.position
        if gx==tx+1 or gx==tx-1 or gy==ty+1 or gy==ty-1:
            if gx==tx or gy==ty:
                if move[1] == 1:
                    print('---> ghost just after the target')
                    return False

        # ghost is in first corridor of path (dangerous)
        if flight == False:
            print('---> verifying if ghost: ' + str(ghost) + 'is in corridor ' + str(path[-2].coordinates))
            if ghost.position in path[-2].coordinates:
                print('invalid: ghost in the first corridor of path')
                return False
        else:
            print('---> verifying if ghost: ' + str(ghost) + 'is in corridor ' + str(path[1].coordinates))
            if ghost.position in path[1].coordinates:
                print('invalid: ghost in the first corridor of path')
                return False

        # pacman is being pursued from behind and there is a ghost in the next corridor of path
        print('---> verify if there is a trap')
        if flight == False:
            if pacman.pursued_from_other_crossroad(crossroad):
                if len(path) >= 3:
                    if ghost.position in path[-3].coordinates:
                        print('invalid: ghost pursuing from behind and trap ahead')
                        return False
        else:
            if pacman.pursued_from_other_crossroad(crossroad):
                if len(path) >= 3:
                    if ghost.position in path[2].coordinates:
                        print('invalid: ghost pursuing from behind and trap ahead')
                        return False

        # ghost just after the first corridor, and pacman just exiting it
        print('---> ghost after first corridor')
        if pacman.dist_to_crossroad(crossroad) == 1 and ghost.dist_to_crossroad == 1:
            print('invalid: ghost just after the first corridor, and pacman just exiting it')
            return False
        
        # ghost not in the path, but in pursuit of pacman, will intercept
        print('---> verify interception')
        if pacman.pursued_from_crossroad(crossroad):
            if ghost.position not in [c for corr in path for c in corr.coordinates]:
                if ghost.side_interception(path):
                    print('invalid: pacman will be intercepted')
                    return False

        # probable interception in the longer run
        if flight or surrounded_eating:
            print('---> verify probable interception in future')
            for ghost in self.advisor.ghosts_info:
                if ghost.crossroad_to_pacman == crossroad:
                    if ghost.side_interception(path):
                        print('invalid: pacman will probably be intercepted in the long run')
                        return False

        # next corridor is safe, but once inside pacman will be trapped
        # ghost from behind is ate distance 1 or 2, which mean that no turning back is possible
        if pacman.position in self.advisor.map_.crossroads and self.ghosts_in_pursuit >= 0:
            print('###')
            print(pacman.position)
            print(self.advisor.map_.crossroads)
            print('###')
            #ignore trap because there is a Boost inside the new corridor
            if counter == True:
                if cost < (ghost.dist_to_pacman - cost):
                    print('valid: trap ignored because pacman will catch boost')
                    return True

            if len(self.advisor.state['energy']) < 20 and self.advisor.state['lives'] >= 2:
                return True
            
            if len(self.advisor.state['energy']) < 5 and self.advisor.state['lives'] == 2:
                return True

            print('---> verify if there will be a future trap')
            if pacman.ghost_at_crossroad(pacman.get_other_crossroad(crossroad)) != None:
                if pacman.dist_to_ghost_at_crossroad(pacman.get_other_crossroad(crossroad)) < 3:
                    
                    if not flight:
                        next_move = path[-2].get_coord_next_to_end(pacman.position)
                    if flight:
                        next_move = path[1].get_coord_next_to_end(pacman.position)

                    corr = None
                    for c in self.advisor.map_.corridors:
                        if next_move in c.coordinates:
                            corr = c
                            break

                    if pacman.ghost_at_crossroad(crossroad).is_coord_in_path(corr.get_other_end(crossroad)):
                        
                        print('ANALYST: corr ' + str(corr))
                        print('ANALYST: corr.get_other_end(crossroad) ' + str(corr.get_other_end(crossroad)))
                        print('ANALYST: next_move_dist_to_end ' + str(corr.dist_to_end(next_move, corr.get_other_end(crossroad))))
                        next_move_dist_to_end = corr.dist_to_end(next_move, corr.get_other_end(crossroad))
                        print('ANALYST: pacman.dist_to_ghost_at_crossroad(crossroad) ' + str(pacman.dist_to_ghost_at_crossroad(crossroad)))
                        print('ANALYST: corr.cost ' + str(corr.cost))
                        print('ANALYST: other_ghost_dist_to_end ' + str(pacman.dist_to_ghost_at_crossroad(crossroad) - corr.cost))
                        other_ghost_dist_to_end = pacman.dist_to_ghost_at_crossroad(crossroad) - corr.cost
                        if next_move_dist_to_end >= other_ghost_dist_to_end-1:
                            print('invalid: next crossroad is safe but pacman will be trapped')
                            #self.avoid_coordinates = corr.get_coord_next_to_end(pacman.position)
                            return False

                    elif pacman.ghost_at_crossroad(crossroad).position in corr.coordinates:
                        print('invalid: next crossroad is safe but pacman will be trapped (ghost inside next corr)')
                        return False

    
        print('MOVE IS REMAING VALID')
        print(' ------------ \n')
        return True