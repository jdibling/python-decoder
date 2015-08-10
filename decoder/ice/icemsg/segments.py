from base.descriptor import *

MessageBlock = Descriptor([
    WireField('ice-session-num', 'h'),
    WireField('ice-sequence-num', 'i'),
    WireField('ice-num-msgs', 'h'),
    WireField('ice-sent-date-time', 'q')
], endian='Big')

MessageHeader = Descriptor([
    WireField('ice-msg-type', 'c'),
    WireField('ice-msg-body-length', 'h')
], endian='Big')

MarketSnapshot = Descriptor([
    WireField('market-id',                                 'i'),
    WireField('market-type',                               'h'),
    WireField('trading-status',                            'c'),
    WireField('volume',                                    'i'),
    WireField('block-volume',                              'i'),
    WireField('efs-volume',                                'i'),
    WireField('efp-volume',                                'i'),
    WireField('open-interest',                             'i'),
    WireField('opening-price',                             'q'),
    WireField('settlement-price-with-deal-priceprecision', 'q'),
    WireField('high',                                      'q'),
    WireField('low',                                       'q'),
    WireField('vwap',                                      'q'),
    WireField('num-of-bookentries',                        'i'),
    WireField('last-trade-price',                          'q'),
    WireField('last-trade-quantity',                       'i'),
    WireField('last-trade-date-time',                       'q'),
    WireField('settle-price-date-time',                     'q'),
    WireField('last-message-sequenceid',                   'i'),
    WireField('reserved-field1',                           'h'),
    WireField('open-interest-date',                        '10s', type=TrimmedString),
    WireField('is-settle-price-official',                  'c'),
    WireField('settlement-price',                          'q'),
], endian='Big') 

Trade = Descriptor([
    WireField('ice-market-id', 'i'),
    WireField('ice-trade-id', 'q'),
    WireField('ice-system-priced-leg', 'c'),
    WireField('ice-price-unscaled', 'q'),
    WireField('ice-quantity', 'i'),
    WireField('ice-off-market-trade-type', 'c'),
    WireField('ice-transact-date-time', 'q'),
    WireField('ice-system-priced-leg-type', 'c'),
    WireField('ice-is-implied-spread-at-market-open', 'c'),
    WireField('ice-is-adjusted-trade', 'c'),
    WireField('ice-aggressor-side', 'c'),
    WireField('ice-extra-flags', 'b')
], endian='Big')

SpotTrade = Descriptor([
    WireField('ice-market-id', 'i'),
    WireField('ice-trade-id', 'q'),
    WireField('ice-price', 'q'),
    WireField('ice-quantity', 'i'),
    WireField('ice-transact-date-time', 'q'),
    WireField('ice-extra-flags', 'b'),
    WireField('ice-delivery-begin-date-time', 'q')
], endian='Big') 

InvestigatedTrade = Descriptor([
    WireField('ice-market-id', 'i'),
    WireField('ice-trade-id', 'q'),
    WireField('ice-price', 'q'),
    WireField('ice-quantity', 'i'),
    WireField('ice-off-market-trade-type', 'c'),
    WireField('ice-date-time', 'q'),
    WireField('ice-status', 'c')
], endian='Big')

CancelledTrade = Descriptor([
    WireField('ice-market-id', 'i'),
    WireField('ice-trade-id', 'q'),
    WireField('ice-price', 'q'),
    WireField('ice-quantity', 'i'),
    WireField('ice-off-market-trade-type', 'c'),
    WireField('ice-date-time', 'q'),
  ], endian='Big') 
  
MarketStatistics = Descriptor([
    WireField('ice-market-id', 'i'),
    WireField('ice-volume', 'i'),
    WireField('ice-block-volume', 'i'),
    WireField('ice-efs-volume', 'i'),
    WireField('ice-efp-volume', 'i'),
    WireField('ice-high', 'q'),
    WireField('ice-low', 'q'),
    WireField('ice-vwap', 'q'),
    WireField('ice-date-time', 'q'),
], endian='Big')
  
MarketStateChange = Descriptor([
    WireField('ice-market-id', 'i'),
    WireField('ice-trading-status', 'c'),
    WireField('ice-date-time', 'q'),
], endian='Big') 
  
SystemText = Descriptor([
    WireField('ice-text-message', '200s', type=TrimmedString),
    WireField('ice-date-time', 'q'),
    WireField('ice-text-message-extra-fld', '800s', type=TrimmedString),
], endian='Big') 
  
