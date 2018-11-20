from abc import ABC, abstractmethod
from corridor import Corridor
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


    def __init__(self, domain, initial_corr, initial_pos, goal_corr, goal_pos):
        
        self.domain = domain.copy() #so we can change the domain as we wish
        self.initial_corr = initial_corr
        self.initial_pos = initial_pos
        self.goal_corr = goal_corr
        self.goal_pos = goal_pos

        # Divide initial/goal corridor in 3 corridors:
        # root/goal = corridor with just 1 coordinate, the initial/goal position
        # sub_init0/sub_goal0 = corridor with all coordinates from 0 to the initial/goal position's index (inclusive)
        # sub_init1/sub_goal1 = corridor with all coordinates from the initial/goal position's index to end (inclusive)
        # so it can be possible to calculate the path for the 2 ends of initial/goal corridor

        self.initial = Corridor([self.initial_pos])
        
        sub_init0, sub_init1 = self.initial_corr.sub_corridors(self.initial_pos)
        self.update_domain(self.initial_corr, self.initial, sub_init0, sub_init1)


        self.goal = Corridor([self.goal_pos])
        
        sub_goal0, sub_goal1 = self.goal_corr.sub_corridors(self.goal_pos)
        self.update_domain(self.goal_corr, self.goal, sub_goal0, sub_goal1)


    def update_domain(self, corridor, sub_corr, sub_corr0, sub_corr1):
        
        self.domain.adjacencies += [(sub_corr, sub_corr0), (sub_corr, sub_corr1)]

        for (corrA, corrB) in self.domain.adjacencies:

            if corridor == corrA:
                if any(e in sub_corr0.ends for e in corrB.ends):
                    self.domain.adjacencies += [(sub_corr0, corrB)]
                elif any(e in sub_corr1.ends for e in corrB.ends):
                    self.domain.adjacencies += [(sub_corr1, corrB)]
                
            elif corridor == corrB:                
                if any(e in sub_corr0.ends for e in corrA.ends):
                    self.domain.adjacencies += [(sub_corr0, corrA)]
                elif any(e in sub_corr1.ends for e in corrA.ends):
                    self.domain.adjacencies += [(sub_corr1, corrA)]
        
        self.domain.adjacencies = [(A,B) for (A, B) in self.domain.adjacencies if (corridor != A and corridor != B) ]
    
    def goal_test(self, state):
        #state=corridor
        return state == self.goal


# NODE ------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# Nos de uma arvore de pesquisa
class SearchNode:
   
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
    
    def __init__(self, problem, strategy='breadth'): 
        
        self.problem = problem

        heur = abs(self.problem.goal.ends[0][0]-self.problem.initial.ends[0][0]) + abs(self.problem.goal.ends[0][1]-self.problem.initial.ends[0][1]) #self.problem.domain.heuristic(self.problem.initial, self.problem.initial, self.problem.goal) 
              
        root = SearchNode(self.problem.initial, parent=None, cost=self.problem.initial.length, heuristic=heur)
        
        self.open_nodes = [root]
        self.strategy = strategy
        self.lvisited = [root.state]
        self.cost = None


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

        while self.open_nodes != []:
            
            #print("\n\n###############################################################\n")
            
            node = self.open_nodes.pop()
            self.lvisited += [node.state]
            #print("node.state = " + str(node.state))
            #print("self.open_nodes = " + str(self.open_nodes))
            #print("self.lvisited = " + str(self.lvisited))

            if self.problem.goal_test(node.state):
                self.cost = node.cost
                if node.parent != None:
                    #print("node.state = " + str(node.state))
                    #print("node.parent.state = " + str(node.parent.state))
                    if node.parent.state.ends[0] in node.state.ends:
                        return node.parent.state.coordinates[1], self.cost#, self.get_path(node)
                    elif node.parent.state.ends[1] in node.state.ends:
                        return node.parent.state.coordinates[node.parent.state.length], self.cost#, self.get_path(node)
                return None

            lnewnodes = []

            #print("node.state = " + str(node.state))

            for action in self.problem.domain.actions(node.state):
        
                #print("action = " + str(action))

                # calculate next state
                new_state = self.problem.domain.result(node.state, action) 
                #print("new_state = " + str(new_state))

                if new_state in self.lvisited:
                    pass
                else:
                    # calculate cost of next node
                    cost = node.cost + 1 + self.problem.domain.cost(node.state, action)
                    #print("cost = " + str(cost))
                    # calculate heuristic of next node
                    heuristic = self.problem.domain.heuristic(node.state, new_state, self.problem.goal)
                    #print("heuristic = " + str(heuristic))
                    # create new node
                    new_node = SearchNode(state=new_state, parent=node, cost=cost, heuristic=heuristic)
                    
                    # add new node to list of new nodes
                    lnewnodes += [new_node]

            

            lnewnodes = [ newNode for newNode in lnewnodes \
                                    if newNode.state not in self.lvisited ]

            #print("lnewnodes = " + str(lnewnodes))

            #print("\n#############################################################\n\n")

            self.add_to_open(lnewnodes)
            self.lvisited.extend(node.state for node in lnewnodes)

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
            self.open_nodes = sorted(self.open_nodes, key=lambda node: node.heuristic + node.cost, reverse=True)

