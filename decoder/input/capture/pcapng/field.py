from base.descriptor import  *
import socket
from struct import pack

class IpAddrField(WireField):
    def __init__(self):
        self.__orig_data = 0L
        self.__rendered = "NotRendered"
    def __call__(self, data):
        self.__orig_data = data
        self.__render()
        return self.__str__()
    def __str__(self):
        return self.__rendered
    def __repr__(self):
        return "IpAddrField ({0}): {1}".format(self.__orig_data, self.__rendered)
    def __render(self):
        self.__rendered = socket.inet_ntoa(pack('!L', self.__orig_data))

