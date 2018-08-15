# COMP9331 lab3 report

- Author: Yiqun Jiang
- zID: z5129432
- Date: Aug 15, 2018

## Question 1. What is the IP address of www.cecs.anu.edu.au . What type of DNS query is sent to get this answer?

- IP address: 150.203.161.98
- DNS query: dig www.cecs.anu.edu.au

```bash
->~dig www.cecs.anu.edu.au

; <<>> DiG 9.10.3-P4-Ubuntu <<>> www.cecs.anu.edu.au
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 60950
;; flags: qr rd ra; QUERY: 1, ANSWER: 2, AUTHORITY: 3, ADDITIONAL: 7

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;www.cecs.anu.edu.au.		IN	A

;; ANSWER SECTION:
www.cecs.anu.edu.au.	3242	IN	CNAME	rproxy.cecs.anu.edu.au.
rproxy.cecs.anu.edu.au.	3242	IN	A	150.203.161.98

;; AUTHORITY SECTION:
cecs.anu.edu.au.	1442	IN	NS	ns3.cecs.anu.edu.au.
cecs.anu.edu.au.	1442	IN	NS	ns4.cecs.anu.edu.au.
cecs.anu.edu.au.	1442	IN	NS	ns2.cecs.anu.edu.au.

;; ADDITIONAL SECTION:
ns3.cecs.anu.edu.au.	1442	IN	A	150.203.161.50
ns3.cecs.anu.edu.au.	1442	IN	AAAA	2001:388:1034:2905::32
ns4.cecs.anu.edu.au.	1335	IN	A	150.203.161.38
ns4.cecs.anu.edu.au.	1442	IN	AAAA	2001:388:1034:2905::26
ns2.cecs.anu.edu.au.	1444	IN	A	150.203.161.36
ns2.cecs.anu.edu.au.	1442	IN	AAAA	2001:388:1034:2905::24

;; Query time: 7 msec
;; SERVER: 127.0.1.1#53(127.0.1.1)
;; WHEN: Wed Aug 15 19:45:34 AEST 2018
;; MSG SIZE  rcvd: 271
```

## Question 2. What is the canonical name for the CECS ANU web server? What is its IP address? Suggest a reason for having an alias for this server.

- canonical name: rproxy.cecs.anu.edu.au
- IP address: 150.203.161.98
- reason: Customize a service address

## Question 3. What can you make of the rest of the response (i.e. the details available in the Authority and Additional sections)?

- if I want to know the IP address of the subdomain, I can query it from the nameserver.

## Question 4. What is the IP address of the local nameserver for your machine?

- 127.0.0.1

```bash
->~ dig localhost

; <<>> DiG 9.10.3-P4-Ubuntu <<>> localhost
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 50568
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 1, ADDITIONAL: 2

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;localhost.			IN	A

;; ANSWER SECTION:
localhost.		86400	IN	A	127.0.0.1

;; AUTHORITY SECTION:
localhost.		86400	IN	NS	localhost.

;; ADDITIONAL SECTION:
localhost.		86400	IN	AAAA	::1

;; Query time: 119 msec
;; SERVER: 127.0.1.1#53(127.0.1.1)
;; WHEN: Wed Aug 15 20:09:43 AEST 2018
;; MSG SIZE  rcvd: 96

```

## Question 5. What are the DNS nameservers for the “cecs.anu.edu.au” domain (note: the domain name is cecs.anu.edu.au and not www.cecs.anu.edu.au )? Find out their IP addresses? What type of DNS query is sent to obtain this information?

- DNS nameservers: 
    - ns2.cecs.anu.edu.au
    - ns3.cecs.anu.edu.au
    - ns4.cecs.anu.edu.au
- IP addresses:
    - 150.203.161.50
    - 150.203.161.36
    - 150.203.161.38
  
