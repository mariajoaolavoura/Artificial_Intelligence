from abc import ABC, abstractmethod
from student import Corridor
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
    """
        Args:
        domain: problem's SearchDomain
        initial: tupple with initial corridor and initial position in the corridor
        goal: tupple with goal corridor and goal position in the corridor (goal will be where pacman is)

        Attr:
        domain: problem's SearchDomain
        initial_corr: initial corridor
        initial_pos: initial position in the corridor
        goal_corr: goal corridor
        goal_pos: goal position in the corridor
        """


    def __init__(self, domain, initial, goal):
        
        self.domain = domain
        self.initial_corr, self.initial_pos = initial
        self.goal_corr, self.goal_pos= goal
    
    def goal_test(self, state):
        '''state=corridor
        '''
        return state == self.goal_corr


# NODE ------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# Nos de uma arvore de pesquisa
class SearchNode:
    '''
        Args:
        state:
        parent:
        cost:
        heuristic:

        Attr:
        state:
        parent:
        cost:
        heuristic:
    '''
    
    def __init__(self, state, parent, cost, heuristic): 
        self.state = state #corridor
        self.parent = parent #SearchNode
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
    debug = False

    def __init__(self, problem, strategy='breadth'): 
        
        self.problem = problem

        # Divide initial/goal corridor in 3 corridors:
        # root/goal = corridor with just 1 coordinate, the initial/goal position
        # sub_init0/sub_goal0 = corridor with all coordinates from 0 to the initial/goal position's index (inclusive)
        # sub_init1/sub_goal1 = corridor with all coordinates from the initial/goal position's index to end (inclusive)
        # so it can be possible to calculate for the 2 ends of initial/goal corridor

        initial = Corridor([self.problem.initial_pos])
        sub_init0, sub_init1 = Corridor.sub_corridor(self.problem.initial_pos)
        self.update_domain(initial, sub_init0, sub_init1)

        goal = Corridor([self.problem.goal_pos])
        sub_goal0, sub_goal1 = Corridor.sub_corridor(self.problem.goal_pos)
        self.update_domain(goal, sub_goal0, sub_goal1)


        heur = self.problem.domain.heuristic(problem.initial_corr, self.problem.goal_corr)        
        root = SearchNode(initial, parent=None, cost=initial.length, heuristic=heur)
        
        heur0 = self.problem.domain.heuristic(sub_init0, self.problem.goal_corr)
        child0 = SearchNode(sub_init0, parent=root, cost=sub_init0.length, heuristic=heur0)

        heur1 = self.problem.domain.heuristic(sub_init1, self.problem.goal_corr)
        child1 = SearchNode(sub_init1, parent=root, cost=sub_init1.length, heuristic=heur1)

        self.open_nodes = [root, child0, child1]
        self.strategy = strategy
        self.lvisited = [root.state]
        self.cost = None

    # TODO put corridor adajcencies in order
    def update_domain(self, corr, sub_corr0, sub_corr1):
        initial_corr = self.problem.initial_corr

        for (corr1, corr2) in self.problem.domain:

            if initial_corr == corr1:
                self.problem.domain.pop((corr1, corr2))
                self.problem.domain += [(sub_corr1, corr2)]
                if initial_corr.ends[1] == corr:
                    self.problem.domain += [(corr, corr2)]

            elif initial_corr == corr2:
                self.problem.domain.pop((corr1, corr2))
                self.problem.domain += [(corr1, sub_corr0)]
                if initial_corr.ends[0] == corr:
                    self.problem.domain += [(corr1, corr)]



    # obter o caminho (sequencia de estados) da raiz ate um no
    def get_path(self,node):
        if node.parent == None:
            return [node.state]
        path = self.get_path(node.parent)
        path += [node.state]
        return(path)


    # TODO
    # procurar a solucao
    def search(self):

        #print()
        #print(self.open_nodes[0])

        #print(self.weight_dict)
        #count = 100
        #print(adjacencies)
        while self.open_nodes != []:
                
            node = self.open_nodes.pop(0)
            self.lvisited.extend(node.state)

            if self.problem.goal_test(node.state):
                #self.cost = node.cost
                if node.parent != None:
                    return (node.parent.state, self.cost)
                else:
                    return None

            lnewnodes = []

            for action in self.problem.domain.actions(node.state):
                
                #print('action: ' + str(action))
                
                # calculate next state
                newstate = self.problem.domain.result(node.state,action)
               
                #print('node.state is: ' + str(node.state))
                #print('newstate is: ' + str(newstate) + str(newstate in self.weight_dict))
                
                # if newstate is already in the list, add this weight to it
                # if newstate in self.lvisited:
                #     pass
                # if newstate in self.weight_dict.keys():
                #     self.weight_dict[newstate] += node.cost
                # else:

                # calculate cost of next node
                cost = node.cost + self.problem.domain.cost(node.state, action)
                # calculate heuristic of next node
                heuristic = self.problem.domain.heuristic(newstate, self.problem.goal)
                # create new node
                newnode = SearchNode(newstate,node,cost,heuristic)
                
                # if self.debug and count > 0:
                #     print("*** *** newnode: " + str(newnode))
                #     print("LVISITED")
                #     print(self.lvisited)
                # add new node to list of new nodes
                lnewnodes += [newnode]
                
            if lnewnodes == []:
                node.cost = 0

            #filterednn = [ newNode for newNode in lnewnodes \
            #                        if newNode.state not in self.lvisited ]
            # if self.debug and count > 0:
            #    print("*** *** filtered newnodes: " + str(filterednn))

            #self.add_to_open(filterednn)
            #self.lvisited.extend([node.state for node in filterednn])
            
            self.add_to_open(lnewnodes)

            # lista = []
            # for newNode in lnewnodes:
            #     if not node.inParent(newNode.state):
            #         lista += [newNode]
            #         #print(newNode)
            # self.add_to_open(lista)

            #count -= 1
        return None

    # juntar novos nos a lista de nos abertos de acordo com a estrategia
    def add_to_open(self,lnewnodes):
        if self.strategy == 'breadth':
            self.open_nodes.extend(lnewnodes)
        elif self.strategy == 'depth':
            self.open_nodes[0:0] = lnewnodes
        elif self.strategy == 'uniform':
            self.open_nodes.extend(lnewnodes)
            self.open_nodes = sorted(self.open_nodes, key=lambda node : node.cost)
        elif self.strategy == 'greedy':
            self.open_nodes.extend(lnewnodes)
            self.open_nodes = sorted(self.open_nodes, key=lambda node: node.heuristic)
        elif self.strategy == 'a*':
            self.open_nodes.extend(lnewnodes)
            self.open_nodes = sorted(self.open_nodes, key=lambda node: node.heuristic + node.cost)

