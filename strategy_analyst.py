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

    
    def decide(self):
        """ Main method of the StartegyAnalyst class, which accomplishes the
        class goal

        Returns:
        The next advised position for Pac-Man to go to
        """

        pursuer_possible_moves = []
        eater_possible_moves = []
        counter_possible_moves = []
        fleer_possible_moves = []

        # ----- if there are zombie ghost nearby, pursuing them is the priority
        mode = MODE.PURSUIT
        print('###################################################')
        print('GOT INTO: ' + str(mode))
        targets = [ghost[0] for ghost in self.advisor.state['ghosts'] if ghost[1] == True]

        # verify that zombies ghosts are not in the den, if they are, don't pursue
        targets = [ghost for ghost in targets if ghost in self.advisor.map_.pathways[0]]

        if targets != []:
            pursuer = PursuitAgent(self.advisor, targets)
            pursuer_possible_moves = pursuer.pursue()
            valid_next_move = self._analyse_best_move(pursuer_possible_moves)
            if valid_next_move:
                print('PURSUIT MODE IS RETURNING NEXT MOVE: ' + str(pursuer_possible_moves[0][0]))
                return pursuer_possible_moves[0][0]  
        

        # ----- if there are no zombie ghosts, eating energies is the priority
        mode = MODE.EATING
        print('###################################################')
        print('GOT INTO: ' + str(mode))
        targets = self.advisor.state['energy'] + self.advisor.state['boost']
        if targets != []:
            eater = EatingAgent(self.advisor, targets)
            eater_possible_moves = eater.eat()
            valid_next_move = self._analyse_best_move(eater_possible_moves)
            if valid_next_move:
                print('EATING MODE IS RETURNING NEXT MOVE: ' + str(eater_possible_moves[0][0]))
                return eater_possible_moves[0][0]


        # ----- if no path to energies was valid, Pac-Man tries to counter ghost
        mode = MODE.COUNTER
        print('###################################################')
        print('GOT INTO: ' + str(mode))
        targets = self.advisor.state['boost']
        # Pac-Man can only counter if there are boost targets
        if targets != []:
            counter = CounterAgent(self.advisor, targets)
            counter_possible_moves = counter.counter()
            valid_next_move = self._analyse_best_move(counter_possible_moves)
            if valid_next_move:
                print('COUNTER MODE IS RETURNING NEXT MOVE: ' + str(counter_possible_moves[0][0]))
                return counter_possible_moves[0][0]

        
        # ----- if neither eating or counter moves are valid, Pac-Man tries to
        # ----- flee towards a boost or some energy
        mode = MODE.FLIGHT
        print('###################################################')
        print('GOT INTO: ' + str(mode))

        # get best move from every agent
        pursuer_best_moves = self._get_best_moves_from_agent(pursuer_possible_moves)
        pursuer_best_moves = sorted(pursuer_best_moves, key=lambda move: move[1])
        eater_best_moves = self._get_best_moves_from_agent(eater_possible_moves)
        eater_best_moves = sorted(eater_best_moves, key=lambda move: move[1])
        counter_best_moves = self._get_best_moves_from_agent(counter_possible_moves)
        counter_best_moves = sorted(counter_best_moves, key=lambda move: move[1])

        best_moves = []
        best_moves += self._get_best_moves_from_agent(counter_best_moves)
        best_moves += self._get_best_moves_from_agent(pursuer_best_moves)
        best_moves += self._get_best_moves_from_agent(eater_best_moves)
        
        if best_moves != []:
            
            print('ANALYST: best_moves is: ')
            for m in best_moves:
                print('-> move: ' + str(m[2][0].coordinates[0]) + ' at cost ' + str(m[1]))

            # flee to a safe corridor (if possible, one in a best_move path)
            targets = [(move[2][0].coordinates[0], move[2][-2]) for move in best_moves if move != []]
            print('Flight targets: ' + str(targets))
            fleer = FlightAgent(self.advisor, targets)
            fleer_possible_moves = fleer.flee()
            for m in fleer_possible_moves:
                print('-> move: ' + str(m[2][0].coordinates[0]) + ' at cost ' + str(m[1]) + \
                ' path starts with ' + str(m[2][-2]))
            for move in fleer_possible_moves:
                print('in flight mode, analysing move: ' + str(move[2][0].coordinates[0]))
                valid_next_move = self._analyse_best_move([move])
                if valid_next_move:
                    print('FLIGHT MODE IS RETURNING NEXT MOVE: ' + str(move[0]))
                    return move[0]


        # ----- if no strategy flight is possible, just flee to first safe position possible
        mode = MODE.PANIC
        print('###################################################')
        print('GOT INTO: ' + str(mode))

        panicker = PanicAgent(self.advisor)
        next_move = panicker.panic()
        print('PANIC MODE IS RETURNING NEXT MOVE: ' + str(next_move))
        return next_move

        # ----- no agent got a move - this should never happen
        print('NO AGENT GOT A MOVE!!!')
        return None


    def _analyse_best_move(self, possible_moves):
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
        path = move[2]
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
        print('Pac-Man distance to target ' + str(move[2][0].coordinates[0]) + ' is: ' + str(move[1]))
        print('pPac-Man corridor is :' + str(pacman.corridor))
        print('crossroad: ' + str(crossroad))
        print('ghost at crossroad is: ' + str(ghost))
        for g in self.advisor.ghosts_info:
            print(g.print())
        

        # There is no ghost reaching pacman at the crossroad
        if ghost == None:
            print('valid: no ghost')
            return True
        
        # The ghost and pacman are in opposite sides of the target
        print('---> before condition: ' + str(ghost.dist_to_pacman) + ', ' + str(move[1]))
        if ghost.dist_to_pacman == 2 and move[1] == 1 and ghost.position not in path[-2].coordinates:
            print('invalid: the ghost is just after the target')
            return False

        # ghost is in first corridor of path (dangerous)
        print('---> verifying if ghost: ' + str(ghost) + 'is in corridor ' + str(path[-2].coordinates))
        if ghost.position in path[-2].coordinates:
            print('invalid: ghost in the first corridor of path')
            return False

        # pacman is being pursued from behind and there is a ghost in the next corridor of path
        print('---> verify if there is a trap')
        if self.advisor.pacman_info.pursued_from_other_crossroad(crossroad):
            if len(path) >= 3:
                if ghost.position in path[-3].coordinates:
                    print('invalid: ghost pursuing from behind and trap ahead')
                    return False
        
        # TODO interception...
        if self.advisor.pacman_info.pursued_from_crossroad(crossroad):
            if ghost.position not in [c for corr in path for c in corr.coordinates]:
                if ghost.side_interception(path):
                    print('invalid: pacman will be intercepted')
                    return False
                else:
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