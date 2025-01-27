echo "starting the stream..."
ffmpeg -re -i input.mp4 -c:v libx264 -preset veryfast -b:v 2500k -maxrate 2500k -bufsize 5000k -pix_fmt yuv420p -c:a aac -b:a 128k -ar 44100 -f flv rtmp://localhost:1935/live/prova