OpenInterest = Descriptor([
    WireField('ice-market-id', 'i'),
    WireField('ice-open-interest', 'i'),
    WireField('ice-open-interest-change', 'i'),
    WireField('ice-date-time', 'q'),
    WireField('ice-open-interest-date', '10s', type=TrimmedString),
], endian='Big') 
  
OpenPrice = Descriptor([
    WireField('ice-market-id', 'i'),
    WireField('ice-open-price', 'q'),
    WireField('ice-date-time', 'q'),
], endian='Big')

ClosePrice = Descriptor([
    WireField('ice-market-id', 'i'),
    WireField('ice-close-price', 'q'),
    WireField('ice-date-time', 'q'),
], endian='Big')

SettlementPrice = Descriptor([
    WireField('ice-market-id', 'i'),
    WireField('ice-settlement-price-with-deal-price-precision', 'q'),
    WireField('ice-date-time', 'q'),
    WireField('ice-is-official', 'c'),
    WireField('ice-valuation-date-time', 'q'),
    WireField('ice-settlement-price', 'q'),
], endian='Big')
  
MarkerIndexPrices = Descriptor([
    WireField('ice-market-id', 'i'),
    WireField('ice-price', 'q'),
    WireField('ice-short-name', '30s', type=TrimmedString),
    WireField('ice-published-date-time', 'q'),
    WireField('ice-valuation-date', '10s', type=TrimmedString),
], endian='Big') 

EndOfDayMarketSummary = Descriptor([
    WireField('ice-market-id', 'i'),
    WireField('ice-volume', 'i'),
    WireField('ice-block-volume', 'i'),
    WireField('ice-efs-volume', 'i'),
    WireField('ice-efp-volume', 'i'),
    WireField('ice-opening-price', 'q'),
    WireField('ice-high', 'q'),
    WireField('ice-low', 'q'),
    WireField('ice-vwap', 'q'),
    WireField('ice-settlement=price', 'q'),
    WireField('ice-open-interest', 'i'),
    WireField('ice-date-time', 'q'),
], endian='Big') 

MarketEvent = Descriptor([
    WireField('ice-market-id', 'i'),
    WireField('ice-event-type', 'c'),
    WireField('ice-date-time', 'q'),
], endian='Big') 

PreOpenPriceIndicator = Descriptor([
    WireField('ice-market-id', 'i'),
    WireField('ice-pre-open-price', 'q'),
    WireField('ice-date-time', 'q'),
], endian='Big')

IntervalPriceLimitNotification = Descriptor([
    WireField('ice-market-id', 'i'),
    WireField('ice-ipl-hold-type', 'c'),
    WireField('ice-notification-date-time', 'q'),
    WireField('ice-is-up', 'c'),
    WireField('ice-ipl-hold-duration', 'i'),
    WireField('ice-ipl-up', 'q'),
    WireField('ice-ipl-down', 'q'),
], endian='Big') 

NewFuturesStrategyDefinition = Descriptor([
    WireField('ice-market-id', 'i'),
    WireField('ice-contract-symbol', '70s', type=TrimmedString),
    WireField('ice-trading-status', 'c'),
    WireField('ice-order-price-denominator', 'b'),
    WireField('ice-increment-price', 'i'),
    WireField('ice-increment-qty', 'i'),
    WireField('ice-min-qty', 'i'),
    RepeatingGroup([
        WireField('ice-legbody-length', 'b'),
        WireField('ice-leg-market-id', 'i'),
        WireField('ice-leg-ratio', 'h'),
        WireField('ice-leg-side', 'c'),
    ], RepeatingGroup.ReprCountFromPayload('b'), embed_as='ice-leg-definition'),
], endian='Big')

UnknownTest = Descriptor([
    WireField('ice-market-id', 'i'),
], endian='Big') 

SnapshotOrder = Descriptor([
    WireField('ice-market-id', 'i'),
    WireField('ice-orderid', 'q'),
    WireField('ice-order-sequenceid', 'h'),
    WireField('ice-side', 'c'),
    WireField('ice-price', 'q'),
    WireField('ice-quantity', 'i'),
    WireField('ice-is-implied', 'c'),
    WireField('ice-is-rfq', 'c'),
    WireField('ice-order-entry-date-time', 'q'),
    WireField('ice-sequence-within-millis', 'i'),

], endian='Big')

