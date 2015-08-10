from decoder.descriptor import *

UnitHeader = Descriptor([
    WireField('mpitch-hdr-length', 'H', type=int),
    WireField('mpitch-hdr-count', 'B', type=int),
    WireField('mpitch-hdr-unit', 'B', type=int),
    WireField('mpitch-hdr-sequence', 'I', type=int)
])

CommonFields = Descriptor([
    WireField('mpitch-length', 'B', type=int),
    WireField('mpitch-msg-type', 'B', type=int)
], checksize=2)

Time = Descriptor([
    WireField('mpitch-time-whole', 'I', type=int)
], checksize=6-CommonFields.WireBytes())

UnitClear = Descriptor([
    WireField('mpitch-time-offset', 'I', type=int)
], checksize=6-CommonFields.WireBytes())

AddOrderLong = Descriptor([
    WireField('mpitch-time-offset', 'I', type=int),
    WireField('mpitch-order-id', 'Q', type=int),
    WireField('mpitch-side', 'c'),
    WireField('mpitch-quantity', 'I', type=int),
    WireField('mpitch-symbol', '6s', type=TrimmedString),
    WireField('mpitch-price', 'Q', type=int),
    WireField('mpitch-add-flags', 'B', type=int),
], checksize=34-CommonFields.WireBytes())

AddOrderShort = Descriptor([
    WireField('mpitch-time-offset', 'I', type=int),
    WireField('mpitch-order-id', 'Q', type=int),
    WireField('mpitch-side', 'c'),
    WireField('mpitch-quantity', 'H', type=int),
    WireField('mpitch-symbol', '6s', type=TrimmedString),
    WireField('mpitch-price', 'H', type=int),
    WireField('mpitch-add-flags', 'B', type=int),
], checksize=26-CommonFields.WireBytes())

AddOrderExpanded = Descriptor([
    WireField('mpitch-time-offset', 'I', type=int),
    WireField('mpitch-order-id', 'Q', type=int),
    WireField('mpitch-side', 'c'),
    WireField('mpitch-quantity', 'I', type=int),
    WireField('mpitch-symbol', '8s', type=TrimmedString),
    WireField('mpitch-price', 'Q', type=int),
    WireField('mpitch-add-flags', 'B', type=int),
    WireField('mpitch-participant', '4s', type=TrimmedString)
], checksize=40-CommonFields.WireBytes())

OrderExecuted = Descriptor([
    WireField('mpitch-time-offset', 'I', type=int),
    WireField('mpitch-order-id', 'Q', type=int),
    WireField('mpitch-quantity', 'I', type=int),
    WireField('mpitch-execution-id', 'Q', type=int)
], checksize=26-CommonFields.WireBytes())

OrderExecutedAtPriceSize = Descriptor([
    WireField('mpitch-time-offset', 'I', type=int),
    WireField('mpitch-order-id', 'Q', type=int),
    WireField('mpitch-quantity', 'I', type=int),
    WireField('mpitch-remaining-quantity', 'I', type=int),
    WireField('mpitch-execution-id', 'Q', type=int),
    WireField('mpitch-price', 'Q', type=int)
], checksize=38-CommonFields.WireBytes())

ReduceSizeLong = Descriptor([
    WireField('mpitch-time-offset', 'I', type=int),
    WireField('mpitch-order-id', 'Q', type=int),
    WireField('mpitch-cancelled-quantity', 'I', type=int),
], checksize=18-CommonFields.WireBytes())

ReduceSizeShort = Descriptor([
    WireField('mpitch-time-offset', 'I', type=int),
    WireField('mpitch-order-id', 'Q', type=int),
    WireField('mpitch-cancelled-quantity', 'H', type=int),
], checksize=16-CommonFields.WireBytes())

ModifyOrderLong = Descriptor([
    WireField('mpitch-time-offset', 'I', type=int),
    WireField('mpitch-order-id', 'Q', type=int),
    WireField('mpitch-quantity', 'I', type=int),
    WireField('mpitch-price', 'Q', type=int),
    WireField('mpitch-modify-flags', 'B', type=int)
], checksize=27-CommonFields.WireBytes())

