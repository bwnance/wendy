#!/bin/sh
# get filename from command line
f=$1
o=$2
ffmpeg -i "$f" -ab `ffmpeg -i "$f" 2>&1 | grep Audio | awk -F', ' '{print $5}' | cut -d' ' -f1`k -map_metadata 0 -id3v2_version 3 -write_id3v1 1 -fps_mode passthrough -c:v copy "$o/${f%.*m4a}.mp3";