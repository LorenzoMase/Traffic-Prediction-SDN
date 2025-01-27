echo "connecting to the stream..."
ffmpeg -i rtmp://10.0.0.3:1935/live/prova -c:v libx264 -c:a aac -preset veryfast -b:v 2500k -b:a 128k output.mp4
