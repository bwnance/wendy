#!/bin/sh

# if input.txt not in /data, copy it from /tmp
if [ ! -f /data/input.txt ]; then
    cp /tmp/input.txt /data/input.txt
fi

mkdir -p /data/config
# if settings.json not in /data/config, copy it from /tmp
if [ ! -f /data/config/settings.json ]; then
    cp /tmp/settings.json /data/config/settings.json
fi
