from socket import *
import sys

s = socket(AF_INET,SOCK_DGRAM)
host =sys.argv[1]
port = 2333
buf =1024
addr = (host,port)

file_name=sys.argv[2]

s.sendto(file_name.encode('utf-8'),addr)

f=open(file_name,"rb")
data = f.read(buf)
while (data):
    if(s.sendto(data,addr)):
        data = f.read(buf)
s.close()
f.close()