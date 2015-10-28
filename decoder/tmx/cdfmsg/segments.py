from decoder.descriptor import *

TransportHeader = Descriptor([
    WireField('cdf-th-stx', 'c', hidden=True),
    WireField('cdf-th-length', '4s', type=int),
    WireField('cdf-th-seq-num', '9s', type=TrimmedString),
    WireField('cdf-th-service-id', '3s'),
    WireField('cdf-th-retransmission', 'c'),
    WireField('cdf-th-continuation', 'c'),
    WireField('cdf-th-msg-type', '2s', type=TrimmedString),
    WireField('cdf-th-exchange-id', '2s', type=TrimmedString)
])

