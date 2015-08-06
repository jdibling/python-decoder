from decoder.descriptor import *
from decoder.ndq.itch.types import *

ItchCommonSegment = Descriptor([
    WireField('itch-msg-type', 'c'),
], endian='Big')

ItchSystemEvent = Descriptor([
    WireField('itch-msg-type', 'c'),
    WireField('itch-stock-locate', 'H'),
    WireField('itch-tracking-number', 'H'),
    WireField('itch-timestamp', '6s', type=ItchTimeStamp()),
    WireField('itch-event-code', 'c')
], endian='Big')

ItchStockDirectory = Descriptor([
    WireField('itch-msg-type', 'c'),
    WireField('itch-stock-locate', 'H'),
    WireField('itch-tracking-number', 'H'),
    WireField('itch-timestamp', '6s', type=ItchTimeStamp()),
    WireField('itch-symbol', '8s', type=TrimmedString),
    WireField('itch-market-categoty', 'c'),
    WireField('itch-fin-status', 'c'),
    WireField('itch-round-lot-size', 'I'),
    WireField('itch-round-lots-only', 'c'),
    WireField('itch-issue-classification', 'c'),
    WireField('itch-issue-subtype', 'c'),
    WireField('itch-authenticity', 'c'),
    WireField('itch-short-sale-thresh', 'c'),
    WireField('itch-ipo-flag', 'c'),
    WireField('itch-luld-reference-price-tier', 'c'),
    WireField('itch-etp-flag', 'c'),
    WireField('itch-etp-leverage-factor', 'I'),
    WireField('itch-inverse', 'c')
], endian='Big')

ItchStockTradingAction = Descriptor([
    WireField('itch-msg-type', 'c'),
    WireField('itch-stock-locate', 'H'),
    WireField('itch-tracking-number', 'H'),
    WireField('itch-timestamp', '6s', type=ItchTimeStamp()),
    WireField('itch-symbol', '8s', type=TrimmedString),
    WireField('itch-trading-state', 'c'),
    WireField('resv', 'c', hidden=True),
    WireField('itch-reason', '4s', type=TrimmedString)
], endian='Big')

ItchRegShoRestriction = Descriptor([
    WireField('itch-msg-type', 'c'),
    WireField('itch-stock-locate', 'H'),
    WireField('itch-tracking-number', 'H'),
    WireField('itch-timestamp', '6s', type=ItchTimeStamp()),
    WireField('itch-symbol', '8s', type=TrimmedString),
    WireField('itch-action', 'c')
], endian='Big')

ItchMarketParticipantPosition = Descriptor([
    WireField('itch-msg-type', 'c'),
    WireField('itch-stock-locate', 'H'),
    WireField('itch-tracking-number', 'H'),
    WireField('itch-timestamp', '6s', type=ItchTimeStamp()),
    WireField('itch-mdip', '4s', type=TrimmedString),
    WireField('itch-symbol', '8s', type=TrimmedString),
    WireField('itch-primary-market-maker', 'c'),
    WireField('itch-market-maker-mode', 'c'),
    WireField('itch-market-participant-state', 'c')
], endian='Big')

ItchMwcbDeclineLevel = Descriptor([
    WireField('itch-msg-type', 'c'),
    WireField('itch-stock-locate', 'H'),
    WireField('itch-tracking-number', 'H'),
    WireField('itch-timestamp', '6s', type=ItchTimeStamp()),
    WireField('itch-level-1-unscaled', 'Q'),
    WireField('itch-level-2-unscaled', 'Q'),
    WireField('itch-level-3-unscaled', 'Q'),
    ConstantField('itch-price-scale', int(100000000)),
    ComputedField('itch-level-1', DecDiv('itch-level-1-unscaled', 'itch-price-scale')),
    ComputedField('itch-level-2', DecDiv('itch-level-3-unscaled', 'itch-price-scale')),
    ComputedField('itch-level-3', DecDiv('itch-level-3-unscaled', 'itch-price-scale'))
], endian='Big')

