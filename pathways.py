from tree_search import SearchDomain
from corridor import Corridor
import math

class Pathways(SearchDomain):

    def __init__(self, adjacencies, targets):
        self.adjacencies = adjacencies
        self.targets = targets

    def actions(self,corridor):
        actlist = []
        #print(self.targets)
        for (corr1, corr2) in self.adjacencies:
            
            if (corr1.coordinates == corridor.coordinates):
                actlist += [(corr1, corr2)]

            elif (corr2.coordinates == corridor.coordinates):
                actlist += [(corr2, corr1)]

        if corridor.length == 0: #is the initial or final corridor
            surrounded = []
            for (corr1, corr2) in actlist:
                if corr2.get_coord_next_to_end(corridor.coordinates[0]) in self.targets:
                    surrounded += [True]
                else:
                    surrounded += [False]
            
            if all(surrounded):
                actlist = []

        return actlist

    def result(self,corridor,action):
        corr1, corr2 = action
        if corr1 == corridor:
            return corr2
 
    def cost(self, cur_corr, action):
        corr1, corr2 = action
        if (corr1 != cur_corr):
            return None
        return corr2.length


    def heuristic(self, curr_state, new_state, goal):
        c_ends = curr_state.ends
        n_ends = new_state.ends

        c_end = [ e for e in c_ends if e in n_ends][0]

        if c_end == n_ends[0]:
            x, y = n_ends[1]
            gx, gy = goal.ends[0]
        else:
            x, y = n_ends[0]
            gx, gy = goal.ends[0]
            
        return abs(gx-x) + abs(gy-y)

    def copy(self):
        return Pathways(self.adjacencies.copy(), self.targets.copy())