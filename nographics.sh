#!/bin/sh
# world red black 

export WTF=/tmp/haeusl-runner.wtf

rm -rf $WTF

./simulator/simulator $1 $2 $3 wtf > $WTF 

exitcode=$?

rm -f $WTF

exit $exitcode
