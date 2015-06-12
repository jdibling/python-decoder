from decoder.arca.xdp.constants import XdpMsgTypeId, XdpMsgType

BboMsgType = XdpMsgType
BboMsgType.update({
    140: 'BboQuote'
})

BboMsgTypeId = dict((v,k) for k,v in BboMsgType.iteritems())
