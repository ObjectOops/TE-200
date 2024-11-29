#!/bin/bash

cd node_modules/rtcmulticonnection-server/
node server &

cd ../..
# source .env
# echo "Signaling Server URL: ${SIGNALING_SERVER_URL}"
./manage.py runserver