AddModifyOrder = Descriptor([
    WireField('ice-market-id', 'i'),
    WireField('ice-orderid', 'q'),
    WireField('ice-order-sequenceid', 'h'),
    WireField('ice-side', 'c'),
    WireField('ice-price', 'q'),
    WireField('ice-quantity', 'i'),
    WireField('ice-is-implied', 'c'),
    WireField('ice-is-rfq', 'c'),
    WireField('ice-order-entry-date-time', 'q'),
    WireField('ice-extra-flags', 'b'),
    WireField('ice-sequence-within-millis', 'i'),
], endian='Big') 

DeleteOrder = Descriptor([
    WireField('ice-market-id', 'i'),
    WireField('ice-orderid', 'q'),
], endian='Big') 

MessageBundleMarker = Descriptor([
    WireField('ice-start-or-end', 'c'),
], endian='Big') 

SnapshotPriceLevel = Descriptor([
    WireField('ice-market-id', 'i'),
    WireField('ice-side', 'c'),
    WireField('ice-price-level-position', 'b'),
    WireField('ice-price', 'q'),
    WireField('ice-quantity', 'i'),
    WireField('ice-order-count', 'h'),
    WireField('ice-implied-quantity', 'i'),
    WireField('ice-implied-order-count', 'h'),
], endian='Big') 

AddPriceLevel = Descriptor([
    WireField('ice-market-id', 'i'),
    WireField('ice-side', 'c'),
    WireField('ice-price-level-position', 'b'),
    WireField('ice-price', 'q'),
    WireField('ice-quantity', 'i'),
    WireField('ice-order-count', 'h'),
    WireField('ice-implied-quantity', 'i'),
    WireField('ice-implied-order-count', 'h'),
], endian='Big') 

ChangePriceLevel = Descriptor([
    WireField('ice-market-id', 'i'),
    WireField('ice-side', 'c'),
    WireField('ice-price-level-position', 'b'),
    WireField('ice-price', 'q'),
    WireField('ice-quantity', 'i'),
    WireField('ice-order-count', 'h'),
    WireField('ice-implied-quantity', 'i'),
    WireField('ice-implied-order-count', 'h'),
], endian='Big') 

DeletePriceLevel = Descriptor([
    WireField('ice-market-id', 'i'),
    WireField('ice-side', 'c'),
    WireField('ice-price-level-position', 'b'),
], endian='Big') 

NewOptionsStrategyDefinition = Descriptor([
    WireField('ice-market-id', 'i'),
    WireField('ice-underlying-market-id', 'i'),
    WireField('ice-contract-symbol', '35s', type=TrimmedString),
    WireField('ice-trading-status', 'c'),
    WireField('ice-order-price-denominator', 'c'),
    WireField('ice-increment-price', 'i'),
    WireField('ice-increment-qty', 'i'),
    WireField('ice-min-qty', 'i'),
    RepeatingGroup([
        WireField('ice-leg-body-length', 'b'),
        WireField('ice-leg-market-id', 'i'),
        WireField('ice-leg-underlying-market-id', 'i'),
        WireField('ice-leg-ratio', 'h'),
        WireField('ice-leg-side', 'c'),
    ], RepeatingGroup.ReprCountFromPayload('b'), embed_as='ice-leg-definition'),
    RepeatingGroup([
        WireField('ice-hedge-body-length', 'b'),
        WireField('ice-hedge-market-id', 'i'),
        WireField('ice-hedge-security-type', 'c'),
        WireField('ice-hedge-side', 'c'),
        WireField('ice-hedge-price', 'q'),
        WireField('ice-hedge-price-denominator', 'c'),
        WireField('ice-hedge-delta', 'h'),
     ], RepeatingGroup.ReprCountFromPayload('b'), embed_as='ice-hedge-definition'),
], endian='Big') 

