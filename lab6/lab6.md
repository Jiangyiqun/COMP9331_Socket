# Exercise 1: Understanding the Impact of Network Dynamics on Routing

## Question 1. 

### Which nodes communicate with which other nodes? 
- 1~5
- 2~5

### Which route do the packets follow? 
- 0->1->4->5
- 2->3->5

### Does it change over time?  
- not change

## Question 2:

### What happens at time 1.0 and at time 1.2?
- route between node 1 and 4 disconnected at 1.0 and reconnected at time 1.2

### Does the route between the communicating nodes change as a result of that? 
- not change

## Question 3:

### Did you observe any additional traffic as compared to Step 3 above?
- yes, it happens at the beginning and at time 1.0

### How does the network react to the changes that take place at time 1.0 and time 1.2 now? 
- the route between node 1 and 4 is disconnected, so it change the route to 0->1->2->3->5

## Question 4: How does this change affect the routing? Explain why. 
- the route change to 0->1->2->3->5 and 2->3->5
- because the cost between node 1 and 4 increased, so it is not the most opitimal route

## Question 5: Describe what happens and deduce the effect of the line you just uncommented.
- traffic from 2 to 5 takes two route, which are 2->1->4->5 and 2->3-5
- the line uncommented allowed take multi-route when the cost are equal

## Exercise 2: Setting up NS2 simulation for measuring TCP throughput 

## Exercise 3: Understanding IP Fragmentation

## Question 1: 

### Which data size has caused fragmentation and why?
- 2000 bytes and 3500 bytes
- because the MTU is 1500 bytes
  
### Which host/router has fragmented the original datagram?
- the source host
  
### How many fragments have been created when data size is specified as 2000?
- 2
  
## Question 2: Did the reply from the destination 8.8.8.8. for 3500-byte data size also get fragmented? Why and why not?
- yes
- three fragments can be seen in wireshark
  
## Question 3: Give the ID, length, flag and offset values for all the fragments of the first packet sent by 192.168.1.103 with data size of 3500 bytes?

ID | length     | flag | offset
---|------------|------|--------
39 | 1480 bytes | MF=1 | 0
40 | 1480 bytes | MF=1 | 185
41 | 548 bytes  | MF=1 | 370

## Question 4: Has fragmentation of fragments occurred when data of size 3500 bytes has been used? Why and why not?
- No
- it has 3 fragments, each with less than 1480 bytes
  
## Question 5: What will happen if for our example one fragment of the original datagram from 192.168.1.103 is lost? 
- it will drop the whole package