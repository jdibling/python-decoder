from base.descriptor import *

MoldPacketHeader = Descriptor([
    WireField('mold-session', '10s', type=TrimmedString),
    WireField('mold-sequence-number', 'Q', type=int),
    WireField('mold-message-count', 'H', type=int)
], endian='Big')

MoldMessageHeader = Descriptor([
    WireField('mold-message-length', 'H', type=int)
], endian='Big')