ItchMwcbBreach = Descriptor([
    WireField('itch-msg-type', 'c'),
    WireField('itch-stock-locate', 'H'),
    WireField('itch-tracking-number', 'H'),
    WireField('itch-timestamp', '6s', type=ItchTimeStamp()),
    WireField('itch-breached-level', 'c')
], endian='Big')

ItchIpoQuotingPeriod = Descriptor([
    WireField('itch-msg-type', 'c'),
    WireField('itch-stock-locate', 'H'),
    WireField('itch-tracking-number', 'H'),
    WireField('itch-timestamp', '6s', type=ItchTimeStamp()),
    WireField('itch-symbol', '8s', type=TrimmedString),
    WireField('itch-quotation-release-time-secs', 'I'),
    WireField('itch-quotation-release-qualifier', 'c'),
    WireField('itch-ipo-price-unscaled', 'I'),
    ConstantField('itch-price-scale', int(10000)),
    ComputedField('itch-ipo-price', DecDiv('itch-ipo-price-unscaled', 'itch-price-scale'))
], endian='Big')

ItchOrderAdd = Descriptor([
    WireField('itch-msg-type', 'c'),
    WireField('itch-stock-locate', 'H'),
    WireField('itch-tracking-number', 'H'),
    WireField('itch-timestamp', '6s', type=ItchTimeStamp()),
    WireField('itch-order-reference', 'Q'),
    WireField('itch-buy-sell', 'c'),
    WireField('itch-shares', 'I'),
    WireField('itch-symbol', '8s', type=TrimmedString),
    WireField('itch-price-unscaled', 'I'),
    ConstantField('itch-price-scale', int(10000)),
    ComputedField('itch-price', DecDiv('itch-price-unscaled', 'itch-price-scale'))
], endian='Big')

ItchOrderAddMpid = Descriptor([
    WireField('itch-msg-type', 'c'),
    WireField('itch-stock-locate', 'H'),
    WireField('itch-tracking-number', 'H'),
    WireField('itch-timestamp', '6s', type=ItchTimeStamp()),
    WireField('itch-order-reference', 'Q'),
    WireField('itch-buy-sell', 'c'),
    WireField('itch-shares', 'I'),
    WireField('itch-symbol', '8s', type=TrimmedString),
    WireField('itch-price-unscaled', 'I'),
    ConstantField('itch-price-scale', int(10000)),
    ComputedField('itch-price', DecDiv('itch-price-unscaled', 'itch-price-scale')),
    WireField('itch-attribution', '4s', type=TrimmedString)
], endian='Big')

ItchOrderExecuted = Descriptor([
    WireField('itch-msg-type', 'c'),
    WireField('itch-stock-locate', 'H'),
    WireField('itch-tracking-number', 'H'),
    WireField('itch-timestamp', '6s', type=ItchTimeStamp()),
    WireField('itch-order-reference', 'Q'),
    WireField('itch-shares', 'I'),
    WireField('itch-match-number', 'Q')
], endian='Big')

ItchOrderExecutedWithPrice = Descriptor([
    WireField('itch-msg-type', 'c'),
    WireField('itch-stock-locate', 'H'),
    WireField('itch-tracking-number', 'H'),
    WireField('itch-timestamp', '6s', type=ItchTimeStamp()),
    WireField('itch-order-reference', 'Q'),
    WireField('itch-shares', 'I'),
    WireField('itch-match-number', 'Q'),
    WireField('itch-printable', 'c'),
    WireField('itch-price-unscaled', 'I'),
    ConstantField('itch-price-scale', int(10000)),
    ComputedField('itch-price', DecDiv('itch-price-unscaled', 'itch-price-scale')),
], endian='Big')

ItchOrderDelete = Descriptor([
    WireField('itch-msg-type', 'c'),
    WireField('itch-stock-locate', 'H'),
    WireField('itch-tracking-number', 'H'),
    WireField('itch-timestamp', '6s', type=ItchTimeStamp()),
    WireField('itch-order-reference', 'Q')
], endian='Big')

ItchOrderCancelled = Descriptor([
    WireField('itch-msg-type', 'c'),
    WireField('itch-stock-locate', 'H'),
    WireField('itch-tracking-number', 'H'),
    WireField('itch-timestamp', '6s', type=ItchTimeStamp()),
    WireField('itch-order-reference', 'Q'),
    WireField('itch-shares', 'I')
], endian='Big')

