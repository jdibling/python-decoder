from segments import *

MsgTypes = {
    0x20: (Time, 'Time'),
    0x21: (AddOrderShort, 'AddOrderLong'),
    0x22: (AddOrderShort, 'AddOrderShort'),
    0x23: (OrderExecuted, 'OrderExecuted'),
    0x24: (OrderExecutedAtPriceSize, 'OrderExecutedAtPriceSize'),
    0x25: (ReduceSizeLong, 'ReduceSizeLong'),
    0x26: (ReduceSizeShort, 'ReduceSizeShort'),
    0x27: (ModifyOrderLong, 'ModifyOrderLong'),
    0x28: (ModifyOrderShort, 'ModifyOrderShort'),
    0x29: (DeleteOrder, 'DeleteOrder'),
    0x2A: (TradeLong, 'TradeLong'),
    0x2B: (TradeShort, 'TradeShort'),
    0x2C: (TradeBreak, 'TradeBreak'),
    0x2D: (EndOfSession, 'EndOfSession'),
    0x2E: (SymbolMapping, 'SymbolMapping'),
    0x30: (TradeExpanded, 'TradeExpanded'),
    0x31: (TradingStatus, 'TradingStatus'),
    0x2F: (AddOrderExpanded, 'AddOrderExpanded'),
    0x95: (AuctionUpdate, 'AuctionUpdate'),
    0x96: (AuctionSummary, 'AuctionSummary'),
    0x97: (UnitClear, 'UnitClear'),
    0x98: (RetailPriceImprovement, 'RetailPriceImprovement'),
}

MsgTypeNames = { v[1]: k for k,v in MsgTypes.iteritems()}

AddOrderMsgTypes = [
    MsgTypeNames['AddOrderShort'],
    MsgTypeNames['AddOrderLong'],
    MsgTypeNames['AddOrderExpanded']
]

