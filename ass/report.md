# Simple Transport Protocol

## STP package structure

No| segment     | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7
--|-------------|---|---|---|---|---|---|---|---
0 | sequence    |   |   |   |   |   |   |   |   
1 | acknowledge |   |   |   |   |   |   |   |   
2 | flag        |000|000|000|ACK|000|000|SYN|FIN
3 | window      |   |   |   |   |   |   |   |   
4 | checksum    |   |   |   |   |   |   |   |   
5 | checksum    |   |   |   |   |   |   |   |   
. | payload     |   |   |   |   |   |   |   |   


## connect

Receiver <--- Sender         SYN
Receiver ---> Sender     SYN ACK 
Receiver <--- Sender     ACK    

## finish

Receiver <--- Sender         FIN
Receiver ---> Sender     FIN ACK 
Receiver <--- Sender     ACK    