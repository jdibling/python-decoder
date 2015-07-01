from base.descriptor import *

MessageBlock = Descriptor([
    WireField('ice-session-num', 'h', type=int),
    WireField('ice-sequence-num', 'i', type=int),
    WireField('ice-num-msgs', 'h', type=int),
    WireField('ice-sent-date-time', 'q', type=int)
], endian='Big')

MessageHeader = Descriptor([
    WireField('ice-msg-type', 'c'),
    WireField('ice-msg-body-length', 'h', type=int)
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
    WireField('opening-price',                             'q', type=int),
    WireField('settlement-price-with-deal-priceprecision', 'q', type=int),
    WireField('high',                                      'q', type=int),
    WireField('low',                                       'q', type=int),
    WireField('vwap',                                      'q', type=int),
    WireField('num-of-bookentries',                        'i', type=int),
    WireField('last-trade-price',                          'q', type=int),
    WireField('last-trade-quantity',                       'i', type=int),
    WireField('last-trade-date-time',                       'q', type=int),
    WireField('settle-price-date-time',                     'q', type=int),
    WireField('last-messages-equenceid',                   'i', type=int),
    WireField('reserved-field1',                           'h', type=int),
    WireField('open-interest-date',                        '10s', type=TrimmedString),
    WireField('is-settle-price-official',                  'b', type=int),
    WireField('settlement-price',                          'q', type=int),
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
    WireField('ice-trade-id', 'q', type=int),
    WireField('ice-price', 'q', type=int),
    WireField('ice-quantity', 'i', type=int),
    WireField('ice-transact-date-time', 'q', type=int),
    WireField('ice-extra-flags', 'b', type=int),
    WireField('ice-delivery-begin-date-time', 'q', type=int)
], endian='Big') 

InvestigatedTrade = Descriptor([
    WireField('ice-market-id', 'i', type=int),
    WireField('ice-trade-id', 'q', type=int),
    WireField('ice-price', 'q', type=int),
    WireField('ice-quantity', 'i', type=int),
    WireField('ice-off-market-trade-type', 'b', type=int),
    WireField('ice-date-time', 'q', type=int),
    WireField('ice-status', 'b', type=int)
], endian='Big')

CancelledTrade = Descriptor([
    WireField('ice-market-id', 'i', type=int),
    WireField('ice-trade-id', 'q', type=int),
    WireField('ice-price', 'q', type=int),
    WireField('ice-quantity', 'i', type=int),
    WireField('ice-off-market-trade-type', 'b', type=int),
    WireField('ice-date-time', 'q', type=int),
  ], endian='Big') 
  
MarketStatistics = Descriptor([
    WireField('ice-market-id', 'i', type=int),
    WireField('ice-volume', 'i', type=int),
    WireField('ice-block-volume', 'i', type=int),
    WireField('ice-efs-volume', 'i', type=int),
    WireField('ice-efp-volume', 'i', type=int),
    WireField('ice-high', 'q', type=int),
    WireField('ice-low', 'q', type=int),
    WireField('ice-vwap', 'q', type=int),
    WireField('ice-date-time', 'q', type=int),
], endian='Big')
  
MarketStateChange = Descriptor([
    WireField('ice-market-id', 'i', type=int),
    WireField('ice-trading-status', 'b', type=int),
    WireField('ice-date-time', 'q', type=int),
], endian='Big') 
  
SystemText = Descriptor([
    WireField('ice-text-message', '200s', type=TrimmedString),
    WireField('ice-date-time', 'q', type=int),
    WireField('ice-text-message-extra-fld', '800s', type=TrimmedString),
], endian='Big') 
  
OpenInterest = Descriptor([
    WireField('ice-market-id', 'i', type=int),
    WireField('ice-open-interest', 'i', type=int),
    WireField('ice-open-interest-change', 'i', type=int),
    WireField('ice-date-time', 'q', type=int),
    WireField('ice-open-interest-date', '10s', type=TrimmedString),
], endian='Big') 
  
OpenPrice = Descriptor([
    WireField('ice-market-id', 'i', type=int),
    WireField('ice-open-price', 'q', type=int),
    WireField('ice-date-time', 'q', type=int),
], endian='Big')
  
