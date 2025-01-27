echo "Building client for all the services..."
docker build -t complete_client client/
echo "Building streaming server image..."
docker build -t server_streaming servers/streaming_server/
echo "Building the bank server image..."
docker build -t operations_server servers/bank_server/
echo "Building the chat server image..."
docker build -t echo_server servers/echo_server/
echo "Building dev test image..."
docker build -t dev_test servers/dev_test/