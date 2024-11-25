from scapy import all as scapy
import lz4.frame
import gzip
import zlib
import lzma

total = 0
count = 0
gziptotal = 0
lz4total = 0
gzipuncomp = 0
lz4uncomp = 0
zlibtotal = 0
lzmatotal = 0
excluded = 0
for pkt in scapy.PcapReader('curleddebianiso.pcapng'):
    pack = bytes(pkt.payload)
    total += len(pack)
    count += 1
    if (len(pack) > 1000):
        #if (len(bytes(pkt.payload)) != 1500):
        #    print(len(bytes(pkt.payload)))
        compare = len(pack)
        mtemp = len(lzma.compress(pack))
        gtemp = len(gzip.compress(pack))
        if(len(pack) <1500):
            print(compare,mtemp,mtemp-compare)
        ltemp = len(lz4.frame.compress(pack))
        ztemp = len(zlib.compress(pack))
        if compare > gtemp:
            gziptotal += gtemp
        else: 
            gziptotal += compare
        if compare > mtemp:
            lzmatotal += mtemp
        else:
            lzmatotal += compare
        if compare > ltemp:
            lz4total += ltemp
        else:
            lz4total += compare
        if compare > ztemp:
            zlibtotal += ztemp
        else:
            zlibtotal += compare
    else:
        excluded+= 1
        gziptotal += len(pack)
        lz4total += len(pack)
        zlibtotal += len(pack)
        lzmatotal += len(pack)

print("NOPackets= "+ str(count)+ "\nOriginal Size= "+str(total)+"B\nGzipped Size= "+ str(gziptotal)+ "B \nLZ4'ed Size = "+str(lz4total) +"B\nZlib'ed Size= "+ str(zlibtotal)+"B\nExcluded= " +str(excluded)+"\n"+ str(gzipuncomp) +"B " + str(lz4uncomp))




'''
NOPackets= 643152
Original Size= 696210863B
Gzipped Size= 710664503B 
LZ4'ed Size = 711003359B
Zlib'ed Size= 702946679B
696210863B 696210863

Original size is 696MB 
after compression with gzip is 710MB and for lz4 is 711MB Zlib is 702MB
gzip and lz4 are both compression algorithms based on LZ77

excluding tcp header
NOPackets= 643152
Original Size= 687206735B
Gzipped Size= 701640197B 
LZ4'ed Size = 701999231B
Zlib'ed Size= 693922373B
687206735B 687206735

excluding under 1kb
NOPackets= 643152
Original Size= 687206735B
Gzipped Size= 697541831B 
LZ4'ed Size = 697541831B
Zlib'ed Size= 692149607B
Excluded= 193800
673180520B 673180520

LZMA algorithm increases by 60 bytes
'''