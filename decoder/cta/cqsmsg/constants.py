from decoder.cta.cqsmsg.segments import *

MsgType = {
    'E': ('Equity', {
        'D': ("ShortQuote", ShortQuote),
        'B': ("LongQuote", LongQuote)
    })
}

PriceDenom = {
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

def GetDescriptor(msgCat, msgType):
    catMap = MsgType.get(msgCat, None)
    if catMap is None:
        return None
    descriptor = catMap[1].get(msgType, None)
    if descriptor is None:
        return None
    return descriptor[1]

def GetMessageName(msgCat, msgType):
    catMap = MsgType.get(msgCat, None)
    if catMap is None:
        return None
    descriptor = catMap[1].get(msgType, None)
    if descriptor is None:
        return None
    return "{0}{1}".format(catMap[0], descriptor[0])
