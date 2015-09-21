from decoder.field import WireField, TrimmedString
from decoder.descriptor import Descriptor

from decoder.cta.types import TimeStamp

PayloadSeperators = [
    # SOH
    0x01,
    # US
    0x1f,
    # ETX
    0x03
]


MsgHeader = Descriptor([
    WireField('cqs-msg-cat', 'c'),
    WireField('cqs-msg-typ', 'c'),
    WireField('cqs-msg-network', 'c'),
    WireField('cqs-retran-requestor', '2s'),
    WireField('cqs-header-id', 'c'),
    WireField('cqs-trans-id-part-a', '2s'),
    WireField('cqs-seq-num', '9s', type=long),
    WireField('cqs-participant-id', 'c'),
    WireField('cqs-timestamp', '6s', type=TimeStamp()),
    WireField('cqs-timestamp-1', '6s', type=TimeStamp()),
    WireField('cqs-timestamp-2', '6s', type=TimeStamp()),
    WireField('cqs-trans-id-part-b', '9s')
])

ShortQuote = Descriptor([
    WireField('cqs-symbol', '3s', type=TrimmedString),
    WireField('cqs-quote-condition', 'c'),
    WireField('cqs-limit-up-limit-down', 'c'),
    WireField('cqs-resv', 'c', hidden=True),
    WireField('cqs-bid-price-denom', 'c'),
    WireField('cqs-bid-price-unscaled', '8s'),
    WireField('cqs-bid-size', '3s'),
    WireField('cqs-resv', 'c', hidden=True),
    WireField('cqs-ask-price-denom', 'c'),
    WireField('cqs-ask-price-unscaled', '8s'),
    WireField('cqs-ask-size', '3s'),
    WireField('cqs-resv', 'c', hidden=True),
    WireField('cqs-nbbo', 'c'),
    WireField('cqs-finra-ice', 'c')
])

LongQuote = Descriptor([
    WireField('cqs-symbol', '11s', type=TrimmedString),
    WireField('cqs-temporary-suffix', 'c'),
    WireField('cqs-test-message', 'c'),
    WireField('cqs-primary-listing-market', 'c'),
    WireField('cqs-sip-generated-message', 'c'),
    WireField('resv', 'c', hidden=True),
    WireField('cqs-financial-status', 'c'),
    WireField('cqs-currency', '3s'),
    WireField('cqs-instrument-type', 'c'),
    WireField('cqs-cancel-correction', 'c'),
    WireField('cqs-settl-condition', 'c'),
    WireField('cqs-market-condition', 'c'),
    WireField('cqs-quote-condition', 'c'),
    WireField('cqs-limit-up-limit-down', 'c'),
    WireField('cqs-retail-interest', 'c'),
    WireField('cqs-bid-price-denom', 'c'),
    WireField('cqs-bid-price-unscaled', '12s'),
    WireField('cqs-bid-size', '7s'),
    WireField('cqs-ask-price-denom', 'c'),
    WireField('cqs-ask-price-unscaled', '12s'),
    WireField('cqs-ask-size', '7s'),
    WireField('cqs-finra-market-maker', '4s'),
    WireField('resv', 'c', hidden=True),
    WireField('cqs-nbbo-luld', 'c'),
    WireField('cqs-finra-ice-luld', 'c'),
    WireField('cqs-short-sale-restriction', 'c'),
    WireField('resv', 'c', hidden=True),
    WireField('cqs-nbbo', 'c'),
    WireField('cqs-finra-ice', 'c')
])

ShortNBbo = Descriptor([
    WireField('cqs-best-bid-participant-national', 'c'),
    WireField('cqs-best-bid-price-denom-national', 'c'),
    WireField('cqs-best-bid-price-unscaled-national', '8s'),
    WireField('cqs-best-bid-size-national', '3s'),
    WireField('resv', 'c', hidden=True),
    WireField('cqs-best-ask-participant-national', 'c'),
    WireField('cqs-best-ask-price-denom-national', 'c'),
    WireField('cqs-best-ask-price-unscaled-national', '8s'),
    WireField('cqs-best-ask-size-national', '3s'),
    WireField('resv', 'c', hidden=True)
])
LongNBbo = Descriptor([
    WireField('resv', '2s', hidden=True),
    WireField('cqs-best-bid-participant-national', 'c'),
    WireField('cqs-best-bid-price-denom-national', 'c'),
    WireField('cqs-best-bid-price-unscaled-national', '12s'),
    WireField('cqs-best-bid-size-national', '7s'),
    WireField('cqs-best-bid-mmid-national', '4s'),
    WireField('resv', '3s', hidden=True),
    WireField('cqs-best-ask-participant-national', 'c'),
    WireField('cqs-best-ask-price-denom-national', 'c'),
    WireField('cqs-best-ask-price-unscaled-national', '12s'),
    WireField('cqs-best-ask-size-national', '7s'),
    WireField('cqs-best-ask-mmid-national', '4s'),
    WireField('resv', 'c', hidden=True)
])
FinraBbo = Descriptor([
    WireField('resv', '2s', hidden=True),
    WireField('cqs-best-bid-price-denom-finra', 'c'),
    WireField('cqs-best-bid-price-unscaled-finra', '12s'),
    WireField('cqs-best-bid-size-finra', '7s'),
    WireField('cqs-best-bid-mmid-finra', '4s'),
    WireField('resv', '3s', hidden=True),
    WireField('cqs-best-ask-price-denom-finra', 'c'),
    WireField('cqs-best-ask-price-unscaled-finra', '12s'),
    WireField('cqs-best-ask-size-finra', '7s'),
    WireField('cqs-best-ask-mmid-finra', '4s'),
    WireField('resv', 'c', hidden=True)
])
