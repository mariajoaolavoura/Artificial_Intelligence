from tree_search import *
from pathways import Pathways
from eating_agent import EatingAgent


class PursuitAgent:
    """Creates the Pursuit Agent, which calculates the path to all accessible
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


    def pursue(self):
        """Calculates the next position of the next move, when in pursuit mode.
        In Counter Mode, Pac-Man is must focus on eating zombie ghosts.
        
        Args:
        advisor
        state

        Returns:
        The [x,y] position of the next_move
        """
        
            #only get the positions

        eating_agent = EatingAgent(self.advisor, self.targets)
        possible_moves = eating_agent.eat()

    #--------------------------------------------------------------------------#
    # SORT MOVES BY ZOMBIES TIMEOUT

        f_moves = []
        for move in possible_moves:
            _, cost, path = move
            ghosts = [ghost for ghost in targets if ghost[0] == path[0].coordinates[0]]
            ghost = sorted(ghosts, key=lambda g: g[2])[0]
            if cost > ghost[2] * 2:
                f_moves += [move]
                    
        # sort
        possible_moves = [move for move in possible_moves if move not in f_moves]

    #--------------------------------------------------------------------------#
    # IF THERE ARE NO POSSIBLE MOVES, RETURN NONE

        if possible_moves == []:
            return possible_moves, False
        return possible_moves, True
                

