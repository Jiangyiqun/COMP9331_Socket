# receiver receiver_port file_r.pdf
import socket
import argparse
from scp import ScpPackage, ScpLogger


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
        # create scpPackage abstraction
        self.sender_pkg = ScpPackage()
        self.receiver_pkg = ScpPackage()
        # create the socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(receiver_addr)
        # create a logger
        self.logger = ScpLogger('Receiver_log.txt')
        print("Receiver is listening on:", receiver_addr, "\n")


    def receive_package(self):
        package, self.sender_addr = self.sock.recvfrom(self.buffer_size)
        self.sender_pkg.extract_package(package)
        self.logger.log('rcv', self.sender_pkg)
        


    def send_package(self):
        self.receiver_pkg.make_package()
        sent_bytes = self.sock.sendto(\
                self.receiver_pkg.package, self.sender_addr)
        print("send package", self.receiver_pkg.acknowledge[0])
        self.logger.log('snd', self.receiver_pkg)
        return sent_bytes

    def receive(self):
        # Usage: not_finish = receive(timeout)
        #   
        # finite state machine
        while(True):
            # stop and wait to receive from the sender
            self.receive_package()
            # when received a fin, then ack on it
            # wait untill a not fin is received
            while (self.sender_pkg.fin):
                # send fin & ack and wait
                self.receiver_pkg.fin = True
                self.receiver_pkg.ack = True
                self.receiver_pkg.make_package()
                self.send_package()
                self.receive_package()
            # there must not have a fin bit
            if (self.sender_pkg.ack):
                self.receiver_pkg.fin = False
                self.receiver_pkg.ack = False
                self.sock.close()
                print("Connection terminated!")
                return False
            # else this package then goes to next step
            # check the package and send ack
            if (self.sender_pkg.validate_package()):
                if (self.last_sequence != self.sender_pkg.sequence):
                    # not corrupted & new package
                    self.last_sequence = self.sender_pkg.sequence
                    print("received package",\
                            self.sender_pkg.sequence[0],\
                            "corrected with checksum",\
                            self.sender_pkg.checksum_str())
                    self.receiver_pkg.acknowledge = self.last_sequence
                    self.send_package()
                    
                    return True
                else:
                    # not corrupted & duplicated package
                    print("received package:",\
                            self.sender_pkg.sequence[0],\
                            "duplicate with checksum",\
                            self.sender_pkg.checksum_str())
                    self.receiver_pkg.acknowledge = self.last_sequence
                    self.send_package()
            else:   
                # corrupted package
                print("received package:",\
                        self.sender_pkg.sequence[0],\
                        "corrupted with checksum",\
                        self.sender_pkg.checksum_str())
                self.receiver_pkg.acknowledge = self.last_sequence
                self.send_package()


    def listen(self):
        while(True):
            # wait syn
            self.receive_package()
            if (self.sender_pkg.syn):
                # send syn & ack and wait
                self.receiver_pkg.syn = True
                self.receiver_pkg.ack = True
                self.receiver_pkg.make_package()
                self.send_package()
                self.receive_package()
                if ((not self.sender_pkg.syn) and self.sender_pkg.ack):
                    self.receiver_pkg.syn = False
                    self.receiver_pkg.ack = False
                    print("Connection estabilished!")
                    return


if __name__ == '__main__':
    # get the arguments Receiver
    args = get_args()
    host = "0.0.0.0"
    buffer_size = 1024
    receiver_addr = (host, args.receiver_port)
    # create instance of Receiver
    instance = Receiver(receiver_addr, buffer_size)
    instance.listen()



    # receiver and write
    not_finish = instance.receive()
    with open(args.file_r, 'wb') as fd:
        while(not_finish):
            fd.write(instance.sender_pkg.payload)
            not_finish = instance.receive()
    
    print("\nSave file", args.file_r, "from", instance.sender_addr)
