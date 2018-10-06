# sender receiver_host_ip receiver_port file.pdf MWS MSS gamma
#        pDrop pDuplicate pCorrupt pOrder maxOrder pDelay maxDelay seed

import socket
import argparse
from scp import ScpPackage, ScpLogger



ACK_SIZE = 512
READ_SIZE = 512
TIME_OUT = 1


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
        # create scpPackage abstraction
        self.sender_pkg = ScpPackage()
        self.receiver_pkg = ScpPackage()
        # create the socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print("Sender is ready\n")


    def send_package(self):
        sent_bytes = self.sock.sendto(\
                self.sender_pkg.package, receiver_addr)
        print("send package", self.sender_pkg.sequence[0],\
                "with checksum",self.sender_pkg.checksum_str())
        return sent_bytes


    def receive_package(self):
        package, receiver_address = self.sock.recvfrom(ACK_SIZE)
        self.receiver_pkg.extract_package(package)
        return receiver_address


    def send(self, data):
        self.sender_pkg.payload = data
        self.sender_pkg.make_package() 
        while(True):    # resend untill receiving correct ack
            # send and wait
            while(True):
                self.send_package()
                self.sock.settimeout(TIME_OUT)
                try:
                    self.receive_package()
                except socket.timeout:
                    continue    # resend when timeout
                self.sock.settimeout(None)
                break   # go on when received a package on time

            # finite state machine
            if (self.receiver_pkg.acknowledge ==\
                    self.sender_pkg.sequence):
                # not currupted, flip sequence number
                self.sender_pkg.flip_sequence()
                print("receive package",\
                        self.receiver_pkg.acknowledge[0],\
                        "send next!")
                break
            else:   
                # currupted, resend package
                print("receive package",\
                        self.receiver_pkg.acknowledge[0],\
                        "need resend!")
                continue
                # break

    def connect(self):
        while(True):
            # send syn and wait
            self.sender_pkg.syn = True
            self.sender_pkg.make_package()
            self.send_package()
            self.receive_package()
            # receive syn & ack
            if (self.receiver_pkg.syn and self.receiver_pkg.ack):
                # send ack
                self.sender_pkg.syn = False
                self.sender_pkg.ack = True
                self.sender_pkg.make_package()
                self.send_package()
                # connection estabilished
                self.sender_pkg.syn = False
                self.sender_pkg.ack = False
                print("Connection estabilished!")
                return


    def finish(self):
        while(True):
            # send fin and wait
            self.sender_pkg.fin = True
            self.sender_pkg.make_package()
            self.send_package()
            self.receive_package()
            # receive fin & ack
            if (self.receiver_pkg.fin and self.receiver_pkg.ack):
                # send ack
                self.sender_pkg.fin = False
                self.sender_pkg.ack = True
                self.sender_pkg.make_package()
                self.send_package()
                # connection terminated
                self.sender_pkg.syn = False
                self.sender_pkg.ack = False
                self.sock.close()
                print("Connection terminated!")
                return


if __name__ == '__main__':
    # get the arguments Sender
    args = get_args()
    host = "0.0.0.0"
    receiver_addr = (args.receiver_host_ip, args.receiver_port)
    # create instance of Sender
    instance = Sender(receiver_addr)
    instance.connect()
    # read and send file
    with open(args.file, 'rb') as fd:
        data = fd.read(READ_SIZE)
        while (data):
            instance.send(data)
            data = fd.read(READ_SIZE)
    
    # terminate connection
    instance.finish()
    print("\nSend", args.file ,"to", instance.receiver_addr)