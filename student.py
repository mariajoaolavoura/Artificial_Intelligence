from tree_search import SearchTree
from corridor import Corridor
from static_analysis import Static_Analysis
import random
import logging

#$ PORT=80 SERVER=pacman-aulas.ws.atnog.av.it.pt python client.py
# to kill server: fuser 8000/tcp

# for debug purposes
debug = True

# logs are written to file logger.log after the client is closed
# possible messages: debug, info, warning, error, critical 
# how to use: logging.typeOfMessage('message')
logger = logging.getLogger('student_logger')
logger_format = '[%(lineno)s - %(funcName)20s() - %(levelname)s]\n %(message)s\n'
#logger_format = '%(levelname)s:\t%(message)' # simpler format

# currently writing over the logger file, change filemode to a to append
logging.basicConfig(format=logger_format, filename='logger.log', filemode='w', level=logging.DEBUG)

class Pacman_agent():
    """Creates the PACMAN agent that analyses the given 'Map' and 'state'
    to decide which direction to take and win the game 

    Args:
    map_: instance of Map for the current level

    Attr:
    map_: instance of Map for the current level
    static_analysis: instance of Static_Analysis containing:
                - pathways: list of all coordinates that are not walls
                - adjacencies: list of pairs of adjacent pathways
                - corridors: list of coordinates that create a corridor
                - crossroads: list of all coordinates that separate corridors
    """

    def __init__(self, map_): 
        logger.warning('\n\n\n ========================== NEW EXECUTION ==========================\n')
        logger.debug('CREATING PACMAN AGENT\n')

        # static info from mapa.py Map
        self.map_ = map_
        self.static_analysis = Static_Analysis(map_)

        logger.debug('CREATED PACMAN AGENT')


    def get_next_move(self, state):
        """Objective of Pacman_agent - calculates the next position using
        multiple auxiliar methods

        Args:
        state: a list of lists with the state of every element in the game

        Returns: the key corresponding to the next move of PACMAN
        """

        #logger.debug(nt("\nEnergy size is : " + str(len(state['energy'])) + "\n")

        #! ##########   STRATEGY   ##########
        #?      -> L
        #*      -> P
        #TODO   -> MJ

        #! corredor SAFE - UNSAFE
            #? SAFE - Não tem fantasmas
            #? UNSAFE - Tem fantasmas

        #! cruzamentos VERDES - AMARELO - VERMELHO
            #* refere-se aos cruzamentos diretamente acessiveis ao Pac-Man
            #? VERDE - Não há fantasmas nas proximidades
            #? AMARELO - Há fantasmas a uma distância perigosa (3 posições?), 
            #?           no entanto se o Pac-Man se dirigir imediatamente para lá
            #?           consegue escapar por eles antes de ser encurralado
            #? VERMELHO - Fantasma a uma distancia que nao permite ao Pac-Man
            #?            escapar antes de ser apanhado (considerando que o fantasma
            #?            está em perseguição, se estiver aleatório, pode haver
            #?            uma possibiliade de fuga)


        #! Modos de jogo para o Pac-Man
            #? EATING_MODE - Modo base. Pac-Man está num corredor SAFE e pelo menos
            #?                   um cruzamento próximo está VERDE
            #? COUNTER_MODE - Pac-Man está a ser perseguido apenas por um lado,
            #?                sem perigo eminente de ser encurralado. Prioridade
            #?                passa a ser encontrar um BOOST para contra-atacar,
            #?                uma vez que tem um fantasma próximo. Na ausencia de
            #?                BOOST, passa a EATING_MODE
            #? PUSUIT_MODE - Pac-Man comeu um BOOST. Prioridade é fazer perseguição
            #?               aos fantasmas, independentemente das energias. 
            #? FLIGHT_MODE - Pac-Man está em perigo eminente de ser encurralado.
            #?               A prioridade passa a ser encontrar corredores seguros,
            #?               e são ignoradas as energias.

        #* modes mais importantes: pursuit e flight mode (eating seria por defeito, o COUNTER é relevante?)
        #* implementação : Enum e detecção usando ifs
        #* how to use enums (if I correctly remember)
        #* from enum import Enum
        # class Mode(Enum):
        #   COUNTER = 1
        #   PURSUIT = 2
        #   EATING  = 3
        #   FLIGHT  = 4

        #! Análise Estática fornece
            #? pathways
            #? corridors
            #? crossroads
            #? coordinates_adjacencies
            #? corridor_adjacencies
        
        #! Análise Base (posição atual do Pac-Man), comum e necessária a todos os MODES
            #? 1.1 - Analisar corredores SAFE - UNSAFE (alterar na lista de adjacencias de corredores)
            #? 1.2 - Determinar meu corredor SAFE - UNSAFE
            #? 2.1 - Calcular distancia aos meus cruzamentos
            #? 2.2 - Calcular distancia dos fantasmas aos meus cruzamentos
            #? 2.3 - Determinar meus cruzamentos VERDE - AMARELO - VERMELHO
            #? 3.1 - Determinar se há fantasmas em modo zombie + tempo para perseguição

        #! chamar MODE correspondente (corredor - cruzamento1 - cruzamento2)
            #* SAFE     - VERDE     - VERDE
                #? EATING_MODE
                    #? dependencias:
                        #? lista de adjacencias de corredores SAFE/UNSAFE
                        #? posição do Pac-Man (coordenada + corredor)
                        #? lista de energias
                        #? lista de boosts (para ser tratado como energias)
                    #? retorna
                        #? próxima posição para energia mais próxima
                    #? considerações
                        #? verifica se o primeiro corredor no caminho para a
                        #? energia é SAFE/UNSAFE. Se for UNSAFE, retorna caminho
                        #? para a segunda energia mais próxima.
                        #? Em caso de ambiguidade, opta por opção mais segura.
            #* SAFE     - VERDE     - AMARELO
                #? EATING_MODE
                    #? idem
                    #? pode considerar sair por caminho VERDE caso distancias sejam muito semelhantes?
            #* SAFE     - VERDE     - VERMELHO
                #? EATING_MODE
                    #? idem
                    #? tem de sair pelo lado VERDE
                    #? verificar o quanto pode arriscar a limpar lado VERMELHO
            #* SAFE     - AMARELO   - AMARELO
                #? COUNTER_MODE
                    #? -- Só funciona se existirem BOOST, caso contrário retorna None
                    #? dependencias
                        #? lista de adjacencias de corredores SAFE/UNSAFE
                        #? posição do Pac-Man (coordenada + corredor)
                        #? lista de energias
                        #? lista de boosts
                
                #? EATING_MODE
                
                #? FLIGHT_MODE
            #* SAFE     - AMARELO   - VERMELHO
                #? FLIGHT_MODE
            #* SAFE     - VERMELHO  - VERMELHO
                #? FLIGHT_MODE

            #* UNSAFE   - VERDE     - VERMELHO
                #? COUNTER_MODE
                #? FLIGHT_MODE
            #* UNSAFE   - AMARELO   - VERMELHO
                #? COUNTER_MODE
                #? FLIGHT_MODE
            #* UNSAFE   - VERMELHO  - VERMELHO
                #? FLIGHT_MODE


            #? corr SAFE - corredores amarelos
                #? COUNTER_MODE
             
            #? calcular distancia a pontos acessiveis
            #? calcular distancia a boosts
            #? calcular distancia a fantasmas
            #* basta um método distanceTo(original_pos, dest_pos)
            #* a diferença estará na forma de obter dest_pos, como é óbvio

            #? verificar condicoes do meu corredor

        #* algoritmo
        #* porque não uma simplificação (só se analisam corredores nos cruzamentos e
        #* deixamos de analisar os cruzamentos em si)
        #? corredor SAFE?
            #* continua no corredor até um cruzamento

            #? Cruzamentos VERDE?
                #? EATING_MODE
                    #? ignorar fantasmas...
                    #? ignorar boosts
                    #? pesquisas bolinhas, caminho mais seguro
            #? cruzamentos VERDE e AMARELO
                #? EATING_MODE
                    #? OPCAO 1 - aproveitar para limpar lado amarelo enquanto 'e possivel
                    #? OPCAO 2 - continuar a pesquisar caminho mais seguro
                    #* OPCAO 1 é mais arriscada mas mais adequada para obter mais pontos mais depressa (prefiro)
            #? cruzamentos AMARELO
                #? FLIGHT_MODE
                    #? OPCAO 1 - fugir para um qualquer caminho seguro
                    #? OPCAO 2 - fugir pelo lado que tem mais bolinhas
                    #? OPCAO 3 - fugir pelo caminha mais curto (evitar que mais fantasmas se aproximem no entretanto?)
                    #? OPCAO 4 - sistema de pesos com as anteriores
                #* muito complexo... temos de tentar simplificar
            #? cruzamento AMARELO e VERMELHO
                #? FLIGHT_MODE
                #? fugir pelo lado possivel para o sitio mais seguro (com ou sem bolinhas)
            #? cruzamentos VERMELHOS
                #? FLIGHT_MODE
                #? morrer com dignidade e apanhar o maximo de bolinhas
                #* simplemesmente evitá-los (voltar para trás)?

        #? corredor NOT SAFE
            #? cruzamento livre a AMARELO
                #? FLIGHT_MODE
            #? cruzamento livre a VERDE
                #? há BOOST?
                    #? pesquisar boost
                #? não há boost
                    #? fantasma nao nos afecta, desde que nao se volte atras. pesquisar bolinhas

            #* se o corredor não for safe: a) evitamo-lo ou b) escolhemos o melhor em termos de pontos (BOOST + energias - ghosts)
            #* ideia: método que, dado um corredor, devolve o seu valor (BOOST + energias - ghosts). 
            #* é um revisit da ideia dos pesos mas não sofre dos mesmo problemas 
            #*(um corredor nunca é muito extenso e a análise seria ocasional)










        #print("\nEnergy size is : " + str(len(state['energy'])) + "\n")
        # create a vector for every element in the game
        # every element points pacman teh next move to get to it
        vectors = []
        #logger.debug(nt(state['energy'])
        
        pac_pos = (state['pacman'][0], state['pacman'][1])
        # if debug:
        #     logger.debug("\t pacman is in position " + str(pac_pos))

        ex, ey = self.get_vector(nodes_to_search=state['energy'], pac_pos=pac_pos)
        #(gx, gy) = self.get_vector(state['ghosts'], pac_pos)

        #sum the vectors
        vec_x = ex #+ (-10*gx)
        vec_y = ey #+ (-10*gy)

        # calculate the key to send
        if abs(vec_x) > abs(vec_y):
            if vec_x > 0:
                key = 'd'
            else:
                key = 'a'
        elif abs(vec_x) < abs(vec_y):
            if vec_y > 0:
                key = 's'
            else:
                key = 'w'
        elif abs(vec_x) == abs(vec_y):
            if vec_x > 0 and vec_y > 0:
                key = random.choice('sd')
            elif vec_x > 0 and vec_y < 0:
                key = random.choice('dw')
            elif vec_x < 0 and vec_y < 0:
                key = random.choice('aw')
            elif vec_x < 0 and vec_y > 0:
                key = random.choice('as')
            elif vec_x == 0:
                logger.warning("There is a problem not solved yet in this line of code!")
        
        if debug:
            logger.debug('The key is: ' + str(key))


        # x, y = state['pacman']
        # if x == cur_x and y == cur_y:
        #     if key in "ad":
        #         key = random.choice("ws")
        #     elif key in "ws":
        #         key = random.choice("ad")
        # cur_x, cur_y = x, y

        return key



    def compute_strategy(self):

        set_corridors_safety()

    def set_corridors_safety(self):



        for (cA, cB) in self.static_analysis.corr_adjacencies:
            pass 


    def get_crossroads_semaphores(self):
        pass


    def boosts_analyser(self):
        pass


    def get_vector(self, nodes_to_search, pac_pos):
        """Calculates the vector given by an element

        Args:
        nodes_to_search -- 
        pac_pos         -- coordinates of PACMAN position

        Returns:

        """
        i = 0
        next_pos = []
        vectors = []
        # if debug:
        #     logger.debug("***********************************************************")
        #     logger.debug('\t get vector was called! ')
        #     logger.debug("***********************************************************")

        # convert list to dictionary with zero weight for each element
        weight_dict = { (x,y):1 for [x,y] in nodes_to_search }

        for (x,y) in nodes_to_search:

            # if debug:
                # logger.debug("#######################################################")
                # logger.debug('\t calculating vector for pos: ' + str((x,y)))
                # logger.debug("#######################################################")
        
            # if debug:
            #     logger.debug("\t cycle  for position " + str((x,y)))

            # search the path
            # if debug:
            #     logger.debug("SearchDomain being called to create")
            domain = Pathways(self.adjacencies)

            # if debug:
            #     logger.debug("SearchProblem " + str(i) + " being called to create")
            my_prob = SearchProblem(domain,(x,y),pac_pos)
            
            # if debug:
            #     logger.debug("SearchTree " + str(i) + " being called to create")
            my_tree = SearchTree(my_prob, weight_dict, self.strategy)
            
            next_result = my_tree.search()

            if next_result != None:
                next_res, next_cost = next_result
                next_pos += [((x,y) , next_res, next_cost)]
            else:
                next_pos += [((x,y), pac_pos, 0)]

            #logger.debug((x,y))
            #logger.debug(next_result)
            
            #logger.debug("\t search " + str(i) + " was completed!")

            # if debug:
            #     logger.debug('\t Calculating next move for position: ' + str((x,y)))

        #logger.debug(next_pos)

        for i in range(len(next_pos)):
            if next_pos[i][1] != pac_pos:
                pac_x, pac_y = pac_pos
                next_x, next_y = (next_pos[i])[1]
                x = pac_x - next_x
                y = pac_y - next_y
                if (x == 1):
                    dir = ( ( -(1/next_pos[i][2])) , 0 )
                elif (x == -1):
                    dir = ( ( (1/next_pos[i][2])) , 0 )
                elif (y == 1):
                    dir = ( 0 , (-(1/next_pos[i][2])) )
                elif (y == -1):
                    dir = ( 0 , ((1/next_pos[i][2])) )
                elif (x > 1):
                    dir = ( ((1/next_pos[i][2])) , 0 )
                elif (x < 1):
                    dir = ( (-(1/next_pos[i][2])) , 0 )
                elif (y > 1):
                    dir = ( 0 , ((1/next_pos[i][2])) )
                elif (y < 1):
                    dir = ( 0 , (-(1/next_pos[i][2])) )
                vectors += [dir]

                logger.debug(str(next_pos[i][0]) + " : vector is: " + str(dir))
            
            # if debug:
            #     logger.debug("#######################################################")
            #     logger.debug('\t Vector is ' + str(dir))
            #     logger.debug("#######################################################")

        #logger.debug(weight_dict)



        # sum all the vectors
        vec_x = 0
        vec_y = 0
        for (x,y) in vectors:
            vec_x += x
            vec_y += y
        
        #logger.debug("\npacman is in position " + str(pac_pos[0], pac_pos[1]))
        #logger.debug('Sum of all vectors is: ' + str(vec_x) + ', ' + str(vec_y) + "\n")

        if debug:
            logger.debug("#######################################################")
            logger.debug('\t Vector is ' + str((vec_x, vec_y)))
            logger.debug("#######################################################")

        return [vec_x, vec_y]





    def calculate_key(self, vector):
        """Calculates the 'wasd' key that corresponds to the next move

        Keyword arguments:
        vector -- the vector that represents next PACMAN move
        """



    def calculate_next_move_direction(self, pac_pos, next_pos):
        """Calculates direction of next PACMAN move

        Keyword arguments:
        pac_pos     -- coordinates of PACMAN position
        next_pos    -- coordinates of next PACMAN move
        """



    def sum_vectors(self, vectors):
        """Sums all vectors

        Keyword arguments:
        vectors -- a list of vectors
        """



    def combinations(self, list_, n):
        """Generates all combinations of the elements in a list

        Keyword arguments:
        list_   -- a list
        n       -- number of elements per combination
        """
        if n==0: yield []
        else:
            for i in range(len(list_)):
                for elem in self.combinations(list_[i+1:],n-1):
                    yield [list_[i]] + elem

    

    def print_debug_block(self, string, var):
        """Prints a debug bar

        Keyword arguments:
        list_   -- a list
        n       -- number of elements per combination
        """
        #logger.debug("#######################################################")
        #logger.debug('\t ' + string + ' is: ')
        #logger.debug("#######################################################")
        #logger.debug(var)


################################################################################
#####################   STATIC ANALYSIS AUXILIAR METHODS   #####################
################################################################################
    
    

################################################################################
#############################   AUXILIAR CLASSES   #############################
################################################################################