SettlementPrice = Descriptor([
    WireField('ice-market-id', 'i', type=int),
    WireField('ice-settlement-price-with-deal-priceprecision', 'q', type=int),
    WireField('ice-date-time', 'q', type=int),
    WireField('ice-is-official', 'b', type=int),
    WireField('ice-valuation-date-time', 'q', type=int),
    WireField('ice-settlement-price', 'q', type=int),
], endian='Big')
  
MarkerIndexPrices = Descriptor([
    WireField('ice-market-id', 'i', type=int),
    WireField('ice-price', 'q', type=int),
    WireField('ice-short-name', '30s', type=TrimmedString),
    WireField('ice-published-date-time', 'q', type=int),
    WireField('ice-valuation-date', '10s', type=TrimmedString),
], endian='Big') 

EndOfDayMarketSummary = Descriptor([
    WireField('ice-market-id', 'i', type=int),
    WireField('ice-volume', 'i', type=int),
    WireField('ice-block-volume', 'i', type=int),
    WireField('ice-efs-volume', 'i', type=int),
    WireField('ice-efp-volume', 'i', type=int),
    WireField('ice-opening-price', 'q', type=int),
    WireField('ice-high', 'q', type=int),
    WireField('ice-low', 'q', type=int),
    WireField('ice-vwap', 'q', type=int),
    WireField('ice-settlement=price', 'q', type=int),
    WireField('ice-open-interest', 'i', type=int),
    WireField('ice-date-time', 'q', type=int),
], endian='Big') 

MarketEvent = Descriptor([
    WireField('ice-market-id', 'i', type=int),
    WireField('ice-event-type', 'b', type=int),
    WireField('ice-date-time', 'q', type=int),
], endian='Big') 

PreOpenPriceIndicator = Descriptor([
    WireField('ice-market-id', 'i', type=int),
    WireField('ice-pre-open-price', 'q', type=int),
    WireField('ice-date-time', 'q', type=int),
], endian='Big') 

#this one is a bit strange.  defined for tcp as well
StripInfo = Descriptor([
    WireField('ice-strip-id', 'h', type=int),
    WireField('ice-strip-type', '20s', type=TrimmedString),
    WireField('ice-begin-year', 'h', type=int),
    WireField('ice-begin-month', 'h', type=int),
    WireField('ice-begin-day', 'h', type=int),
    WireField('ice-end-year', 'h', type=int),
    WireField('ice-end-month', 'h', type=int),
    WireField('ice-end-day', 'h', type=int),
    WireField('ice-strip-name', '50s', type=TrimmedString),
], endian='Big')

IntervalPriceLimitNotification = Descriptor([
    WireField('ice-market-id', 'i', type=int),
    WireField('ice-ipl-hold-type', 'b', type=int),
    WireField('ice-notification-date-time', 'q', type=int),
    WireField('ice-is-up', 'b', type=int),
    WireField('ice-ipl-hold-duration', 'i', type=int),
    WireField('ice-ipl-up', 'q', type=int),
    WireField('ice-ipl-down', 'q', type=int),
], endian='Big') 

NewFuturesStrategyDefinition = Descriptor([
    WireField('ice-market-id', 'i', type=int),
    WireField('ice-contract-symbol', '70s', type=TrimmedString),
    WireField('ice-trading-status', 'b', type=int),
    WireField('ice-order-price-denominator', 'b', type=int),
    WireField('ice-increment-price', 'i', type=int),
    WireField('ice-increment-qty', 'i', type=int),
    WireField('ice-min-qty', 'i', type=int),
    #TODO Repeating group?
    RepeatingGroup([
        WireField('ice-legbody-length', 'b', type=int),
        WireField('ice-leg-market-id', 'i', type=int),
        WireField('ice-leg-ratio', 'h', type=int),
        WireField('ice-leg-side', 'b', type=int),
    ], RepeatingGroup.ReprCountFromPayload('b')),
], endian='Big')

UnknownTest = Descriptor([
    WireField('ice-market-id', 'i', type=int),
], endian='Big') 

