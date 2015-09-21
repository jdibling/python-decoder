from decoder.decoder import Decoder
from decoder.tmx.cdfmsg.segments import *

class Decoder(Decoder):
    def __init__(self, opts, next_decoder):
        super(Decoder, self).__init__('tmx/cdf', opts, next_decoder)
        self.__parse_options(opts)
        self.__unhandledMessages = dict()
        self.__translation = dict()
        self.__frameCount = 0
        self.__msgCount = dict()
        self.__byteCount = 0

    def __parse_options(self, opts):
        pass

    def on_message(self, inputContext, payload):
            # decode the transport header
            transport_headers, payload = self.decode_segment(TransportHeader, payload)
            if len(transport_headers) != 1:
                raise ValueError("Internal error processing tmx/cdf transport header")
            transport_header = transport_headers[0]

            # send to next
            context = dict()
            context.update(transport_header)
            context.update(inputContext)
            self.dispatch_to_next(context, payload)

    def summarize(self):
        return {
            'bbo-unhandled-messages': self.__unhandledMessages,
            'bbo-translation-entries': len(self.__translation),
            'bbo-frames': self.__frameCount,
            'bbo-bytes': self.__byteCount,
            'bbo-msg-counts': self.__msgCount
        }