```bash
->~ dig cecs.anu.edu.au

; <<>> DiG 9.10.3-P4-Ubuntu <<>> cecs.anu.edu.au
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 15730
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 3, ADDITIONAL: 7

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;cecs.anu.edu.au.		IN	A

;; ANSWER SECTION:
cecs.anu.edu.au.	3600	IN	A	150.203.161.98

;; AUTHORITY SECTION:
cecs.anu.edu.au.	823	IN	NS	ns3.cecs.anu.edu.au.
cecs.anu.edu.au.	823	IN	NS	ns4.cecs.anu.edu.au.
cecs.anu.edu.au.	823	IN	NS	ns2.cecs.anu.edu.au.

;; ADDITIONAL SECTION:
ns3.cecs.anu.edu.au.	2903	IN	A	150.203.161.50
ns3.cecs.anu.edu.au.	2903	IN	AAAA	2001:388:1034:2905::32
ns2.cecs.anu.edu.au.	3367	IN	A	150.203.161.36
ns2.cecs.anu.edu.au.	823	IN	AAAA	2001:388:1034:2905::24
ns4.cecs.anu.edu.au.	724	IN	A	150.203.161.38
ns4.cecs.anu.edu.au.	823	IN	AAAA	2001:388:1034:2905::26

;; Query time: 14 msec
;; SERVER: 127.0.1.1#53(127.0.1.1)
;; WHEN: Wed Aug 15 20:11:43 AEST 2018
;; MSG SIZE  rcvd: 246
```

## Question 6. What is the DNS name associated with the IP address 149.171.158.109? What type of DNS query is sent to obtain this information?

- DNS name:
    - engplws008.ad.unsw.edu.au
    - engplws008.eng.unsw.edu.au
    - www.engineering.unsw.edu.au

```bash
->~ dig -x 149.171.158.109

; <<>> DiG 9.10.3-P4-Ubuntu <<>> -x 149.171.158.109
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 10872
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 3, AUTHORITY: 3, ADDITIONAL: 7

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;109.158.171.149.in-addr.arpa.	IN	PTR

;; ANSWER SECTION:
109.158.171.149.in-addr.arpa. 3600 IN	PTR	engplws008.ad.unsw.edu.au.
109.158.171.149.in-addr.arpa. 3600 IN	PTR	engplws008.eng.unsw.edu.au.
109.158.171.149.in-addr.arpa. 3600 IN	PTR	www.engineering.unsw.edu.au.

;; AUTHORITY SECTION:
158.171.149.in-addr.arpa. 10800	IN	NS	ns2.unsw.edu.au.
158.171.149.in-addr.arpa. 10800	IN	NS	ns3.unsw.edu.au.
158.171.149.in-addr.arpa. 10800	IN	NS	ns1.unsw.edu.au.

;; ADDITIONAL SECTION:
ns1.unsw.edu.au.	10800	IN	A	129.94.0.192
ns1.unsw.edu.au.	10800	IN	AAAA	2001:388:c:35::1
ns2.unsw.edu.au.	10800	IN	A	129.94.0.193
ns2.unsw.edu.au.	10800	IN	AAAA	2001:388:c:35::2
ns3.unsw.edu.au.	10800	IN	A	192.155.82.178
ns3.unsw.edu.au.	10800	IN	AAAA	2600:3c01::f03c:91ff:fe73:5f10

;; Query time: 5 msec
;; SERVER: 127.0.1.1#53(127.0.1.1)
;; WHEN: Wed Aug 15 20:13:53 AEST 2018
;; MSG SIZE  rcvd: 341
```

## Question 7. Run dig and query the CSE nameserver (129.94.242.33) for the mail servers for Yahoo! Mail (again the domain name is yahoo.com, not www.yahoo.com ). Did you get an authoritative answer? Why? (HINT: Just because a response contains information in the authoritative part of the DNS response message does not mean it came from an authoritative name server. You should examine the flags in the response to determine the answer)

- mail servers:
    - mta5.am0.yahoodns.net
    - mta6.am0.yahoodns.net
    - mta7.am0.yahoodns.net