SnapshotOrder = Descriptor([
    WireField('ice-market-id', 'i', type=int),
    WireField('ice-orderid', 'q', type=int),
    WireField('ice-order-sequenceid', 'h', type=int),
    WireField('ice-side', 'b', type=int),
    WireField('ice-price', 'q', type=int),
    WireField('ice-quantity', 'i', type=int),
    WireField('ice-isimplied', 'b', type=int),
    WireField('ice-isrfq', 'b', type=int),
    WireField('ice-order-entry-date-time', 'q', type=int),
    WireField('ice-sequence-within-millis', 'i', type=int),

], endian='Big')

AddModifyOrder = Descriptor([
    WireField('ice-market-id', 'i', type=int),
    WireField('ice-orderid', 'q', type=int),
    WireField('ice-order-sequenceid', 'h', type=int),
    WireField('ice-side', 'b', type=int),
    WireField('ice-price', 'q', type=int),
    WireField('ice-quantity', 'i', type=int),
    WireField('ice-isimplied', 'b', type=int),
    WireField('ice-isrfq', 'b', type=int),
    WireField('ice-order-entry-date-time', 'q', type=int),
    WireField('ice-extra-flags', 'b', type=int),
    WireField('ice-sequence-within-millis', 'i', type=int),
], endian='Big') 

DeleteOrder = Descriptor([
    WireField('ice-market-id', 'i', type=int),
    WireField('ice-orderid', 'q', type=int),
], endian='Big') 

MessageBundleMarker = Descriptor([
    WireField('ice-market-id', 'i', type=int),
    WireField('ice-start-or-end', 'b', type=int),
], endian='Big') 

SnapshotPriceLevel = Descriptor([
    WireField('ice-market-id', 'i', type=int),
    WireField('ice-side', 'b', type=int),
    WireField('ice-price-level-position', 'b', type=int),
    WireField('ice-price', 'q', type=int),
    WireField('ice-quantity', 'i', type=int),
    WireField('ice-order-count', 'h', type=int),
    WireField('ice-implied-quantity', 'i', type=int),
    WireField('ice-implied-order-count', 'h', type=int),
], endian='Big') 

AddPriceLevel = Descriptor([
    WireField('ice-market-id', 'i', type=int),
    WireField('ice-side', 'b', type=int),
    WireField('ice-price-level-position', 'b', type=int),
    WireField('ice-price', 'q', type=int),
    WireField('ice-quantity', 'i', type=int),
    WireField('ice-order-count', 'h', type=int),
    WireField('ice-implied-quantity', 'i', type=int),
    WireField('ice-implied-order-count', 'h', type=int),
], endian='Big') 

ChangePriceLevel = Descriptor([
    WireField('ice-market-id', 'i', type=int),
    WireField('ice-side', 'b', type=int),
    WireField('ice-price-level-position', 'b', type=int),
    WireField('ice-price', 'q', type=int),
    WireField('ice-quantity', 'i', type=int),
    WireField('ice-order-count', 'h', type=int),
    WireField('ice-implied-quantity', 'i', type=int),
    WireField('ice-implied-order-count', 'h', type=int),
], endian='Big') 

DeletePriceLevel = Descriptor([
    WireField('ice-market-id', 'i', type=int),
    WireField('ice-side', 'b', type=int),
    WireField('ice-price-level-position', 'b', type=int),
], endian='Big') 
#TODO repeating Groups
NewOptionsStrategyDefinition = Descriptor([
    WireField('ice-market-id', 'i', type=int),
    WireField('ice-underlying-market-id', 'i', type=int),
    WireField('ice-contract-symbol', '35s', type=TrimmedString),
    WireField('ice-trading-status', 'b', type=int),
    WireField('ice-order-price-denominator', 'b', type=int),
    WireField('ice-increment-price', 'i', type=int),
    WireField('ice-increment-qty', 'i', type=int),
    WireField('ice-min-qty', 'i', type=int),
    #WireField('ice-number-of-leg-definition', 'b', type=int),
    RepeatingGroup([
        WireField('ice-leg-body-length', 'b', type=int),
        WireField('ice-leg-market-id', 'i', type=int),
        WireField('ice-leg-underlying-market-id', 'i', type=int),
        WireField('ice-leg-ratio', 'h', type=int),
        WireField('ice-leg-side', 'b', type=int),
    ], RepeatingGroup.ReprCountFromPayload('b')),
    #WireField('ice-number-of-hedge-definition', 'b', type=int),
    RepeatingGroup([
        WireField('ice-hedge-body-length', 'b', type=int),
        WireField('ice-hedge-market-id', 'i', type=int),
        WireField('ice-hedge-security-type', 'b', type=int),
        WireField('ice-hedge-side', 'b', type=int),
        WireField('ice-hedge-price', 'q', type=int),
        WireField('ice-hedge-price-denominator', 'b', type=int),
        WireField('ice-hdege-delta', 'h', type=int),
    ], RepeatingGroup.ReprCountFromPayload('b')),
], endian='Big') 

