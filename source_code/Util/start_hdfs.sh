#!/bin/sh
# Setup based on: https://github.com/codingtony/docker-impala
sudo /create-hdfs-sockets.sh
sudo /start-hdfs.sh
sudo /start-impala.sh