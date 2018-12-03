from tree_search import *
from pathways import Pathways


class FlightAgent:

    def __init__(self, advisor, targets):
        self.advisor = advisor
        self.targets = targets


    def flee(self):
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

    #--------------------------------------------------------------------------#
    # IN CASE THERE ARE NO TARGETS TO SEARCH FOR
        if self.targets == []:
            return None

    #--------------------------------------------------------------------------#
    # 
        
        pac_info = self.advisor.pacman_info
        pacman = pac_info.position
        pac_crossroads = pac_info.crossroads

        pac_adj0, pac_safe_corr0 = self.calc_adj_and_safe(pac_crossroads[0])
        # print("---")
        # print(pac_adj0)
        # print("---")
        # print(pac_safe_corr0)
        # print("---")

        pac_adj1, pac_safe_corr1 = self.calc_adj_and_safe(pac_crossroads[1])
        # print(pac_adj1)
        # print("---")
        # print(pac_safe_corr1)
        ########################################################################
        ## PAC CORR UNSAFE #####################################################
        ########################################################################

        # pacman is blocked from both sides - moves to the side with the farthest ghost
        if pac_info.crossroad0_is_blocked == True and pac_info.crossroad1_is_blocked == True:
            if pac_info.dist_to_ghost_at_crossroad0 >= pac_info.dist_to_ghost_at_crossroad1:
                #escolhe crossroad0
                print('1 - unsafe - both blocked: goes for 0')
                return self.calc_next_coord(pacman, pac_info.crossroad0, [])
            else:
                #escolhe crossroad1
                print('2 - unsafe - both blocked: goes for 1')
                return self.calc_next_coord(pacman, pac_info.crossroad1, [])

            # pacman is blocked only from one side - moves to the other side (probably)
            blocked_cross = None
            free_cross = None
            semaphore = None
            pac_adj = None
            pac_safe_corr = None
            if pac_info.crossroad0_is_blocked == True:
                blocked_cross = pac_info.crossroad0
                free_cross = pac_info.crossroad1
                semaphore = pac_info.semaphore1
                pac_adj = pac_adj1
                pac_safe_corr = pac_safe_corr1
            if pac_info.crossroad1_is_blocked == True:
                blocked_cross = pac_info.crossroad1
                free_cross = pac_info.crossroad0
                semaphore = pac_info.semaphore0
                pac_adj = pac_adj0
                pac_safe_corr = pac_safe_corr0


            #pacman consegue fugir pelo crossroad1
            if semaphore == SEMAPHORE.YELLOW or semaphore == SEMAPHORE.GREEN:   

                #ha corr safe
                if pac_safe_corr != []:
                    #escolhe pac_safe_corr1[0]
                    print('3 - unsafe - ' + str(blocked_cross) + ' blocked: goes for ' + str(free_cross) + 'which is safe')
                    return self.calc_next_coord(pacman, free_cross, pac_safe_corr[0])
                
                #NAO ha corr safe
                else:
                    #escolhe corr com ghost mais afastado
                    next_corr = self.calc_corridor_ghost_farther(pac_adj)
                    print('4 - unsafe - ' + str(blocked_cross) + ' blocked: goes for ' + str(free_cross) + 'which is not safe')
                    return self.calc_next_coord(pacman, free_cross, next_corr)

            #pacman NAO consegue fugir pelo crossroad1 -> crossroad1 is RED
            else:
                print('5 - unsafe - ' + str(blocked_cross) + ' blocked: goes for ' + str(free_cross) + 'which is not safe')
                return self.calc_next_coord(pac_info, free_cross, [])


        ####################################################################
        ## PAC CORR SAFE ###################################################
        ####################################################################

        #corr do pacman NAO tem ghosts -> crossroad[0].SAFE and crossroad[1].SAFE
 
        #pacman consegue fugir pelo crossroad0
        if pac_info.semaphore0 == SEMAPHORE.YELLOW or pac_info.semaphore0 == SEMAPHORE.GREEN:
        
            #pacman consegue fugir por qualquer crossroad
            if pac_info.semaphore1 == SEMAPHORE.YELLOW or pac_info.semaphore1 == SEMAPHORE.GREEN:

                #crossroad0 liga a corr SAFE
                if pac_safe_corr0 != []:
                    #ambos os crossroads ligam a corr SAFE
                    if pac_safe_corr1 != []:
                        #escolhe o crossroad mais longe
                        #crossroad0 mais longe do pacman
                        if pac_info.dist_to_crossroad0 >= pac_info.dist_to_crossroad1:
                            #escolhe pac_safe_corr0[0]
                            print('6 - safe  - green or yellow crossroads: goes for ' + str(pac_safe_corr0[0]))
                            return self.calc_next_coord(pacman, pac_info.crossroad0, pac_safe_corr0[0])

                        #crossroad1 mais longe do pacman    
                        else:
                            #escolhe pac_safe_corr1[0]
                            print('7 - safe - green or yellow crossroads: goes for ' + str(pac_safe_corr1[0]))
                            return self.calc_next_coord(pacman, pac_info.crossroad1, pac_safe_corr1[0])

                    #apenas crossroad0 liga a corr SAFE
                    else:
                        #escolhe pac_safe_corr0[0]
                        print('8 - safe - green or yellow crossroads: goes for ' + str(pac_safe_corr0[0]))
                        return self.calc_next_coord(pacman, pac_info.crossroad0, pac_safe_corr0[0])
                
                #crossroad0 nao liga a corr SAFE
                else:
                    #apenas crossroad1 liga a corr SAFE
                    if pac_safe_corr1 != []:
                        #escolhe pac_safe_corr1[0]
                        print('9 - safe - green or yellow crossroads: goes for ' + str(pac_safe_corr1[0]))
                        return self.calc_next_coord(pacman, pac_info.crossroad1, pac_safe_corr1[0])

                    #NAO ha corr SAFE        
                    else:
                        #escolhe corr com ghost mais afastado
                        next_corr = self.calc_corridor_ghost_farther(pac_adj1)
                        #?return self.calc_corridor_ghost_farther(pac_info, pac_adj0 + pac_adj1, ghosts_info)
                        print('9 - safe - green or yellow crossroads: goes for ' + str(pac_adj0[0]))
                        return self.calc_next_coord(pacman, pac_info.crossroad0, pac_adj0[0])#, return self.calc_next_coord(pac_info.position, pac_info.crossroad1)
            
            #pacman consegue fugir apenas pelo crossroad0
            else:

                #crossroad0 liga a corr SAFE
                if pac_safe_corr0 != []:
                    #escolhe pac_safe_corr0[0]
                    print('10 - safe - crossroad ' + str(pac_info.crossroad1) + ' is red: goes for ' + str(pac_safe_corr0[0]))
                    return self.calc_next_coord(pacman, pac_info.crossroad0, pac_safe_corr0[0])
                
                #NAO ha corr SAFE pelo crossroad0
                else:
                    #escolhe corr com ghost mais afastado
                    next_corr = self.calc_corridor_ghost_farther(pac_adj0)
                    print('11 - safe - crossroad ' + str(pac_info.crossroad1) + ' is red: goes for ' + str(pac_adj0[0]))
                    #?return self.calc_corridor_ghost_farther(pac_info, pac_adj0, ghosts_info)
                    return self.calc_next_coord(pacman, pac_info.crossroad0, pac_adj0[0])
        
        #pacman NAO consegue fugir pelo crossroad0
        else:

            #pacman consegue fugir apenas pelo crossroad1
            if pac_info.semaphore1 == SEMAPHORE.YELLOW:
                #crossroad1 liga a corr SAFE
                if pac_safe_corr1 != []:
                    #escolhe pac_safe_corr1[0]
                    print('12 - safe - crossroad ' + str(pac_info.crossroad0) + ' is red: goes for ' + str(pac_safe_corr1[0]))
                    return self.calc_next_coord(pacman, pac_info.crossroad1, pac_safe_corr1[0])
                
                #NAO ha corr SAFE pelo crossroad1
                else:
                    #escolhe corr com ghost mais afastado
                    next_corr = self.calc_corridor_ghost_farther(pac_adj1)
                    print('13 - safe - crossroad ' + str(pac_info.crossroad0) + ' is red: goes for ' + str(pac_adj1[0]))
                    #?return self.calc_corridor_ghost_farther(pac_info, pac_adj1, ghosts_info)
                    return self.calc_next_coord(pacman, pac_info.crossroad1, pac_adj1[0])

            #pacman NAO consegue fugir por nenhum crossroad
            else:
                #escolhe lado com ghost mais afastado
                next_corr = self.calc_corridor_ghost_farther(pac_adj0 + pac_adj1)
                print('14 - safe - both crossroads are red: goes for ' + str(pac_info.crossroad0))
                #?return self.calc_corridor_ghost_farther(pac_info, pac_adj0 + pac_adj1, ghosts_info)
                return self.calc_next_coord(pacman, pac_info.crossroad0, [])


    def calc_adj_and_safe(self, crossroad):
        adj = []
        adj += [cA for [cA, cB] in self.advisor.map_.corr_adjacencies if crossroad in cA.ends]
        adj += [cB for [cA, cB] in self.advisor.map_.corr_adjacencies if crossroad in cB.ends]

        safe = [c for c in adj if c.safe == CORRIDOR_SAFETY.SAFE]

        return adj, safe
                

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
            next_move = self.advisor.pacman_info.corridor.get_next_coord_to_the_side_of_crossroad(pacman, crossroad)

        elif pacman == crossroad:
            next_move = next_corridor.get_coord_next_to_end(crossroad)

        return next_move


    #escolhe corr com ghost mais afastado
    def calc_corridor_ghost_farther(self, pac_adj):
        corridors_with_ghost = []

        for ghost in self.advisor.ghosts_info:
            for corr in pac_adj:
                if ghost.position in corr.coordinates:
                    corridors_with_ghost += [(corr, ghost.dist_to_pacman)]
                    break

        return sorted(corridors_with_ghost, key=lambda t: t[1], reverse=True)[0]
