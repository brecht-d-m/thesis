#!/bin/bash
# Install npm packages
npm install

# Prepare client
git submodule init
git submodule update
#npm link clients/ldf-client
ln -s ../clients/ldf-client/ ./node_modules/ldf-client
