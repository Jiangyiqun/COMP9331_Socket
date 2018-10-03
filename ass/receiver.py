#!/home/z5129432/anaconda3/bin/python
# receiver receiver_port file_r.pdf
import socket
import argparse
import select




def get_args ():
    parser = argparse.ArgumentParser()
    parser.add_argument('receiver_port', type=int)
    parser.add_argument('file_r', type=str)
    args = parser.parse_args()
    return args


def bind_socket(address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(address)
    print("Receiver is listening on:", address)
    return sock


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


def process_checksum(data):
    data_checksum = (data[0], data[1])
    data_payload = data[2:]
    real_checksum = get_checksum(data_payload)
    print("real_checksum = ", real_checksum)
    print("data_checksum = ", data_checksum)
    if (real_checksum == data_checksum):
        return data_payload
    else:
        return False
     



if __name__ == '__main__':
    host = "0.0.0.0"
    buffer_size = 1024
    args = get_args()
    address = (host, args.receiver_port)
    sock = bind_socket(address)
    
    data, addr = sock.recvfrom(buffer_size)
    data_payload = process_checksum(data)
    if (not data_payload):
        print("data is corrupted!\n")
        exit(1)
    with open(args.file_r, 'wb') as fd:
        try:
            while(data):
                fd.write(data)
                sock.settimeout(2)
                data,addr = sock.recvfrom(buffer_size)
                data_payload = process_checksum(data)
                if (not data_payload):
                    print("data is corrupted!\n")
                    exit(1)
        except socket.timeout:
            sock.close()
            print("Received file from", addr)
