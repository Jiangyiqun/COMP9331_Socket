# python3 receiver.py receiver_port file_r.pdf
# python3 receiver.py 2333 new.pdf
import socket
import argparse
from scp import ScpPackage, ScpLogger, ScpMath


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
        self.last_sequence = bytes([0, 0, 0, 1])
        # create scpPackage abstraction
        self.sender_pkg = ScpPackage()
        self.receiver_pkg = ScpPackage()
        # create the socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(receiver_addr)
        # create a logger
        self.logger = ScpLogger('Receiver_log.txt')
        print("Receiver is listening on:", receiver_addr)


    def receive_package(self):
        package, self.sender_addr = self.sock.recvfrom(self.buffer_size)
        self.sender_pkg.extract_package(package)

        

    def send_package(self):
        self.receiver_pkg.make_package()
        sent_bytes = self.sock.sendto(\
                self.receiver_pkg.package, self.sender_addr)
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
                self.logger.log('rcv', self.sender_pkg)
                # send fin & ack and wait
                self.receiver_pkg.fin = True
                self.receiver_pkg.ack = True
                self.receiver_pkg.make_package()
                self.send_package()
                self.logger.log('snd', self.receiver_pkg)
                self.receive_package()
            # there must not have a fin bit
            if (self.sender_pkg.ack):
                self.logger.log('rcv', self.sender_pkg)
                self.receiver_pkg.fin = False
                self.sock.close()
                print("Connection terminated!")
                return False
            # else this package then goes to next step
            # check the package and send ack
            if (self.sender_pkg.validate_package()):
                if (self.last_sequence != self.sender_pkg.sequence):
                    self.logger.log('rcv', self.sender_pkg)
                    # not corrupted & new package
                    self.last_sequence = self.sender_pkg.sequence
                    self.receiver_pkg.acknowledge = self.last_sequence
                    self.send_package()
                    self.logger.log('snd', self.receiver_pkg)
                    
                    return True
                else:
                    # not corrupted & duplicated package
                    self.logger.log('rcv', self.sender_pkg)
                    self.receiver_pkg.acknowledge = self.last_sequence
                    self.send_package()
                    self.logger.log('snd/DA', self.receiver_pkg)
            else:   
                # corrupted package
                self.logger.log('rcv/corr', self.sender_pkg)
                self.receiver_pkg.acknowledge = self.last_sequence
                self.send_package()
                self.logger.log('snd/DA', self.receiver_pkg)


    def listen(self):
        while(True):
            # wait syn
            self.receive_package()
            self.logger.reset_timer()
            if (self.sender_pkg.syn):
                self.logger.log('rcv', self.sender_pkg)
                # send syn & ack and wait
                self.receiver_pkg.syn = True
                self.receiver_pkg.ack = True
                self.receiver_pkg.make_package()
                self.send_package()
                self.logger.log('snd', self.receiver_pkg)
                self.receive_package()
                if ((not self.sender_pkg.syn) and self.sender_pkg.ack):
                    self.logger.log('rcv', self.sender_pkg)
                    self.receiver_pkg.syn = False
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
