#!/bin/bash
#run one round and copy the winner into a directory that shows its ancestry
function duplicate
{
    for index in {0..49}
    do 
        cp $1 $1$index
    done
}

cd ..
./nographics.sh ./data/sample2.world estrat/$1/ant estrat/$2/ant
exitstatus=$?
cd estrat
if [ $exitstatus -eq 1 ]
then
    winner=$1
else
    winner=$2
fi
cp -r $winner $winner"_old"
python mutate.py $winner 3
