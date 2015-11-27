from decoder.field import *
from decoder.descriptor import *
from decoder.module import *

from decoder.arca.xdpmsg.constants import XdpMsgTypeId, DeliveryFlag, MarketId
from decoder.arca.xdpmsg.convert import XdpTimeStamp

XdpSegment = {
    XdpMsgTypeId['XdpPacketHeader']: Descriptor([
        WireField('xdp-pkt-size', 'H', type=int),
        LookupField('xdp-delivery-flag', 'b', DeliveryFlag, type=int),
        WireField('xdp-number-msgs', 'b', type=int),
        WireField('xdp-seq-num', 'I', type=int),
        WireField('xdp-send-time-sec-part', 'I', type=int),
        WireField('xdp-send-time-nano-part', 'I', type=int),
        ComputedField('xdp-send-timestamp', XdpTimeStamp('xdp-send-time-sec-part', 'xdp-send-time-nano-part'))
    ]),
    XdpMsgTypeId['XdpCommonHeader']: Descriptor([
        WireField('xdp-msg-size', 'H', type=int),
        WireField('xdp-msg-type', 'H', type=int)
    ]),
   XdpMsgTypeId['XdpSeqNumReset']: Descriptor([
        WireField('xdp-msg-size', 'H', type=int),
        WireField('xdp-msg-type', 'H', type=int),
        WireField('xdp-source-time-sec-part', 'I', type=int),
        WireField('xdp-source-time-nano-part', 'I', type=int),
        ComputedField('xdp-source-timestamp', XdpTimeStamp('xdp-source-time-sec-part', 'xdp-source-time-nano-part')),
        WireField('xdp-product-id', 'B', type=int),
        WireField('xdp-channel-id', 'B', type=int)
    ]),
    XdpMsgTypeId['XdpSourceTimeReference']:  Descriptor([
        WireField('xdp-msg-size', 'H', type=int),
        WireField('xdp-msg-type', 'H', type=int),
        WireField('xdp-symbol-index', 'I', type=int),
        WireField('xdp-symbol-seq-num', 'I', type=int),
        WireField('xdp-time-reference', 'I', type=int)
    ]),
    XdpMsgTypeId['XdpSymbolIndexMapping']: Descriptor([
        WireField('xdp-msg-size', 'H', type=int),
        WireField('xdp-msg-type', 'H', type=int),
        WireField('xdp-symbol-index', 'I', type=int),
        WireField('xdp-symbol', '11s', type=TrimmedString),
        WireField('xdp-filler', 'B', hidden=True),
        LookupField('xdp-market-id', 'H', MarketId, type=int),
        WireField('xdp-system-id', 'B', type=int),
        WireField('xdp-exchange-code', 'c'),
        WireField('xdp-price-scale-code', 'B', type=int),
        WireField('xdp-security-type', 'c'),
        WireField('xdp-round-lot-size', 'H', type=int),
        WireField('xdp-prev-close-price-unscaled', 'I', type=int),
        WireField('xdp-prev-close-volume', 'I', type=int),
        WireField('xdp-price-resolution', 'B', type=int),
        WireField('xdp-round-lot-accepted', 'c')
    ]),
    XdpMsgTypeId['XdpSecurityStatus']: Descriptor([
        WireField('xdp-msg-size', 'H', type=int),
        WireField('xdp-msg-type', 'H', type=int),
        WireField('xdp-source-time-sec-part', 'I', type=int),
        WireField('xdp-source-time-nano-part', 'I', type=int),
        ComputedField('xdp-source-timestamp', XdpTimeStamp('xdp-source-time-sec-part', 'xdp-source-time-nano-part')),
        WireField('xdp-symbol-index', 'I', type=int),
        WireField('xdp-symbol-seq-num', 'I', type=int),
        WireField('xdp-security-status', 'c'),
        WireField('xdp-halt-condition', 'c'),
        # WireField('xdp-transaction-id', 'I', type=int),
        # WireField('xdp-price-1-unscaled', 'I', type=int),
        # WireField('xdp-price-2-unscaled', 'I', type=int),
        # WireField('xdp-ssr-triggering-exchange-id', 'c'),
        # WireField('xdp-ssr-triggering-volume', 'I', type=int),
        # WireField('xdp-time', 'I', type=int),
        # WireField('xdp-ssr-state', 'c'),
        # WireField('xdp-market-state', 'c'),
        # WireField('xdp-session-state', 'c')
    ], checksize=22)
}
