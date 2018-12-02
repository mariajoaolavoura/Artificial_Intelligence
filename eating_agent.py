from game_consts import *
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
        self.targets = targets


    def eat(self):
        """Calculates the path to all accessible targets, and sorts them by cost
        and safety with the following criteria:
        1 - cost
        2 - if being pursued, distance of pacman to target smaller than ghost's
        3 - proximity of ghost in path to target

        Returns:
        A list of paths to every accessible target, ordered by cost and safety
        """

    #--------------------------------------------------------------------------#
    # IN CASE THERE ARE NO TARGETS TO SEARCH FOR
        if self.targets == []:
            return None

    #--------------------------------------------------------------------------#
    # CREATE DOMAIN AND AUXILIAR VARIABLES
        pacman = self.advisor.pacman_info
        acessible_energies = []
        possible_moves = []
        domain = Pathways(self.advisor.map_.corr_adjacencies, self.targets, self.advisor.map_)

    #--------------------------------------------------------------------------#
    # SEARCH FOR ENERGIES

        for energy in self.targets:
            
            # find this energy corridor
            corridor = None
            for corr in self.advisor.map_.corridors:
                if energy in corr.coordinates:
                    corridor = corr
                    break
            
            # create problem and search
            my_prob = SearchProblem(domain, corridor, energy, pacman.corridor, \
                                    pacman.position, self.advisor.map_, self.advisor.state)
            my_tree = SearchTree(my_prob, "a*")
            search_results = my_tree.search()
            
            # filter valid results and store them in possible_moves
            if search_results != None:
                acessible_energies += [energy]
                possible_moves += [search_results]

        # if there are no possible moves, everything is eaten
        if len(possible_moves) == 0:
            return possible_moves

    #-------------------------------------------------------------------------#
    # SORT MOVES BY COST
        possible_moves = sorted(possible_moves,key=lambda res: res[1])

    #--------------------------------------------------------------------------#
    # SORT MOVES BY WHERE A GHOST IS BLOCKING THE NEXT CORRIDOR
        f_moves = []
        for move in possible_moves:
            if move[2][-3].safe == CORRIDOR_SAFETY.UNSAFE:
                f_moves += [move]

        possible_moves = [move for move in possible_moves if move not in f_moves]
        possible_moves += f_moves

    #--------------------------------------------------------------------------#
    # SORT MOVES BY WHERE A GHOST IS BLOCKING PAC-MAN CORRIDOR
        f_moves = []
        for move in possible_moves:
            if move[2][-2].safe == CORRIDOR_SAFETY.UNSAFE:
                f_moves += [move]

        possible_moves = [move for move in possible_moves if move not in f_moves]
        possible_moves += f_moves

    #--------------------------------------------------------------------------#
    # DISCARD MOVES WHERE A GHOST IN PURSUIT IS CLOSER TO THE ENERGY THAN PAC-MAN
    # TODO after strategy_analyser is done, reverify if this last sort/discar works
        f_moves = []
        for move in possible_moves[:]:

            _, cost, path = move
            energy_inside_corr = False
            clear_path = True
            
            # verify which ghost is blocking the path or if the path is clear
            if pacman.ghost_at_crossroad0 != None:
                
                if any([c in pacman.ghost_at_crossroad0.position for corr in path for c in corr.coordinates]):
                    clear_path = False
                    ghost = pacman.ghost_at_crossroad0
                    
            if pacman.ghost_at_crossroad1 != None:
                if any([c in pacman.ghost_at_crossroad1.position for corr in path for c in corr.coordinates]):
                    clear_path = False
                    ghost = pacman.ghost_at_crossroad1

            if clear_path:
                continue

            # verify which crossroad is in the path
            crossroad = None
            if any([c in pacman.crossroad0 for corr in path for c in corr.coordinates]):
                crossroad = pacman.crossroad0
            elif any([c in pacman.crossroad1 for corr in path for c in corr.coordinates]):
                crossroad = pacman.crossroad1

            # if no crossroad is in the path, then the energy is inside the corridor
            # it's needed to verify from which crossroad is the energy will be accessed
            if crossroad == None:
                energy_inside_corr = True
                sub_corr0 = pacman.corridor.sub_corridors(pacman.position)[0].coordinates
                sub_corr1 = pacman.corridor.sub_corridors(pacman.position)[1].coordinates
                if any([ c in sub_corr0 for corr in path for c in corr.coordinates ]):
                    crossroad = pacman.crossroad0
                elif any([ c in sub_corr1 for corr in path for c in corr.coordinates ]):
                    crossroad = pacman.crossroad1

            # calculate distances of pacman and ghost to energy, according to
            # if energy is inside or outside pacman corridor

            # calculate distancies for when energy is in pacman corridor
            if energy_inside_corr:
                cross_to_energy = pacman.dist_to_crossroad(crossroad) - cost
                ghost_dist_to_energy = ghost.dist_to_crossroad + cross_to_energy
            # calculate distancies for when energy is NOT in pacman corridor
            else:
                cross_to_energy = cost - pacman.dist_to_crossroad(crossroad)
                ghost_dist_to_energy = ghost.dist_to_crossroad - cross_to_energy
            
            # if pacman distance to energy is smaller than ghost's, discard move
            if cost < ghost_dist_to_energy and pacman.pursued_from_crossroad(crossroad):
                possible_moves.remove(move)
            elif cost < ghost_dist_to_energy:
                f_moves += [move]

        # sort
        possible_moves = [move for move in possible_moves if move not in f_moves]
        possible_moves += f_moves

    #--------------------------------------------------------------------------#
    # RETURN OPTIONS
        return possible_moves