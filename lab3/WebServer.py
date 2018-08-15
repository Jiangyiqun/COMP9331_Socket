# Python 3.6.5
from socket import *
import sys

# parse the argument to get the port
serverPort = int(sys.argv[1])

# create a connection socket
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print("The server is ready to receive")

while True:
    # receive HTTP request
    connectionSocket, addr = serverSocket.accept()
    # parse the request to determine the file path
    receivedData = connectionSocket.recv(1024).decode()
    resourcePath = '.' + receivedData.split()[1]
    print('request to send ', resourcePath)
    try:
        # read the file
        with open(resourcePath, 'rb') as fileToSend:
            dataToSend = fileToSend.read()
            # print(dataToSend)
            # send 200 and the file
            connectionSocket.send(b'HTTP/1.1 200 OK\r\n\r\n')
            connectionSocket.sendall(dataToSend)
    # send 404 if file not exist
    except FileNotFoundError:
        print(resourcePath, ' does not exist!')
        connectionSocket.send(b'HTTP/1.1 404 Not Found\r\n\r\n')
        connectionSocket.send(b'404 Not Found')
    # close the socket
    connectionSocket.close()