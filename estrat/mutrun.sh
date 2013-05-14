#!/bin/bash
#run one round and copy the winner into a directory that shows its ancestry
function duplicate
{
    for index in {0..49}
    do 
        cp $1 $1$index
    done
}
i=0
while true 
do
    let i+=1
    echo "Trial "$i
    cd ..
    ./nographics.sh ./data/sample2.world estrat/$1/ant estrat/$2/ant
    exitstatus=$?
    cd estrat
    if [ $exitstatus -eq 1 ]
    then
        winner=$1
        loser=$2
    else
        loser=$1
        winner=$2
    fi
    rm -rf $loser
    cp -r $winner $loser
    python mutate.py $winner 3
    python mutate.py $loser 3
done
