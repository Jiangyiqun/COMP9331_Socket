#!/usr/bin/python3
#/home/z5129432/anaconda3/bin/python
# receiver receiver_port file_r.pdf
import socket
import argparse
import select
# from sender import get_checksum

def get_args ():
    parser = argparse.ArgumentParser()
    parser.add_argument('receiver_port', type=int)
    parser.add_argument('file_r', type=str)
    args = parser.parse_args()
    return args


def get_checksum(msg):
    # acknowlegement:
    # modified from blog 
    # http://www.bitforestinfo.com/2018/01/python-codes-to-calculate-tcp-checksum.html
    #
    s = 0       # Binary Sum
    # loop taking 2 characters at a time
    for i in range(0, len(msg), 2):
        if (i+1) < len(msg):
            a = msg[i]
            b = msg[i+1]
            s = s + (a+(b << 8))
        elif (i+1)==len(msg):
            s += msg[i]
        else:
            raise "Something Wrong here"
    # One's Complement
    s = s + (s >> 16)
    s = ~s & 0xffff
    high = s // 256
    low = s % 256
    return high, low
     


def check_checksum(msg):
    # acknowlegement:
    # modified from blog 
    # http://www.bitforestinfo.com/2018/01/python-codes-to-calculate-tcp-checksum.html
    #
    s = 0       # Binary Sum
    # loop taking 2 characters at a time
    for i in range(0, len(msg), 2):
        if (i+1) < len(msg):
            a = msg[i]
            b = msg[i+1]
            s = s + (a+(b << 8))
        elif (i+1)==len(msg):
            s += msg[i]
        else:
            raise "Something Wrong here"
    # One's Complement
    # s = s + (s >> 16)
    # s = ~s & 0xffff
    # high = s // 256
    # low = s % 256
    return s




class Receiver():
    def __init__(self, receiver_addr, buffer_size):
        self.receiver_addr = receiver_addr
        self.buffer_size = buffer_size
        self.sender_addr = ""
        self.package = bytes()
        self.payload = bytes()
        self.checksum = bytes()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(receiver_addr)
        print("Receiver is listening on:", receiver_addr, "\n")
    def receive_package(self):
        self.package, self.sender_addr = self.sock.recvfrom(buffer_size)
        self.payload = self.package[2:]
        self.checksum = (self.package[0], self.package[1])
    def payload_checksum_matches(self):
        payload_checksum = get_checksum(instance.payload)
        print("receive package with checksum: ", payload_checksum)
        if (payload_checksum == instance.checksum):
            return True
        else:
            print("receive package withpayload checksum: ",
                    payload_checksum,
                    "header checksum: ",
                    instance.checksum)
            return False
    def package_checksum_matches(self):
        package_checksum = check_checksum(instance.package)
        print("receive package with checksum: ", package_checksum)
        return True
        # if (payload_checksum == instance.checksum):
        #     return True
        # else:
        #     print("receive package withpayload checksum: ",
        #             payload_checksum,
        #             "header checksum: ",
        #             instance.checksum)
        #     return False
    def send_ACK(self):
        self.sock.sendto(bytes([1]), self.sender_addr)
    def send_NAK(self):
        self.sock.sendto(bytes([0]), self.sender_addr)
    def close(self):
        self.sock.close()
    def receive_good_package(self):
        while(True):
            self.receive_package()
            if self.package_checksum_matches():
                print("send ACK to: ", self.sender_addr)
                self.send_ACK()
                break
            else:
                print("send NAK to: ", self.sender_addr)
                self.send_NAK()



if __name__ == '__main__':
    args = get_args()
    host = "0.0.0.0"
    buffer_size = 1024
    receiver_addr = (host, args.receiver_port)
    instance = Receiver(receiver_addr, buffer_size)

    instance.receive_good_package()
    with open(args.file_r, 'wb') as fd:
        try:
            while(instance.package):
                fd.write(instance.payload)
                instance.sock.settimeout(2)
                instance.receive_good_package()
        except socket.timeout:
            instance.close()
            print("\nSave file", args.file_r, "from", instance.sender_addr)
