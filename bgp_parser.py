#!/usr/bin/python

#Takes the output of a MRT BGP RIB human-printed (using bgpdump) and calculates the number of prefixes advertised by each next hop IP Address

BGP_FILE = 'kenyaIXP2016Readable.txt'
nextHop_to_prefixCount = {}

file = open(BGP_FILE, "r")

#Iterate through the BGP File
while True:
    line = file.readline()
    bgp_index = line.split(":")
    
    if not line: break

    prefix = ''
    next_hop = ''

    if bgp_index[0]=='PREFIX':
        prefix = bgp_index[1]
        prefix.strip('\n')
    
    if bgp_index[0]=='NEXT_HOP':
        next_hop = bgp_index[1].replace('\n', '')
        
    if next_hop in nextHop_to_prefixCount:
        nextHop_to_prefixCount[next_hop] = nextHop_to_prefixCount[next_hop] + 1
    else:
        nextHop_to_prefixCount[next_hop] = 1

#print entries
for entry in nextHop_to_prefixCount:
    print entry + ": " + str(nextHop_to_prefixCount[entry])
