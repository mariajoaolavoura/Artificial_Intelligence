#!/bin/bash
# Nov 7 2018

# backup original file

NUM_ITERS=10

# for file in consts_files

    # move file to const


    # run n tests

        # mapa de nıvel 1 conhecido, número de fantasmas 0
        run_tests 1 0    


        # mapa de nıvel 2 conhecido, número de fantasmas 2, dificuldade 1
        run_tests 2 2 1

        # mapa de nıvel 2 conhecido, número de fantasmas 2, dificuldade 2
        run_tests 2 2 2


        # mapa de nıvel 2 conhecido, número de fantasmas 4, dificuldade 1
        run_tests 2 4 1

        # mapa de nıvel 2 conhecido, número de fantasmas 4, dificuldade 2
        run_tests 2 4 2
    
    


run_tests() {
    LEVEL=$1
    GHOSTS=$2
    GHOSTS_LEVEL=$3

    # run the server

    # run N_ITERS tests

    # 
}
    # get averages and put them in a file


