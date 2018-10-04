#!/usr/bin/python3
#/home/z5129432/anaconda3/bin/python
# receiver receiver_port file_r.pdf
import socket
import argparse
import select
from checksum import Checksum

def get_args ():
    parser = argparse.ArgumentParser()
    parser.add_argument('receiver_port', type=int)
    parser.add_argument('file_r', type=str)
    args = parser.parse_args()
    return args


class Receiver():
    # sent package:
    #   header:
    #       sequence: 1 byte
    #       checksum: 2 bytes
    #   payload
    #
    # ack package:
    #   sequence: 1 byte
    #
    def __init__(self, receiver_addr, buffer_size):
        self.receiver_addr = receiver_addr
        self.buffer_size = buffer_size
        self.sender_addr = ""
        self.package = bytes()
        self.sequence = bytes()
        self.last_sequence = bytes()
        self.checksum = bytes()
        self.payload = bytes()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(receiver_addr)
        print("Receiver is listening on:", receiver_addr, "\n")
    def receive_package(self):
        self.package, self.sender_addr = self.sock.recvfrom(buffer_size)
        self.sequence = self.package[0]
        self.checksum = (self.package[1], self.package[2])
        self.payload = self.package[3:]
    def send_ACK(self):
        self.sock.sendto(self.last_sequence, self.sender_addr)
    # def send_NAK(self):
    #     self.sock.sendto(bytes([0]), self.sender_addr)
    def close(self):
        self.sock.close()
    # def receive_good_package(self):
    #     while(True):
    #         self.receive_package()
    #         if Checksum.validate_checksum(self.package):
    #             print("send ACK to: ", self.sender_addr)
    #             self.send_ACK()
    #             break
    #         else:
    #             print("send NAK to: ", self.sender_addr)
    #             self.send_NAK()
    def receive(self):
        while(True):
            # receive extract of the package
            self.receive_package()
            # not currupted, update last sequence number
            if (Checksum.validate_checksum(self.package)\
                and (self.sequence != self.last_sequence[0])):
                self.last_sequence = bytes([self.sequence])
                print("send ACK to: ", self.sender_addr)
                self.send_ACK()
                break
            else:   # currupted
                print("send NAK to: ", self.sender_addr)
                self.send_ACK()


if __name__ == '__main__':
    # get the arguments Receiver
    args = get_args()
    host = "0.0.0.0"
    buffer_size = 1024
    receiver_addr = (host, args.receiver_port)
    # create instance of Receiver
    instance = Receiver(receiver_addr, buffer_size)

    # receiver and write
    instance.receive()
    with open(args.file_r, 'wb') as fd:
        try:
            while(instance.package):
                fd.write(instance.payload)
                instance.sock.settimeout(2)
                instance.receive()
        except socket.timeout:
            # close socket
            instance.close()
    print("\nSave file", args.file_r, "from", instance.sender_addr)
