from tree_search import SearchDomain
from corridor import Corridor
import math

class Pathways(SearchDomain):

    def __init__(self, adjacencies, energies):
        self.adjacencies = adjacencies
        self.energies = energies

    def actions(self,corridor):
        actlist = []
        for (corr1, corr2) in self.adjacencies:
            
            if (corr1 == corridor):

                #get the same crossroad
                curr_ends = corr1.ends
                next_ends = corr2.ends

                curr_end = [ e for e in curr_ends if e in next_ends][0]

                if corr2.length == 1:
                    pos = 0
                else:
                    if curr_end == next_ends[0]:
                        pos = 1                    
                    else:
                        pos = -2

                #verify if there is an energy in the first position of the next corridor
                if corr2.coordinates[pos] not in self.energies:
                    actlist += [(corr1, corr2)]

            elif (corr2 == corridor):

                #get the same crossroad
                curr_ends = corr2.ends
                next_ends = corr1.ends

                curr_end = [ e for e in curr_ends if e in next_ends][0]

                if corr1.length == 1:
                    pos = 0
                else:
                    if curr_end == next_ends[0]:
                        pos = 1                    
                    else:
                        pos = -2

                #verify if there is an energy in the first position of the next corridor
                if corr1.coordinates[pos] not in self.energies:
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
        return Pathways(self.adjacencies.copy(), self.energies.copy())