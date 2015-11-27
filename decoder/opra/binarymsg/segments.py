from decoder.descriptor import *

BlockHeader = Descriptor([
    WireField('opra-block-version', 'B'),
    WireField('opra-block-size', 'H'),
    WireField('opra-block-feed-ind', 'B'),
    WireField('opra-block-retran-ind', 'B'),
    WireField('opra-block-session-ind', 'B'),
    WireField('opra-block-seq-num', 'I', type=int),
    WireField('opra-block-msg-count', 'B', type=int),
    WireField('opra-block-timestamp','Q'),
    WireField('opra-block-checksum', 'H')
], endian='Big')

MessageHeader = {
    3: Descriptor([
        WireField('opra-part-id', 'c'),
        WireField('opra-msg-cat', 'c'),
        WireField('opra-msg-type', 'c'),
        WireField('opra-msg-ind', 'c')
    ], endian='Big'),

    5: Descriptor([
        WireField('opra-part-id', 'c'),
        WireField('opra-msg-cat', 'c'),
        WireField('opra-msg-type', 'c'),
        WireField('opra-msg-ind', 'c'),
        WireField('opra-trans-id', '8s')
    ], endian='Big')
}


"""  CONTROL MESSAGES
"""
LineIntegrityMessage = Descriptor([
    WireField()
], endian='Big')
