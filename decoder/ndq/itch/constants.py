from decoder.ndq.itch.segments import *

MsgTypes = {
    'A': (ItchOrderAdd, 'OrderAdd'),
    'B': (ItchBrokenTrade, 'BrokenTrade'),
    'C': (ItchOrderExecutedWithPrice, 'OrderExecutedWithPrice'),
    'D': (ItchOrderDelete, 'OrderDelete'),
    'E': (ItchOrderExecuted, 'OrderExecuted'),
    'F': (ItchOrderAddMpid, 'OrderAddWithAttribution'),
    'H': (ItchStockTradingAction, 'StockTradingAction'),
    'I': (ItchNoii, 'Noii'),
    'K': (ItchIpoQuotingPeriod, 'IpoQuotingPeriod'),
    'L': (ItchMarketParticipantPosition, 'MarketParticipantPosition'),
    'N': (ItchRpii, "Rpii"),
    'P': (ItchTrade, 'Trade'),
    'Q': (ItchCrossTrade, 'CrossTrade'),
    'R': (ItchStockDirectory, 'StockDirectory'),
    'S': (ItchSystemEvent, 'SystemEvent'),
    'U': (ItchOrderReplace, 'OrderReplace'),
    'V': (ItchMwcbDeclineLevel, 'MwcbDeclineLevel'),
    'W': (ItchMwcbBreach, 'MwcbBreach'),
    'X': (ItchOrderCancelled, 'OrderCancelled'),
    'Y': (ItchRegShoRestriction, 'RegShoRestriction')
}