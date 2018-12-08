#!/bin/bash
# Nov 7 2018

NUM_ITERS=10


# aux functions
# run a batch of tests
run_tests() {
    LEVEL=$1
    GHOSTS=$2
    GHOSTS_LEVEL=$3

    # run the server
    if [ $GHOSTS -eq 0 ]; then
        python3 ../server.py s --map data/map$LEVEL.bmp
    
    else 
        python3 ../server.py s --map data/map$LEVEL.bmp --ghosts $GHOSTS --level $GHOSTS_LEVEL &
    fi
    
    # run N_ITERS tests
    # it will append a value to our_tests/averages 
    ../test_tool.sh $NUM_ITERS    

    killall python3
}

# compute average of a scores file
average () {
    if [ -f $1 ]; then
        s=${1%%.*}
        
        awk 'NF' $1 > aaaaaa #trim empty lines
        #awk '{s+=$1}END{print "\t",(NR?s/NR:"NaN")}' RS="\n" aaaaaa
        awk '{s+=$1}END{print "\t",(NR?s/NR:"NaN")}' RS="\n" aaaaaa >> consts_averages/consts_averages
        rm -f aaaaaa   
    fi  
}


# backup original file
mv ../game_consts.py our_tests/game_consts.py.backup


# for file in consts_files
for FILE in consts_files/*.py; do

    # move file to const
    mv $FILE ../game_consts.py 

    # run n tests

        # mapa de nıvel 1 conhecido, número de fantasmas 0
        run_tests 1 0 0  

        # mapa de nıvel 2 conhecido, número de fantasmas 2, dificuldade 1
        run_tests 2 2 1 

        # mapa de nıvel 2 conhecido, número de fantasmas 2, dificuldade 2
        run_tests 2 2 2 

        # mapa de nıvel 2 conhecido, número de fantasmas 4, dificuldade 1
        run_tests 2 4 1 

        # mapa de nıvel 2 conhecido, número de fantasmas 4, dificuldade 2
        run_tests 2 4 2 
    
    # get average of all tests
    echo "${FILE:12} -> " $(average $our_tests/averages)

    # remove game_const file and average file
    rm ../game_consts.py
    rm our_tests/averages 


# restore game_consts
mv our_tests/game_consts.py.backup ../game_consts.py
