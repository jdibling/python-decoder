from decoder.arca.xdpmsg.constants import XdpMsgTypeId, XdpMsgType

BboMsgType = XdpMsgType
BboMsgType.update({
    100: 'AddOrder',
    140: 'BboQuote'
})

BboMsgTypeId = dict((v,k) for k,v in BboMsgType.iteritems())
