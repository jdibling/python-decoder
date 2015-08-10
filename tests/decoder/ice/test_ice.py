from unittest import TestCase
from decoder.ice.ice import Decoder


import struct
__author__ = 'rkulseth'


class MyDecoder(Decoder):
    def __init__(self):
        pass

    def on_message(self, inputContext, payload):
        self.decoded = inputContext

    def dispatch_to_next(self, context, payload):
        pass


class TestDecoder(TestCase):
    def test_on_message(self):
        context = {}
        options = {}
        # build a Delete Price Level Message
        msg = struct.pack(">HIHQcHIcb",100, 2, 1, 1429755001, 'r', 6, 1001, '1', 1)
        checker = MyDecoder()
        d = Decoder(options, checker)
        d.on_message(context, msg)
        self.assertEquals(checker.decoded['ice-price-level-position'], 1)
        self.assertEquals(checker.decoded['ice-sent-date-time'], 1429755001)
        self.assertEquals(checker.decoded['ice-sequence-num'], 2)
        self.assertEquals(checker.decoded['ice-side'], '1')
        self.assertEquals(checker.decoded['ice-msg-body-length'], 6)
        self.assertEquals(checker.decoded['ice-session-num'], 100)
        self.assertEquals(checker.decoded['ice-market-id'], 1001)
        self.assertEquals(checker.decoded['ice-num-msgs'], 1)
        self.assertEquals(checker.decoded['ice-msg-type'], 'r')