from tree_search import *
from pathways import Pathways


class FlightAgent:

    def __init__(self, advisor, state, targets):
        self.advisor = advisor
        self.state = state
        self.targets = targets


    def flee(self, advisor):
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
                
        pac_info = advisor.pacman_info
        pac_crossroads = pac_info.crossroads

        pac_adj0, pac_safe_corr0 = self.calc_adj_and_safe(pac_info.corridor, pac_crossroads[0])
        print("---")
        print(pac_adj0)
        print("---")
        print(pac_safe_corr0)
        print("---")

        pac_adj1, pac_safe_corr1 = self.calc_adj_and_safe(pac_info.corridor, pac_crossroads[1])
        print(pac_adj1)
        print("---")
        print(pac_safe_corr1)
        ########################################################################
        ## PAC CORR UNSAFE #####################################################
        ########################################################################

        #corr pacman tem ghost do lado do crossroad0       
        if pac_info.crossroad0_is_blocked == True:

            #pacman esta encurralado (corr do pacman tem ghosts dos 2 lados)
            if pac_info.crossroad1_is_blocked == True:
                
                #escolhe lado com ghost mais afastado
                if pac_info.dist_to_ghost_at_crossroad0 >= pac_info.dist_to_ghost_at_crossroad1:
                    #escolhe crossroad0
                    return self.calc_next_coord(pac_info, pac_info.crossroad0, [])
                else:
                    #escolhe crossroad1
                    return self.calc_next_coord(pac_info, pac_info.crossroad1, [])

            #ghost no corr do pacman apenas do lado do crossroad0 -> crossroad0 is RED
            else:

                #pacman consegue fugir pelo crossroad1
                if pac_info.semaphore1 == SEMAPHORE.YELLOW:   

                    #ha corr safe
                    if pac_safe_corr1 != []:
                        #escolhe pac_safe_corr1[0]
                        return self.calc_next_coord(pac_info, pac_info.crossroad1, pac_safe_corr1)
                    
                    #NAO ha corr safe
                    else:
                        #escolhe corr com ghost mais afastado
                        #?return self.calc_corridor_ghost_farther(pac_info, pac_adj1, ghosts_info)
                        return self.calc_next_coord(pac_info, pac_info.crossroad1, pac_adj1)

                #pacman NAO consegue fugir pelo crossroad1 -> crossroad1 is RED
                else:
                    #escolhe crossroad1
                    return self.calc_next_coord(pac_info, pac_info.crossroad1, [])

        #corr do pacman NAO tem ghost do lado crossroad0
        else:

            #corr do pacman tem ghost apenas do lado crossroad1 -> crossroad1 is RED
            if pac_info.crossroad1_is_blocked == True:

                #pacman consegue fugir apenas pelo crossroad0
                if pac_info.semaphore0 == SEMAPHORE.YELLOW:
                    #crossroad0 liga a corr SAFE
                    if pac_safe_corr0 != []:
                        #escolhe pac_safe_corr0[0]
                        return self.calc_next_coord(pac_info, pac_info.crossroad0, pac_safe_corr0)
                    
                    #NAO ha corr SAFE pelo crossroad0
                    else:
                        #escolhe corr com ghost mais afastado
                        #?return self.calc_corridor_ghost_farther(pac_info, pac_adj0, ghosts_info)
                        return self.calc_next_coord(pac_info, pac_info.crossroad0, pac_adj0)

                #pacman NAO consegue fugir por nenhum crossroad -> crossroad0 is RED
                else:
                    #escolhe lado com ghost mais afastado
                    #?return self.calc_corridor_ghost_farther(pac_info, pac_adj0 + pac_adj1, ghosts_info)
                    return self.calc_next_coord(pac_info, pac_info.crossroad0, [])


            ####################################################################
            ## PAC CORR SAFE ###################################################
            ####################################################################

            #corr do pacman NAO tem ghosts -> crossroad[0].SAFE and crossroad[1].SAFE
            else:
                
                #pacman consegue fugir pelo crossroad0
                if pac_info.semaphore0 == SEMAPHORE.YELLOW:
                
                    #pacman consegue fugir por qualquer crossroad
                    if pac_info.semaphore1 == SEMAPHORE.YELLOW:

                        #crossroad0 liga a corr SAFE
                        if pac_safe_corr0 != []:
                            #ambos os crossroads ligam a corr SAFE
                            if pac_safe_corr1 != []:
                                #escolhe o crossroad mais longe
                                #crossroad0 mais longe do pacman
                                if pac_info.dist_to_crossroad0 >= pac_info.dist_to_crossroad1:
                                    #escolhe pac_safe_corr0[0]
                                    return self.calc_next_coord(pac_info, pac_info.crossroad0, pac_safe_corr0)

                                #crossroad1 mais longe do pacman    
                                else:
                                    #escolhe pac_safe_corr1[0]
                                    return self.calc_next_coord(pac_info, pac_info.crossroad1, pac_safe_corr1)

                            #apenas crossroad0 liga a corr SAFE
                            else:
                                #escolhe pac_safe_corr0[0]
                                return self.calc_next_coord(pac_info, pac_info.crossroad0, pac_safe_corr0)
                        
                        #crossroad0 nao liga a corr SAFE
                        else:
                            #apenas crossroad1 liga a corr SAFE
                            if pac_safe_corr1 != []:
                                #escolhe pac_safe_corr1[0]
                                return self.calc_next_coord(pac_info, pac_info.crossroad1, pac_safe_corr1)

                            #NAO ha corr SAFE        
                            else:
                                #escolhe corr com ghost mais afastado
                                #?return self.calc_corridor_ghost_farther(pac_info, pac_adj0 + pac_adj1, ghosts_info)
                                return self.calc_next_coord(pac_info, pac_info.crossroad0, pac_adj0)#, return self.calc_next_coord(pac_info.position, pac_info.crossroad1)
                    
                    #pacman consegue fugir apenas pelo crossroad0
                    else:

                        #crossroad0 liga a corr SAFE
                        if pac_safe_corr0 != []:
                            #escolhe pac_safe_corr0[0]
                            return self.calc_next_coord(pac_info, pac_info.crossroad0, pac_safe_corr0)
                        
                        #NAO ha corr SAFE pelo crossroad0
                        else:
                            #escolhe corr com ghost mais afastado
                            #?return self.calc_corridor_ghost_farther(pac_info, pac_adj0, ghosts_info)
                            return self.calc_next_coord(pac_info, pac_info.crossroad0, pac_adj0)
                
                #pacman NAO consegue fugir pelo crossroad0
                else:

                    #pacman consegue fugir apenas pelo crossroad1
                    if pac_info.semaphore1 == SEMAPHORE.YELLOW:
                        #crossroad1 liga a corr SAFE
                        if pac_safe_corr1 != []:
                            #escolhe pac_safe_corr1[0]
                            return self.calc_next_coord(pac_info, pac_info.crossroad1, pac_safe_corr1)
                        
                        #NAO ha corr SAFE pelo crossroad1
                        else:
                            #escolhe corr com ghost mais afastado
                            #?return self.calc_corridor_ghost_farther(pac_info, pac_adj1, ghosts_info)
                            return self.calc_next_coord(pac_info, pac_info.crossroad1, pac_adj1)

                    #pacman NAO consegue fugir por nenhum crossroad
                    else:
                        #escolhe lado com ghost mais afastado
                        #?return self.calc_corridor_ghost_farther(pac_info, pac_adj0 + pac_adj1, ghosts_info)
                        return self.calc_next_coord(pac_info, pac_info.crossroad0, [])


    def calc_adj_and_safe(self, pac_corr, crossroad):
        adj = [[cA, cB] for [cA, cB] in self.map_.corr_adjacencies\
                                        if crossroad in cA.ends\
                                        or crossroad in cB.ends]
            
        safe = [[cA, cB] for [cA, cB] in adj\
                            if (cA.coordinates == pac_corr.coordinates and cB.safe == CORRIDOR_SAFETY.SAFE)\
                            or (cB.coordinates == pac_corr.coordinates and cA.safe == CORRIDOR_SAFETY.SAFE)]

        return adj, safe
                

    def calc_next_coord(self, pac_info, end, adj_end):
        '''
            Args:
            pac_info:   advisor.pacman_info
            end     :   crossroad do lado escolhido para o pacman fugir
            adj_end :   lista de corredores adjacentes ao end
                        - adj_end == [] é porque o pacman não consegue fugir pelo end
                                        tanto por existir um fantasma no mesmo corredor desse lado
                                        tanto por o end ser RED
        '''

        [px, py] = pac_info.position
        
        next_move_pac_corr = [ coord for coord in pac_info.corridor.coordinates\
                                        if coord == [px-1, py]\
                                        or coord == [px+1, py]\
                                        or coord == [px, py-1]\
                                        or coord == [px, py+1]]

        #pacman esta num crossroad
        if len(next_move_pac_corr) == 1:
            print(adj_end)
            next_moves = [ coord for corridor in adj_end\
                                    for coord in [corridor.get_coord_next_to_end(end)]]

            return next_moves[0]

        #pacman NAO está num crossroad
        else:      

            [ex, ey] = end

            next_coord = next_move_pac_corr[0]
            dx = abs(ex - next_coord[0])
            dy = abs(ey - next_coord[1])

            for i in range(1, len(next_move_pac_corr)):

                [a,b] = next_move_pac_corr[i]
                da = abs(ex-a)
                db = abs(ey-b)

                if py == ey:
                    next_coord, dx, dy = [[a,b], da, db] if da<dx else [next_coord, dx, dy]
                elif px == ex:
                    next_coord, dx, dy = [[a,b], da, db] if db<dy else [next_coord, dx, dy]
                else:
                    next_coord, dx, dy = [[a,b], da, db] if (da==dx and db<dy)\
                                                            or (db==dy and da<dx)\
                                                            else [next_coord, dx, dy]

            return next_coord




    #escolhe corr com ghost mais afastado
    #TODO not done
    def calc_corridor_ghost_farther(self, pac_info, pac_adj, ghosts_info):
        dist = 0
        corr = []
        for adj_corr in pac_adj:
            for g_info in ghosts_info:
                if g_info.corridor == adj_corr and dist < g_info.dist_to_pacman:
                    dist = g_info.dist_to_pacman
                    corr = g_info.corridor                                                   
        
        #TODO devolver prox coord
        pass