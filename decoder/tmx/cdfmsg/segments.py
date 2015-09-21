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

Heartbeat = Descriptor([
    WireField('sep', 'c', hidden=True), # '['
    WireField('cdf-hb-section-name', '10s', hidden=True), # 'HEARTBEAT'
    WireField('cdf-hb-date', '10s'),
    WireField('sep', 'c', hidden=True), # ' '
    WireField('cdf-hb-time-of-day', '8s'),
    WireField('sep', 'c', hidden=True), # '-'
    WireField('cdf-hb-epoch', '19s'),
    WireField('sep', '12s', hidden=True), # '][LAST SENT'
    WireField('cdf-hb-last-seq-num', '9s', type=int),
    WireField('sep', 'c', hidden=True), # '-'
    WireField('cdf-hb-last-time', '8s'),
    WireField('sep', 'c', hidden=True), # '-'
    WireField('cdf-hb-last-seq-num-2', '9s', type=int),
    WireField('sep', 'c', hidden=True), # '-'
    WireField('cdf-hb-last-time-of-day', '8s'),
    WireField('sep', 'c', hidden=True), # '-'
    WireField('cdf-hb-last-epoch', '19s'),
    WireField('sep', 'c', hidden=True), # ']'
    WireField('cdf-hb-ocsa-subject', '20s'),
    WireField('cdf=hb-ocsa-instan)
])


