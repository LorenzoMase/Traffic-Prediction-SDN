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
    python3-pip

RUN apt-get -qy update && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y \
	ffmpeg 

COPY ./viewer.sh /client_bank.py /client_chat_h1.py /client_chat_h2.py /operations.txt /home/

RUN chmod +777 /home/viewer.sh; chmod +x /home/client_bank.py; chmod +x /home/client_chat_h1.py; chmod +x /home/client_chat_h2.py

CMD ["bash"]