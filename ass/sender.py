#!/home/z5129432/anaconda3/bin/python
# sender receiver_host_ip receiver_port file.pdf MWS MSS gamma
#        pDrop pDuplicate pCorrupt pOrder maxOrder pDelay maxDelay seed

import socket
import argparse


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
            s += ord(msg[i])
        else:
            raise "Something Wrong here"
    # One's Complement
    s = s + (s >> 16)
    s = ~s & 0xffff
    high = s // 256
    low = s % 256
    return high, low


def add_checksum(data):
    # print(data)
    checksum = get_checksum(data)
    print("send package with checksum: ", checksum)
    checksum = bytes(list(checksum))
    return checksum + data


if __name__ == '__main__':
    host = "0.0.0.0"
    buffer_size = 512
    args = get_args()
    address = (args.receiver_host_ip, args.receiver_port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    with open(args.file, 'rb') as fd:
        data = fd.read(buffer_size)
        while (data):
            data = add_checksum(data)
            if(sock.sendto(data, address)):
                data = fd.read(buffer_size)
    sock.close()
    print("Send", args.file ,"to", address)