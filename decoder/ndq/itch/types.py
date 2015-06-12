from struct import calcsize, unpack_from
from datetime import time

class ItchTimeStamp(object):
    def __init__(self):
        super(ItchTimeStamp, self).__init__()
        self.__wireFormat = '>6B'
        self.__wireBytes = calcsize(self.__wireFormat)

    def __call__(self, data):
        # data is expected to be a 6-character string
        if not isinstance(data, str):
            raise ValueError("Internal error processing ItchTimeStamp field")
        # itch timestamp is a 6-byte integer
        # we need to unpack it a byte at a time and build an integer
        val = 0
        fields = unpack_from(self.__wireFormat, data)
        for field in fields:
            val <<= 8
            val += field
        # this value is nanoseconds since midnight
        # so let's make a time object
        nanos = val % 1000000000
        val /= 1000000000
        secs = val % 60
        val /= 60
        mins = val % 60
        val /= 60
        hrs = val
        return time(hrs, mins, secs, int(nanos/1000))

def ItchPrice(object):
    def __init__(self, scale):
        super(ItchPrice, self).__init__()
        self.__scale = float(scale)
    def __call__(self, data):
        val = float(data)
        return data/self.__scale