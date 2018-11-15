from tree_search import SearchDomain
from student import Corridor
import math

class Pathways(SearchDomain):

    def __init__(self, adjacencies):
        self.adjacencies = adjacencies

    def actions(self,corridor):
        actlist = []
        for (corr1, corr2) in self.adjacencies:
            if (corr1 == corridor):
                actlist += [(corr1, corr2)]
            elif (corr2 == corridor):
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


    # TODO
    def heuristic(self, curr_state, new_state, goal):
        c_ends = curr_state.ends
        n_ends = new_state.ends

        c_end = [ e for e in c_ends if e in n_ends]

        if c_end == n_ends[0]:
            x, y = n_ends[1]
            gx, gy = goal.ends[0]
        else:
            x, y = n_ends[0]
            gx, gy = goal.ends[0]
            
        return abs(gx-x) + abs(gy-y)