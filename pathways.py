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
            
            if (corr1 == corridor):
                #verify if there is an energy in the next corridor
                if any(([x,y] in self.targets) for [x,y] in [c for c in corr2.coordinates if c not in corr1.ends]):
                    pass
                else:
                    actlist += [(corr1, corr2)]


            elif (corr2 == corridor):
                #verify if there is an energy in the next corridor
                if any(([x,y] in self.targets) for [x,y] in [c for c in corr1.coordinates if c not in corr2.ends]):
                    pass
                else:
                    actlist += [(corr2, corr1)]

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