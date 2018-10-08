# python3 sender.py receiver_host_ip receiver_port file.pdf MWS MSS gamma
#          pDrop pDuplicate pCorrupt pOrder maxOrder pDelay maxDelay seed
# python3 sender.py localhost 2333 test0.pdf 512 512 0 0 0 0

import socket, argparse, random, threading, time
from scp import ScpPackage, ScpLogger, ScpMath, HEADER_SIZE


DEFAULT_TIMEOUT = 0.5


def get_args ():
    parser = argparse.ArgumentParser()
    parser.add_argument('receiver_host_ip', type=str)
    parser.add_argument('receiver_port', type=int)
    parser.add_argument('file', type=str)
    parser.add_argument('MWS', type=int)
    parser.add_argument('MSS', type=int)
    # parser.add_argument('gamma', type=str)
    parser.add_argument('pDrop', type=float)
    parser.add_argument('pDuplicate', type=float)
    parser.add_argument('pCorrupt', type=float)
    # parser.add_argument('pOrder', type=str)
    # parser.add_argument('maxOrder', type=str)
    # parser.add_argument('pDelay', type=str)
    # parser.add_argument('maxDelay', type=str)
    parser.add_argument('seed', type=str)
    args = parser.parse_args()
    return args




class Sender():
    def __init__(self, args):
        # get and parse the args
        self.args = args
        self.receiver_addr = (self.args.receiver_host_ip,\
                self.args.receiver_port)
        # max package in a window
        self.base_seq = 0
        self.next_seq = 0
        self.sender_buffer = {}
        self.timeout = 0.5
        self.sender_timer = threading.Timer(\
                self.timeout, self.retransmit_buffer) 
        # create scpPackage abstraction
        self.sender_pkg = ScpPackage()
        self.receiver_pkg = ScpPackage()
        # create the socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # create the logger
        self.logger = ScpLogger('Sender_log.txt')
        # initialize the PLD module
        random.seed(self.args.seed)
        print("Sender is ready")


    def send_package(self):
        sent_bytes = self.sock.sendto(\
                self.sender_pkg.package, self.receiver_addr)
        self.logger.log('snd', self.sender_pkg)
        return sent_bytes


    def PLD_send_package(self):
        if (random.random() < self.args.pDrop):
            # pDrop
            sent_bytes = 0
            self.logger.log('drop', self.sender_pkg)
        elif (random.random() < self.args.pDuplicate):
            sent_bytes_1 = self.sock.sendto(\
                    self.sender_pkg.package, self.receiver_addr)
            self.logger.log('snd', self.sender_pkg)
            sent_bytes_2 = self.sock.sendto(\
                    self.sender_pkg.package, self.receiver_addr)
            sent_bytes = sent_bytes_1 + sent_bytes_2
            self.logger.log('snd/DA', self.sender_pkg)
        elif (random.random() < self.args.pCorrupt):
            self.sender_pkg.flip_a_bit()
            sent_bytes = self.sock.sendto(\
                    self.sender_pkg.package, self.receiver_addr)
            self.logger.log('snd/corr', self.sender_pkg)
            self.sender_pkg.flip_a_bit()
        else:
            sent_bytes = self.sock.sendto(\
                    self.sender_pkg.package, self.receiver_addr)
            self.logger.log('snd', self.sender_pkg)
        return sent_bytes



    def receive_package(self):
        package, receiver_address = self.sock.recvfrom(HEADER_SIZE)
        self.receiver_pkg.extract_package(package)
        return receiver_address


    def restart_timer(self):
        self.sender_timer.cancel()
        self.sender_timer = threading.Timer(\
                self.timeout, self.retransmit_buffer) 
        self.sender_timer.start()


    def send(self, data):
        # window is not full: send one package and return
        # window is full: receive and parse ACK
        while(True):
            # event 1: send packages
            if (self.next_seq < self.base_seq + self.args.MWS):
                # window is not full, send packages
                # reset timer at for the first package of a window
                if (self.next_seq == self.base_seq):
                    self.restart_timer()
                    print("restart timer for new window", self.base_seq)
                # send package
                self.sender_pkg.sequence =\
                        ScpMath.int_to_bytes(self.next_seq, 4)
                self.sender_pkg.payload = data
                self.sender_pkg.make_package()
                self.PLD_send_package()
                # add to buffer
                self.sender_buffer[self.next_seq] = data
                # update next sequence number
                self.next_seq += len(data)
                # continue read and send till window is full
                return
            # come there when window is full
            self.receive_ack()


    # event 2: time out
    def retransmit_buffer(self):
        buffered_package = sorted(list(self.sender_buffer.keys()))
        print("timeout! buffer is", buffered_package)
        sent_bytes = 0
        for seq in buffered_package:
            # send package
            self.sender_pkg.sequence =\
                    ScpMath.int_to_bytes(seq, 4)
            self.sender_pkg.payload = self.sender_buffer[seq]
            self.sender_pkg.make_package()
            sent_bytes = self.sock.sendto(\
                self.sender_pkg.package, self.receiver_addr)
            self.logger.log('snd/RXT', self.sender_pkg)
        self.restart_timer()
        return sent_bytes

    # event 3: receive packages
    def receive_ack(self):
        self.receive_package()
        ack_value =\
                ScpMath.bytes_to_int(self.receiver_pkg.acknowledge)
        if (ack_value >= self.base_seq):
            # new packages has been acked
            self.logger.log('rsv', self.receiver_pkg)
            # update base sequence number
            self.base_seq = ack_value + len(self.sender_pkg.payload)
            # remove acked data from buffer
            buffered_package = sorted(list(self.sender_buffer.keys()))
            for seq in buffered_package:
                if (seq < self.base_seq):
                    del self.sender_buffer[seq]
            # reset timer unless buffer is empty
            if (len(self.sender_buffer)):
                self.restart_timer()
                print("restart timer for new base", self.base_seq)
        else:
            # duplicated packages has been acked
            self.logger.log('rsv/DA', self.receiver_pkg)



    def connect(self):
        while(True):
            # send syn and wait
            self.sender_pkg.syn = True
            self.sender_pkg.make_package()
            self.send_package()
            self.receive_package()
            # receive syn & ack
            if (self.receiver_pkg.syn and self.receiver_pkg.ack):
                self.logger.log('rsv', self.receiver_pkg)
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
        # clean the buffer
        while (self.sender_buffer):
            self.retransmit_buffer()
            self.receive_ack()
        self.sender_timer.cancel()
        while(True):
            # send fin and wait
            self.sender_pkg.fin = True
            self.sender_pkg.payload = bytes()
            self.sender_pkg.make_package()
            self.send_package()
            self.receive_package()
            # receive fin & ack
            if (self.receiver_pkg.fin and self.receiver_pkg.ack):
                self.logger.log('rsv', self.receiver_pkg)
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
    # create instance of Sender
    instance = Sender(args)
    instance.connect()
    # read and send file
    with open(args.file, 'rb') as fd:
        data = fd.read(args.MSS)
        while (data):
            instance.send(data)
            data = fd.read(args.MSS)

    # terminate connection
    instance.finish()
    print("\nSend", args.file ,"to", instance.receiver_addr)