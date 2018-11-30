from tree_search import *
from pathways import Pathways


class EatingAgent:
    """Creates the Eating Agent, which calculates the path to all accessible
    targets, and sorts them by cost and safety with the following criteria:
    1 - cost
    2 - if being pursued, distance of pacman to target smaller than ghost's
    3 - proximity of ghost in path to target

    Attr:
    advisor: provides extensive information about the current situation of the map
    targets: the targets to search paths to
    """

    def __init__(self, advisor, targets):
        self.advisor = advisor
        self.state = state
        self.targets = targets


    def eat(self):
        """Creates the Eating Agent, which calculates the path to all accessible
        targets, and sorts them by cost and safety with the following criteria:
        1 - cost
        2 - if being pursued, distance of pacman to target smaller than ghost's
        3 - proximity of ghost in path to target

        Returns:
        A list of paths to every accessible target, ordered by cost and safety
        """

    #--------------------------------------------------------------------------#
    # CREATE DOMAIN AND AUXILIAR VARIABLES
    
        pacman = advisor.pacman_info
        acessible_energies = []
        possible_moves = []
        domain = Pathways(self.advisor.map_.corr_adjacencies, self.targets)

    #--------------------------------------------------------------------------#
    # SEARCH FOR ENERGIES

        for energy in self.targets:
            
            # find this energy corridor
            corridor = None
            for corr in self.map_.corridors:
                if energy in corr.coordinates:
                    corridor = corr
                    break
            
            # create problem and search
            my_prob = SearchProblem(domain, corridor, energy, pacman.corridor, pacman.position)
            my_tree = SearchTree(my_prob, "a*")
            search_results = my_tree.search()
            
            # filter valid results and store them in possible_moves
            if search_results != None:
                acessible_energies += [energy]
                possible_moves += [search_results]

        # if there are no possible moves, everything is eaten
        print(len(possible_moves))
        if len(possible_moves) == 0:
            return (possible_moves, False)

    #-------------------------------------------------------------------------#
    # SORT MOVES BY COST
        possible_moves = sorted(possible_moves,key=lambda res: res[1])

    #--------------------------------------------------------------------------#
    # SORT MOVES BY WHERE A GHOST IS BLOCKING THE NEXT CORRIDOR
        f_moves = []
        for move in possible_moves:
            if move[2][-3].safe == True:
                f_moves += [move]

        possible_moves = [move for move in possible_moves if move not in f_moves]
        possible_moves += f_moves

    #--------------------------------------------------------------------------#
    # SORT MOVES BY WHERE A GHOST IN PURSUIT IS CLOSER TO THE ENERGY THAN PAC-MAN
        f_moves = []
        BEST_GHOST_DIST_TO_ENERGY = 1000
        for move in possible_moves:

            next_move, cost, path = move
            energy_inside_corr = False
            clear_path = True
            
            # verify which ghost is blocking the path or if the path is clear
            if pacman.ghost_at_crossroad0 != None:
                #print('A: ' + str(pacman.ghost_at_crossroad0.position))
                #print('B: ' + str([c for lcoor in corr.coordinates for corr in path for c in lcoor]))
                if pacman.ghost_at_crossroad0.position in [c for lcoor in corr.coordinates for corr in path for c in lcoor]:
                    clear_path = False
                    ghost = pacman.ghost_at_crossroad0
                    
            if pacman.ghost_at_crossroad1 != None:
                if pacman.ghost_at_crossroad1.position in [ c for lcoor in corr.coordinates for corr in path for c in lcoor]:
                    clear_path = False
                    ghost = pacman.ghost_at_crossroad1

            if clear_path:
                f_moves += [move]
                continue

            # verify which crossroad is in the path
            crossroad = None
            if pacman.crossroad0 in [ c for lcoor in corr.coordinates for corr in path for c in lcoor]:
                crossroad = pacman.crossroad0
                #print('ps_cross0: ' + str(pacman.crossroad0))
            elif pacman.crossroad1 in [ c for lcoor in corr.coordinates for corr in path for c in lcoor]:
                crossroad = pacman.crossroad1
                #print('ps_cross1: ' + str(pacman.crossroad1))

            # if no crossroad is in the path, then the energy is inside the corridor
            # it's needed to verify from which crossroad is the energy will be accessed
            if crossroad == None:
                energy_inside_corr = True
                sub_corr0 = pacman.corridor.sub_corridors(pacman.position)[0].coordinates
                sub_corr1 = pacman.corridor.sub_corridors(pacman.position)[0].coordinates
                if any([ c in path for c in sub_corr0]):
                    crossroad = pacman.crossroad0
                elif any([ c in path for c in sub_corr1]):
                    crossroad = pacman.crossroad1

            # calculate distances of pacman and ghost to energy, according to
            # if energy is inside or outside pacman corridor

            # calculate distancies for when energy is in pacman corridor
            if energy_inside_corr:
                cross_to_energy = pacman.dist_to_crossroad(crossroad) - cost
                ghost_dist_to_energy = ghost.dist_to_crossroad + cross_to_energy
                #print(ghost_dist_to_energy)
                BEST_GHOST_DIST_TO_ENERGY = ghost_dist_to_energy if ghost_dist_to_energy < BEST_GHOST_DIST_TO_ENERGY else BEST_GHOST_DIST_TO_ENERGY
            # calculate distancies for when energy is NOT in pacman corridor
            else:
                cross_to_energy = cost - pacman.dist_to_crossroad(crossroad)
                ghost_dist_to_energy = ghost.dist_to_crossroad - cross_to_energy
                #print(ghost_dist_to_energy)
                BEST_GHOST_DIST_TO_ENERGY = ghost_dist_to_energy if ghost_dist_to_energy < BEST_GHOST_DIST_TO_ENERGY else BEST_GHOST_DIST_TO_ENERGY
            
            # if pacman distance to energy is smaller than ghost's, discard move
            if cost < ghost_dist_to_energy:
                f_moves += [move]

            # sort
            possible_moves = [move for move in possible_moves if move not in f_moves]
            possible_moves += f_moves

    #--------------------------------------------------------------------------#
    # FAKE ADJUSTER

        option = possible_moves[0]
        #print('closer ghosts: ' + str(BEST_GHOST_DIST_TO_ENERGY) + 'cost: ' + str(option[1]))
        if BEST_GHOST_DIST_TO_ENERGY < option[1]:
            return possible_moves, False

    #--------------------------------------------------------------------------#
    # RETURN OPTIONS

        return possible_moves, True