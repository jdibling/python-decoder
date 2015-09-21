__author__ = 'jdibling'
from decoder.descriptor import *

PacketHeader = Descriptor([
    WireField('md-byte-order', 'H'), # 0 byte order
    WireField('md-version', 'c'),
    WireField('md-more', 'c'),
    WireField('md-data-dict', 'c'),
    WireField('md-flags', 'c'), # 4 flags
    WireField('md-signature', 'H'), # 5 signature
    WireField('md-length', 'I'), # 6 length
    WireField('md-total-length', 'I'), # 7 total length
    WireField('md-orig-length', 'I'), # 8 orig length
    WireField('md-field-count', 'I'), # 9 field count
    WireField('md-seq-num', 'I'), # 10 seq num
    WireField('md-packet-count', 'I') # 11packet count
], endian='Little')

