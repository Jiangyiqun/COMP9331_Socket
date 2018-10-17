# python3 receiver.py receiver_port file_r.pdf
# python3 receiver.py 2333 new.pdf
import socket, argparse, time
from scp import ScpPackage, ScpLogger, ScpMath


############################# Receiver Class ###########################
class Receiver():
    def __init__(self, args):
        self.receiver_addr = ("0.0.0.0", args.receiver_port)
        self.receiver_buffer = 4096
        self.sender_addr = ""
        self.last_seq = bytes([255, 255, 255, 255])
        self.expected_seq = 0
        # create scpPackage abstraction
        self.sender_pkg = ScpPackage()
        self.receiver_pkg = ScpPackage()
        # create the socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(self.receiver_addr)
        # create a logger
        self.logger = ScpLogger('Receiver_log.txt')
        # used for statistics
        self.handshake_rcv_count = 0
        print("Receiver is listening on:", self.receiver_addr)



    def receive_package(self):
        package, self.sender_addr = \
                self.sock.recvfrom(self.receiver_buffer)
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
            
            # Finish
            # when received a fin, then ack on it
            # wait untill a not fin is received
            if (self.sender_pkg.fin):
                self.handshake_rcv_count += 1
                self.logger.log('rcv', self.sender_pkg)
                # send  ack and wait
                self.receiver_pkg.fin = False
                self.receiver_pkg.ack = True
                self.receiver_pkg.make_package()
                self.send_package()
                self.logger.log('snd', self.receiver_pkg)
                # send  fin and wait
                self.receiver_pkg.fin = True
                self.receiver_pkg.ack = False
                self.receiver_pkg.make_package()
                self.send_package()
                self.logger.log('snd', self.receiver_pkg)
                # wait ack
                self.receive_package()
                self.handshake_rcv_count += 1
                self.logger.log('rcv', self.sender_pkg)
                if (self.sender_pkg.ack):
                    self.sock.close()
                    print("Connection terminated!")
                    self.write_statistic()
                    return False

            # not Finish
            #       this package then goes to next step
            if (self.sender_pkg.validate_package()):
                # package is not corrupted
                if (ScpMath.bytes_to_int(self.sender_pkg.sequence)\
                         == self.expected_seq):
                    # package is in order
                    self.logger.log('rcv', self.sender_pkg)
                    # update last seq & expected sequence
                    self.last_seq = self.sender_pkg.sequence
                    self.expected_seq += len(self.sender_pkg.payload)
                    # ACK on last received in order package
                    self.receiver_pkg.acknowledge = self.last_seq
                    self.send_package()
                    self.logger.log('snd', self.receiver_pkg)
                    # write to file and continue to receive
                    return True
                else:
                    # package is not in order(duplicated)
                    self.logger.log('rcv/DA', self.sender_pkg)
                    # ACK on last received in order package
                    self.receiver_pkg.acknowledge =\
                            self.last_seq
                    self.send_package()
                    self.logger.log('snd/DA', self.receiver_pkg)
                    # continue to receive
            else:   
                # package is corrupted
                self.logger.log('rcv/corr', self.sender_pkg)
                # ACK on last received in order package
                self.receiver_pkg.acknowledge =\
                            self.last_seq
                self.send_package()
                self.logger.log('snd/DA', self.receiver_pkg)


    def listen(self):
        while(True):
            # wait syn
            self.receive_package()
            self.logger.reset_timer()
            if (self.sender_pkg.syn):
                self.handshake_rcv_count += 1
                self.logger.log('rcv', self.sender_pkg)
                # send syn & ack and wait
                self.receiver_pkg.syn = True
                self.receiver_pkg.ack = True
                self.receiver_pkg.make_package()
                self.send_package()
                self.logger.log('snd', self.receiver_pkg)
                self.receive_package()
                if ((not self.sender_pkg.syn) and self.sender_pkg.ack):
                    self.handshake_rcv_count += 1
                    self.logger.log('rcv', self.sender_pkg)
                    self.receiver_pkg.syn = False
                    print("Connection estabilished!")
                    return


    def write_statistic(self):
        # print(self.logger.statistic_bytes)
        # print(self.logger.statistic_count)
        # print(self.handshake_rcv_count)
        statistic = ''
        horizontal_line = '=' * 60 + '\n'

        size_title = 'Amount of data received (bytes):'
        size_count = self.logger.statistic_bytes['rcv']
        size_line = '{:52}{:>7}\n'.format(size_title, size_count)
        
        total_title = 'Total Segments Received:'
        total_count = self.logger.statistic_count['rcv']\
                + self.logger.statistic_count['rcv/DA']\
                + self.logger.statistic_count['rcv/corr']\
                - self.handshake_rcv_count
        total_line = '{:52}{:>7}\n'.format(total_title, total_count)

        data_title = 'Data segments received:'
        data_count = self.logger.statistic_count['rcv']\
                - self.handshake_rcv_count
        data_line = '{:52}{:>7}\n'.format(data_title, data_count)

        corr_title = 'Data segments with Bit Errors:'
        corr_count = self.logger.statistic_count['rcv/corr']
        corr_line = '{:52}{:>7}\n'.format(corr_title, corr_count)

        rcv_da_title = 'Duplicate data segments received:'
        rcv_da_count = self.logger.statistic_count['rcv/DA']
        rcv_da_line = '{:52}{:>7}\n'.format(rcv_da_title, rcv_da_count)

        snd_da_title = 'Duplicate ACKs sent:'
        snd_da_count = self.logger.statistic_count['snd/DA']
        snd_da_line = '{:52}{:>7}\n'.format(snd_da_title, snd_da_count)


        statistic = horizontal_line\
                + size_line + total_line + data_line + corr_line + rcv_da_line + snd_da_line\
                + horizontal_line

        print(statistic)

        with open(self.logger.log_file, 'a') as fd:
            fd.write(statistic)


############################# Main Function ############################
if __name__ == '__main__':
    # get the arguments Receiver
    parser = argparse.ArgumentParser()
    parser.add_argument('receiver_port', type=int)
    parser.add_argument('file_r', type=str)
    args = parser.parse_args()
    
    # create instance of Receiver
    instance = Receiver(args)
    instance.listen()

    # receiver and write
    not_finish = instance.receive()
    with open(args.file_r, 'wb') as fd:
        while(not_finish):
            fd.write(instance.sender_pkg.payload)
            not_finish = instance.receive()
    
    # finish
    print("\nSave file", args.file_r, "from", instance.sender_addr)
