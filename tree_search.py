
# Modulo: tree_search
# 
# Fornece um conjunto de classes para suporte a resolucao de 
# problemas por pesquisa em arvore:
#    SearchDomain  - dominios de problemas
#    SearchProblem - problemas concretos a resolver 
#    SearchNode    - nos da arvore de pesquisa
#    SearchTree    - arvore de pesquisa, com metodos para 
#                    a respectiva construcao
#
#  (c) Luis Seabra Lopes, Introducao a Inteligencia Artificial, 2012-2014

from abc import ABC, abstractmethod




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
        # print("\t### SearchProblem was created!")
        # print("\t### Domain is: ")
        # print(self.domain)
        # print("\t### Initial is: " + str(self.initial))
        # print("\t### Goal is: " + str(self.goal))
    
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
    debug = False

    # construtor
    def __init__(self,problem, strategy='breadth'): 
        self.problem = problem
        heur = self.problem.domain.heuristic(problem.initial, self.problem.goal)
        root = SearchNode(problem.initial, parent=None, cost=0, heuristic=heur)
        self.open_nodes = [root]
        self.strategy = strategy
        self.cost = None
        self.lvisited = [root.state]
        # print("\t### SearchTree was created!")
        # print("\t### open nodes starts with only root: " + str(self.open_nodes))
        # print("\t### root heuristic is: " + str(heur))
        # print("\t### root is: " + str(root))

    # obter o caminho (sequencia de estados) da raiz ate um no
    def get_path(self,node):
        if node.parent == None:
            return [node.state]
        path = self.get_path(node.parent)
        path += [node.state]
        return(path)

    # procurar a solucao
    def search(self, adjacencies):

        #print("*** Entering Tree search() method")
        #print("*** open_nodes is empty? " + str(len(self.open_nodes) == 0))
        
        count = 100
        #print(adjacencies)
        while self.open_nodes != []:
            
            if self.debug and count > 0:
                print("\n*** open_nodes is empty? " + str(len(self.open_nodes) == 0))
                
            node = self.open_nodes.pop(0)
            
            # if self.debug and count > 0:
            #     print(self.lvisited)

            if self.debug and count > 0:
                print("*** popped node: " + str(node))

            if self.problem.goal_test(node.state):
                self.cost = node.cost
                #return self.get_path(node)
                if node.parent != None:
                    return node.parent.state
                else:
                    return None

            lnewnodes = []
            #print(self.open_nodes)

            for action in self.problem.domain.actions(node.state):

                if self.debug and count > 0:
                    print("*** *** action: " + str(action))

                # calculate next state
                newstate = self.problem.domain.result(node.state,action)
                if self.debug and count > 0:
                    print("*** *** newstate: " + str(newstate))
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
                
            filterednn = [ newNode for newNode in lnewnodes \
                                    if newNode.state not in self.lvisited \
                                    and [newnode.state[0],newnode.state[1]] not in adjacencies ]
            if self.debug and count > 0:
               print("*** *** filtered newnodes: " + str(filterednn))

            self.add_to_open(filterednn)
            self.lvisited.extend([node.state for node in filterednn])
            
            # lista = []
            # for newNode in lnewnodes:
            #     if not node.inParent(newNode.state):
            #         lista += [newNode]
            #         #print(newNode)
            # self.add_to_open(lista)

            count -= 1
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

    # fazer execicio 13
    # fazer exercicio 14
