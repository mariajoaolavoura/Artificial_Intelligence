from tree_search import SearchDomain
import math

class Pathways(SearchDomain):

    def __init__(self, adjacencies):
        self.adjacencies = adjacencies
        #print("### " + str(self.adjacencies))
        for ((x,y),(a,b)) in adjacencies:
            if (x,y) == (7,15):
                    print(((x,y),(a,b)))
            if (a,b) == (7,15):
                print(((x,y),(a,b)))

    def actions(self,coordinate):
        actlist = []
        for ((x,y),(a,b)) in self.adjacencies:
            if ((x,y) == coordinate):
                actlist += [((x,y),(a,b))]
            elif ((a,b) == coordinate):
                actlist += [((a,b),(x,y))]
        return actlist 

    def result(self,coordinate,action):
        (x,y),(a,b) = action
        if (x,y) == coordinate:
            return (a,b)
        
    def cost(self, cur_pos, action):
        orig, _ = action
        if (orig != cur_pos):
            return None
        return 1

    def heuristic(self, new_state, goal):
        x, y = new_state
        gx, gy = goal
        return math.hypot((gx-x), (gy-y))