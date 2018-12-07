#!/bin/bash
# Nov 5 2018
# create needed dirs
mkdir -p consts_files/

BASEFILENAME='consts_files/game_consts_'
BASEFILEEXTENSION='.py'

# consts bounds
MIN_SAFE_DIST_TO_CROSSROAD=2
MAX_SAFE_DIST_TO_CROSSROAD=4
STEP_SAFE_DIST_TO_CROSSROAD=1

MIN_SAFE_DIST_TO_GHOST=4
MAX_SAFE_DIST_TO_GHOST=9
STEP_SAFE_DIST_TO_GHOST=1

MIN_GHOST_PURSUIT_MULTIPLIER=2      # * 10 the wanted value
MAX_GHOST_PURSUIT_MULTIPLIER=10     # * 10 the wanted value
STEP_GHOST_PURSUIT_MULTIPLIER=1     # * 10 the wanted value
CONST=10

for (( i=MIN_SAFE_DIST_TO_CROSSROAD; i<MAX_SAFE_DIST_TO_CROSSROAD; i+=STEP_SAFE_DIST_TO_CROSSROAD )); do
    for (( j=MIN_SAFE_DIST_TO_GHOST; j<MAX_SAFE_DIST_TO_GHOST; j+=STEP_SAFE_DIST_TO_GHOST )); do
        for (( k=MIN_GHOST_PURSUIT_MULTIPLIER; k<MAX_GHOST_PURSUIT_MULTIPLIER; k+=STEP_GHOST_PURSUIT_MULTIPLIER )); do
            echo $i','$j','$k','$k_value
            k_value=$(echo "print($k/$CONST)" | python3)
            echo "from enum import Enum
import logging

#------------------------------------------------------------------------------#
# ENUMERATES

# Usage MODE.EATING
class MODE(Enum):
    PURSUIT = 1
    EATING  = 2
    COUNTER = 3
    FLIGHT  = 4
    PANIC = 5

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
SAFE_DIST_TO_CROSSROAD = $i
# distance at which ghost probably isn't in pursuit of pacman
SAFE_DIST_TO_GHOST = $j
# value from 0 to 1.
# 0 -> Pac-Man does not pursue the ghots
# 1 -> Pac-Man pursues ant ghost in maximum range until timeout
GHOST_PURSUIT_MULTIPLIER = $k_value

#------------------------------------------------------------------------------#
# LOGGER 
# After many solutions, I found an elegant one (kudos to 
# https://stackoverflow.com/questions/11232230/logging-to-two-files-with-different-settings)


def setup_logger(name, log_file, level=logging.DEBUG, mode='w', format='[%(lineno)s - %(funcName)20s() - %(levelname)s] %(message)s\n'):
    """Function setup as many loggers as you want"""

    # currently writing over the logger file, change filemode to a to append
    handler = logging.FileHandler(log_file, mode)        
    
    # '%(levelname)s:\t%(message)' # simpler format
    format = logging.Formatter(format)
    handler.setFormatter(format)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger" > $BASEFILENAME'_'$i'_'$j'_'$k$BASEFILEEXTENSION
            
        done
    done
done

echo "Done!"