#!/usr/bin/python3
with open("test0.pdf", 'rb') as fd:
    data = fd.read(512)
    print(len(data))