from abc import ABC, abstractmethod
import math
# DOMAIN ----------------------------------------------------------------------
# -----------------------------------------------------------------------------

# Dominios de pesquisa. Permitem calcular as accoes possiveis em cada estado
class SearchDomain(ABC):

    # construtor
    @abstractmethod
    def __init__(self):
        pass

    # lista de accoes possiveis num estado
    @abstractmethod
    def actions(self, state):
        pass

    # resultado de uma accao num estado, ou seja, o estado seguinte
    @abstractmethod
    def result(self, state, action):
        pass

    # custo de uma accao num estado
    @abstractmethod
    def cost(self, state, action):
        pass

    # custo estimado de chegar de um estado a outro
    @abstractmethod
    def heuristic(self, state, goal_state):
        pass


# PROBLEM ---------------------------------------------------------------------
# -----------------------------------------------------------------------------
# Problemas concretos a resolver dentro de um determinado dominio
class SearchProblem:
    
    def __init__(self, domain, initial, goal):
        self.domain = domain
        self.initial = initial
        self.goal = goal
    
    def goal_test(self, state):
        return state == self.goal


# NODE ------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# Nos de uma arvore de pesquisa
class SearchNode:
    
    def __init__(self, state, parent, cost, heuristic): 
        self.state = state
        self.parent = parent
        self.cost = cost
        self.heuristic = heuristic
        
    def inParent(self, state):
        if self.parent == None:
            return False
        if self.parent.state == state:
            return True
        return self.parent.inParent(state)
    
    def __str__(self):
        return "no(" + str(self.state) +  ")" # "," + str(self.parent) +
    
    def __repr__(self):
        return str(self)



# TREE ------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# Arvores de pesquisa
class SearchTree:

    # construtor
    def __init__(self,problem, strategy='breadth'): 
        self.problem = problem
        heur = self.problem.domain.heuristic(problem.initial, self.problem.goal)
        root = SearchNode(problem.initial, parent=None, cost=0, heuristic=heur)
        self.open_nodes = [root]
        self.strategy = strategy
        self.cost = None

    # obter o caminho (sequencia de estados) da raiz ate um no
    def get_path(self,node):
        if node.parent == None:
            return [node.state]
        path = self.get_path(node.parent)
        path += [node.state]
        return(path)

    # procurar a solucao
    def search(self, limit=None):
        while self.open_nodes != []:

            node = self.open_nodes.pop(0)

            if self.problem.goal_test(node.state):
                self.cost = node.cost
                if node.parent == None:
                    return self.get_path(node), node.state
                return self.get_path(node), node.parent.state

            lnewnodes = []
            #print(self.open_nodes)

            for action in self.problem.domain.actions(node.state):
                # calculate next state
                newstate = self.problem.domain.result(node.state,action)
                # calculate cost of next node
                cost = node.cost + self.problem.domain.cost(node.state, action)
                # calculate heuristic of next node
                heuristic = self.problem.domain.heuristic(newstate, self.problem.goal)
                # create new node
                newnode = SearchNode(newstate,node,cost,heuristic)
                # add new node to list of new nodes
                lnewnodes += [newnode]

            #self.add_to_open(newNode for newNode in lnewnodes if not node.inParent(newNode.state))
            lista = []
            for newNode in lnewnodes:
                if not node.inParent(newNode.state):
                    lista += [newNode]
                    #print(newNode)
            self.add_to_open(lista)
        return None

    # juntar novos nos a lista de nos abertos de acordo com a estrategia
    def add_to_open(self,lnewnodes):
        if self.strategy == 'a*':
            self.open_nodes.extend(lnewnodes)
            self.open_nodes = sorted(self.open_nodes, key=lambda node: node.heuristic + node.cost)



class Pathways(SearchDomain):

    def __init__(self, adjacencies):
        self.adjacencies = adjacencies
        #print(self.adjacencies)

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
        return 1

    def heuristic(self, new_state, goal):
        x, y = new_state
        gx, gy = goal
        return math.hypot((gx-x), (gy-y))





# map = []
# length = 10
# for i in range(length):
#     map += [(i,j) for j in range(length)]

# domain = []
# for (x,y) in map:
#     domain += [ ((x,y),(a,b)) for (a,b) in map \
#                         if ((a == x+1 and b == y) \
#                         or (a == x-1 and b == y) \
#                         or (b == y+1 and a == x) \
#                         or (b == y-1 and a == x)) \
#                         and not domain.__contains__(((a,b),(x,y)))]


