from decoder.descriptor import *
from decoder.arca.xdpmsg.segments import XdpSegment
from decoder.arca.bbomsg.constants import BboMsgTypeId
from decoder.arca.bbomsg.maps import BboSymbolMap

BboSegment = XdpSegment
BboSegment.update({
    BboMsgTypeId['BboQuote']: Descriptor([
        WireField('xdp-msg-size', 'H', type=int),
        WireField('xdp-msg-type', 'H', type=int),
        WireField('xdp-source-time-nano', 'I', type=int),
        WireField('xdp-symbol-index', 'I', type=int),
        WireField('xdp-symbol-seq-num', 'I', type=int),
        WireField('xdp-ask-price-unscaled', 'I', type=int),
        WireField('xdp-ask-volume', 'I', type=int),
        WireField('xdp-bid-price-unscaled', 'I', type=int),
        WireField('xdp-bid-volume', 'I', type=int),
        WireField('xdp-quote-condition', 'c'),
#        WireField('xdp-rpi-indicator', 'c'),
#        WireField('xdp-transaction-id', 'I'),
    ])
})

