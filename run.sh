#!/bin/bash

FINAL_DIR="/tracks"

# login (will continue if already logged in)
echo "Logging in..."
echo "downloading from soundcloud..."
mkdir -p /data/sc_archives
mkdir -p /data/download/SCTRACKS
cd /data/download/SCTRACKS
for i in $(cat /data/sc_input.txt); do
    echo "Downloading playlist $i..."
    #get md5 of playlist url
    md5=$(echo -n "$i" | md5sum | awk '{print $1}')
    scdl -l $i --download-archive /data/sc_archives/$md5.txt -c
done
for i in $(ls -d */); do
    # cd into the directory
    cd "$i"
    # for all files in directory
    for f in *; do
        # continue if not m4a or mp3
        if [[ ! "$f" =~ \.(m4a|mp3)$ ]]; then
            echo "Skipping $f, not a m4a or mp3 file."
            continue
        fi
        # remove folder name prefix from filename
        # eg, folder name /data/download/SCDL/DJ, filename is DJ_TrackName.m4a, output should be TrackName.m4a
        folder_name=$(basename "$i")
        new_name="${f#$folder_name\_}"
        #if names are the same, skip
        if [[ "$f" == "$new_name" ]]; then
            continue
        fi
        mv "$f" "$new_name"
    done
    #for each m4a in the directory, convert to mp3
    for f in *.m4a; do
        if [[ ! -f "$f" ]]; then
            # echo "No m4a files found, skipping..."
            continue
        fi
        # if corresponding mp3 file exists, skip
        # check if file exists
        # get filename without extension
        filename=$(basename "$f" .m4a)
        o="$FINAL_DIR"
        # check if filename.mp3 exists in $o
        if [ -f "$o/$filename.mp3" ]; then
            # echo "$o/$filename.mp3 already exists, skipping..."
            continue
        fi
        echo "Converting $f to $o/$filename.mp3..."
        convert-m4a-to-mp3 "$f" "$o"
        rm "$f"
        touch "$f"  # create an empty m4a file in its place
    done
    # copy all mp3 files to /tracks
    for f in *.mp3; do
        if [[ ! -f "$f" ]]; then
            # echo "No mp3 files found, skipping..."
            continue
        fi
        # get filename without extension
        filename=$(basename "$f" .mp3)
        o="$FINAL_DIR"
        # check if filename.mp3 exists in final dir
        if [ -f "$o/$filename.mp3" ]; then
            echo "$o/$filename.mp3 already exists, skipping..."
            continue
        fi
        echo "Moving $f to $o/$filename.mp3..."
        mv "$f" "$o/$filename.mp3"
        touch "$f"  # create an empty mp3 file in its place
    done
done


tidal-dl-ng login
mkdir -p /data/download/Tracks
#clear out /data/download/Tracks folder
echo "Clearing out /data/download/Tracks folder..."
rm -rf /data/download/Tracks/*
# for each file in /tracks, copy it to /data/download/Tracks
for f in /tracks/*.mp3; do
    # get filename without extension
    filename=$(basename "$f" .mp3)
    o="/data/download/Tracks"
    touch "$o/$filename.m4a"
done
echo "Downloading..."
# for each line in input.txt, run tidal-dl-ng dl
for i in $(cat /data/tidal_input.txt); do
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
    o="$FINAL_DIR"
    # check if filename.mp3 exists in $o
    if [ -f "$o/$filename.mp3" ]; then
        # echo "$o/$filename.mp3 already exists, skipping..."
        continue
    fi
    echo "Converting $f to $o/$filename.mp3..."
    convert-m4a-to-mp3 "$f" "$o"
done
#convert files already in /tracks
cd /tracks
for f in *.m4a; do
    if [[ ! -f "$f" ]]; then
        # echo "No m4a files found, skipping..."
        continue
    fi
    # if corresponding mp3 file exists, skip
    # check if file exists
    # get filename without extension
    filename=$(basename "$f" .m4a)
    o="$FINAL_DIR"
    # check if filename.mp3 exists in $o
    if [ -f "$o/$filename.mp3" ]; then
        # echo "$o/$filename.mp3 already exists, skipping..."
        continue
    fi
    echo "Converting $f to $o/$filename.mp3..."
    convert-m4a-to-mp3 "$f" "$o"
    rm "$f"  # remove the m4a file after conversion
    echo "Removed $f after conversion."
done
for f in *.flac; do
    if [[ ! -f "$f" ]]; then
        # echo "No flac files found, skipping..."
        continue
    fi
    # if corresponding mp3 file exists, skip
    # check if file exists
    # get filename without extension
    filename=$(basename "$f" .flac)
    o="/tracks"
    # check if filename.mp3 exists in $o
    if [ -f "$o/$filename.mp3" ]; then
        # echo "$o/$filename.mp3 already exists, skipping..."
        continue
    fi
    echo "Converting $f to $o/$filename.mp3..."
    ffmpeg -i "$f" -ab 320k -map_metadata 0 -id3v2_version 3 "$o/$filename.mp3"
    rm "$f"  # remove the flac file after conversion
    echo "Removed $f after conversion."
    echo "Converted $f to $o/$filename.mp3!"
done
for f in *.wav; do
    if [[ ! -f "$f" ]]; then
        # echo "No wav files found, skipping..."
        continue
    fi
    # if corresponding mp3 file exists, skip
    # check if file exists
    # get filename without extension
    filename=$(basename "$f" .wav)
    o="/tracks"
    # check if filename.mp3 exists in $o
    if [ -f "$o/$filename.mp3" ]; then
        echo "$o/$filename.mp3 already exists, skipping..."
        continue
    fi
    echo "Converting $f to $o/$filename.mp3..."
    ffmpeg -i "$f" -ab 320k -map_metadata 0 -id3v2_version 3 "$o/$filename.mp3"
    rm "$f"  # remove the wav file after conversion
    echo "Removed $f after conversion."
    echo "Converted $f to $o/$filename.mp3!"
done
echo "Done!"