# domain = [((0, 15), (1, 15)), ((0, 15), (18, 15)), ((1, 1), (1, 2)), ((1, 1), (2, 1)), ((1, 2), (1, 3)), ((1, 3), (1, 4)), ((1, 4), (2, 4)), ((1, 7), (1, 8)), ((1, 7), (2, 7)), ((1, 8), (1, 9)), ((1, 9), (1, 10)), ((1, 10), (2, 10)), ((1, 15), (2, 15)), ((1, 20), (1, 21)), ((1, 20), (2, 20)), ((1, 21), (1, 22)), ((1, 22), (1, 23)), ((1, 23), (2, 23)), ((1, 26), (1, 27)), ((1, 26), (2, 26)), ((1, 27), (1, 28)), ((1, 28), (1, 29)), ((1, 29), (2, 29)), ((2, 1), (3, 1)), ((2, 4), (2, 5)), ((2, 4), (3, 4)), ((2, 5), (2, 6)), ((2, 6), (2, 7)), ((2, 10), (3, 10)), ((2, 15), (3, 15)), ((2, 20), (3, 20)), ((2, 23), (2, 24)), ((2, 24), (2, 25)), ((2, 25), (2, 26)), ((2, 26), (3, 26)), ((2, 29), (3, 29)), ((3, 1), (4, 1)), ((3, 4), (4, 4)), ((3, 10), (4, 10)), ((3, 15), (4, 15)), ((3, 20), (4, 20)), ((3, 26), (4, 26)), ((3, 29), (4, 29)), ((4, 1), (5, 1)), ((4, 4), (4, 5)), ((4, 5), (4, 6)), ((4, 6), (4, 7)), ((4, 7), (4, 8)), ((4, 7), (5, 7)), ((4, 8), (4, 9)), ((4, 9), (4, 10)), ((4, 10), (4, 11)), ((4, 10), (5, 10)), ((4, 11), (4, 12)), ((4, 12), (4, 13)), ((4, 13), (4, 14)), ((4, 14), (4, 15)), ((4, 15), (4, 16)), ((4, 15), (5, 15)), ((4, 16), (4, 17)), ((4, 17), (4, 18)), ((4, 18), (4, 19)), ((4, 19), (4, 20)), ((4, 20), (4, 21)), ((4, 20), (5, 20)), ((4, 21), (4, 22)), ((4, 22), (4, 23)), ((4, 23), (4, 24)), ((4, 23), (5, 23)), ((4, 24), (4, 25)), ((4, 25), (4, 26)), ((4, 29), (5, 29)), ((5, 1), (6, 1)), ((5, 7), (6, 7)), ((5, 10), (6, 10)), ((5, 15), (6, 15)), ((5, 20), (6, 20)), ((5, 23), (6, 23)), ((5, 29), (6, 29)), ((6, 1), (7, 1)), ((6, 4), (6, 5)), ((6, 4), (7, 4)), ((6, 5), (6, 6)), ((6, 6), (6, 7)), ((6, 7), (7, 7)), ((6, 10), (6, 11)), ((6, 10), (7, 10)), ((6, 11), (6, 12)), ((6, 12), (6, 13)), ((6, 12), (7, 12)), ((6, 13), (6, 14)), ((6, 14), (6, 15)), ((6, 15), (6, 16)), ((6, 15), (7, 15)), ((6, 16), (6, 17)), ((6, 17), (6, 18)), ((6, 18), (6, 19)), ((6, 18), (7, 18)), ((6, 19), (6, 20)), ((6, 20), (7, 20)), ((6, 23), (6, 24)), ((6, 23), (7, 23)), ((6, 24), (6, 25)), ((6, 25), (6, 26)), ((6, 26), (7, 26)), ((6, 29), (7, 29)), ((7, 1), (8, 1)), ((7, 4), (8, 4)), ((7, 7), (8, 7)), ((7, 10), (8, 10)), ((7, 12), (8, 12)), ((7, 15), (8, 15)), ((7, 18), (8, 18)), ((7, 20), (8, 20)), ((7, 23), (8, 23)), ((7, 26), (8, 26)), ((7, 29), (8, 29)), ((8, 1), (8, 2)), ((8, 1), (9, 1)), ((8, 2), (8, 3)), ((8, 3), (8, 4)), ((8, 7), (8, 8)), ((8, 7), (9, 7)), ((8, 8), (8, 9)), ((8, 9), (8, 10)), ((8, 12), (9, 12)), ((8, 14), (8, 15)), ((8, 14), (9, 14)), ((8, 15), (8, 16)), ((8, 15), (9, 15)), ((8, 16), (9, 16)), ((8, 18), (9, 18)), ((8, 20), (8, 21)), ((8, 21), (8, 22)), ((8, 22), (8, 23)), ((8, 23), (9, 23)), ((8, 26), (8, 27)), ((8, 27), (8, 28)), ((8, 28), (8, 29)), ((8, 29), (9, 29)), ((9, 1), (10, 1)), ((9, 7), (10, 7)), ((9, 12), (10, 12)), ((9, 14), (9, 15)), ((9, 14), (10, 14)), ((9, 15), (9, 16)), ((9, 15), (10, 15)), ((9, 16), (10, 16)), ((9, 18), (10, 18)), ((9, 23), (10, 23)), ((9, 29), (10, 29)), ((10, 1), (10, 2)), ((10, 1), (11, 1)), ((10, 2), (10, 3)), ((10, 3), (10, 4)), ((10, 4), (11, 4)), ((10, 7), (10, 8)), ((10, 7), (11, 7)), ((10, 8), (10, 9)), ((10, 9), (10, 10)), ((10, 10), (11, 10)), ((10, 12), (11, 12)), ((10, 14), (10, 15)), ((10, 15), (10, 16)), ((10, 18), (11, 18)), ((10, 20), (10, 21)), ((10, 20), (11, 20)), ((10, 21), (10, 22)), ((10, 22), (10, 23)), ((10, 23), (11, 23)), ((10, 26), (10, 27)), ((10, 26), (11, 26)), ((10, 27), (10, 28)), ((10, 28), (10, 29)), ((10, 29), (11, 29)), ((11, 1), (12, 1)), ((11, 4), (12, 4)), ((11, 7), (12, 7)), ((11, 10), (12, 10)), ((11, 12), (12, 12)), ((11, 18), (12, 18)), ((11, 20), (12, 20)), ((11, 23), (12, 23)), ((11, 26), (12, 26)), ((11, 29), (12, 29)), ((12, 1), (13, 1)), ((12, 4), (12, 5)), ((12, 5), (12, 6)), ((12, 6), (12, 7)), ((12, 7), (13, 7)), ((12, 10), (12, 11)), ((12, 10), (13, 10)), ((12, 11), (12, 12)), ((12, 12), (12, 13)), ((12, 13), (12, 14)), ((12, 14), (12, 15)), ((12, 15), (12, 16)), ((12, 15), (13, 15)), ((12, 16), (12, 17)), ((12, 17), (12, 18)), ((12, 18), (12, 19)), ((12, 19), (12, 20)), ((12, 20), (13, 20)), ((12, 23), (12, 24)), ((12, 23), (13, 23)), ((12, 24), (12, 25)), ((12, 25), (12, 26)), ((12, 29), (13, 29)), ((13, 1), (14, 1)), ((13, 7), (14, 7)), ((13, 10), (14, 10)), ((13, 15), (14, 15)), ((13, 20), (14, 20)), ((13, 23), (14, 23)), ((13, 29), (14, 29)), ((14, 1), (15, 1)), ((14, 4), (14, 5)), ((14, 4), (15, 4)), ((14, 5), (14, 6)), ((14, 6), (14, 7)), ((14, 7), (14, 8)), ((14, 8), (14, 9)), ((14, 9), (14, 10)), ((14, 10), (14, 11)), ((14, 10), (15, 10)), ((14, 11), (14, 12)), ((14, 12), (14, 13)), ((14, 13), (14, 14)), ((14, 14), (14, 15)), ((14, 15), (14, 16)), ((14, 15), (15, 15)), ((14, 16), (14, 17)), ((14, 17), (14, 18)), ((14, 18), (14, 19)), ((14, 19), (14, 20)), ((14, 20), (14, 21)), ((14, 20), (15, 20)), ((14, 21), (14, 22)), ((14, 22), (14, 23)), ((14, 23), (14, 24)), ((14, 24), (14, 25)), ((14, 25), (14, 26)), ((14, 26), (15, 26)), ((14, 29), (15, 29)), ((15, 1), (16, 1)), ((15, 4), (16, 4)), ((15, 10), (16, 10)), ((15, 15), (16, 15)), ((15, 20), (16, 20)), ((15, 26), (16, 26)), ((15, 29), (16, 29)), ((16, 1), (17, 1)), ((16, 4), (16, 5)), ((16, 4), (17, 4)), ((16, 5), (16, 6)), ((16, 6), (16, 7)), ((16, 7), (17, 7)), ((16, 10), (17, 10)), ((16, 15), (17, 15)), ((16, 20), (17, 20)), ((16, 23), (16, 24)), ((16, 23), (17, 23)), ((16, 24), (16, 25)), ((16, 25), (16, 26)), ((16, 26), (17, 26)), ((16, 29), (17, 29)), ((17, 1), (17, 2)), ((17, 2), (17, 3)), ((17, 3), (17, 4)), ((17, 7), (17, 8)), ((17, 8), (17, 9)), ((17, 9), (17, 10)), ((17, 15), (18, 15)), ((17, 20), (17, 21)), ((17, 21), (17, 22)), ((17, 22), (17, 23)), ((17, 26), (17, 27)), ((17, 27), (17, 28)), ((17, 28), (17, 29))]
# energy = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 7), (1, 8), (1, 9), (1, 10), (1, 20), (1, 21), (1, 23), (1, 26), (1, 27), (1, 28), (1, 29), (2, 1), (2, 4), (2, 5), (2, 7), (2, 10), (2, 20), (2, 23), (2, 24), (2, 25), (2, 26), (2, 29), (3, 1), (3, 4), (3, 10), (3, 20), (3, 26), (3, 29), (4, 1), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8), (4, 9), (4, 10), (4, 11), (4, 12), (4, 13), (4, 14), (4, 15), (4, 16), (4, 17), (4, 18), (4, 19), (4, 20), (4, 21), (4, 22), (4, 23), (4, 24), (4, 25), (4, 26), (4, 29), (5, 1), (5, 7), (5, 10), (5, 20), (5, 23), (5, 29), (6, 1), (6, 4), (6, 5), (6, 6), (6, 7), (6, 10), (6, 20), (6, 23), (6, 24), (6, 25), (6, 26), (6, 29), (7, 1), (7, 4), (7, 7), (7, 10), (7, 20), (7, 23), (7, 26), (7, 29), (8, 1), (8, 2), (8, 3), (8, 4), (8, 7), (8, 8), (8, 9), (8, 10), (8, 20), (8, 21), (8, 22), (8, 23), (8, 26), (8, 27), (8, 28), (8, 29), (9, 1), (9, 7), (9, 23), (9, 29), (10, 1), (10, 2), (10, 3), (10, 4), (10, 7), (10, 8), (10, 9), (10, 10), (10, 20), (10, 21), (10, 22), (10, 23), (10, 26), (10, 27), (10, 28), (10, 29), (11, 1), (11, 4), (11, 7), (11, 10), (11, 20), (11, 23), (11, 26), (11, 29), (12, 1), (12, 4), (12, 5), (12, 6), (12, 7), (12, 10), (12, 20), (12, 23), (12, 24), (12, 25), (12, 26), (12, 29), (13, 1), (13, 7), (13, 10), (13, 20), (13, 23), (13, 29), (14, 1), (14, 4), (14, 5), (14, 6), (14, 7), (14, 8), (14, 9), (14, 10), (14, 11), (14, 12), (14, 13), (14, 14), (14, 15), (14, 16), (14, 17), (14, 18), (14, 19), (14, 20), (14, 21), (14, 22), (14, 23), (14, 24), (14, 25), (14, 26), (14, 29), (15, 1), (15, 4), (15, 10), (15, 20), (15, 26), (15, 29), (16, 1), (16, 4), (16, 5), (16, 7), (16, 10), (16, 20), (16, 23), (16, 24), (16, 25), (16, 26), (16, 29), (17, 1), (17, 2), (17, 3), (17, 4), (17, 7), (17, 8), (17, 9), (17, 10), (17, 20), (17, 21), (17, 23), (17, 26), (17, 27), (17, 28), (17, 29)]
# for (x,y) in energy:
#     init_pos = (x,y)
#     goal_pos = (4,15)
#     my_prob = SearchProblem( domain=Pathways(domain), initial=init_pos, goal=goal_pos )
#     my_tree = SearchTree(my_prob, 'a*')
#     path, next_pos = my_tree.search()
#     #print('init pos ' + str(init_pos))
#     #print('goal pos ' + str(goal_pos))
#     print('next pos ' + str(next_pos))
#     #print('path ' + str(path))
        
    
#print(domain)

def test_search(domain, energy):
    vectors = []
    for (x,y) in energy:
        init_pos = (x,y)
        goal_pos = (1,15)
        my_prob = SearchProblem( domain=Pathways(domain), initial=init_pos, goal=goal_pos )
        my_tree = SearchTree(my_prob, 'a*')
        path, next_pos = my_tree.search()
        # print('init pos ' + str(init_pos))
        # print('goal pos ' + str(goal_pos))
        # print('next pos ' + str(next_pos))
        # print('path ' + str(path))

        dir = None
        x = goal_pos[0] - next_pos[0]
        y = goal_pos[1] - next_pos[1]
        if (x > 0):
            dir = (-1/my_tree.cost,0)
        if (x < 0):
            dir = (1/my_tree.cost,0)
        if (y > 0):
            dir = (0,-1/my_tree.cost)
        if (y < 0):
            dir = (0,1/my_tree.cost)

        vectors += [dir]
    return vectors





