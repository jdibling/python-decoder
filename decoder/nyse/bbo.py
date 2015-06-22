from base.decoder import Decoder
from decoder.nyse.bbo.segments import *

class Decoder(Decoder):
    def __init__(self, opts, next_decoder):
        super(Decoder, self).__init__('nyse/bbo', opts, next_decoder)
        self.__parse_options(opts)
        self.__unhandledMessages = dict()
        self.__translation = dict()
        self.__frameCount = 0
        self.__msgCount = dict()
        self.__byteCount = 0

    def __parse_options(self, opts):
        pass

    def on_message(self, inputContext, payload):
        # parse the packet header
        headers, payload = self.decode_segment(MessageHeader, payload)
        if len(headers) is not 1:
            raise ValueError("Internal error processing AMEX/BBO packet header")
        header = headers[0]

        # update stats
        self.__byteCount += MessageHeader.WireBytes()
        self.__frameCount += 1

        # process each message
        for msgIdx in range(0, header['bbo-num-body-entries']):
            context = dict()

            messages, payload = self.decode_segment(Bbo, payload)
            if len(messages) is not 1:
                raise ValueError('Internal error processing NYSEBBO packet')
            message = messages[0]

            context['sequence-number'] = header['bbo-msg-seq-num']

            # compute send/source diff
            sendTime = header['bbo-send-time']
            sourceTime = message['bbo-source-time']
            timeDiff = sendTime-sourceTime
            context['bbo-send-source-diff'] = timeDiff

            # send to next
            context.update(inputContext)
            context.update(header)
            context.update(message)
            self.dispatch_to_next(context, payload)

    def summarize(self):
        return {
            'bbo-unhandled-messages': self.__unhandledMessages,
            'bbo-translation-entries': len(self.__translation),
            'bbo-frames': self.__frameCount,
            'bbo-bytes': self.__byteCount,
            'bbo-msg-counts': self.__msgCount
        }
