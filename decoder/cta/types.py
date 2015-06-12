from base.field import WireField
from base.types import DecDiv

class TimeStamp(object):
    def __init__(self, **kwargs):
        self.__orig_data = ""
        self.__parts = []
        self.__rendered = "NotRendered"

    def __call__(self, data):
        self.__orig_data = data
        self.__parts = [(ord(c)-0x30) for c in data]
        self.__render()
        return self.__str__()

    def __str__(self):
        return self.__rendered
    def __repr__(self):
        return "TimeStamp {0} '{1}' '{2}' '{3}'".format(super(TimeStamp,self).__repr__(), self.__orig_data, self.__parts, self.__rendered)

    def __render(self):
        if len(self.__parts) < 3:
            raise ValueError ('Invalid time data ({0}): {1}'.format(len(self.__parts), repr(self)))

        rendered_parts = []
        for idx, part in enumerate(self.__parts):
            if idx < 3:
                rendered_part = '{0:02d}'.format(part)
            else:
                rendered_part = '{0}'.format(part)
            rendered_parts.append(rendered_part)

        self.__rendered = ":".join(rendered_parts[0:3]) + '.' + ''.join(rendered_parts[3:])

class PriceDenominator(object):
    DENOMS = {
        # fractionals
        '3': 8,
        '4': 16,
        '5': 32,
        '6': 64,
        '7': 128,
        '8': 256,
        # decimals
        'A': 10,
        'B': 100,
        'C': 1000,
        'D': 10000,
        'E': 100000,
        'F': 1000000,
        'G': 10000000,
        'H': 100000000,
        'I': 1000000000,
        ' ': 1,
        '0': 1,
        '1': 1,
    }

    def __init__(self, data):
        strData = str(data)
        if len(strData) != 1:
            raise ValueError('{0} cannot be interpreted as a string with 1 character'.format(data))
        self.__denom = PriceDenominator.DENOMS[strData]

    def __str__(self):
        return '{0}'.format(self.__denom)

    def __long__(self):
        return self.__denom