NewOptionsMarketDefinition = Descriptor([
    WireField('ice-market-id', 'i'),
    WireField('ice-underlying-market-id', 'i'),
    WireField('ice-contract-symbol', '70s', type=TrimmedString),
    WireField('ice-trading-status', 'c'),
    WireField('ice-order-price-denominator', 'b'),
    WireField('ice-increment-qty', 'i'),
    WireField('ice-lot-size', 'i'),
    WireField('ice-market-desc', '120s', type=TrimmedString),
    WireField('ice-option-type', 'c'),
    WireField('ice-strike-price', 'q'),
    WireField('ice-deal-price-denominator', 'b'),
    WireField('ice-min-qty', 'i'),
    WireField('ice-currency', '20s', type=TrimmedString),
    WireField('ice-num-decimals-strike-price', 'c'),
    WireField('ice-min-options-price', 'q'),
    WireField('ice-max-options-price', 'q'),
    WireField('ice-increment-premium-price', 'i'),
    WireField('ice-options-expiration-year', 'h'),
    WireField('ice-options-expiration-month', 'h'),
    WireField('ice-options-expiration-day', 'h'),
    WireField('ice-options-settlment-type', 'c'),
    WireField('ice-options-expiration-type', 'c'),
    WireField('ice-serial-underlying-market-id', 'i'),
], endian='Big') 

RFQ = Descriptor([
    WireField('ice-market-id', 'i'),
    WireField('ice-message-timestamp', 'q'),
    WireField('ice-rfq-system-id', 'q'),
    WireField('ice-market-type-id', 'h'),
    WireField('ice-underlying-market-id', 'i'),
    WireField('ice-quantity', 'i'),
    WireField('ice-side', 'c'),
], endian='Big') 

OptionOpenInterest = Descriptor([
    WireField('ice-market-id', 'i'),
    WireField('ice-openinterest', 'i'),
    WireField('ice-date-time', 'q'),
    WireField('ice-openinterestdate', '10s', type=TrimmedString),
], endian='Big') 

OptionSettlementPrice = Descriptor([
    WireField('ice-market-id', 'i'),
    WireField('ice-settlementpricewithdealpriceprecision', 'q'),
    WireField('ice-date-time', 'q'),
    WireField('ice-is-official', 'c'), 
    WireField('ice-valuation-date-time', 'q'),
    WireField('ice-volatility', 'q'),
    WireField('ice-settlement-price', 'q'),
    WireField('ice-delta', 'q'),
], endian='Big') 

OldStyleOptionsTradeAndMarketStats = Descriptor([
    WireField('ice-underlying-market-id', 'i'),
    WireField('ice-trade-id', 'q'),
    WireField('ice-price', 'q'),
    WireField('ice-quantity', 'i'),
    WireField('ice-off-market-trade-type', 'c'),
    WireField('ice-transact-date-time', 'q'),
    WireField('ice-option-type', 'c'),
    WireField('ice-strike-price', 'q'),
    WireField('ice-event-code', 'c'),
    WireField('ice-total-volume', 'i'),
    WireField('ice-block-volume', 'i'),
    WireField('ice-efs-volume', 'i'),
    WireField('ice-efp-volume', 'i'),
    WireField('ice-high', 'q'),
    WireField('ice-low', 'q'),
    WireField('ice-vwap', 'q'),
], endian='Big')

# TCP Messages
# # Login
LoginRequest = Descriptor([
    WireField('ice-request-seq-id',          'i',   type=int),
    WireField('ice-user-name',               '30s', type=TrimmedString),
    WireField('ice-password',                '30s', type=TrimmedString),
    WireField('ice-get-strip-info-messages', 'c'),
    WireField('resv1',                       'h',   hidden=True),
], endian='Big')

LoginResponse = Descriptor([
    WireField('ice-request-seq-id',            'i',    type=int),
    WireField('ice-code',                      'c'),
    WireField('ice-text',                      '120s', type=TrimmedString),
    WireField('ice-market-types-permissioned', '300s', type=TrimmedString)
], endian='Big')

# # Product Definitions
ProductDefRequest = Descriptor([
    WireField('ice-request-seq-id', 'i'),
    WireField('ice-market-type',    'h'),
    WireField('ice-security-type',  'c')
], endian='Big')

