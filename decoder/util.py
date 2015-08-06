###############################################################################
# Author: Rob Kulseth
# Short script to convert the ipaddress port combo packed into an int for use
# in a hash map back into the string representation
###############################################################################


def bytesToAddr(addr):
    firstoctet  = (addr & 0x0000FF0000000000) >> (8*5)
    secondoctet = (addr & 0x000000FF00000000) >> (8*4)
    thirdoctet  = (addr & 0x00000000FF000000) >> (8*3)
    fourthoctet = (addr & 0x0000000000FF0000) >> (8*2)
    port        = (addr & 0x000000000000FFFF)
    return "{0}.{1}.{2}.{3}:{4}".format(firstoctet, secondoctet, thirdoctet, fourthoctet, port)


def addrToStreamId(ip, port):
    octets = ip.split('.')
    stream_id =  int(octets[0]) << (8 * 5)
    stream_id += int(octets[1]) << (8 * 4)
    stream_id += int(octets[2]) << (8 * 3)
    stream_id += int(octets[3]) << (8 * 2)
    stream_id |= int(port)
    return stream_id