- No, because this server has been cached

```bash
->~ dig @129.94.242.33 yahoo.com mx

; <<>> DiG 9.10.3-P4-Ubuntu <<>> @129.94.242.33 yahoo.com mx
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 25281
;; flags: qr rd ra; QUERY: 1, ANSWER: 3, AUTHORITY: 5, ADDITIONAL: 9

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;yahoo.com.			IN	MX

;; ANSWER SECTION:
yahoo.com.		1403	IN	MX	1 mta5.am0.yahoodns.net.
yahoo.com.		1403	IN	MX	1 mta6.am0.yahoodns.net.
yahoo.com.		1403	IN	MX	1 mta7.am0.yahoodns.net.

;; AUTHORITY SECTION:
yahoo.com.		76222	IN	NS	ns2.yahoo.com.
yahoo.com.		76222	IN	NS	ns5.yahoo.com.
yahoo.com.		76222	IN	NS	ns1.yahoo.com.
yahoo.com.		76222	IN	NS	ns4.yahoo.com.
yahoo.com.		76222	IN	NS	ns3.yahoo.com.

;; ADDITIONAL SECTION:
ns1.yahoo.com.		162610	IN	A	68.180.131.16
ns1.yahoo.com.		63220	IN	AAAA	2001:4998:130::1001
ns2.yahoo.com.		560161	IN	A	68.142.255.16
ns2.yahoo.com.		41761	IN	AAAA	2001:4998:140::1002
ns3.yahoo.com.		229209	IN	A	203.84.221.53
ns3.yahoo.com.		9514	IN	AAAA	2406:8600:b8:fe03::1003
ns4.yahoo.com.		145511	IN	A	98.138.11.157
ns5.yahoo.com.		153555	IN	A	119.160.253.83

;; Query time: 8 msec
;; SERVER: 129.94.242.33#53(129.94.242.33)
;; WHEN: Wed Aug 15 20:29:44 AEST 2018
;; MSG SIZE  rcvd: 371
```

```bash
->~ nslookup yahoo.com
Server:		127.0.1.1
Address:	127.0.1.1#53

Non-authoritative answer:
Name:	yahoo.com
Address: 98.137.246.8
Name:	yahoo.com
Address: 98.137.246.7
Name:	yahoo.com
Address: 72.30.35.9
Name:	yahoo.com
Address: 98.138.219.231
Name:	yahoo.com
Address: 98.138.219.232
Name:	yahoo.com
Address: 72.30.35.10
```

## Question 8. Repeat the above (i.e. ## Question 7) but use one of the nameservers obtained in ## Question 5. What is the result?


```bash
->~ dig @150.203.161.36 yahoo.com mx

; <<>> DiG 9.10.3-P4-Ubuntu <<>> @150.203.161.36 yahoo.com mx
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: REFUSED, id: 45548
;; flags: qr rd; QUERY: 1, ANSWER: 0, AUTHORITY: 0, ADDITIONAL: 1
;; WARNING: recursion requested but not available

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;yahoo.com.			IN	MX

;; Query time: 9 msec
;; SERVER: 150.203.161.36#53(150.203.161.36)
;; WHEN: Wed Aug 15 20:36:47 AEST 2018
;; MSG SIZE  rcvd: 38

```

## Question 9. Obtain the authoritative answer for the mail servers for Yahoo! mail. What type of DNS query is sent to obtain this information?

- dig @ns1.yahoo.com yahoo.com MX

