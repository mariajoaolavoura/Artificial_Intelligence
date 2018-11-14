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
        corr1, _ = action
        if (corr1 != cur_corr):
            return None
        return corr1.length


    # TODO
    def heuristic(self, new_state, goal):
        x, y = new_state
        gx, gy = goal
        return math.hypot((gx-x), (gy-y))