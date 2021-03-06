TransactionTypes = {
    0: "Undefined",
    1: "Quote",
    2: "Trade",
    3: "News",
    4: "Summary",
    5: "Range",
    6: "Cancel",
    7: "Correction",
    8: "OrderAdd",
    9: "OrderDelete",
    10: "OrderRevise",
    11: "OrderDeleteBySymbol",
    12: "Create",
    13: "Open",
    14: "Close",
    15: "Clear",
    16: "Load",
    17: "Save",
    18: "GetFirst",
    19: "GetLast",
    20: "GetEqual",
    21: "GetApprox",
    22: "GetDirect",
    23: "GetNext",
    24: "GetPrevious",
    25: "GetGreater",
    26: "GetGreaterOrEqual",
    27: "GetLess",
    28: "GetLessOrEqual",
    29: "GetFirstPartial",
    30: "GetLastPartial",
    31: "GetNextPartial",
    32: "GetPreviousPartial",
    33: "AddRecord",
    34: "DeleteKey",
    35: "DeleteRecord",
    36: "DeleteId",
    37: "UpdateRecord",
    38: "UpdateId",
    39: "GetRecordCount",
    40: "GetMaxRecords",
    41: "GetKeyLength",
    42: "GetRecordLength",
    43: "TableStop",
    44: "OpenStream",
    45: "CloseStream",
    46: "StartSessionReset",
    47: "EndSessionReset",
    48: "GetDirectKey",
    49: "GetId",
    50: "AddEntry",
    51: "DeleteEntry",
    52: "InsertEntry",
    53: "UpdateEntry",
    54: "Bid",
    55: "Ask",
    56: "GetTableInfo",
    57: "EntitlementUpdate",
    58: "SecurityReset",
    59: "IncrementReference",
    60: "DecrementReference",
    61: "Fetch",
    62: "UpdateTable",
    63: "GetIndexStats",
    64: "LookUp",
    65: "SystemMessage",
    66: "DepthQuote",
    67: "OrderImbalance",
}

TransactionTypeNames = dict((v,k) for k,v in TransactionTypes.iteritems())

