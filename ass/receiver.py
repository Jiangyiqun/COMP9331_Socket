# receiver receiver_port file_r.pdf
import socket
import argparse
from scp import Checksum, Package


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
        self.last_sequence = bytes([1])
        # initialize the segment to be sent
        self.sequence = bytes([0])
        self.acknowledge = bytes([0])
        self.flag = bytes([0])
        self.window = bytes([0])
        self.checksum = bytes([0, 0])
        # the data to be sent
        self.package = bytes()
        # the received data
        self.data = bytes()
        # create the socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(receiver_addr)
        print("Receiver is listening on:", receiver_addr, "\n")

    def receive_package(self):
        package, self.sender_addr = self.sock.recvfrom(self.buffer_size)
        sender = Package(package)
        self.data = sender.payload
        return sender

    def send_package(self):
        self.acknowledge = self.last_sequence
        self.package = self.sequence\
                + self.acknowledge\
                + self.flag\
                + self.window\
                + self.checksum
        sent_bytes = self.sock.sendto(self.package, self.sender_addr)
        print("send package", self.acknowledge[0])
        return sent_bytes

    def receive(self, timeout=None):
        # Usage: not_finish = receive(timeout)
        #   
        self.sock.settimeout(timeout)
        while(True):
            # receive extract of the package
            try:
                sender = self.receive_package()
            except socket.timeout:
                return False
            # check the package and send ack
            if (Checksum.validate_checksum(sender.package)):
                if (self.last_sequence != sender.sequence):
                    # not corrupted & new package
                    self.last_sequence = sender.sequence
                    print("received package", sender.sequence[0],\
                            "corrected")
                    self.send_package()
                    return True
                else:
                    # not corrupted & duplicated package
                    print("received package:", sender.sequence[0],\
                            "duplicate")
                    self.send_package()
            else:   
                # corrupted package
                print("received package:", sender.sequence[0],\
                        "corrupted with checksum:",\
                        sender.checksum[0], sender.checksum[1])
                self.send_package()



    def close(self):
        self.sock.close()


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
            fd.write(instance.data)
            not_finish = instance.receive(1)
    
    # close
    instance.close()
    print("\nSave file", args.file_r, "from", instance.sender_addr)
