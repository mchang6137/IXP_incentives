#!/usr/bin/python

#Takes the output of a MRT BGP RIB human-printed (using bgpdump) and calculates the number of prefixes that goes through the next hop IP address

BGP_FILE = './ribTables/kenyaIXP2016Readable.txt'
as_to_prefixCount = {}

file = open(BGP_FILE, "r")

#Iterate through the BGP File
while True:
    line = file.readline()
    bgp_index = line.split(":")
    
    if not line: break

    prefix = ''
    AS = ''

    if bgp_index[0]=='PREFIX':
        prefix = bgp_index[1]
    elif bgp_index[0]=='ASPATH':
        #Retrieve the last item in the AS Path. This is the AS where the destination prefix is
        AS = bgp_index[1][1:].split(' ')[-1].strip('\n')
    else:
        continue
            
    if AS in as_to_prefixCount:
        as_to_prefixCount[AS] = as_to_prefixCount[AS] + 1
    else:
        as_to_prefixCount[AS] = 1

#print entries
for entry in as_to_prefixCount:
    if entry == '':
        print "Total entries: " + str(as_to_prefixCount[entry])
    else:
        print entry + ": " + str(as_to_prefixCount[entry])


