from base.descriptor import *

MessageHeader = Descriptor([
    WireField('bbo-msg-size', 'H', type=int),
    WireField('bbo-msg-type', 'H', type=int),
    WireField('bbo-msg-seq-num', 'I', type=int),
    WireField('bbo-send-time', 'I', type=int),
    WireField('bbo-product-id', 'B', type=int),
    WireField('bbo-retrans-flag', 'B', type=int),
    WireField('bbo-num-body-entries', 'B', type=int),
    WireField('resv', 'c', hidden=True)
], endian='Big', checksize=16)

Bbo = Descriptor([
    WireField('bbo-source-time', 'I', type=int),
    WireField('resv', '3s', hidden=True),
    WireField('bbo-rpi-interest', 'c', type=TrimmedString),
    WireField('bbo-ask-prbbo-unscaled', 'I', type=int),
    WireField('bbo-ask-size', 'I', type=int),
    WireField('bbo-bid-prbbo-unscaled', 'I', type=int),
    WireField('bbo-bid-size', 'I', type=int),
    WireField('bbo-prbbo-scale-code', 'B', type=int),
    WireField('bbo-exchange-id', 'c'),
    WireField('bbo-security-type', 'c'),
    WireField('bbo-quote-condition', 'c'),
    WireField('bbo-symbol', '16s', type=TrimmedString)
], endian='Big', checksize=44)