# python receiver.py receiver_port file_r.pdf



import socket
import argparse



HOST = "0.0.0.0"
BUFFER = 1024


def get_args ():
    parser = argparse.ArgumentParser()
    parser.add_argument('port', type=int)
    parser.add_argument('file', type=str)
    args = parser.parse_args()
    address = (HOST, args.port)
    return args, address



args, address = get_args()







sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(address)
print("Receiver ready!\n")


while True:
    data, addr = sock.recvfrom(BUFFER)
    if data:
        print("File name:", data)
        file_name = data.strip()

    # print ("received message:", data.decode('utf-8'))