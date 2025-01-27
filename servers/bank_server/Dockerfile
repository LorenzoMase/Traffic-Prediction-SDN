FROM ubuntu:20.04

RUN apt-get -qy update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    bash \
    bash-completion \
    curl \
    iperf \
    iperf3 \
    iproute2 \
    iputils-ping \
    net-tools \
    stress-ng \
    tcpdump \
    netcat \
    telnet \
    python3 \
    python3-pip && \
    rm -rf /var/lib/apt/lists/*

COPY server.py /home/server.py

RUN chmod +x /home/server.py

EXPOSE 65000

CMD ["bash"]