```bash
->~ dig yahoo.com NS

; <<>> DiG 9.10.3-P4-Ubuntu <<>> yahoo.com NS
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 29756
;; flags: qr rd ra; QUERY: 1, ANSWER: 5, AUTHORITY: 0, ADDITIONAL: 9

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;yahoo.com.			IN	NS

;; ANSWER SECTION:
yahoo.com.		168736	IN	NS	ns5.yahoo.com.
yahoo.com.		168736	IN	NS	ns2.yahoo.com.
yahoo.com.		168736	IN	NS	ns4.yahoo.com.
yahoo.com.		168736	IN	NS	ns1.yahoo.com.
yahoo.com.		168736	IN	NS	ns3.yahoo.com.

;; ADDITIONAL SECTION:
ns3.yahoo.com.		329154	IN	A	203.84.221.53
ns3.yahoo.com.		133597	IN	AAAA	2406:8600:b8:fe03::1003
ns5.yahoo.com.		134697	IN	A	119.160.253.83
ns4.yahoo.com.		219984	IN	A	98.138.11.157
ns2.yahoo.com.		138170	IN	A	68.142.255.16
ns2.yahoo.com.		133597	IN	AAAA	2001:4998:140::1002
ns1.yahoo.com.		155005	IN	A	68.180.131.16
ns1.yahoo.com.		62683	IN	AAAA	2001:4998:130::1001

;; Query time: 7 msec
;; SERVER: 127.0.1.1#53(127.0.1.1)
;; WHEN: Wed Aug 15 20:38:40 AEST 2018
;; MSG SIZE  rcvd: 292
```

```bash
->~ dig @ns1.yahoo.com yahoo.com MX

; <<>> DiG 9.10.3-P4-Ubuntu <<>> @ns1.yahoo.com yahoo.com MX
; (2 servers found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 36984
;; flags: qr aa rd; QUERY: 1, ANSWER: 3, AUTHORITY: 5, ADDITIONAL: 9
;; WARNING: recursion requested but not available

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1272
;; QUESTION SECTION:
;yahoo.com.			IN	MX

;; ANSWER SECTION:
yahoo.com.		1800	IN	MX	1 mta7.am0.yahoodns.net.
yahoo.com.		1800	IN	MX	1 mta6.am0.yahoodns.net.
yahoo.com.		1800	IN	MX	1 mta5.am0.yahoodns.net.

;; AUTHORITY SECTION:
yahoo.com.		172800	IN	NS	ns1.yahoo.com.
yahoo.com.		172800	IN	NS	ns3.yahoo.com.
yahoo.com.		172800	IN	NS	ns2.yahoo.com.
yahoo.com.		172800	IN	NS	ns4.yahoo.com.
yahoo.com.		172800	IN	NS	ns5.yahoo.com.

;; ADDITIONAL SECTION:
ns1.yahoo.com.		1209600	IN	A	68.180.131.16
ns2.yahoo.com.		1209600	IN	A	68.142.255.16
ns3.yahoo.com.		1209600	IN	A	203.84.221.53
ns4.yahoo.com.		1209600	IN	A	98.138.11.157
ns5.yahoo.com.		1209600	IN	A	119.160.253.83
ns1.yahoo.com.		86400	IN	AAAA	2001:4998:130::1001
ns2.yahoo.com.		86400	IN	AAAA	2001:4998:140::1002
ns3.yahoo.com.		86400	IN	AAAA	2406:8600:b8:fe03::1003

;; Query time: 240 msec
;; SERVER: 68.180.131.16#53(68.180.131.16)
;; WHEN: Wed Aug 15 20:39:16 AEST 2018
;; MSG SIZE  rcvd: 371
```

## Question 10. In this exercise you simulate the iterative DNS query process to find the IP address of your machine (e.g. lyre00.cse.unsw.edu.au). First, find the name server (query type NS) of the "." domain (root domain). Query this nameserver to find the authoritative name server for the "au." domain. Query this second server to find the authoritative nameserver for the "edu.au." domain. Now query this nameserver to find the authoritative nameserver for "unsw.edu.au". Next query the nameserver of unsw.edu.au to find the authoritative name server of cse.unsw.edu.au. Now query the nameserver of cse.unsw.edu.au to find the IP address of your host. How many DNS servers do you have to query to get the authoritative answer?

## Question 11. Can one physical machine have several names and/or IP addresses associated with it? 