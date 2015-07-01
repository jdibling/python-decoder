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

# TODO Repeating Groups in here?
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

# TCP Messages

# # Login
LoginRequest = Descriptor([
    WireField('ice-request-seq-id',          'i',   type=int),
    WireField('ice-user-name',               '30s', type=TrimmedString),
    WireField('ice-password',                '30s', type=TrimmedString),
    WireField('ice-get-strip-info-messages', 'c'),
    WireField('ice-request-seq-id',          'i',   type=int),
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
    WireField('ice-request-seq-id', 'i', type=int),
    WireField('ice-market-type',    'h', type=int),
    WireField('ice-security-type',  'c')
], endian='Big')

ProductDefResponseFutures = Descriptor([
    WireField('ice-request-seq-id',              'i', type=int),
    WireField('ice-request-market-type',         'h', type=int),
    WireField('ice-num-of-markets',              'h', type=int),
    WireField('ice-market-id',                   'i', type=int),
    WireField('ice-contract-symbol',             '35s', type=TrimmedString),
    WireField('ice-trading-status',              'c'),
    WireField('ice-order-price-denominator',     'c'),
    WireField('ice-increment-price',             'i', type=int),
    WireField('ice-increment-qty',               'i', type=int),
    WireField('ice-lot-size',                    'i', type=int),
    WireField('ice-market-desc',                 '120s', type=TrimmedString),
    WireField('ice-maturity-year',               'h', type=int),
    WireField('ice-maturity-month',              'h', type=int),
    WireField('ice-maturity-day',                'h', type=int),
    WireField('ice-is-spread',                   'c'),
    WireField('ice-is-crack-spread',             'c'),
    WireField('ice-primary-market-id',           'i', type=int),
    WireField('ice-secondary-market-id',         'i', type=int),
    WireField('ice-is-options',                  'c'),
    WireField('ice-option-type',                 'c'),
    WireField('ice-strike-price',                'q', type=int),
    WireField('ice-second-strike',               'q', type=int),
    WireField('ice-deal-price-denominator',      'c'),
    WireField('ice-min-qty',                     'i', type=int),
    WireField('ice-unit-qty',                    'i', type=int),
    WireField('ice-currency',                    '20s', type=TrimmedString),
    WireField('ice-min-strike-price',            'q', type=int),
    WireField('ice-max-strike-price',            'q', type=int),
    WireField('ice-increment-strike-price',      'i', type=int),
    WireField('ice-num-decimals-strike-price',   'c'),
    WireField('ice-min-options-price',           'q', type=int),
    WireField('ice-max-options-price',           'q', type=int),
    WireField('ice-increment-options-price',     'i', type=int),
    WireField('ice-num-decimals-options-price',  'c'),
    WireField('ice-tick-value',                  'q', type=int),
    WireField('ice-allow-options',               'c'),
    WireField('ice-cleared-alias',               '15s', type=TrimmedString),
    WireField('ice-allows-implied',              'c'),
    WireField('ice-options-expiration-year',     'h', type=int),
    WireField('ice-options-expiration-month',    'h', type=int),
    WireField('ice-options-expiration-day',      'h', type=int),
    WireField('ice-min-price',                   'q', type=int),
    WireField('ice-max-price',                   'q', type=int),
    WireField('ice-product-id',                  'h', type=int),
    WireField('ice-product-name',                '62s', type=TrimmedString),
    WireField('ice-hub-id',                      'h', type=int),
    WireField('ice-hub-alias',                   '80s', type=TrimmedString),
    WireField('ice-strip-id',                    'h', type=int),
    WireField('ice-strip-alias',                 '39s', type=TrimmedString),
    WireField('resv1',                           'c'),
    WireField('ice-is-serial-options-supported', 'c'),
    WireField('ice-is-tradable',                 'c'),
    WireField('ice-settle-price-denominator',    'c'),
    WireField('ice-mic-code',                    '4s', type=TrimmedString),
    WireField('ice-unit-qty-denominator',        'c')
], endian='Big')

StripInfo = Descriptor([
    WireField('ice-strip-id',    'h', type=int),
    WireField('ice-strip-type',  '20s', type=TrimmedString),
    WireField('ice-begin-year',  'h', type=int),
    WireField('ice-begin-month', 'h', type=int),
    WireField('ice-begin-day',   'h', type=int),
    WireField('ice-end-year',    'h', type=int),
    WireField('ice-end-month',   'h', type=int),
    WireField('ice-end-day',     'h', type=int),
    WireField('ice-strip-name',  '50s', type=TrimmedString)
], endian='Big')

