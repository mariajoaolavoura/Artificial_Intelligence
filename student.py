from tree_search import SearchTree, SearchProblem
from corridor import Corridor
from static_analysis import Static_Analysis
from pathways import Pathways
from strategy_advisor import Strategy_Advisor
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

SAFE_DIST_TO_CROSSROAD = 1

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

        self.map_ = Static_Analysis(map_)

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


        advisor = Strategy_Advisor(map_)
        mode_handler = advisor.advise()
        next_move = mode(mode_handler)
        if (next_move == False):
            adjuster = Strategy_Adjuster()
            mode_handler = adjuster.adjustStrategy()
        else:
        key = calculateKey()


    def calculate_key(self, vector):
        """Calculates the 'wasd' key that corresponds to the next move

        Keyword arguments:
        vector -- the vector that represents next PACMAN move
        """
        # # calculate the key to send
        # if abs(vec_x) > abs(vec_y):
        #     if vec_x > 0:
        #         key = 'd'
        #     else:
        #         key = 'a'
        # elif abs(vec_x) < abs(vec_y):
        #     if vec_y > 0:
        #         key = 's'
        #     else:
        #         key = 'w'
        # elif abs(vec_x) == abs(vec_y):
        #     if vec_x > 0 and vec_y > 0:
        #         key = random.choice('sd')
        #     elif vec_x > 0 and vec_y < 0:
        #         key = random.choice('dw')
        #     elif vec_x < 0 and vec_y < 0:
        #         key = random.choice('aw')
        #     elif vec_x < 0 and vec_y > 0:
        #         key = random.choice('as')
        #     elif vec_x == 0:
        #         logger.warning("There is a problem not solved yet in this line of code!")



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
