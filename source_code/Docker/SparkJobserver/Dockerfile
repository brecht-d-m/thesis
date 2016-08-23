# x86_64 || armv7l
#FROM bigboards/java-8-__arch__
FROM bigboards/java-8-x86_64

MAINTAINER bredmeul <brecht.demeulenaere@ugent.be>

USER root

# Install Python to support PySpark
RUN apt-get update && \
    apt-get install -y -q python && \
    curl -s http://d3kbcqa49mib13.cloudfront.net/spark-1.6.1-bin-hadoop2.6.tgz | tar -xz -C /opt && \
    ln -s /opt/spark-1.6.1-bin-hadoop2.6 /opt/spark && \
    apt-get clean && \
    apt-get autoclean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /var/cache/*

# Install vim
RUN apt-get update && \
    apt-get install -y -q vim

# Install nodejs and npm
RUN apt-get update && \
    apt-get install -y -q nodejs && \
    apt-get install -y -q npm

RUN ln -s /usr/bin/nodejs /usr/bin/node

ADD config/ldf-server       /opt/ldf-server
ADD config/ldf-client       /opt/ldf-client
ADD config/spark-jobserver  /opt/spark-jobserver
ADD config/bootstrap        /opt/bootstrap
ADD config/benchmark        /opt/benchmark

RUN chmod 0700 /opt/bootstrap/bootstrap_master.sh
RUN chmod 0700 /opt/bootstrap/bootstrap_worker.sh

#        master    worker   jobserver   LDF server
#     +---------+---------+-----------+------------+
EXPOSE 7077 8080 7078 8081  8090        8000

CMD ["/bin/bash"]
