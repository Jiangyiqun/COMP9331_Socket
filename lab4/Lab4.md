# Excercise 1
## Question 1 . 

### What is the IP address of gaia.cs.umass.edu? 
128.119.245.12

### On what port number is it sending and receiving TCP segments for this connection? 
80

### What is the IP address and TCP port number used by the client computer (source) that is transferring the file to gaia.cs.umass.edu?
192.168.1.102: 1161

## Question 2.

### What is the sequence number of the TCP segment containing the HTTP POST command? Note that in order to find the POST command, you’ll need to dig into the packet content field at the bottom of the Ethereal window, looking for a segment with a “POST” within its DATA field.
232129013

## Question 3. Consider the TCP segment containing the HTTP POST as the first segment in the TCP connection. What are the sequence numbers of the first six segments in the TCP connection (including the segment containing the HTTP POST) sent from the client to the web server (Do not consider the ACKs received from the server as part of these six segments)? At what time was each segment sent? When was the ACK for each segment received? Given the difference between when each TCP segment was sent, and when its acknowledgement was received, what is the RTT value for each of the six segments? What is the EstimatedRTT value (see relevant parts of Section 3.5 or lecture slides) after the receipt of each ACK? Assume that the initial value of EstimatedRTT is equal to the measured RTT ( SampleRTT ) for the first segment, and then is computed using the EstimatedRTT equation for all subsequent segments. Set alpha to 0.125. 
sequence No.| sent time | ACK time | sampleRTT | EstimatedRTT
------------|-----------|----------|-----------|-------------
232129013   | 0.026477  | 0.053937 | 0.027460  | 0.027460
232129578   | 0.041737  | 0.077294 | 0.035557  | 0.028472
232131038   | 0.054026  | 0.124085 | 0.070059  | 0.033670
232132498   | 0.054690  | 0.169118 | 0.114428  | 0.043765
232133958   | 0.077405  | 0.217299 | 0.139894  | 0.055781
232135418   | 0.078157  | 0.267802 | 0.189645  | 0.072514

# Excercise 2

##  Question 1 . What is the sequence number of the TCP SYN segment that is used to initiate the TCP connection between the client computer and server?
2818463618

## Question 2. 
### What is the sequence number of the SYNACK segment sent by the server to the client computer in reply to the SYN? 
1247095790

### What is the value of the Acknowledgement field in the SYNACK segment? 
2818463619

### How did the server determine that value?
increase the sequence number in the initial connection by 1


## Question 3 . 
### What is the sequence number of the ACK segment sent by the client computer in response to the SYNACK? 
2818463619

### What is the value of the Acknowledgment field in this ACK segment? 
1247095790

### Does this segment contain any data?
Yes, the length of data is (2818463652- 2818463619 - 1)

## Question 4 . 
### Who has done the active close? client or the server? how you have determined this?
the client. In No 304, the client send FIN.

### What type of closure has been performed? 3 Segment (FIN/FINACK/ACK), 4 Segment (FIN/ACK/FIN/ACK) or Simultaneous close?
Simultaneous close

## Question 5 . 
### How many data bytes have been transferred from the client to the server and from the server to the client during the whole duration of the connection? What relationship does this have with the Initial Sequence Number and the final ACK received from the other side?  
from client to server: 2818463653(client initial sequence number) - 2818463618(server final ACK) = 35 bytes
from server to client: 1247095832(server initial sequence number) - 1247095790(client final ACK) = 42 bytes