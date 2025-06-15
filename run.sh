#!/bin/bash

# login (will continue if already logged in)
echo "Logging in..."
tidal-dl-ng login
mkdir -p /data/download/Tracks

#clear out /data/download/Tracks folder
echo "Clearing out /data/download/Tracks folder..."
rm -rf /data/download/Tracks/*
# for each file in /tracks, copy it to /data/download/Tracks
for f in /tracks/*; do
    # get filename without extension
    filename=$(basename "$f" .mp3)
    o="/data/download/Tracks"
    touch "$o/$filename.m4a"
done
echo "Downloading..."
# for each line in input.txt, run tidal-dl-ng dl
for i in $(cat /data/input.txt); do
    echo "Downloading $i..."
    tidal-dl-ng dl "$i"
done
cd /data/download/Tracks
echo "Converting..."
# run convert-m4a-to-mp3 for all m4a files
for f in *.m4a; do
    # if corresponding mp3 file exists, skip
    # check if file exists
    # get filename without extension
    filename=$(basename "$f" .m4a)
    o="/tracks"
    # check if filename.mp3 exists in $o
    if [ -f "$o/$filename.mp3" ]; then
        # echo "$o/$filename.mp3 already exists, skipping..."
        continue
    fi
    echo "Converting $f to $o/$filename.mp3..."
    convert-m4a-to-mp3 "$f" "$o"
done
echo "Done!"