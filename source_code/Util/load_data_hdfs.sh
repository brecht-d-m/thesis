#!/bin/sh

sudo ./create-hdfs-sockets.sh
ps aux | grep node # If needed stop hdfs namenode
sudo ./start-hdfs.sh
sudo ./start-impala.sh # If needed multiple times

# Leave safemode if necessary
sudo -u hdfs hdfs dfsadmin -safemode leave

# Create directory
sudo hadoop dfs -mkdir -p /tmp/watdiv.100k
sudo hadoop dfs -mkdir -p /tmp/watdiv.1M
sudo hadoop dfs -mkdir -p /tmp/watdiv.10M

# Load data into hdfs
sudo hadoop dfs -put /home/brecht/Thesis/watdiv/watdiv/bin/Release/datasets/100k/watdiv.100k.csv /tmp/watdiv.100k
sudo hadoop dfs -put /home/brecht/Thesis/watdiv/watdiv/bin/Release/datasets/1M/watdiv.1M.csv /tmp/watdiv.1M
sudo hadoop dfs -put /home/brecht/Thesis/watdiv/watdiv/bin/Release/datasets/10M/watdiv.10M.csv /tmp/watdiv.10M

# To check if it is loaded, after execution you should see csv files
sudo hadoop dfs -ls /tmp/watdiv.100k
sudo hadoop dfs -ls /tmp/watdiv.1M
sudo hadoop dfs -ls /tmp/watdiv.10M