ProductDefResponseOptions = Descriptor([
    WireField('ice-request-seq-id',              'i', type=int),
    WireField('ice-request-market-type',         'h', type=int),
    WireField('ice-num-of-markets-obsolete',     'h', type=int),
    WireField('ice-market-id',                   'i', type=int),
    WireField('ice-underlying-market-id',        'i', type=int),
    WireField('ice-contract-symbol',             '35s', type=TrimmedString),
    WireField('ice-trading-status',              'c'),
    WireField('ice-order-price-denominator',     'c'),
    WireField('ice-increment-qty',               'i', type=int),
    WireField('ice-lot-size',                    'i', type=int),
    WireField('ice-market-desc',                 '120s', type=TrimmedString),
    WireField('ice-option-type',                 'c'),
    WireField('ice-strike-price',                'q', type=int),
    WireField('ice-deal-price-denominator',      'c'),
    WireField('ice-min-qty',                     'i', type=int),
    WireField('ice-currency',                    '20s', type=TrimmedString),
    WireField('ice-num-decimals-strike-price',   'c'),
    WireField('ice-min-options-price',           'q', type=int),
    WireField('ice-max-options-price',           'q', type=int),
    WireField('ice-increment-premium-price',     'i', type=int),
    WireField('ice-options-expiration-year',     'h', type=int),
    WireField('ice-options-expiration-month',    'h', type=int),
    WireField('ice-options-expiration-day',      'h', type=int),
    WireField('ice-options-settlment-type',      'c'),
    WireField('ice-options-expiration-type',     'c'),
    WireField('ice-num-of-markets',              'i', type=int),
    WireField('ice-serial-underlying-market-id', 'i', type=int),
    WireField('ice-contract-symbol-extra',       '35s', type=TrimmedString),
    WireField('ice-settle-price-denominator',    'c'),
    WireField('ice-unit-qty-denominator',        'c'),
], endian='Big')

StrategyDefResponseOptions = Descriptor([
    WireField('ice-request-seq-id',             'i', type=int),
    WireField('ice-request-market-type',        'h', type=int),
    WireField('ice-num-of-markets',             'h', type=int),
    WireField('ice-market-id',                  'i', type=int),
    WireField('ice-underlying-market-id',       'i', type=int),
    WireField('ice-contract-symbol',            '35s', type=TrimmedString),
    WireField('ice-trading-status',             'c'),
    WireField('ice-order-price-denominator',    'c'),
    WireField('ice-increment-price',            'i', type=int),
    WireField('ice-increment-qty',              'i', type=int),
    WireField('ice-min-qty',                    'i', type=int),
    WireField('ice-number-of-leg-definition',   'b', type=int),  # repeating group...
    WireField('ice-leg-body-length',            'b', type=int),
    WireField('ice-leg-market-id',              'i', type=int),
    WireField('ice-leg-underlying-market-id',   'i', type=int),
    WireField('ice-leg-ratio',                  'h', type=int),
    WireField('ice-leg-side',                   'i', type=int),
    WireField('ice-number-of-hedge-definition', 'b', type=int),  # repeating group...
    WireField('ice-hedge-body-length',          'b', type=int),
    WireField('ice-hedge-market-id',            'i', type=int),
    WireField('ice-hedge-security-type',        'c'),
    WireField('ice-hedge-side',                 'c'),
    WireField('ice-hedge-price',                'q', type=int),
    WireField('ice-hedge-price-denominator',    'c'),
    WireField('ice-hedge-delta',                'i', type=int),
], endian='Big')

StrategyDefResponseFutures = Descriptor([
    WireField('ice-request-seq-id',           'i', type=int),
    WireField('ice-request-market-type',      'h', type=int),
    WireField('ice-num-of-markets',           'h', type=int),
    WireField('ice-market-id',                'i', type=int),
    WireField('ice-contract-symbol',          '70s', type=TrimmedString),
    WireField('ice-trading-status',           'c'),
    WireField('ice-order-price-denominator',  'c'),
    WireField('ice-increment-price',          'i', type=int),
    WireField('ice-increment-qty',            'i', type=int),
    WireField('ice-min-qty',                  'i', type=int),
    WireField('ice-number-of-leg-definition', 'b', type=int),  # repeating group...
    WireField('ice-leg-body-length',          'b', type=int),
    WireField('ice-leg-market-id',            'i', type=int),
    WireField('ice-leg-ratio',                'h', type=int),
    WireField('ice-leg-side',                 'i', type=int),
], endian='Big')

# # Historical Replay
HistoricalRequest = Descriptor([
    WireField('ice-request-seq-id',        'i', type=int),
    WireField('ice-multicast-group-addr',  '15s', type=TrimmedString),
    WireField('ice-multicast-port',        'h', type=int),
    WireField('ice-session-id',            'h', type=int),
    WireField('ice-start-sequence-number', 'i', type=int),
    WireField('ice-end-sequence-number',   'i', type=int),
], endian='Big')

HistoricalResponse = Descriptor([
    WireField('ice-request-seq-id',        'i', type=int),
    WireField('ice-multicast-group-addr',  '15s', type=TrimmedString),
    WireField('ice-multicast-port',        'h', type=int),
    WireField('ice-session-id',            'h', type=int),
    WireField('ice-start-sequence-number', 'i', type=int),
    WireField('ice-end-sequence-number',   'i', type=int),
], endian='Big')

# # Debug Message
DebugRequest = Descriptor([
    WireField('ice-request-seq-id', 'i', type=int),
], endian='Big')

DebugResponse = Descriptor([
    WireField('ice-request-seq-id', 'i', type=int),
    WireField('ice-text',           '60s', type=TrimmedString),
], endian='Big')

# # HeartBeat
HeartBeat = Descriptor([
    WireField('ice-request-seq-id', 'i', type=int),
], endian='Big')

# # Logout
LogoutRequest = Descriptor([
    WireField('ice-request-seq-id', 'i', type=int),
], endian='Big')

# # ErrorResponse
ErrorResponse = Descriptor([
    WireField('ice-request-seq-id', 'i', type=int),
    WireField('ice-code',           'c'),
    WireField('ice-text',           '100s', type=TrimmedString),
])