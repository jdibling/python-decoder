from base.descriptor import *

MessageHeader = Descriptor([
    WireField('ice-msg-size', 'H', type=int),
    WireField('ice-msg-type', 'H', type=int),
    WireField('ice-msg-seq-num', 'I', type=int),
    WireField('ice-send-time', 'I', type=int),
    WireField('ice-product-id', 'B', type=int),
    WireField('ice-retrans-flag', 'B', type=int),
    WireField('ice-num-body-entries', 'B', type=int),
    WireField('resv', 'c', hidden=True)
], endian='Big')

Bbo = Descriptor([
    WireField('ice-source-time', 'I', type=int),
    WireField('resv', '3s', hidden=True),
    WireField('ice-rpi-interest', 'c', type=TrimmedString),
    WireField('ice-ask-price-unscaled', 'I', type=int),
    WireField('ice-ask-size', 'I', type=int),
    WireField('ice-bid-price-unscaled', 'I', type=int),
    WireField('ice-bid-size', 'I', type=int),
    WireField('ice-price-scale-code', 'B', type=int),
    WireField('ice-exchange-id', 'c'),
    WireField('ice-security-type', 'c'),
    WireField('ice-quote-condition', 'c'),
    WireField('ice-symbol', '16s', type=TrimmedString)
], endian='Big')