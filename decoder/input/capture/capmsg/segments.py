from decoder.descriptor import *
from decoder.input.capture.capmsg.types import *

FileHeader = Descriptor([
    WireField('cap-file-signature', '8s', type=TrimmedString),
    WireField('cap-file-data-offset', 'I', type=int),
    WireField('cap-file-create-time', 'I', type=int),
    WireField('cap-file-version', '16s'),
    WireField('cap-file-creation-date', '8s'),
    WireField('cap-file-creation-time', '8s')
])

RecordHeader = Descriptor([
    WireField('cap-packet-length', 'I', type=int)
])

PacketHeader = Descriptor([
    WireField('cap-packet-month', 'B', hidden=True),
    WireField('cap-packet-day', 'B', hidden=True),
    WireField('cap-packet-hour', 'B', hidden=True),
    WireField('cap-packet-minute', 'B',hidden=True),
    WireField('cap-packet-second', 'B', hidden=True),
    WireField('cap-packet-micro', 'B', hidden=True),
    WireField('resv', '2s', hidden=True),
    WireField('cap-packet-hires', 'd', type=float),
    ComputedField('cap-packet-timestamp', HiResTimeStamp('cap-packet-hires')),
    ComputedField('cap-packet-recv-sec', HiResRecvSec('cap-packet-hires')),
    EchoField('packet-recv-time-gmt', 'cap-packet-recv-sec')
])

PacketFooter = Descriptor([
    WireField('cap-packet-length-check', 'I', type=int)
])
