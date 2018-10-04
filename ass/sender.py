#!/usr/bin/python3
#/home/z5129432/anaconda3/bin/python
# sender receiver_host_ip receiver_port file.pdf MWS MSS gamma
#        pDrop pDuplicate pCorrupt pOrder maxOrder pDelay maxDelay seed

import socket
import argparse
from checksum import Checksum


def get_args ():
    parser = argparse.ArgumentParser()
    parser.add_argument('receiver_host_ip', type=str)
    parser.add_argument('receiver_port', type=int)
    parser.add_argument('file', type=str)
    # parser.add_argument('MWS', type=str)
    # parser.add_argument('MSS', type=str)
    # parser.add_argument('gamma', type=str)
    # parser.add_argument('pDrop', type=str)
    # parser.add_argument('pDuplicate', type=str)
    # parser.add_argument('pCorrupt', type=str)
    # parser.add_argument('pOrder', type=str)
    # parser.add_argument('maxOrder', type=str)
    # parser.add_argument('pDelay', type=str)
    # parser.add_argument('maxDelay', type=str)
    # parser.add_argument('seed', type=str)
    args = parser.parse_args()
    return args


class Receiver():
    def __init__(self, receiver_addr, buffer_size):
        self.receiver_addr = receiver_addr
        self.buffer_size = buffer_size
        self.package = bytes()
        self.payload = bytes()
        self.checksum = bytes()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print("Socket created!\n")
    def make_package(self, payload):
        self.payload = payload
        self.checksum = Checksum.calculate_checksum(payload)
        self.package = bytes(list(self.checksum)) + self.payload
    def close(self):
        self.sock.close()
    def send_package(self):
        sent_bytes = self.sock.sendto(self.package, receiver_addr)
        print("send package with checksum: ",
                self.checksum[0], self.checksum[1])
        return sent_bytes
    def send_good_package(self):
        while(True):
            self.send_package()
            pkg, addr = self.sock.recvfrom(self.buffer_size)
            ack = pkg[0]
            if (ack == 1):
                print("received ACK from: ", addr)
                break
            else:
                print("received NAK from: ", addr)
                continue


if __name__ == '__main__':
    args = get_args()
    host = "0.0.0.0"
    buffer_size = 512
    receiver_addr = (args.receiver_host_ip, args.receiver_port)
    instance = Receiver(receiver_addr, buffer_size)


    with open(args.file, 'rb') as fd:
        data = fd.read(instance.buffer_size)
        instance.make_package(data)
        while (data):
            instance.send_good_package()
            data = fd.read(instance.buffer_size)
            instance.make_package(data)
    instance.close()
    print("\nSend", args.file ,"to", instance.receiver_addr)