#!/bin/bash

cd node_modules
cd rtcmulticonnection-server
cp ../../scripts/server.js .
rm -r node_modules
mkdir node_modules
npm install
