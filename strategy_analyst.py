from game_consts import *
from pursuit_agent import *
from eating_agent import *
from counter_agent import *
from flight_agent import *
from panic_agent import *
from move_risk_assessor import *
import logging

# logs are written to file advisor.log after the client is closed
# possible messages: debug, info, warning, error, critical 
# how to use: logger.typeOfMessage('message')
logger = logging.getLogger('analyst')
logger_format = '[%(lineno)s - %(funcName)20s() - %(levelname)s]\n %(message)s\n'
#logger_format = '%(levelname)s:\t%(message)' # simpler format

# currently writing over the logger file, change filemode to a to append
logging.basicConfig(format=logger_format, filename='ANALYST.log', filemode='w', level=logging.DEBUG)

# logger
# logs are written to file strategy_advisor.log after the client is closed
# possible messages: debug, info, warning, error, critical 
# how to use: logger.typeOfMessage('message')
logger = setup_logger('strategy_analyst', 'strategy_analyst.log')

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
        self.ghosts_in_pursuit = 0
        self.move_risk_assessor = None
        self.avoid_coordinates = []
    
    def decide(self):
        """ Main method of the StartegyAnalyst class, which accomplishes the
        class goal

        Returns:
        The next advised position for Pac-Man to go to
        """

        # if there are no ghosts to pursue pacman counters if is surrounded or eats if not
        
        for ghost in self.advisor.ghosts_info:

            #!!!
            px, py = self.advisor.pacman_info.position
            gx, gy = ghost.position
            
            heuristics = []
            internal_heuristic = abs(gx-px) + abs(gy-py)
            heuristics += [internal_heuristic]
            hor_tunnel_heuristic = self.advisor.map_.map_.hor_tiles - abs(gx-px) + abs(gy-py) if self.advisor.map_.hor_tunnel_exists else None
            heuristics += [hor_tunnel_heuristic]
            ver_tunnel_heuristic = abs(gx-px) + self.advisor.map_.map_.ver_tiles - abs(gy-py) if self.advisor.map_.ver_tunnel_exists else None
            heuristics += [ver_tunnel_heuristic]
            heuristics = [heur for heur in heuristics if heur != None]
            ghost_manhattam_dist_to_pacman = min(heuristics)
            #!!!

            if ghost_manhattam_dist_to_pacman <= SAFE_DIST_TO_GHOST:
                self.ghosts_in_pursuit += 1

        self.move_risk_assessor = MoveRiskAssessor(self.advisor, self.ghosts_in_pursuit)


        # always tries to pursue ghosts first
        next_move = self._try_pursuit()
        if next_move != None:
            return next_move

        # counter (if not possible, try eating)
        if self.ghosts_in_pursuit >= NUMBER_OF_GHOST_TO_OFFENSIVE:
            
            next_move = self._try_counter(surrounded_counter=True)
            if next_move != None:
                return next_move
        
            next_move = self._try_eating(surrounded_eating=True)
            if next_move != None:
                return next_move

            next_move = self._try_flight(avoid_suggestion=False)
            if next_move != None:
                return next_move
        
        # eat (if not possible, try counter)
        else:
            next_move = self._try_eating()
            if next_move != None:
                return next_move

            next_move = self._try_counter()
            # if next_move != None:
            #     return next_move
            
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
            valid_next_move = self.move_risk_assessor.analyse_best_move(self.pursuer_possible_moves)
            if valid_next_move:
                print('PURSUIT MODE IS RETURNING NEXT MOVE: ' + str(self.pursuer_possible_moves[0][0]))
                return self.pursuer_possible_moves[0][0]
        return None

    def _try_eating(self, surrounded_eating=False):
        print('###################################################')
        print('GOT INTO: ' + str(MODE.EATING))
        targets = self.advisor.state['energy'] + self.advisor.state['boost']

        if len(self.advisor.state['energy']) > 50:
            if self.ghosts_in_pursuit < NUMBER_OF_GHOST_TO_OFFENSIVE:
                
                remove_coords = []
                for boost in self.advisor.state['boost']:
                    for corr in self.advisor.map_.corridors:
                        if boost in corr.coordinates:
                            remove_coords += corr.coordinates
                targets = [t for t in targets if t not in remove_coords]


        if targets != []:
            eater = EatingAgent(self.advisor, targets)
            self.eater_possible_moves = eater.eat()
            valid_next_move = self.move_risk_assessor.analyse_best_move(self.eater_possible_moves, flight=False, surrounded_eating=surrounded_eating)
            if valid_next_move:
                print('EATING MODE IS RETURNING NEXT MOVE: ' + str(self.eater_possible_moves[0][0]))
                return self.eater_possible_moves[0][0]
        return None
    
    def _try_counter(self, surrounded_counter=False):
        print('###################################################')
        print('GOT INTO: ' + str(MODE.COUNTER))
        targets = self.advisor.state['boost']
        # Pac-Man can only counter if there are boost targets
        if targets != []:
            counter = CounterAgent(self.advisor, targets)
            self.counter_possible_moves = counter.counter()
            valid_next_move = self.move_risk_assessor.analyse_best_move(self.counter_possible_moves, flight=False, surrounded_eating= surrounded_counter, counter=True)
            if valid_next_move:
                print('COUNTER MODE IS RETURNING NEXT MOVE: ' + str(self.counter_possible_moves[0][0]))
                return self.counter_possible_moves[0][0]
        return None
        
    def _try_flight(self, avoid_suggestion=False):
        print('###################################################')
        print('GOT INTO: ' + str(MODE.FLIGHT))

        pacman = self.advisor.pacman_info

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
            # args: target coordinate, coordinate to avoid
            targets = [(move[2][0].coordinates[0], [move[2][-2].get_coord_next_to_end(pacman.position)])]
            
            #print('Flight targets: ' + str(targets))
            
            fleer = FlightAgent(self.advisor, targets)
            next_move = fleer.flee()

            #print('--> move: ' + str(m[2][-1].coordinates[0]) + ' at cost ' + str(m[1]) + ' path starts with ' + str(m[2][-2]))
            print('in flight mode, analysing move: ' + str(move[2][0].coordinates[0]))
            print('FLIGHT: NEXT MOVE ' + str(next_move))
            valid_next_move = self.move_risk_assessor.analyse_best_move(possible_moves=next_move, flight=True)
            if valid_next_move:
                print('FLIGHT MODE IS RETURNING NEXT MOVE: ' + str(next_move[0][0]))
                return next_move[0][0]

 
        best_moves = self._get_best_moves_from_agent(eater_best_moves)

        for move in best_moves:

            # define which corridor flight_mode will avoid
            sub_corr0, sub_corr1 = pacman.corridor.sub_corridors(pacman.position)
            path_coords = [c for corr in move[2] for c in corr.coordinates]
            print('FLIGHT: sub_corr0: ' + str(sub_corr0))
            print('FLIGHT: sub_corr1: ' + str(sub_corr1))
            print('FLIGHT: path_coords: ' + str(path_coords))
            self.avoid_coordinates = []
            avoid = None
            # TODO ele 'as vezes nao entra em nenhum dos ifs...
            if all([c in path_coords for c in sub_corr0.coordinates]):
                print('GOT IN IF 1')
                if avoid_suggestion:
                    print('GOT IN IF 1.1')
                    avoid = sub_corr0.get_coord_next_to_end(pacman.position)
                else:
                    print('GOT IN IF 1.2')
                    avoid = sub_corr1.get_coord_next_to_end(pacman.position)
            elif all([c in path_coords for c in sub_corr1.coordinates]):
                print('GOT IN IF 2')
                if avoid_suggestion:
                    print('GOT IN IF 2.1')
                    avoid = sub_corr1.get_coord_next_to_end(pacman.position)
                else:
                    print('GOT IN IF 2.2')
                    avoid = sub_corr0.get_coord_next_to_end(pacman.position)
            
            if avoid == None:
                for corr in self.advisor.map_.corridors:
                    if corr != pacman.corridor:
                        if pacman.position in corr.ends:
                            av = corr.get_coord_next_to_end(pacman.position)
                            if av != None:
                                self.avoid_coordinates += [av]
            else:
               self.avoid_coordinates += [avoid]

            # flee to a safe corridor (if possible, one in a best_move path)
            targets = [(move[2][0].coordinates[0], self.avoid_coordinates)]
            
            #print('Flight targets: ' + str(targets))
            
            fleer = FlightAgent(self.advisor, targets)
            next_move = fleer.flee()

            #print('--> move: ' + str(m[2][-1].coordinates[0]) + ' at cost ' + str(m[1]) + ' path starts with ' + str(m[2][-2]))
            print('in flight mode, analysing move: ' + str(move[2][0].coordinates[0]))
            print('FLIGHT: NEXT MOVE ' + str(next_move))
            valid_next_move = self.move_risk_assessor.analyse_best_move(possible_moves=next_move, flight=True)
            if valid_next_move:
                print('FLIGHT MODE IS RETURNING NEXT MOVE: ' + str(next_move[0][0]))
                return next_move[0][0]

        return None
    
    def _panic(self):
        print('###################################################')
        print('GOT INTO: ' + str(MODE.PANIC))

        panicker = PanicAgent(self.advisor)
        # ignore one previously verified bad move (not possible to block more than one)
        next_move = panicker.panic([])
        print('PANIC MODE IS RETURNING NEXT MOVE: ' + str(next_move))
        return next_move
    