FROM tiangolo/nginx-rtmp:latest
# Install useful tools
RUN apt-get -qy update && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
	bash \
	bash-completion \
	curl \
	iperf \
	iperf3 \
	iproute2 \
	iputils-ping \
	net-tools


COPY nginx.conf /etc/nginx/nginx.conf

COPY stream.sh input.mp4 /home/

RUN chmod +x /home/stream.sh; apt install ffmpeg -y

EXPOSE 1935

CMD ["nginx", "-g", "daemon off;"]