ModifyOrderShort = Descriptor([
    WireField('mpitch-time-offset', 'I', type=int),
    WireField('mpitch-order-id', 'Q', type=int),
    WireField('mpitch-quantity', 'H', type=int),
    WireField('mpitch-price', 'H', type=int),
    WireField('mpitch-modify-flags', 'B', type=int)
], checksize=19-CommonFields.WireBytes())

DeleteOrder = Descriptor([
    WireField('mpitch-time-offset', 'I', type=int),
    WireField('mpitch-order-id', 'Q', type=int),
], checksize=14-CommonFields.WireBytes())

TradeLong = Descriptor([
    WireField('mpitch-time-offset', 'I', type=int),
    WireField('mpitch-order-id', 'Q', type=int),
    WireField('mpitch-side', 'c'),
    WireField('mpitch-quantity', 'I', type=int),
    WireField('mpitch-symbol', '6s', type=TrimmedString),
    WireField('mpitch-price', 'Q', type=int),
    WireField('mpitch-execution-id', 'Q', type=int)
], checksize=41-CommonFields.WireBytes())

TradeShort = Descriptor([
    WireField('mpitch-time-offset', 'I', type=int),
    WireField('mpitch-order-id', 'Q', type=int),
    WireField('mpitch-side', 'c'),
    WireField('mpitch-quantity', 'H', type=int),
    WireField('mpitch-symbol', '6s', type=TrimmedString),
    WireField('mpitch-price', 'H', type=int),
    WireField('mpitch-execution-id', 'Q', type=int)
], checksize=33-CommonFields.WireBytes())

TradeExpanded = Descriptor([
    WireField('mpitch-time-offset', 'I', type=int),
    WireField('mpitch-order-id', 'Q', type=int),
    WireField('mpitch-side', 'c'),
    WireField('mpitch-quantity', 'I', type=int),
    WireField('mpitch-symbol', '8s', type=TrimmedString),
    WireField('mpitch-price', 'Q', type=int),
    WireField('mpitch-execution-id', 'Q', type=int)
], checksize=43-CommonFields.WireBytes())

TradeBreak = Descriptor([
    WireField('mpitch-time-offset', 'I', type=int),
    WireField('mpitch-execution-id', 'Q', type=int)
], checksize=14-CommonFields.WireBytes())

EndOfSession = Descriptor([
    WireField('mpitch-timestamp', 'I', type=int),
], checksize=6-CommonFields.WireBytes())

SymbolMapping = Descriptor([
    WireField('mpitch-feed-symbol', '6s', type=TrimmedString),
    WireField('mpitch-osi-symbol', '21s', type=TrimmedString),
    WireField('mpitch-symbol-condition', 'c')
], checksize=30-CommonFields.WireBytes())

TradingStatus = Descriptor([
    WireField('mpitch-time-offset', 'I', type=int),
    WireField('mpitch-symbol', '8s', type=TrimmedString),
    WireField('mpitch-trading-status', 'c'),
    WireField('mpitch-reg-sho-action', 'c'),
    WireField('resv1', 'c', hidden=True),
    WireField('resv2', 'c', hidden=True),
], checksize=18-CommonFields.WireBytes())

AuctionUpdate = Descriptor([
    WireField('mpitch-time-offset', 'I', type=int),
    WireField('mpitch-symbol', '8s', type=TrimmedString),
    WireField('mpitch-auction-type', 'c'),
    WireField('mpitch-reference-price', 'Q', type=int),
    WireField('mpitch-buy-shares', 'I', type=int),
    WireField('mpitch-sell-shares', 'I', type=int),
    WireField('mpitch-indicative-price', 'Q', type=int),
    WireField('mpitch-auction-only-price', 'Q', type=int),
], checksize=47-CommonFields.WireBytes())

AuctionSummary = Descriptor([
    WireField('mpitch-time-offset', 'I', type=int),
    WireField('mpitch-symbol', '8s', type=TrimmedString),
    WireField('mpitch-auction-type', 'c'),
    WireField('mpitch-price', 'Q', type=int),
    WireField('mpitch-shares', 'I', type=int),
], checksize=27-CommonFields.WireBytes())

RetailPriceImprovement = Descriptor([
    WireField('mpitch-time-offset', 'I', type=int),
    WireField('mpitch-symbol', '8s', type=TrimmedString),
    WireField('mpitch-retail-price-improvement', 'c'),
], checksize=15-CommonFields.WireBytes())

