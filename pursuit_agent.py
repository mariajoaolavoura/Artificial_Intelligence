from tree_search import *
from pathways import Pathways


class PursuitAgent:

    def __init__(self, advisor, state, targets):
        self.advisor = advisor
        self.state = state
        self.targets = targets


    def pursuit(self, advisor, state):
        """Calculates the next position of the next move, when in pursuit mode.
        In Counter Mode, Pac-Man is must focus on eating zombie ghosts.
        
        Args:
        advisor
        state

        Returns:
        The [x,y] position of the next_move
        """
        
        zombie_ghosts = [ghost for ghost in state['ghosts'] if ghost[1]]    #only get the positions
        possible_moves   = []

        # call eating agent for zombies not in den
        for ghost in zombie_ghosts:
            for corr in self.map_.corridors:
                if ghost[0] in corr.coordinates:
                    possible_moves += self.eating_agent(advisor, state, [ghost[0]])[0]
                    break


    #--------------------------------------------------------------------------#
    # SORT MOVES BY ZOMBIES TIMEOUT

        f_moves = []
        for move in possible_moves:
            _, cost, path = move
            ghosts = [ghost for ghost in zombie_ghosts if ghost[0] == path[0].coordinates[0]]
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
                

