#!/bin/bash

cd node_modules/rtcmulticonnection-server/
node server &

cd ../..
./manage.py runserver
