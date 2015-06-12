from base.descriptor import *

MessageBlock = Descriptor([
    WireField('ice-session-num', 'h', type=int),
    WireField('ice-sequence-num', 'i', type=int),
    WireField('ice-num-msgs', 'h', type=int),
    WireField('ice-sent-date-time', 'q', type=int)
], endian='Big')

MessageHeader = Descriptor([
    WireField('ice-msg-type', 'c'),
    WireField('ice-msg-body-length', 'i', type=int)
], endian='Big')

Trade = Descriptor([
    WireField('ice-market-id', 'i', type=int),
    WireField('ice-trade-id', 'q', type=int),
    WireField('ice-system-priced-leg', 'c'),
    WireField('ice-price-unscaled', 'q', type=int),
    WireField('ice-quantity', 'i', type=int),
    WireField('ice-off-market-trade-type', 'c'),
    WireField('ice-transact-date-time', 'q', type=int),
    WireField('ice-system-priced-leg-type', 'c'),
    WireField('ice-is-implied-spread-at-market-open', 'c'),
    WireField('ice-is-adjusted-trade', 'c'),
    WireField('ice-aggressor-side', 'c'),
    WireField('ice-extra-flags', 'b', type=int)
], endian='Big')
