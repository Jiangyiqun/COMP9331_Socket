# sender receiver_host_ip receiver_port file.pdf MWS MSS gamma
#        pDrop pDuplicate pCorrupt pOrder maxOrder pDelay maxDelay seed

import socket
import argparse
from scp import Checksum, Package



ACK_SIZE = 512
READ_SIZE = 512



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




class Sender():
    def __init__(self, receiver_addr):
        self.receiver_addr = receiver_addr
        # initialize the segment to be sent
        self.sequence = bytes([0])
        self.acknowledge = bytes([0])
        self.flag = bytes([0])
        self.window = bytes([0])
        self.checksum = bytes([0, 0])
        # the data flow to be sent
        self.header = bytes()
        self.payload = bytes()
        self.package = bytes()
        # create the socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print("Sender is ready\n")


    def make_package(self, data):
        self.payload = data
        header_without_checksum = self.sequence\
                                + self.acknowledge\
                                + self.flag\
                                + self.window
        self.checksum = Checksum.calculate_checksum(\
                        header_without_checksum\
                        + self.payload)
        self.header = header_without_checksum + self.checksum
        self.package = self.header + self.payload



    def send_package(self):
        sent_bytes = self.sock.sendto(self.package, receiver_addr)
        print("send package", self.sequence[0],
                "with checksum", self.checksum[0], self.checksum[1])
        return sent_bytes


    def receive_package(self):
        package, address = self.sock.recvfrom(ACK_SIZE)
        receiver = Package(package)
        return receiver


    def flip_sequence(self):
        if (self.sequence == bytes([0])):
            self.sequence = bytes([1])
        elif (self.sequence == bytes([1])):
            self.sequence = bytes([0])
        else:
            raise "Bad sequence number!"


    def send(self, data):
        self.make_package(data)
        while(True):
            # send and wait
            self.send_package()
            receiver = self.receive_package()

            # determine whether the return is currupted
            if (receiver.acknowledge == self.sequence):
                # not currupted, increase sequence number
                print("receive package", receiver.acknowledge[0],\
                        "send next!")
                self.flip_sequence()
                break
            else:   # currupted, resend package
                print("receive package", receiver.acknowledge[0],\
                        "need resend!")
                # continue
                break

                
    def close(self):
        self.sock.close()


if __name__ == '__main__':
    # get the arguments Sender
    args = get_args()
    host = "0.0.0.0"
    receiver_addr = (args.receiver_host_ip, args.receiver_port)
    # create instance of Sender
    instance = Sender(receiver_addr)
    # read and send file
    with open(args.file, 'rb') as fd:
        data = fd.read(READ_SIZE)
        while (data):
            instance.send(data)
            data = fd.read(READ_SIZE)

    # close
    instance.close()
    print("\nSend", args.file ,"to", instance.receiver_addr)