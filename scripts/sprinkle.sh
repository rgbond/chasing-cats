#!/bin/bash
if [ -f /home/rgb/bin/sprinkler_off ]
then
    echo "Sprinkle disabled"
    exit 0
fi
curl https://api.particle.io/v1/devices/id/sprinkle -d access_token=token -d params=on
