# python3 sender.py receiver_host_ip receiver_port file.pdf MWS MSS gamma
#          pDrop pDuplicate pCorrupt pOrder maxOrder pDelay maxDelay seed
# python3 sender.py localhost 2333 test0.pdf 512 512 4 0 0 0 0 0 0.2 100 0

import socket, argparse, random, threading, time
from scp import ScpPackage, ScpLogger, ScpMath, HEADER_SIZE


########################## RTTEstimator Class ##########################
class RTTEstimator():
    def __init__(self, gamma):
        # varibles for calculating timeout
        self.alpha = 0.125
        self.beta = 0.25
        self.gamma = gamma
        self.estimate_interval = 5 # estimate every 10 packages
        self.sample_start = 0
        self.sample_end = 0
        self.sampleRTT = 0
        self.EstimatedRTT = 0.5
        self.DevRTT = 0
        self.timeout = self.EstimatedRTT
        # other varibles
        self.estimating = False # whether is estimating timeout or not
        self.count = 0
        self.seq = bytes([0, 0, 0, 0])


    def monitor_sender_package(self, seq):
        # insert before send package
        if (not self.estimating):
            if (self.count >= self.estimate_interval):
                # start estimate
                self.estimating = True
                self.count = 0
                self.sample_start = time.time()
                self.seq = seq
            else:
                self.count += 1

    def monitor_receiver_package(self, ack):
        # insert before receive package
        if (self.estimating):
            if (ack == self.seq):
                # update timeout and finish estimate procedure
                self.sample_end = time.time()
                self.estimating = False
                self.get_sampleRTT()
                # print("sampleRTT =", self.sampleRTT)
                self.get_EstimatedRTT()
                # print("EstimatedRTT =", self.EstimatedRTT)
                self.get_DevRTT()
                # print("DevRTT =", self.DevRTT)
                self.get_timeout()
                print("timeout updated to:", self.timeout)

    def get_sampleRTT(self):
        self.sampleRTT = self.sample_end - self.sample_start

    def get_EstimatedRTT(self):
        self.EstimatedRTT = (1 - self.alpha) * self.EstimatedRTT\
                          + self.alpha * self.sampleRTT

    def get_DevRTT(self):
        self.DevRTT = (1 - self.beta) * self.DevRTT\
                    + self.beta * abs(self.sampleRTT - self.EstimatedRTT)

    def get_timeout(self):
        self.timeout = self.EstimatedRTT + self.gamma * self.DevRTT



############################# Sender Class #############################
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
        self.estimator = RTTEstimator(self.args.gamma)
        self.duplicated_ack = 0
        self.sender_timer = threading.Timer(\
                self.estimator.timeout, self.retransmit_buffer)
        # for reorder send and delay send
        self.reordered_pkg = ScpPackage()
        self.delayed_pkg = ScpPackage()
        # 0 means nothing in the queue
        self.reorder_send_countdown = 0
        self.delay_send_time = 0
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
        self.estimator.monitor_sender_package(self.sender_pkg.sequence)
        sent_bytes = 0

        # check for reorder send
        if (self.reorder_send_countdown):
            # something has been reorderd need to be sent
            self.reorder_send_countdown -= 1
            if (self.reorder_send_countdown == 0):
                # now we can send
                sent_bytes = self.sock.sendto(\
                        self.reordered_pkg.package, self.receiver_addr)
                self.logger.log('snd/rord', self.reordered_pkg)

        # check for delayed send
        if (self.delay_send_time):
            # something has been reorderd need to be sent
            now = time.time()
            if (now >= self.delay_send_time):
                # now we can send
                sent_bytes = self.sock.sendto(\
                        self.delayed_pkg.package, self.receiver_addr)
                self.logger.log('snd/dely', self.reordered_pkg)
                self.delay_send_time = 0 # clear the flag

        # PLD module
        if (random.random() < self.args.pDrop):
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
        elif (self.reorder_send_countdown == 0\
                and random.random() < self.args.pOrder):
            self.reordered_pkg.extract_package(self.sender_pkg.package)
            self.reorder_send_countdown = self.args.maxOrder
        elif (self.delay_send_time == 0\
                and random.random() < self.args.pDelay):
            self.delayed_pkg.extract_package(self.sender_pkg.package)
            self.delay_send_time = time.time()\
                    + self.args.maxDelay / 1000
        else:
            sent_bytes = self.sock.sendto(\
                    self.sender_pkg.package, self.receiver_addr)
            self.logger.log('snd', self.sender_pkg)
        return sent_bytes


    def receive_package(self):
        package, receiver_address = self.sock.recvfrom(HEADER_SIZE)
        self.receiver_pkg.extract_package(package)
        self.estimator.monitor_receiver_package(\
                self.receiver_pkg.acknowledge)
        return receiver_address


    def restart_timer(self):
        self.sender_timer.cancel()
        self.sender_timer = threading.Timer(\
                self.estimator.timeout, self.retransmit_buffer) 
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
        print("retransmit on buffer", buffered_package)
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
            # reset duplicated ack counter if valid ack received
            self.duplicated_ack = 0
        else:
            # duplicated packages has been acked
            self.logger.log('rsv/DA', self.receiver_pkg)
            # increse counter for fast retransmit
            self.duplicated_ack += 1
            # fast retransmit and reset counter
            if (self.duplicated_ack >= 3):
                self.retransmit_buffer()
                self.duplicated_ack = 0
            



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
        print("Finishing up!")
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
            self.logger.log('rsv', self.receiver_pkg)
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




############################# Main Function ############################
if __name__ == '__main__':
    # get the arguments Sender
    parser = argparse.ArgumentParser()
    parser.add_argument('receiver_host_ip', type=str)
    parser.add_argument('receiver_port', type=int)
    parser.add_argument('file', type=str)
    parser.add_argument('MWS', type=int)
    parser.add_argument('MSS', type=int)
    parser.add_argument('gamma', type=int)
    parser.add_argument('pDrop', type=float)
    parser.add_argument('pDuplicate', type=float)
    parser.add_argument('pCorrupt', type=float)
    parser.add_argument('pOrder', type=float)
    parser.add_argument('maxOrder', type=int, choices=range(0, 7))
    parser.add_argument('pDelay', type=float)
    parser.add_argument('maxDelay', type=float)
    parser.add_argument('seed', type=str)
    args = parser.parse_args()

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