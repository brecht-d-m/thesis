#!/bin/bash

wget ftp://brecht:brecht@172.18.16.126/Thesis/watdiv/watdiv/bin/Release/datasets/100k/watdiv.100k.nt -O /data/watdiv.100k.nt
wget ftp://brecht:brecht@172.18.16.126/Thesis/watdiv/watdiv/bin/Release/datasets/1M/watdiv.1M.nt -O /data/watdiv.1M.nt
wget ftp://brecht:brecht@172.18.16.126/Thesis/watdiv/watdiv/bin/Release/datasets/10M/watdiv.10M.nt -O /data/watdiv.10M.nt

/opt/spark/bin/spark-class org.apache.spark.deploy.master.Master --port 7077 --webui-port 8080

cd /opt/spark-jobserver
./server_start.sh

cd /opt/ldf-server/bin
./start.sh
