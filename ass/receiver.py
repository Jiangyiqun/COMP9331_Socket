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
    def __init__(self, receiver_addr, buffer_size):
        self.receiver_addr = receiver_addr
        self.buffer_size = buffer_size
        self.sender_addr = ""
        self.package = bytes()
        self.sequence = bytes() # current received sequence number
        self.last_sequence = bytes([0, 1]) # last received sequence nb
        self.checksum = bytes()
        self.payload = bytes()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(receiver_addr)
        print("Receiver is listening on:", receiver_addr, "\n")
    def receive_package(self):
        self.package, self.sender_addr = self.sock.recvfrom(buffer_size)
        self.sequence = self.package[0:2]
        self.checksum = self.package[2:4]
        self.payload = self.package[4:]
    def send_ACK(self):
        self.sock.sendto(self.last_sequence, self.sender_addr)
    def close(self):
        self.sock.close()
    def flip_sequence(self):
        if (self.sequence == bytes([0, 0])):
            self.sequence == bytes([0, 1])
        elif (self.sequence == bytes([0, 1])):
            self.sequence == bytes([0, 0])
        else:
            raise "Bad sequence number!"
    def receive(self, timeout=None):
        # Usage: not_finish = receive(timeout)
        #   
        # self.sock.settimeout(timeout)
        try:
            while(True):
                # receive extract of the package
                self.receive_package()
                if (Checksum.validate_checksum(self.package)):
                    if (self.sequence != self.last_sequence):
                        # not corrupted, new package
                        # update last sequence number & return
                        self.last_sequence = self.sequence
                        print("correct package:", self.last_sequence)
                        self.send_ACK()
                        return True
                    else:
                        # not corrupted, but duplicated package
                        print("duplicate package:", self.last_sequence)
                        self.send_ACK()
                else:   
                    # package currupted
                    print("corrupted package:", self.last_sequence, 
                            "with checksum:", self.checksum)
                    self.send_ACK()
        except socket.timeout:
            return False


if __name__ == '__main__':
    # get the arguments Receiver
    args = get_args()
    host = "0.0.0.0"
    buffer_size = 1024
    receiver_addr = (host, args.receiver_port)
    # create instance of Receiver
    instance = Receiver(receiver_addr, buffer_size)

    # receiver and write
    not_finish = instance.receive()
    with open(args.file_r, 'wb') as fd:
        while(not_finish):
            fd.write(instance.payload)
            not_finish = instance.receive(2)
    
    # close
    instance.close()
    print("\nSave file", args.file_r, "from", instance.sender_addr)
