# Simple Transport Protocol

## STP package structure

No| segment     | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7
--|-------------|---|---|---|---|---|---|---|---
0 | sequence    |   |   |   |   |   |   |   |   
1 | sequence    |   |   |   |   |   |   |   |   
2 | sequence    |   |   |   |   |   |   |   |   
3 | sequence    |   |   |   |   |   |   |   |   
4 | acknowledge |   |   |   |   |   |   |   |   
5 | acknowledge |   |   |   |   |   |   |   |   
6 | acknowledge |   |   |   |   |   |   |   |   
7 | acknowledge |   |   |   |   |   |   |   |   
8 | flag        |000|000|000|ACK|000|000|SYN|FIN
9 | flag        |000|000|000|ACK|000|000|SYN|FIN
10| window      |   |   |   |   |   |   |   |   
11| window      |   |   |   |   |   |   |   |   
12| checksum    |   |   |   |   |   |   |   |   
13| checksum    |   |   |   |   |   |   |   |   
. | payload     |   |   |   |   |   |   |   |   


## connect

Receiver <--- Sender         SYN
Receiver ---> Sender     SYN ACK 
Receiver <--- Sender     ACK    

## finish

Receiver <--- Sender         FIN
Receiver ---> Sender     FIN ACK 
Receiver <--- Sender     ACK    