ProductDefResponseFutures = Descriptor([
    WireField('ice-request-seq-id',              'i'),
    WireField('ice-request-market-type',         'h'),
    WireField('ice-num-of-markets',              'h'),
    WireField('ice-market-id',                   'i'),
    WireField('ice-contract-symbol',             '35s', type=TrimmedString),
    WireField('ice-trading-status',              'c'),
    WireField('ice-order-price-denominator',     'c'),
    WireField('ice-increment-price',             'i'),
    WireField('ice-increment-qty',               'i'),
    WireField('ice-lot-size',                    'i'),
    WireField('ice-market-desc',                 '120s', type=TrimmedString),
    WireField('ice-maturity-year',               'h'),
    WireField('ice-maturity-month',              'h'),
    WireField('ice-maturity-day',                'h'),
    WireField('ice-is-spread',                   'c'),
    WireField('ice-is-crack-spread',             'c'),
    WireField('ice-primary-market-id',           'i'),
    WireField('ice-secondary-market-id',         'i'),
    WireField('ice-is-options',                  'c'),
    WireField('ice-option-type',                 'c'),
    WireField('ice-strike-price',                'q'),
    WireField('ice-second-strike',               'q'),
    WireField('ice-deal-price-denominator',      'c'),
    WireField('ice-min-qty',                     'i'),
    WireField('ice-unit-qty',                    'i'),
    WireField('ice-currency',                    '20s', type=TrimmedString),
    WireField('ice-min-strike-price',            'q'),
    WireField('ice-max-strike-price',            'q'),
    WireField('ice-increment-strike-price',      'i'),
    WireField('ice-num-decimals-strike-price',   'c'),
    WireField('ice-min-options-price',           'q'),
    WireField('ice-max-options-price',           'q'),
    WireField('ice-increment-options-price',     'i'),
    WireField('ice-num-decimals-options-price',  'c'),
    WireField('ice-tick-value',                  'q'),
    WireField('ice-allow-options',               'c'),
    WireField('ice-cleared-alias',               '15s', type=TrimmedString),
    WireField('ice-allows-implied',              'c'),
    WireField('ice-options-expiration-year',     'h'),
    WireField('ice-options-expiration-month',    'h'),
    WireField('ice-options-expiration-day',      'h'),
    WireField('ice-min-price',                   'q'),
    WireField('ice-max-price',                   'q'),
    WireField('ice-product-id',                  'h'),
    WireField('ice-product-name',                '62s', type=TrimmedString),
    WireField('ice-hub-id',                      'h'),
    WireField('ice-hub-alias',                   '80s', type=TrimmedString),
    WireField('ice-strip-id',                    'h'),
    WireField('ice-strip-alias',                 '39s', type=TrimmedString),
    WireField('resv1',                           'c'),
    WireField('ice-is-serial-options-supported', 'c'),
    WireField('ice-is-tradable',                 'c'),
    WireField('ice-settle-price-denominator',    'c'),
    WireField('ice-mic-code',                    '4s', type=TrimmedString),
    WireField('ice-unit-qty-denominator',        'c')
], endian='Big')

StripInfo = Descriptor([
    WireField('ice-strip-id',    'h'),
    WireField('ice-strip-type',  '20s', type=TrimmedString),
    WireField('ice-begin-year',  'h'),
    WireField('ice-begin-month', 'h'),
    WireField('ice-begin-day',   'h'),
    WireField('ice-end-year',    'h'),
    WireField('ice-end-month',   'h'),
    WireField('ice-end-day',     'h'),
    WireField('ice-strip-name',  '50s', type=TrimmedString)
], endian='Big')

ProductDefResponseOptions = Descriptor([
    WireField('ice-request-seq-id',              'i'),
    WireField('ice-request-market-type',         'h'),
    WireField('ice-num-of-markets-obsolete',     'h'),
    WireField('ice-market-id',                   'i'),
    WireField('ice-underlying-market-id',        'i'),
    WireField('ice-contract-symbol',             '35s', type=TrimmedString),
    WireField('ice-trading-status',              'c'),
    WireField('ice-order-price-denominator',     'c'),
    WireField('ice-increment-qty',               'i'),
    WireField('ice-lot-size',                    'i'),
    WireField('ice-market-desc',                 '120s', type=TrimmedString),
    WireField('ice-option-type',                 'c'),
    WireField('ice-strike-price',                'q'),
    WireField('ice-deal-price-denominator',      'c'),
    WireField('ice-min-qty',                     'i'),
    WireField('ice-currency',                    '20s', type=TrimmedString),
    WireField('ice-num-decimals-strike-price',   'c'),
    WireField('ice-min-options-price',           'q'),
    WireField('ice-max-options-price',           'q'),
    WireField('ice-increment-premium-price',     'i'),
    WireField('ice-options-expiration-year',     'h'),
    WireField('ice-options-expiration-month',    'h'),
    WireField('ice-options-expiration-day',      'h'),
    WireField('ice-options-settlment-type',      'c'),
    WireField('ice-options-expiration-type',     'c'),
    WireField('ice-num-of-markets',              'i'),
    WireField('ice-serial-underlying-market-id', 'i'),
    WireField('ice-contract-symbol-extra',       '35s', type=TrimmedString),
    WireField('ice-settle-price-denominator',    'c'),
    WireField('ice-unit-qty-denominator',        'c'),
], endian='Big')

