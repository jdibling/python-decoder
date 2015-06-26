from base.descriptor import *

MoldPacketHeader = Descriptor([
    WireField('mold-session', '10s', type=TrimmedString),
    WireField('mold-sequence-number', 'Q'),
    WireField('mold-message-count', 'H')
], endian='Big')

MoldMessageHeader = Descriptor([
    WireField('mold-message-length', 'H')
], endian='Big')


