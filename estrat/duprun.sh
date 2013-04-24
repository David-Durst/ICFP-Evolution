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
cd estrat
if [ $? -eq 1 ]
then
    winner=$1
else
    winner=$2
fi
echo $winner
let newdirIndex=($winner+1)
newdir=$newdirIndex"_"$winner
mkdir $newdir
cp $winner/ant $newdir/
duplicate $newdir"/ant"