StrategyDefResponseOptions = Descriptor([
    WireField('ice-request-seq-id',             'i'),
    WireField('ice-request-market-type',        'h'),
    WireField('ice-num-of-markets',             'h'),
    WireField('ice-market-id',                  'i'),
    WireField('ice-underlying-market-id',       'i'),
    WireField('ice-contract-symbol',            '35s', type=TrimmedString),
    WireField('ice-trading-status',             'c'),
    WireField('ice-order-price-denominator',    'c'),
    WireField('ice-increment-price',            'i'),
    WireField('ice-increment-qty',              'i'),
    WireField('ice-min-qty',                    'i'),
    RepeatingGroup([
        WireField('ice-leg-body-length',          'b'),
        WireField('ice-leg-market-id',            'i'),
        WireField('ice-leg-underlying-market-id', 'i'),
        WireField('ice-leg-ratio',                'h'),
        WireField('ice-leg-side',                 'c'),
    ], RepeatingGroup.ReprCountFromPayload('b'), embed_as='ice-leg-definition'),
    RepeatingGroup([
        WireField('ice-hedge-body-length',       'b'),
        WireField('ice-hedge-market-id',         'i'),
        WireField('ice-hedge-security-type',     'c'),
        WireField('ice-hedge-side',              'c'),
        WireField('ice-hedge-price',             'q'),
        WireField('ice-hedge-price-denominator', 'c'),
        WireField('ice-hedge-delta',             'h'),
    ], RepeatingGroup.ReprCountFromPayload('b'), embed_as='ice-hedge-definition'),
], endian='Big')

StrategyDefResponseFutures = Descriptor([
    WireField('ice-request-seq-id',           'i'),
    WireField('ice-request-market-type',      'h'),
    WireField('ice-num-of-markets',           'h'),
    WireField('ice-market-id',                'i'),
    WireField('ice-contract-symbol',          '70s', type=TrimmedString),
    WireField('ice-trading-status',           'c'),
    WireField('ice-order-price-denominator',  'c'),
    WireField('ice-increment-price',          'i'),
    WireField('ice-increment-qty',            'i'),
    WireField('ice-min-qty',                  'i'),
    RepeatingGroup([
        WireField('ice-leg-body-length',      'b'),
        WireField('ice-leg-market-id',        'i'),
        WireField('ice-leg-ratio',            'h'),
        WireField('ice-leg-side',             'c'),
    ], RepeatingGroup.ReprCountFromPayload('b'), embed_as='ice-leg-definition'),
], endian='Big')

# # Historical Replay
HistoricalRequest = Descriptor([
    WireField('ice-request-seq-id',        'i'),
    WireField('ice-multicast-group-addr',  '15s', type=TrimmedString),
    WireField('ice-multicast-port',        'h'),
    WireField('ice-session-id',            'h'),
    WireField('ice-start-sequence-number', 'i'),
    WireField('ice-end-sequence-number',   'i'),
], endian='Big')

HistoricalResponse = Descriptor([
    WireField('ice-request-seq-id',        'i'),
    WireField('ice-multicast-group-addr',  '15s', type=TrimmedString),
    WireField('ice-multicast-port',        'h'),
    WireField('ice-session-id',            'h'),
    WireField('ice-start-sequence-number', 'i'),
    WireField('ice-end-sequence-number',   'i'),
], endian='Big')

# # Debug Message
DebugRequest = Descriptor([
    WireField('ice-request-seq-id', 'i'),
], endian='Big')

DebugResponse = Descriptor([
    WireField('ice-request-seq-id', 'i'),
    WireField('ice-text',           '60s', type=TrimmedString),
], endian='Big')

# # HeartBeat
HeartBeat = Descriptor([
    WireField('ice-request-seq-id', 'i'),
], endian='Big')

# # Logout
LogoutRequest = Descriptor([
    WireField('ice-request-seq-id', 'i'),
], endian='Big')

# # ErrorResponse
ErrorResponse = Descriptor([
    WireField('ice-request-seq-id', 'i'),
    WireField('ice-code',           'c'),
    WireField('ice-text',           '100s', type=TrimmedString),
])
