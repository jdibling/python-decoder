from base.descriptor import *
from decoder.input.capture.cap.types import HiResTimeStamp

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
    WireField('cap-packet-month', 'B', type=int),
    WireField('cap-packet-day', 'B', type=int),
    WireField('cap-packet-hour', 'B', type=int),
    WireField('cap-packet-minute', 'B',type=int),
    WireField('cap-packet-second', 'B', type=int),
    WireField('cap-packet-micro', 'B', type=int),
    WireField('resv', '2s', hidden=True),
    WireField('cap-packet-hires', 'd', type=float),
    ComputedField('cap-packet-timestamp', HiResTimeStamp('cap-packet-hires'))
])

PacketFooter = Descriptor([
    WireField('cap-packet-length-check', 'I', type=int)
])
