from socket import *
import time
import sys

serverName = sys.argv[1]
serverPort = int(sys.argv[2])


clientSocket = socket(AF_INET,SOCK_DGRAM)
clientSocket.settimeout(1.0)
time_list = []
sum_time = 0

for i in range(10):
    before_send_time = time.time()
    message = ('PING'+ ' '+str(i) + ' ' + str(before_send_time)).encode()
    #print(message)
    clientSocket.sendto(message,(serverName,serverPort))

    try:
        modifedMessage, serverAddress = clientSocket.recvfrom(2048)
        rtt = time.time() - before_send_time
        print('ping to %s , seq = %d , rtt = %.0f ms' % (serverName, i, rtt * 1000))
        time_list.append(rtt*1000)
        sum_time += rtt*1000
    except Exception as t:           # transmitted successfully
        print('ping to %s , seq = %d , has been time out' % (serverName, i))

#time_list.sort()s
#print(time_list)
print('MAX RTT: %.0f ms' % (max(time_list)))
print('MIN RTT: %.0f ms' % (min(time_list)))

print('AVG RTT: %.0f ms' % (sum_time / len(time_list)))
clientSocket.close()