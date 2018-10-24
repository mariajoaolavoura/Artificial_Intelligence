
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
                #return self.get_path(node)
                return node.parent

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
