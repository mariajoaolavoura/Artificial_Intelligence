#!/bin/bash
# Nov 3 2018

# validate arguments sanity
if [ $# != 1 ]; then
	echo "$0 number_of_iterations"
	exit 1
fi

if [ $# -lt 1 ]; then
	echo "Number of iterations must be 1 or more"
	exit 2
fi

# aux functions 

# compute average
average () {
    if [ -f $1 ]; then
        s=${1%%.*}
        if [[ $2 == 1 ]]; then
            printf "\t${s:18}" 
        else
            printf "\t${s:7}" 
        fi
        
        awk 'NF' $1 > aaaaaa #trim empty lines
        awk '{s+=$1}END{print "\t",(NR?s/NR:"NaN")}' RS="\n" aaaaaa
        rm -f aaaaaa    
    fi  
}

# time stats
average_time () {
    if [ -f $1 ]; then
        awk 'NF' $1 > aaaaaa #trim empty lines
        awk '{s+=$1}END{print "",(NR?s/NR:"NaN")}' RS="\n" aaaaaa
    fi
}

max () {
    if [ -f $1 ]; then
        grep -Eo '[0-9]+.[0-9]+' $1 | sort -rn | head -n 1
    fi 
}

# print history averages
print_last_averages () {
    echo -e "\n--------------------\nLast averages: "

    average 'old_scores/scores.log'
    average 'old_scores/scores_ghosts_level0.log' 1
    average 'old_scores/scores_ghosts_level1.log' 1
    average 'old_scores/scores_ghosts_level2.log' 1
}

# print run info
print_run_info () {
    echo -e "--------------------\nThis run:\n"
    average 'scores.log'
    average 'scores_ghosts_level0.log'
    average 'scores_ghosts_level1.log'
    average 'scores_ghosts_level2.log'
    echo -e "\n\tCrashes:\t" $1
    echo -e "\tTimes (seg):"
    printf "\n\t\tAver:\t" 
    average_time time.txt
    printf "\t\tMax:\t"
    max time.txt
}

# trap ctrl-c and exit
trap ctrl_c INT

function ctrl_c() {
    echo -e "\nAborting"
    exit 2
}

if [ $1 -eq 1 ]; then
    echo -e "Pacman Test Tool ($1 iteration)\n"
else
    echo -e "Pacman Test Tool ($1 iterations)\n"
fi
# save old scores 
mkdir -p old_scores
mv scores* old_scores/ > /dev/null 2>&1
mkdir -p backup_scores
mkdir -p iter_logs

# debug
#cat 'scores.log'
#cat 'scores_ghosts_level0.log'
#cat 'scores_ghosts_level1.log'
#cat 'scores_ghosts_level2.log'

declare -i crash_count
crash_count=0

# run $1 times
for i in $(seq 1 $1); do 
    echo -e "Execution #$i"
    /usr/bin/time -f "%e" -a -o "time.txt" --quiet python3 student.py > iter_logs/output_$i.txt #2> tmp_error.txt  
    
    printf "\nTime was: " 
    sed "${i}q;d" time.txt
    
    #printf "\nOutput was: "
    #cat iter_logs/output$i.txt
    
    # copy save of scores
    if [ $? -eq 0 ]; then 
        cp scores* backup_scores/
    
    # program failed, restore scores
    else    
        echo -e "\033[93mERROR: Execution #$i failed (game crashed). Restoring scores\033[0m"
        
        #echo -e "Error: " 
        #cat tmp_error.txt
        
        crash_count=crash_count+1
        
        mv -f backup_scores/scores* .. > /dev/null 2>&1
    fi

    # debug
    # echo -e "---------\n"
    # cat 'scores.log'
    # cat 'scores_ghosts_level0.log'
    # cat 'scores_ghosts_level1.log'
    # cat 'scores_ghosts_level2.log'
    
    echo -e "---------------------\n"
done

echo -e "\nAll $1 iterations done\n\n"

# print results
print_run_info $crash_count
print_last_averages
echo -e "\nIf an average is NaN it's not an error.\nIt means a script execution failed or was canceled."

# clean up
rm -f tmp_error.txt
rm -f time.txt

echo -e "\n"

