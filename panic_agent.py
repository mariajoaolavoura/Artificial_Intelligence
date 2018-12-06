from tree_search import *
from pathways import Pathways
from corridor import *


class PanicAgent:

    def __init__(self, advisor):
        self.advisor = advisor
        self.pac_info = advisor.pacman_info
        self.pacman = advisor.pacman_info.position
        self.crossroad0 = advisor.pacman_info.crossroad0
        self.crossroad1 = advisor.pacman_info.crossroad1
        self.semaphore0 = advisor.pacman_info.semaphore0
        self.semaphore1 = advisor.pacman_info.semaphore1


    def panic(self, avoid_corridor):
        '''
        args:
        advisor: instance of Strategy_Advisor
                self.map_ = map_
                self.state = state
                self.unsafe_corridors = self.set_corridors_safety()
                self.pacman_info = Pacman_Info(state['pacman'])
                self.calculate_pacman_corridor()
                self.ghosts_info = self.calculate_ghosts_info()
        '''
    
        pac_adj0, pac_safe_corr0 = self.calc_adj_and_safe(self.pac_info.crossroads[0], avoid_corridor)
        escape_corridors0 = pac_safe_corr0 if pac_safe_corr0 != [] else pac_adj0

        pac_adj1, pac_safe_corr1 = self.calc_adj_and_safe(self.pac_info.crossroads[1], avoid_corridor)
        escape_corridors1 = pac_safe_corr1 if pac_safe_corr1 != [] else pac_adj1

        all_adjacent_corridors = pac_adj0 + pac_adj1
        all_safe_adjacent_corridors = pac_safe_corr0 + pac_safe_corr1
        all_escape_corridors = escape_corridors0 + escape_corridors1

        print('PANICKING INIT:')
        print('---> pac_adj0: ' + str(pac_adj0))
        print('---> pac_safe_corr0: ' + str(pac_safe_corr0))
        print('---> escape_corridors0: ' + str(escape_corridors0))
        print('---> pac_adj1: ' + str(pac_adj1))
        print('---> pac_safe_corr1: ' + str(pac_safe_corr1))
        print('---> escape_corridors1: ' + str(escape_corridors1))

   
        ########################################################################
        ## PAC CORR UNSAFE #####################################################
        ########################################################################

        # pacman is blocked from both sides - moves to the side with the farthest ghost
        if self.pac_info.crossroad0_is_blocked == True and self.pac_info.crossroad1_is_blocked == True:
            if self.pac_info.dist_to_ghost_at_crossroad0 >= self.pac_info.dist_to_ghost_at_crossroad1:
                #escolhe crossroad0
                #! deu bem 1 vez
                print('0 - blocked from both sides: goes for 0')
                return self.calc_next_coord(self.pacman, self.crossroad0, [])
            else:
                #escolhe crossroad1
                print('1 - blocked from both sides: goes for 1')
                return self.calc_next_coord(self.pacman, self.crossroad1, [])
        
        # pacman is blocked only from one side - moves to the other side (probably)
        if self.pac_info.crossroad0_is_blocked == True or self.pac_info.crossroad1_is_blocked == True:
            blocked_cross = None
            free_cross = None
            semaphore = None
            escape_coridors = None
            if self.pac_info.crossroad0_is_blocked == True:
                blocked_cross = self.crossroad0
                free_cross = self.crossroad1
                semaphore = self.pac_info.semaphore1
                escape_corridors = escape_corridors1
            if self.pac_info.crossroad1_is_blocked == True:
                blocked_cross = self.crossroad1
                free_cross = self.crossroad0
                semaphore = self.pac_info.semaphore0
                escape_corridors = escape_corridors0

            print('PANICKING BLOCKED FROM ONE SIDE:')
            print('---> bocked_cross: ' + str(blocked_cross))
            print('---> free_cross: ' + str(free_cross))
            print('---> semaphore: ' + str(semaphore))
            print('---> escape_corridors: ' + str(escape_corridors))

            # unblocked crossroad is not red - pacman can pass through it
            if semaphore == SEMAPHORE.YELLOW or semaphore == SEMAPHORE.GREEN:   

                print('2 - blocked from side: ' + str(blocked_cross) + ' goes for ' + str(free_cross) + 'which is yellow or green')
                next_corr = self.calc_next_corridor(escape_corridors)
                return self.calc_next_coord(self.pacman, free_cross, next_corr)

            # unblocked crossroad is red - pacman cannot go through it
            if semaphore == SEMAPHORE.RED:
                #! deu bem 1 vez
                print('3 - blocked from side: ' + str(blocked_cross) + ' goes for ' + str(free_cross) + 'which is red')
                return self.escape_to_farthest_ghost_side(free_cross, blocked_cross)


        ####################################################################
        ## PAC CORR SAFE ###################################################
        ####################################################################

        # pacman corridor is not blocked in either side

        # both crossroads are red - chooses side with farthest ghost
        if self.semaphore0 == SEMAPHORE.RED and self.semaphore1 == SEMAPHORE.RED:
            print('4 - not blocked. Both crossroads are red: goes for farthest side')
            return self.escape_to_farthest_ghost_side(self.crossroad0, self.crossroad1)

        # one crossroad is red - chooses the other crossroad
        if self.semaphore0 == SEMAPHORE.RED:
            next_corr = self.calc_next_corridor(escape_corridors1)
            print('5 - not blocked. crossroad ' + str(self.crossroad0) + ' is red, goes for the other')
            return self.calc_next_coord(self.pacman, self.crossroad1, next_corr)
        if self.semaphore1 == SEMAPHORE.RED:
            next_corr = self.calc_next_corridor(escape_corridors0)
            print('6 - not blocked. crossroad ' + str(self.crossroad1) + ' is red, goes for the other')
            return self.calc_next_coord(self.pacman, self.crossroad0, next_corr)

        # both crossroads are yellow - chooses farthest crossroad
        if self.semaphore0 == SEMAPHORE.YELLOW and self.semaphore1 == SEMAPHORE.YELLOW:
            print('7 - not blocked. both crossroads are yellow: goes for farthest side')
            return self.escape_to_farthest_crossroad(self.crossroad0, self.crossroad1, escape_corridors0, escape_corridors1)

        # crossroads are green or yellow - chooses a safe corridor
        if all_safe_adjacent_corridors != []:
            next_corr = self.calc_next_corridor(all_safe_adjacent_corridors)
            print('8 - not blocked. crossroads are green or yellow: goes for a safe corridor')
            return self.calc_next_coord(pacman=self.pacman, crossroad=None , next_corridor=next_corr)

        next_corr = self.calc_next_corridor(all_adjacent_corridors)
        print('9 - not blocked. crossroads are green or yellow: goes for an unsafe corridor')
        return self.calc_next_coord(pacman=self.pacman, crossroad=None , next_corridor=next_corr)


    def calc_adj_and_safe(self, crossroad, avoid_corridor):

        adj_corrs = []
        adj_corrs += [cA for [cA, cB] in self.advisor.map_.corr_adjacencies if crossroad in cA.ends]
        adj_corrs += [cB for [cA, cB] in self.advisor.map_.corr_adjacencies if crossroad in cB.ends]
        print('#################################')
        print('#################################')
        #remove pacman corridor
        adj_corrs = [c for c in adj_corrs if c != self.pac_info.corridor]
        adj_corrs = list(set(adj_corrs))

        # set corridors as unsafe
        for ghost in [ghost for ghost in self.advisor.state['ghosts'] if ghost[1] == False]:
            for corr in adj_corrs:
                if ghost[0] in corr.coordinates:
                    corr.safe = CORRIDOR_SAFETY.UNSAFE
                else:
                    corr.safe = CORRIDOR_SAFETY.SAFE

        print('PANIC: calculating adjacent corridors ' + str(adj_corrs))
        if avoid_corridor != None:
            adj_corrs = [c for c in adj_corrs if c != avoid_corridor]
            print('#################################')
            print('#################################')
            print('PANIC: avoid corridor is ' + str(avoid_corridor))
            print('PANIC: filtered avoid corridor from adjacent corridors ' + str(adj_corrs))
            print('#################################')
            print('#################################')
        # aux = []
        # for c in adj_corrs:
        #     for coord in c.coordinates:
        #         if coord not in self.pac_info.corridor.coordinates: 
        #             aux += [c]
        #             break
        for c in adj_corrs:
            print('--> safe ' + str(c) + ', ' + str(c.safe))
        # adj = aux
        safe = [c for c in adj_corrs if c.safe == CORRIDOR_SAFETY.SAFE]
        print('PANIC: calculating adjacent SAFE corridors ' + str(safe))

        return adj_corrs, safe
                

    def calc_next_coord(self, pacman, crossroad, next_corridor):
        '''
            Args:
            pac_info:   advisor.pacman_info
            end     :   crossroad do lado escolhido para o pacman fugir
            adj_end :   lista de corredores adjacentes ao end
                        - adj_end == [] é porque o pacman não consegue fugir pelo end
                                        tanto por existir um fantasma no mesmo corredor desse lado
                                        tanto por o end ser RED
        '''

        next_move = None

        if next_corridor == []:
            if crossroad != None:
                return self.advisor.pacman_info.corridor.get_next_coord_to_the_side_of_crossroad(pacman, crossroad)
            else:
                return None
        
        # corridor exists
        if next_corridor != []:
            # crossroad is None
            if crossroad == None:
                crossroad = [c for c in next_corridor.coordinates if c in self.pac_info.corridor.coordinates][0]
                next_move = self.pac_info.corridor.get_next_coord_to_the_side_of_crossroad(pacman, crossroad)
                if next_move != None:
                    return next_move
                else:
                    print('PANIC: calculate coordinate, SHOULD NOT BE NONE!')
            # crossroad exists
            else:
                # tries to get next coordinate to the side of crossroad
                next_move =  self.advisor.pacman_info.corridor.get_next_coord_to_the_side_of_crossroad(pacman, crossroad)
                if next_move != None:
                    return next_move
                else:
                    print(next_corridor)
                    return next_corridor.get_coord_next_to_end(crossroad)


    #escolhe corr com ghost mais afastado
    def calc_next_corridor(self, pac_adj):

        for corr in pac_adj:
            if corr.safe == CORRIDOR_SAFETY.SAFE:
                print('PANIC: calculated next corridor as safe: ' + str(corr))
                return corr

        corridors_with_ghost = []
        for ghost in self.advisor.ghosts_info:
            for corr in pac_adj:
                if ghost.position in corr.coordinates:
                    corridors_with_ghost += [(corr, ghost.dist_to_pacman)]
                    break
        print('PANIC: calculated next corridor as unsafe: ' + str(sorted(corridors_with_ghost, key=lambda t: t[1], reverse=True)[0][0]))
        return sorted(corridors_with_ghost, key=lambda t: t[1], reverse=True)[0][0]


    def escape_to_farthest_ghost_side(self, cross0, cross1):
        if self.pac_info.dist_to_ghost_at_crossroad(cross0) <= self.pac_info.dist_to_ghost_at_crossroad(cross1):
            return self.calc_next_coord(self.pacman, cross1, [])
        else:
            return self.calc_next_coord(self.pacman, cross0, [])

    def escape_to_farthest_crossroad(self, cross0, cross1, escape_corridors0, escape_corridors1):
        
        if self.pac_info.dist_to_crossroad(cross0) >= self.pac_info.dist_to_crossroad(cross1):
            next_corr = self.calc_next_corridor(escape_corridors0)
            return self.calc_next_coord(self.pacman, cross0, next_corr)  
        else:
            next_corr = self.calc_next_corridor(escape_corridors1)
            return self.calc_next_coord(self.pacman, self.crossroad1, next_corr)