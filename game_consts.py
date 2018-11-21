#------------------------------------------------------------------------------#
# ENUMERATES

# Usage MODE.EATING
class MODE(Enum):
    EATING  = 1
    FLIGHT  = 2
    PURSUIT = 3
    COUNTER = 4

class CORRIDOR_SAFETY(Enum):
    SAFE   = 1
    UNSAFE = 2

# crossroad_safety
class SEMAPHORE(Enum):
    GREEN  = 1
    YELLOW = 2
    RED    = 3


#------------------------------------------------------------------------------#
# GLOBAL VARIABLES

# minimum escape margin if pacman is racing towards crossroad against a ghost
SAFE_DIST_TO_CROSSROAD = 1
# distance at which ghost probably isn't in pursuit of pacman
SAFE_DIST_TO_GHOST = 7