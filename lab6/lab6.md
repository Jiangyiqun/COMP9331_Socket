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
