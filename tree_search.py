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
        self.debug = True and (goal_pos == [4,15] or goal_pos == [4,14]) and (initial_pos == [4,13] or initial_pos == [4,16])
        # if (initial_pos == [4,10] or initial_pos == [4,11] or initial_pos == [4,12] \
        # or initial_pos == [4,13] or initial_pos == [4,14] or initial_pos == [4,15] \
        # or initial_pos == [4,16] or initial_pos == [4,17] or initial_pos == [4,18] \
        # or initial_pos == [4,19] or initial_pos == [4,20] ):
        #     self.debug = False

        # if (initial_pos == [4,23] or initial_pos == [4,24]):
        #     self.debug = False

        #self.debug = True    
        #self.debug = False

        # Divide initial/goal corridor in 3 corridors:
        # root/goal = corridor with just 1 coordinate, the initial/goal position
        # sub_init0/sub_goal0 = corridor with all coordinates from 0 to the initial/goal position's index (inclusive)
        # sub_init1/sub_goal1 = corridor with all coordinates from the initial/goal position's index to end (inclusive)
        # so it can be possible to calculate the path for the 2 ends of initial/goal corridor

        if self.debug:
            print("Analizing path: " + str(initial_pos) + " --> " + str(goal_pos))    

        self.initial = Corridor([self.initial_pos])
        
        sub_init0, sub_init1 = self.initial_corr.sub_corridors(self.initial_pos)
        self.update_domain(self.initial_corr, self.initial, sub_init0, sub_init1)

        if goal_pos in sub_init0.coordinates:
            self.goal_corr = sub_init0
        elif goal_pos in sub_init1.coordinates:
            self.goal_corr = sub_init1

        self.goal = Corridor([self.goal_pos])

        sub_goal0, sub_goal1 = self.goal_corr.sub_corridors(self.goal_pos)
        self.update_domain(self.goal_corr, self.goal, sub_goal0, sub_goal1)


    def update_domain(self, corridor, sub_corr, sub_corr0, sub_corr1):
        
        new_adjacencies = []
        debug = self.debug
        if debug:
            print()
            print("initial_pos: " + str(self.initial_pos))
            print("goal_pos: " + str(self.goal_pos))
            print("corridor: " + str(corridor))
            print("sub_corr: " + str(sub_corr))
            print("sub_corr0: " + str(sub_corr0))
            print("sub_corr1: " + str(sub_corr1))


        if corridor.coordinates != sub_corr0.coordinates and corridor.coordinates != sub_corr1.coordinates:

            for [corrA, corrB] in self.domain.adjacencies:
                
                
                if corridor.coordinates == corrA.coordinates:
                    if any(e in sub_corr0.ends for e in corrB.ends):
                        new_adjacencies += [[sub_corr0, corrB]]
                    elif any(e in sub_corr1.ends for e in corrB.ends):
                        new_adjacencies += [[sub_corr1, corrB]]
                    
                elif corridor.coordinates == corrB.coordinates:                
                    if any(e in sub_corr0.ends for e in corrA.ends):
                        new_adjacencies += [[sub_corr0, corrA]]
                    elif any(e in sub_corr1.ends for e in corrA.ends):
                        new_adjacencies += [[sub_corr1, corrA]]

            # eliminar das adjacencias o corredor inicial que foi dividido e j'a nao existe inteiro
            
            self.domain.adjacencies = [[A,B] for [A, B] in self.domain.adjacencies if (corridor != A and corridor != B)]
            self.domain.adjacencies += new_adjacencies

        else:
            for [corrA, corrB] in self.domain.adjacencies:

                if sub_corr0.coordinates == sub_corr.coordinates:
                    
                    if corridor.coordinates == corrA.coordinates:
                        if any(e in sub_corr.ends for e in corrB.ends):
                            #self.printd(debug, ("added: " + str([[sub_corr, corrB]])))
                            new_adjacencies += [[sub_corr, corrB]]
                        elif any(e in sub_corr1.ends for e in corrB.ends):
                            #self.printd(debug, ("added: " + str([[sub_corr1, corrB]])))
                            new_adjacencies += [[sub_corr1, corrB]]
                        
                    elif corridor.coordinates == corrB.coordinates:                
                        if any(e in sub_corr.ends for e in corrA.ends):
                            #self.printd(debug, "added: " + str([[sub_corr, corrA]]))
                            new_adjacencies += [[sub_corr, corrA]]
                        elif any(e in sub_corr1.ends for e in corrA.ends):
                            #self.printd(debug, "added: " + str([[sub_corr1, corrA]]))
                            new_adjacencies += [[sub_corr1, corrA]]

                if sub_corr1.coordinates == sub_corr.coordinates:
                    
                    if corridor.coordinates == corrA.coordinates:
                        if any(e in sub_corr.ends for e in corrB.ends):
                            #self.printd(debug, "added: " + str([[sub_corr, corrB]]))
                            new_adjacencies += [[sub_corr, corrB]]
                        elif any(e in sub_corr0.ends for e in corrB.ends):
                            #self.printd(debug, "added: " + str([[sub_corr1, corrB]]))
                            new_adjacencies += [[sub_corr0, corrB]]
                        
                    elif corridor.coordinates == corrB.coordinates:                
                        if any(e in sub_corr.ends for e in corrA.ends):
                            #self.printd(debug, "added: " + str([[sub_corr, corrA]]))
                            new_adjacencies += [[sub_corr, corrA]]
                        elif any(e in sub_corr0.ends for e in corrA.ends):
                            #self.printd(debug, "added: " + str([[sub_corr1, corrA]]))
                            new_adjacencies += [[sub_corr0, corrA]]

            self.domain.adjacencies = [[A,B] for [A, B] in self.domain.adjacencies if (corridor != A and corridor != B)]
            # if debug:
            #     print('new_adjacencies: ' + str(new_adjacencies))
            self.domain.adjacencies += new_adjacencies


        if sub_corr.coordinates != sub_corr0.coordinates:
            self.domain.adjacencies += [[sub_corr, sub_corr0]]
        if sub_corr.coordinates != sub_corr1.coordinates:
            self.domain.adjacencies += [[sub_corr, sub_corr1]]


    def printd (self, valid, string):
        if valid:
            print(string)

    
    def goal_test(self, state):
        #state=corridor
        #print("state = " + str(state))
        #print("self.goal = " + str(self.goal))
        return state.coordinates == self.goal.coordinates
        

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
    
    def __init__(self, problem, strategy='a*'): 
        
        self.problem = problem

        heur = abs(self.problem.goal.ends[0][0]-self.problem.initial.ends[0][0]) + abs(self.problem.goal.ends[0][1]-self.problem.initial.ends[0][1]) #self.problem.domain.heuristic(self.problem.initial, self.problem.initial, self.problem.goal) 
              
        root = SearchNode(self.problem.initial, parent=None, cost=self.problem.initial.length, heuristic=heur)
        
        self.open_nodes = [root]
        self.strategy = strategy
        #self.lvisited = []
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


        debug = self.problem.debug

        if debug:
            print("initial position is :" + str(self.problem.initial_pos))

        while self.open_nodes != []:
            
            if (debug):
                print("\n\n###############################################################\n")
            
            node = self.open_nodes.pop()
            #self.lvisited += [node.state]
            if (debug):
                print("node.state = " + str(node.state))
                print("self.open_nodes = " + str(self.open_nodes))
                print("self.lvisited = " + str(self.lvisited))
                print("self.problem.goal_test(node.state) = " + str(self.problem.goal_test(node.state)))
            if self.problem.goal_test(node.state):
                self.cost = node.cost
                if node.parent != None:
                    #print("node.state = " + str(node.state))
                    #print("node.parent.state = " + str(node.parent.state))
                    if node.parent.state.ends[0] in node.state.ends:
                        #print("RETURNED ---> SOMETHING")
                        return node.parent.state.coordinates[1], self.cost, self.get_path(node)
                        #print("RETURNED ---> SOMETHING")
                    elif node.parent.state.ends[1] in node.state.ends:
                        return node.parent.state.coordinates[node.parent.state.length], self.cost, self.get_path(node)
                #print("RETURNED ---> NONE")
                return None

            lnewnodes = []

            if (debug):
                print("node.state = " + str(node.state))

            for action in self.problem.domain.actions(node.state):
                
                if (debug):
                    print("action = " + str(action))

                # calculate next state
                new_state = self.problem.domain.result(node.state, action)
                if (debug): 
                    print("new_state = " + str(new_state))

                if new_state in self.lvisited:
                    pass
                else:
                    # calculate cost of next node
                    cost = node.cost + 1 + self.problem.domain.cost(node.state, action)
                    if (debug): 
                        print("cost = " + str(cost))
                    # calculate heuristic of next node
                    heuristic = self.problem.domain.heuristic(node.state, new_state, self.problem.goal)
                    if (debug): 
                        print("heuristic = " + str(heuristic))
                    # create new node
                    new_node = SearchNode(state=new_state, parent=node, cost=cost, heuristic=heuristic)
                    
                    # add new node to list of new nodes
                    lnewnodes += [new_node]

            

            lnewnodes = [ newNode for newNode in lnewnodes \
                                    if newNode.state not in self.lvisited ]

            if (debug):
                print("lnewnodes = " + str(lnewnodes))

                print("\n#############################################################\n\n")

            self.add_to_open(lnewnodes)
            self.lvisited.extend(node.state for node in lnewnodes)
        #print("RETURNED ---> NONE")
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


