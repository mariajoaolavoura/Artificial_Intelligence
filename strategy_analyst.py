from game_consts import *
from eating_agent import *
from pursuit_agent import *
from counter_agent import *
from flight_agent import *

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

        targets = [ghost[0] for ghost in self.advisor.state['ghosts'] if ghost[1] == True]

        # verify that zombies ghosts are not in the den, if they are, don't pursue
        targets = [ghost for ghost in targets if ghost in self.advisor.map_.pathways[0]]

        if targets != []:
            pursuer = PursuitAgent(self.advisor, targets)
            pursuer_possible_moves = pursuer.pursue()
            valid_next_move = self._analyse_best_move(pursuer_possible_moves)
            if valid_next_move:
                print('valid move from : ' + str(mode))
                return pursuer_possible_moves[0][0]  
        

        # ----- if there are no zombie ghosts, eating energies is the priority
        mode = MODE.EATING

        targets = self.advisor.state['energy'] + self.advisor.state['boost']
        if targets != []:
            eater = EatingAgent(self.advisor, targets)
            eater_possible_moves = eater.eat()
            valid_next_move = self._analyse_best_move(eater_possible_moves)
            if valid_next_move:
                return eater_possible_moves[0][0]


        # ----- if no path to energies was valid, Pac-Man tries to counter ghost
        mode = MODE.COUNTER
        print('GOT INTO: ' + str(mode))
        targets = self.advisor.state['boost']
        # Pac-Man can only counter if there are boost targets
        if targets != []:
            counter = CounterAgent(self.advisor, targets)
            counter_possible_moves = counter.counter()
            valid_next_move = self._analyse_best_move(counter_possible_moves)
            if valid_next_move:
                print('valid move from: ' + str(mode))
                return counter_possible_moves[0][0]


        # if neither eating or counter moves are valid, Pac-Man must flee
        mode = MODE.FLIGHT
        print('GOT INTO: ' + str(mode))
        # get best move from every agent
        pursuer_best_moves = self._get_best_moves_from_agent(pursuer_possible_moves)
        eater_best_moves = self._get_best_moves_from_agent(eater_possible_moves)
        counter_best_moves = self._get_best_moves_from_agent(counter_possible_moves)
        #best_moves = pursuer_best_moves + eater_best_moves + counter_best_moves
        
        best_moves = []
        best_moves += self._get_best_moves_from_agent(counter_best_moves)
        best_moves += self._get_best_moves_from_agent(pursuer_best_moves)
        best_moves += self._get_best_moves_from_agent(eater_best_moves)

        if best_moves != []:
            
            # sort best moves by cost
            # best_moves = sorted(best_moves,key=lambda res: res[1])

            # flee to a safe corridor (if possible, one in a best_move path)
            fleer = FlightAgent(self.advisor, targets)
            next_move = fleer.flee()

            # flight agent is a last resort, and its advice is final
            print(mode)
            print()
            print(self.advisor.pacman_info)
            for ghost in self.advisor.ghosts_info:
                print(ghost.print())
            print('FLIGHT MODE IS RETURNING NEXT MOVE: ' + str(next_move))
            return next_move

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

        for move in possible_moves:
            path = move[2]
            pacman = self.advisor.pacman_info
            ghost = None
            # print()
            # print(pacman)
            # print(' ------------ \n')
            # for ghost in self.advisor.ghosts_info:
            #     print(ghost.print())

            # verify which crossroad is in the path
            crossroad = None
            semaphore = None
            if any([c == pacman.crossroad0 for corr in path for c in corr.coordinates]):
                crossroad = pacman.crossroad0
                semaphore = pacman.semaphore0
                ghost = pacman.ghost_at_crossroad0
            elif any([c == pacman.crossroad1 for corr in path for c in corr.coordinates]):
                crossroad = pacman.crossroad1
                semaphore = pacman.semaphore1
                ghost = pacman.ghost_at_crossroad1

            if ghost == None:
                print('valid: no ghost')
                return True
            
            # if semaphore == SEMAPHORE.GREEN:
            #     print('valid: semaphore is green')
            #     return True
             
            if ghost.position not in [c for corr in path for c in corr.coordinates]:
                if not ghost.side_interception(path):
                    print('valid: ghost nearby cannot intercept')
                    return True
        
        print('MOVE IS NOT VALID')
        return False


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
        return possible_moves[0]