NewOptionsMarketDefinition = Descriptor([
    WireField('ice-market-id', 'i', type=int),
    WireField('ice-underlying-market-id', 'i', type=int),
    WireField('ice-contract-symbol', '70s', type=TrimmedString),
    WireField('ice-trading-status', 'b', type=int),
    WireField('ice-order-price-denominator', 'b', type=int),
    WireField('ice-increment-qty', 'i', type=int),
    WireField('ice-lot-size', 'i', type=int),
    WireField('ice-market-desc', '120s', type=TrimmedString),
    WireField('ice-option-type', 'b', type=int),
    WireField('ice-strike-price', 'q', type=int),
    WireField('ice-deal-price-denominator', 'b', type=int),
    WireField('ice-min-qty', 'i', type=int),
    WireField('ice-currency', '20s', type=TrimmedString),
    WireField('ice-num-decimals-strike-price', 'b', type=int),
    WireField('ice-min-options-price', 'q', type=int),
    WireField('ice-max-options-price', 'q', type=int),
    WireField('ice-increment-premium-price', 'i', type=int),
    WireField('ice-options-expiration-year', 'h', type=int),
    WireField('ice-options-expiration-month', 'h', type=int),
    WireField('ice-options-expiration-day', 'h', type=int),
    WireField('ice-options-settlment-type', 'b', type=int),
    WireField('ice-options-expiration-type', 'b', type=int),
    WireField('ice-serial-underlying-market-id', 'i', type=int),
], endian='Big') 

RFQ = Descriptor([
    WireField('ice-market-id', 'i', type=int),
    WireField('ice-message-timestamp', 'q', type=int),
    WireField('ice-rfq-system-id', 'q', type=int),
    WireField('ice-market-type-id', 'h', type=int),
    WireField('ice-underlying-market-id', 'i', type=int),
    WireField('ice-quantity', 'i', type=int),
    WireField('ice-side', 'b', type=int),
], endian='Big') 

OptionOpenInterest = Descriptor([
    WireField('ice-market-id', 'i', type=int),
    WireField('ice-openinterest', 'i', type=int),
    WireField('ice-date-time', 'q', type=int),
    WireField('ice-openinterestdate', '10s', type=TrimmedString),
], endian='Big') 

OptionSettlementPrice = Descriptor([
    WireField('ice-market-id', 'i', type=int),
    WireField('ice-settlementpricewithdealpriceprecision', 'q', type=int),
    WireField('ice-date-time', 'q', type=int),
    WireField('ice-is-official', 'b', type=int), 
    WireField('ice-valuation-date-time', 'q', type=int),
    WireField('ice-volatility', 'q', type=int),
    WireField('ice-settlement-price', 'q', type=int),
    WireField('ice-delta', 'q', type=int),
], endian='Big') 

OldStyleOptionsTradeAndMarketStats = Descriptor([
    WireField('ice-underlying-market-id', 'i', type=int),
    WireField('ice-trade-id', 'q', type=int),
    WireField('ice-price', 'q', type=int),
    WireField('ice-quantity', 'i', type=int),
    WireField('ice-off-market-trade-type', 'b', type=int),
    WireField('ice-transact-date-time', 'q', type=int),
    WireField('ice-option-type', 'b', type=int),
    WireField('ice-strike-price', 'q', type=int),
    WireField('ice-event-code', 'b', type=int),
    WireField('ice-total-volume', 'i', type=int),
    WireField('ice-block-volume', 'i', type=int),
    WireField('ice-efs-volume', 'i', type=int),
    WireField('ice-efp-volume', 'i', type=int),
    WireField('ice-high', 'q', type=int),
    WireField('ice-low', 'q', type=int),
    WireField('ice-vwap', 'q', type=int),
], endian='Big')

