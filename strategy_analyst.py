from game_consts import *
from pursuit_agent import *
from eating_agent import *
from counter_agent import *
from flight_agent import *
from panic_agent import *

class StrategyAnalyst():
    """Creates the Strategy Analist, which coordinates the possible moves given
    by the Pursuit, Eating, Counter and Flight Agents and chooses the best Pac-Man
    next move overall

    Attr:
    advisor: provides extensive information about the current situation of the map
    """

    def __init__(self, advisor):
        self.advisor = advisor
        self.pursuer_possible_moves = []
        self.eater_possible_moves = []
        self.counter_possible_moves = []
        self.fleer_possible_moves = []

    
    def decide(self):
        """ Main method of the StartegyAnalyst class, which accomplishes the
        class goal

        Returns:
        The next advised position for Pac-Man to go to
        """

        # always tries to pursue ghosts first
        next_move = self._try_pursuit()
        if next_move != None:
            return next_move

        # if there are no ghosts to pursue pacman counters if is surrounded or eats if not
        ghosts_in_pursuit = 0
        for ghost in self.advisor.ghosts_info:
            if ghost.dist_to_pacman <= SAFE_DIST_TO_GHOST:
                ghosts_in_pursuit += 1
        # counter (if not possible, try eating)
        if ghosts_in_pursuit >= 2:
            
            next_move = self._try_counter()
            if next_move != None:
                return next_move
        
            next_move = self._try_eating()

            next_move = self._try_flight(avoid_suggestion=False)
            if next_move != None:
                return next_move
        
        # eat (if not possible, try counter)
        else:
            next_move = self._try_eating()
            if next_move != None:
                return next_move

            next_move = self._try_counter()
            if next_move != None:
                return next_move
            
            next_move = self._try_flight(avoid_suggestion=True)
            if next_move != None:
                return next_move
        
        
        # no strategy available, time to panic! Goes for the first safe corridor
        panicked_for_a_way_out = self._panic()

        # ----- no agent got a move - this should never happen
        if panicked_for_a_way_out == None:
            print('NO AGENT GOT A MOVE!!!')
            return None

        return panicked_for_a_way_out



    def _analyse_best_move(self, possible_moves, flight=False):
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
        path = move[2]
        #print('ANALYSE: path is ' + str(path))
        path_coords = [c for corr in path for c in corr.coordinates]
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
        if len([c for c in sub_corr0 if c in path_coords]) != 0:
            crossroad = pacman.crossroad0
            semaphore = pacman.semaphore0
            ghost = pacman.ghost_at_crossroad0
        elif len([c for c in sub_corr1 if c in path_coords]) != 0:
            crossroad = pacman.crossroad1
            semaphore = pacman.semaphore1
            ghost = pacman.ghost_at_crossroad1
        else:
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
            #pass
            print(g.print())
        

        # There is no ghost reaching pacman at the crossroad
        if ghost == None:
            print('valid: no ghost')
            return True
        
        # The ghost and pacman are in opposite sides of the target
        print('---> before condition: ' + str(ghost.dist_to_pacman) + ', ' + str(move[1]))
        tx,ty = move[0]
        gx,gy = ghost.position
        if gx==tx+1 or gx==tx-1 or gy==ty+1 or gy==ty-1:
            if gx==tx or gy==ty:
                if move[1] == 1:
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
        if pacman.dist_to_crossroad(crossroad) == 1 and ghost.dist_to_crossroad == 1:
            print('invalid: ghost just after the first corridor, and pacman just exiting it')
            return False
        
        # ghost not in the path, but in pursuit of pacman, will intercept
        if pacman.pursued_from_crossroad(crossroad):
            if ghost.position not in [c for corr in path for c in corr.coordinates]:
                if ghost.side_interception(path):
                    print('invalid: pacman will be intercepted')
                    return False
                else:
                    #pass
                    print('valid: ghost nearby cannot intercept')
                    
    
        print('MOVE IS REMAING VALID')
        print(' ------------ \n')
        return True


    def _get_best_moves_from_agent(self, possible_moves):
        """ Auxiliary method for MODE.FLIGHT that selects the best moves of given
        Agent (Pursuit, Eating and Counter) according to different criteria

        Args:
        possible_moves: the ordered list of possible_moves of the Agent

        Returns:
        A list with the chosen best moves
        """

        if possible_moves == []:
            return []
        return sorted(possible_moves, key=lambda move: move[1])


    def _try_pursuit(self):
        print('###################################################')
        print('GOT INTO: ' + str(MODE.PURSUIT))
        targets = [ghost[0] for ghost in self.advisor.state['ghosts'] if ghost[1] == True]

        # verify that zombies ghosts are not in the den, if they are, don't pursue
        targets = [ghost for ghost in targets if ghost in self.advisor.map_.pathways[0]]

        if targets != []:
            pursuer = PursuitAgent(self.advisor, targets)
            self.pursuer_possible_moves = pursuer.pursue()
            valid_next_move = self._analyse_best_move(self.pursuer_possible_moves)
            if valid_next_move:
                print('PURSUIT MODE IS RETURNING NEXT MOVE: ' + str(self.pursuer_possible_moves[0][0]))
                return self.pursuer_possible_moves[0][0]
        return None

    def _try_eating(self):
        print('###################################################')
        print('GOT INTO: ' + str(MODE.EATING))
        targets = self.advisor.state['energy'] + self.advisor.state['boost']
        if targets != []:
            eater = EatingAgent(self.advisor, targets)
            self.eater_possible_moves = eater.eat()
            valid_next_move = self._analyse_best_move(self.eater_possible_moves)
            if valid_next_move:
                print('EATING MODE IS RETURNING NEXT MOVE: ' + str(self.eater_possible_moves[0][0]))
                return self.eater_possible_moves[0][0]
        return None
    
    def _try_counter(self):
        print('###################################################')
        print('GOT INTO: ' + str(MODE.COUNTER))
        targets = self.advisor.state['boost']
        # Pac-Man can only counter if there are boost targets
        if targets != []:
            counter = CounterAgent(self.advisor, targets)
            self.counter_possible_moves = counter.counter()
            valid_next_move = self._analyse_best_move(self.counter_possible_moves)
            if valid_next_move:
                print('COUNTER MODE IS RETURNING NEXT MOVE: ' + str(self.counter_possible_moves[0][0]))
                return self.counter_possible_moves[0][0]
        return None
        
    def _try_flight(self, avoid_suggestion=False):
        print('###################################################')
        print('GOT INTO: ' + str(MODE.FLIGHT))



        # get best move from every agent
        pursuer_best_moves = self._get_best_moves_from_agent(self.pursuer_possible_moves)
        pursuer_best_moves = sorted(pursuer_best_moves, key=lambda move: move[1])
        eater_best_moves = self._get_best_moves_from_agent(self.eater_possible_moves)
        eater_best_moves = sorted(eater_best_moves, key=lambda move: move[1])
        counter_best_moves = self._get_best_moves_from_agent(self.counter_possible_moves)
        counter_best_moves = sorted(counter_best_moves, key=lambda move: move[1])

        best_moves = []
        best_moves += self._get_best_moves_from_agent(counter_best_moves)
        best_moves += self._get_best_moves_from_agent(pursuer_best_moves)
        
        for move in best_moves:

            #print('ANALYST: best_moves is: ')
            #print('-> move: ' + str(m[2][0].coordinates[0]) + ' at cost ' + str(m[1]))

            # flee to a safe corridor (if possible, one in a best_move path)
            targets = [(move[2][0].coordinates[0], move[2][-2])]
            
            #print('Flight targets: ' + str(targets))
            
            fleer = FlightAgent(self.advisor, targets)
            next_move = fleer.flee()

            #print('--> move: ' + str(m[2][-1].coordinates[0]) + ' at cost ' + str(m[1]) + ' path starts with ' + str(m[2][-2]))
            print('in flight mode, analysing move: ' + str(move[2][0].coordinates[0]))
            valid_next_move = self._analyse_best_move(possible_moves=next_move, flight=True)
            if valid_next_move:
                print('FLIGHT MODE IS RETURNING NEXT MOVE: ' + str(next_move[0][0]))
                return next_move[0][0]

 
        best_moves = self._get_best_moves_from_agent(eater_best_moves)

        for move in best_moves:

            # define which corridor flight_mode will avoid
            sub_corr0, sub_corr1 = self.advisor.pacman_info.corridor.sub_corridors(self.advisor.pacman_info.position)
            path_coords = [c for corr in move[2] for c in corr.coordinates]
            print('FLIGHT: sub_corr0: ' + str(sub_corr0))
            print('FLIGHT: sub_corr1: ' + str(sub_corr1))
            print('FLIGHT: path_coords: ' + str(path_coords))
            avoid_corridor = []
            # TODO ele 'as vezes nao entra em nenhum dos ifs...
            if all([c in path_coords for c in sub_corr0.coordinates]):
                print('GOT IN IF 1')
                if avoid_suggestion:
                    print('GOT IN IF 1.1')
                    avoid_corridor = sub_corr0
                else:
                    print('GOT IN IF 1.2')
                    avoid_corridor = sub_corr1    
            elif all([c in path_coords for c in sub_corr1.coordinates]):
                print('GOT IN IF 2')
                if avoid_suggestion:
                    print('GOT IN IF 2.1')
                    avoid_corridor = sub_corr1
                else:
                    print('GOT IN IF 2.2')
                    avoid_corridor = sub_corr0

            #print('ANALYST: best_moves is: ')
            #print('-> move: ' + str(m[2][0].coordinates[0]) + ' at cost ' + str(m[1]))

            # flee to a safe corridor (if possible, one in a best_move path)
            targets = [(move[2][0].coordinates[0], avoid_corridor)]
            
            #print('Flight targets: ' + str(targets))
            
            fleer = FlightAgent(self.advisor, targets)
            next_move = fleer.flee()

            #print('--> move: ' + str(m[2][-1].coordinates[0]) + ' at cost ' + str(m[1]) + ' path starts with ' + str(m[2][-2]))
            print('in flight mode, analysing move: ' + str(move[2][0].coordinates[0]))
            valid_next_move = self._analyse_best_move(possible_moves=next_move, flight=True)
            if valid_next_move:
                print('FLIGHT MODE IS RETURNING NEXT MOVE: ' + str(next_move[0][0]))
                return next_move[0][0]

        return None
    
    def _panic(self):
        print('###################################################')
        print('GOT INTO: ' + str(MODE.PANIC))

        panicker = PanicAgent(self.advisor)
        next_move = panicker.panic()
        print('PANIC MODE IS RETURNING NEXT MOVE: ' + str(next_move))
        return next_move
    