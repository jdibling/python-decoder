FieldTypes = {
    0: "none",
    1: "binary",
    2: "uint8",
    3: "uint16",
    4: "uint32",
    5: "uint64",
    6: "int8",
    7: "int16",
    8: "int32",
    9: "int64",
    10: "float",
    11: "double",
    12: "reserved1",
    13: "reserved2",
    14: "reserved3",
    15: "reserved4",
    16: "reserved5",
    17: "generic",
    18: "blob",
    19: "padding",
    20: "stringz",
    21: "string",
    22: "nocasestringz",
    23: "nocasestring",
    24: "mask8",
    25: "mask16",
    26: "mask32",
    27: "mask64",
    28: "ptr32",
    29: "ptr64",
    30: "ip4",
    31: "price-array",
    32: "order-sku",
    33: "expiration-type",
    34: "processing-indicator",
    35: "record-status",
    36: "entitlement-array",
    37: "password",
    38: "entitlement",
    39: "source-content",
    40: "date",
    41: "time",
    42: "datetime",
    43: "sku",
    44: "value",
    45: "price",
    46: "value64",
    47: "price64",
    48: "sun-tick",
    49: "intraday-bar",
    50: "daily-bar",
    51: "series-list",
    52: "corporate-action",
    53: "trade-condition",
    54: "price-tick",
    55: "utcdatetime",
    56: "content-description",
    57: "performance-info",
    58: "order",
    59: "repeating-group",
    60: "order-imbalance"
}

FieldTypeNames = dict ([(v, k) for (k, v) in FieldTypes.items ()])
