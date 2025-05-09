FROM flink:latest

# Install Python and dependencies
USER root
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-dev build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    ln -s /usr/bin/python3 /usr/bin/python

# Install Python packages
RUN pip3 install apache-flink==1.16.1 pandas

# Switch back to the flink user
USER flink 