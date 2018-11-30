from tree_search import *
from pathways import Pathways


class CounterAgent:

    def __init__(self, advisor, state, targets):
        self.advisor = advisor
        self.state = state
        self.targets = targets


    def counter(self, advisor, state, targets):
        """Calculates the next position of the next move, when in counter mode.
        In Counter Mode, Pac-Man is almost surrounded by ghosts and must focus on eating boosts.
        
        Args:
        advisor
        state

        Returns:
        The [x,y] position of the next_move

        Considerations/Strategy:
        -> For each corridor where the boosts are, check for safe ones
        -> From the safest ones, choose the closest (if no one is safe, choose the closest one)
        
        ghost [[9, 15], False, 0],
        """
        boosts = state['boost']
        acessible_boosts = []
        possible_moves   = []
        safeties         = []

        domain = Pathways(self.map_.corr_adjacencies, boosts)

        for boost in boosts:
            
            corridor = None
            for corr in self.map_.corridors:
                if boost in corr.coordinates:
                    corridor = corr

            my_prob = SearchProblem(domain, corridor, boost, advisor.pacman_info.corridor, advisor.pacman_info.position)
            my_tree = SearchTree(my_prob, "a*")
            search_results = my_tree.search()
            
            if search_results != None:
                acessible_boosts += [boost]
                possible_moves += [(search_results[0], search_results[1])]
                safeties         += [search_results[2][len(search_results[2]) - 3].safe]        #safety of two to last corridor

        # print("BOOSTS"   + str(acessible_boosts) + "\n")
        # print("MOVES"    + str(possible_moves)+ "\n")
        # print("SAFETIES" + str(safeties)+ "\n")
        
    #-------------------------------------------------------------------------#
    # SORT MOVES BY COST
        possible_moves = sorted(possible_moves,key=lambda res: res[1])



        other_choices = []
        blocked = True

        if len([safety for safety in safeties if safety == CORRIDOR_SAFETY.SAFE]) > 1: #if any corridor is safe
            blocked = False
            #remove unsafe corridors info
            for i in range(0, len(acessible_boosts)):
                if safeties[i] == CORRIDOR_SAFETY.UNSAFE:
                    other_choices += possible_moves[i]
                    
                    del safeties[i]
                    del acessible_boosts[i]
                    del possible_moves[i]        

        # should not be on this mode (no more boosts)
        if (len(possible_moves) == 0):
            return possible_moves, False
        
        # choose the closest boost 
        # either there are several boosts in a safe corridor 
        # OR there are only boosts in unsafe corridors)
        
        possible_moves = sorted(possible_moves,key=lambda elem: elem[1])
        other_choices += [possible_move[0] for possible_move in possible_moves[1:]]
        #response = ModeResponse(possible_moves[0][0], other_choices, blocked)
        #print(response)
        return possible_moves, True