ItchOrderReplace = Descriptor([
    WireField('itch-msg-type', 'c'),
    WireField('itch-stock-locate', 'H'),
    WireField('itch-tracking-number', 'H'),
    WireField('itch-timestamp', '6s', type=ItchTimeStamp()),
    WireField('itch-original-order-reference', 'Q'),
    WireField('itch-new-order-reference', 'Q'),
    WireField('itch-shares', 'I'),
    WireField('itch-price-unscaled', 'I'),
    ConstantField('itch-price-scale', int(10000)),
    ComputedField('itch-price', DecDiv('itch-price-unscaled', 'itch-price-scale')),
], endian='Big')

ItchTrade = Descriptor([
    WireField('itch-msg-type', 'c'),
    WireField('itch-stock-locate', 'H'),
    WireField('itch-tracking-number', 'H'),
    WireField('itch-timestamp', '6s', type=ItchTimeStamp()),
    WireField('itch-order-reference', 'Q'),
    WireField('itch-buy-sell', 'c'),
    WireField('itch-shares', 'I'),
    WireField('itch-symbol', '8s', type=TrimmedString),
    WireField('itch-price-unscaled', 'I'),
    ConstantField('itch-price-scale', int(10000)),
    ComputedField('itch-price', DecDiv('itch-price-unscaled', 'itch-price-scale')),
    WireField('itch-match-number', 'Q')
], endian='Big')

ItchCrossTrade = Descriptor([
    WireField('itch-msg-type', 'c'),
    WireField('itch-stock-locate', 'H'),
    WireField('itch-tracking-number', 'H'),
    WireField('itch-timestamp', '6s', type=ItchTimeStamp()),
    WireField('itch-shares', 'I'),
    WireField('itch-symbol', '8s', type=TrimmedString),
    WireField('itch-cross-price-unscaled', 'I'),
    ConstantField('itch-cross-price-scale', int(10000)),
    ComputedField('itch-cross-price', DecDiv('itch-cross-price-unscaled', 'itch-cross-price-scale')),
    WireField('itch-match-number', 'Q'),
    WireField('itch-cross-type', 'c')
], endian='Big')

ItchBrokenTrade = Descriptor([
    WireField('itch-msg-type', 'c'),
    WireField('itch-stock-locate', 'H'),
    WireField('itch-tracking-number', 'H'),
    WireField('itch-timestamp', '6s', type=ItchTimeStamp()),
    WireField('itch-match-number', 'Q')
], endian='Big')

ItchNoii = Descriptor([
    WireField('itch-msg-type', 'c'),
    WireField('itch-stock-locate', 'H'),
    WireField('itch-tracking-number', 'H'),
    WireField('itch-timestamp', '6s', type=ItchTimeStamp()),
    WireField('itch-paired-shares', 'Q'),
    WireField('itch-imbalance-shares', 'Q'),
    WireField('itch-imbalance-direction', 'c'),
    WireField('itch-symbol', '8s', type=TrimmedString),
    ConstantField('itch-price-scale', int(10000)),
    WireField('itch-far-price-unscaled', 'I'),
    ComputedField('itch-far-price', DecDiv('itch-far-price-unscaled', 'itch-price-scale')),
    WireField('itch-near-price-unscaled', 'I'),
    ComputedField('itch-near-price', DecDiv('itch-near-price-unscaled', 'itch-price-scale')),
    WireField('itch-reference-price-unscaled', 'I'),
    ComputedField('itch-reference-price', DecDiv('itch-reference-price-unscaled', 'itch-price-scale')),
    WireField('itch-cross-type', 'c'),
    WireField('itch-price-variation', 'c')
], endian='Big')

ItchRpii = Descriptor([
    WireField('itch-msg-type', 'c'),
    WireField('itch-stock-locate', 'H'),
    WireField('itch-tracking-number', 'H'),
    WireField('itch-timestamp', '6s', type=ItchTimeStamp()),
    WireField('itch-symbol', '8s', type=TrimmedString),
    WireField('itch-interest', 'c')
], endian='Big')
