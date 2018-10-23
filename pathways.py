from tree_search import *
import math

class Pathways(SearchDomain):

    def __init__(self, adjacencies):
        self.adjacencies = adjacencies

    def actions(self,coordinate):
        actlist = []
        for ((x,y),(a,b)) in self.adjacencies:
            if ((x,y) == coordinate):
                actlist += [((x,y),(a,b))]
            elif ((a,b) == coordinate):
                actlist += [((a,b),(x,y))]
        return actlist 

    def result(self,coordinate,action):
        ((x,y),(a,b)) = action
        if (x,y) == coordinate:
            return (a,b)
        
    def cost(self, cur_pos, action):
        (orig, dest) = action
        if (orig != cur_pos):
            return None
        
        for (c1,c2) in self.adjacencies:
            if (orig == c1 and dest == c2) or\
            (orig == c2 and dest == c1):
                return 1
        
        return None

    def heuristic(self, cur, goal):
        cur_x, cur_y = cur
        g_x, g_y = goal
        return math.hypot((g_x-cur_x), (g_y-cur_y))