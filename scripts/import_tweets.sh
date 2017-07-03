#!/bin/sh

#BASE="http://localhost:17080/import_tweets"
BASE="http://hard-at-work.appspot.com/import_tweets"

d=$(date +"%Y-%m-%d")

start=$1
shift

#for d in "06" "05" "04" "03" "02"; do
for m in $start; do
    i=1
    while [ $i -lt 32 ]; do
        d="2017-$m-$i"
        i=$((i + 1))
        req="$BASE?since=$d"
        echo $req
        open $req
    done
done

