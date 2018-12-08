#!/bin/bash
# Nov 7 2018

NUM_ITERS=1


# aux functions

# trap ctrl-c and exit
trap ctrl_c INT

function ctrl_c() {
    echo -e "\nAborting"
    killall python3
    exit 2
}

# run a batch of tests
run_tests() {
    LEVEL=$1
    GHOSTS=$2
    GHOSTS_LEVEL=$3

    echo -e ""

    cd .. > /dev/null
    # run the server
    if [ $GHOSTS -eq 0 ]; then
        python3 server.py --map data/map$LEVEL.bmp --ghosts 0 >> log_run_consts_test_server 2>&1 &
    
    else 
        python3 server.py --map data/map$LEVEL.bmp --ghosts $GHOSTS --level $GHOSTS_LEVEL >> log_run_consts_test_server 2>&1 &
    fi
    cd - > /dev/null


    # run N_ITERS tests
    # it will append a value to our_tests/averages 
    
    cd .. > /dev/null
    ./test_tool.sh $NUM_ITERS #>> log_run_consts_test 2>&1   
    cd - > /dev/null

    killall python3 -q
}

# compute average of a scores file
average () {
    if [ -f $1 ]; then
        s=${1%%.*}
        
        awk 'NF' $1 > aaaaaa #trim empty lines
        awk '{s+=$1}END{print "\t",(NR?s/NR:"NaN")}' RS="\n" aaaaaa
        awk '{s+=$1}END{print "\t",(NR?s/NR:"NaN")}' RS="\n" aaaaaa >> consts_averages
        rm -f aaaaaa   
    fi  
}


# backup original file
mv ../game_consts.py game_consts.py.backup

FILES=consts_files/*
for FILE in $FILES ; do

    echo -e "\e[34mProcessing $FILE file...\033[0m"

    rm -f averages_run 

    # move file to const
    mv $FILE ../game_consts.py 

    # run n tests

        # mapa de nıvel 1 conhecido, número de fantasmas 
        echo -e "\e[34m\tLevel 1, No ghosts\033[0m"
        run_tests 1 0 0  

        # mapa de nıvel 2 conhecido, número de fantasmas 2, dificuldade 1
        echo -e "\e[34m\tLevel 2, 2 Ghosts, Level 1\033[0m"
        run_tests 2 2 1 

        # mapa de nıvel 2 conhecido, número de fantasmas 2, dificuldade 2
        echo -e "\e[34m\tLevel 2, 2 Ghosts, Level 2\033[0m"
        run_tests 2 2 2 

        # mapa de nıvel 2 conhecido, número de fantasmas 4, dificuldade 1
        echo -e "\e[34m\tLevel 2, 4 Ghosts, Level 1\033[0m"
        run_tests 2 4 1 

        # mapa de nıvel 2 conhecido, número de fantasmas 4, dificuldade 2
        echo -e "\e[34m\tLevel 2, 4 Ghosts, Level 2\033[0m"
        run_tests 2 4 2 
    
    # get average of all tests
    awk '!/NaN/' averages_run > temp && mv temp averages_run

    echo "${FILE:12} -> " $(average averages_run)
    exit 1

    # remove game_const file and average file
    rm ../game_consts.py
    


done

# restore game_consts
mv game_consts.py.backup ../game_consts.py
