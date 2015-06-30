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

#TODO Repeasing Groups in here?
MarketSnapshot = Descriptor([
  WireField('market-id',                                 'i', type=int),
  WireField('market-type',                               'h', type=int),
  WireField('trading-status',                            'c', type=int),
  WireField('volume',                                    'i', type=int),
  WireField('block-volume',                              'i', type=int),
  WireField('efs-volume',                                'i', type=int),
  WireField('efp-volume',                                'i', type=int),
  WireField('open-interest',                             'i', type=int),
  WireField('opening-price',                             'l', type=int),
  WireField('settlement-price-with-deal-priceprecision', 'l', type=int),
  WireField('high',                                      'l', type=int),
  WireField('low',                                       'l', type=int),
  WireField('vwap',                                      'l', type=int),
  WireField('num-of-bookentries',                        'i', type=int),
  WireField('last-trade-price',                          'l', type=int),
  WireField('last-trade-quantity',                       'i', type=int),
  WireField('last-trade-date-time',                       'l', type=int),
  WireField('settle-price-date-time',                     'l', type=int),
  WireField('last-messages-equenceid',                   'i', type=int),
  WireField('reserved-field1',                           'h', type=int),
  WireField('open-interest-date',                        '10s', type=TrimmedString),
  WireField('is-settle-price-official',                  'b', type=int),
  WireField('settlement-price',                          'l', type=int),
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

SpotTrade = Descriptor([
  WireField('ice-market-id', 'i', type=int),
  WireField('ice-trade-id', 'l', type=int),
  WireField('ice-price', 'l', type=int),
  WireField('ice-quantity', 'i', type=int),
  WireField('ice-transact-date-time', 'l', type=int),
  WireField('ice-extra-flags', 'b', type=int),
  WireField('ice-delivery-begin-date-time', 'l', type=int)
], endian='Big') 

InvestigatedTrade = Descriptor([
  WireField('ice-market-id', 'i', type=int),
  WireField('ice-trade-id', 'l', type=int),
  WireField('ice-price', 'l', type=int),
  WireField('ice-quantity', 'i', type=int),
  WireField('ice-off-market-trade-type', 'b', type=int),
  WireField('ice-date-time', 'l', type=int),
  WireField('ice-status', 'b', type=int)
], endian='Big')

CancelledTrade = Descriptor([
  WireField('ice-market-id', 'i', type=int),
  WireField('ice-trade-id', 'l', type=int),
  WireField('ice-price', 'l', type=int),
  WireField('ice-quantity', 'i', type=int),
  WireField('ice-off-market-trade-type', 'b', type=int),
  WireField('ice-date-time', 'l', type=int),
], endian='Big') 

MarketStatistics = Descriptor([
  WireField('ice-market-id', 'i', type=int),
  WireField('ice-volume', 'i', type=int),
  WireField('ice-block-volume', 'i', type=int),
  WireField('ice-efs-volume', 'i', type=int),
  WireField('ice-efp-volume', 'i', type=int),
  WireField('ice-high', 'l', type=int),
  WireField('ice-low', 'l', type=int),
  WireField('ice-vwap', 'l', type=int),
  WireField('ice-date-time', 'l', type=int),
], endian='Big')

MarketStateChange = Descriptor([], endian='Big') 
SystemText = Descriptor([], endian='Big') 
OpenInterest = Descriptor([], endian='Big') 
OpenPrice = Descriptor([], endian='Big') 
SettlementPrice = Descriptor([], endian='Big') 
MarkerIndexPrices = Descriptor([], endian='Big') 
EndOfDayMarketSummary              = Descriptor([], endian='Big') 
MarketEvent                        = Descriptor([], endian='Big') 
PreOpenPriceIndicator              = Descriptor([], endian='Big') 
StripInfo                          = Descriptor([], endian='Big') 
IntervalPriceLimitNotification     = Descriptor([], endian='Big') 
NewFuturesStrategyDefinition       = Descriptor([], endian='Big') 
UnknownTest                        = Descriptor([], endian='Big') 
SnapshotOrder                      = Descriptor([], endian='Big') 
AddModifyOrder                     = Descriptor([], endian='Big') 
DeleteOrder                        = Descriptor([], endian='Big') 
MessageBundleMarker                = Descriptor([], endian='Big') 
SnapshotPriceLevel                 = Descriptor([], endian='Big') 
AddPriceLevel                      = Descriptor([], endian='Big') 
ChangePriceLevel                   = Descriptor([], endian='Big') 
DeletePriceLevel                   = Descriptor([], endian='Big') 
NewOptionsStrategyDefinition       = Descriptor([], endian='Big') 
NewOptionsMarketDefinition         = Descriptor([], endian='Big') 
RFQ                                = Descriptor([], endian='Big') 
OptionOpenInterest                 = Descriptor([], endian='Big') 
OptionSettlementPrice              = Descriptor([], endian='Big') 
OldStyleOptionsTradeAndMarketStats = Descriptor([], endian='Big')

