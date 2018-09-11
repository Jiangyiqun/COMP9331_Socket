## Revision of TCP Congestion Control

### Question 1. Name the loss events that occur at 1 and 2. Explain why the congestion window is changed differently in those two cases.
- 1: duplicate ACK, congestion window reduce to half
- 2: timeout, congestion window set to zero.
- Because timeout is a more serious issue.

### Question 2. What phase of the TCP congestion control algorithm coincides with the circled segment marked by 3 ?
- slow start

### Question 3. What phase of the TCP congestion control algorithm coincides with the circled segment marked by 4 ?
- additive increase

### Question 4: Why is the congestion window increased more rapidly at 3 than at 4?
- because in 3, it increases exponentially

### Question 5: Can you precisely explain what happens to the window after 2 ? 
- it first enter a slow start phase, windows size doubles every RTT
- after it reaches a threshold, which is equal to CWND/2, the CWND increase by 1/CWND every RTT.

