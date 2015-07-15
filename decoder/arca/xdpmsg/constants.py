DeliveryFlag = {
    1: 'heartbeat',
    10: 'xdp-failover',
    11: 'original-message',
    12: 'seq-num-reset',
    13: 'one-packet-retran-uncomp',
    15: 'part-retran-uncomp',
    17: 'one-packet-refresh-uncomp',
    18: 'start-refresh-uncomp',
    19: 'part-refresh-uncomp',
    20: 'end-refresh-uncomp',
    21: 'message-unavailable-21',
    30: 'compacted=xdp-failover',
    41: 'message-unavailable-41'
}

MarketId = {
    1: 'NyseCash',
    2: 'EuropeCash',
    3: 'NyseArcaCash',
    4: 'NyseArcaOptions',
    5: 'NyseArcaBonds',
    6: 'GlobalOtc',
    7: 'Liffe',
    8: 'NyseAmexOptions',
    9: 'NyseMktCash'
}

XdpMsgType ={
    -2: 'XdpPacketHeader',
    -1: 'XdpCommonHeader',
    1: 'XdpSeqNumReset',
    2: 'XdpSourceTimeReference',
    3: 'XdpSymbolIndexMapping',
    4: 'XdpVendorMapping',
    34: 'XdpSecurityStatus'
}

XdpMsgTypeId = dict((v,k) for k,v in XdpMsgType.iteritems())
