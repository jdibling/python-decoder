import datetime

def TrimmedString(data, **kwargs):
    delims = kwargs.get('delims', ' \0')
    return str(data).strip(delims)

class HexArray(object):
    def __init__ (self, data):
        self.payload = str (data)
    def __toHex (self, x):
        return ' '.join ([hex (ord (c))[2:].zfill (2) for c in x])
    def __toCHex (self, x):
        return ", ".join ([hex (ord (c)) for c in x])
    def __str__ (self):
        return '[{0}]'.format(self.__toHex(self.payload))

def EpochTime(data, **kwargs):
    epoch = kwargs.get('epoch', 'unix').lower()

    val = int(data)

    nanos = val % 1000
    val /= 1000
    mics = val % 1000
    val /= 1000
    millis = val

    return datetime.datetime.fromtimestamp(millis).replace(microsecond=((millis*1000)+mics))



class TimeFromFields(object):
    def __init__(self, hourField, minField, secField, **kwargs):
        self.hourField = hourField
        self.minuteField = minField
        self.secondField = secField
        if kwargs.has_key('mic') and kwargs.has_key('nano'):
            raise RuntimeError("Can't specify both mic and nano kwargs for TimeTime conversion object")
        self.micsField = kwargs.get('mic', None)
        self.nanosField = kwargs.get('nano', None)
    def __call__(self, context):
        hour = context.get(self.hourField, None)
        min = context.get(self.minuteField, None)
        sec = context.get(self.secondField, None)
        mics = None
        if self.nanosField is not None:
            mics = context.get(self.nanosField, None)
            if mics is not None:
                mics = mics/1000
        elif self.micsField is not None:
            mics = context.get(self.micsField, None)
        # convert
        if hour is not None:
            if min is not None:
                if sec is not None:
                    if mics is not None:
                        return datetime.time(hour, min, sec, mics)
                    else:
                        return datetime.time(hour, min, sec)
                else:
                    return datetime.time(hour, min)
            else:
                return datetime.time(hour)
        else:
            return None

from decimal import Decimal

class DecDiv(object):
    def __init__(self, lhf, rhf):
        self.leftField = lhf
        self.rightField = rhf
        self.value = None
    def __str__(self):
        return '{0}'.format(self.value)
    def __call__(self, context):
        leftVal = long(context[self.leftField])
        rightVal = long(context[self.rightField])

        self.value = Decimal(leftVal) / Decimal(rightVal)
        return self.value

class Sub(object):
    def __init__(self, lhf, rhf):
        self.leftField = lhf
        self.rightField = rhf
        self.value = None
    def __str__(self):
        return '{0}'.format(self.value)
    def __call__(self, context):
        leftVal = context[self.leftField]
        rightVal = context[self.rightField]

        self.value = leftVal - rightVal
        return self.value

