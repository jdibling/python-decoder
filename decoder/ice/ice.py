from base.decoder import Decoder
from decoder.ice.ice.segments import  *

class Decoder(Decoder):
    def __init__(self, opts, next_decoder):
        super(Decoder, self).__init__('ice/ice', opts, next_decoder)
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
        msgBlocks, payload = self.decode_segment(MessageBlock, payload)
        if len(msgBlocks) is not 1:
            raise ValueError("Internal error processing ICE message block")
        msgBlock = msgBlocks[0]

        # update stats
        self.__byteCount += MessageBlock.WireBytes()
        self.__frameCount += 1

        print msgBlock

        # process each message
        for msgIdx in range(0, msgBlock['ice-num-msgs']):
            context = dict()
            context.update(msgBlock)

            # grab the message header (first two fields of every message)
            headers, payload = self.decode_segment(MessageHeader, payload)
            if len(headers) is not 1:
                raise ValueError("Internal error decoding ICE message header")
            context.update(headers[0])

            # extract the message payload
            msgBodyLen = context['ice-msg-body-length']
            msgPayload = payload[:msgBodyLen]
            payload = payload[msgBodyLen]

            # parse the message body
            msgType = context['ice-msg-type']
            if msgType not in MsgTypeIndex:
                self.__unhandledMessages[msgType] = self.__unhandledMessages.get(msgType, 0) + 1
            else:
                msgs, msgPayload = self.decode_segment(MsgTypeIndex[msgType], msgPayload)
                if len(msgs) is not 1:
                    raise ValueError("Internal error decoding ICE message type {0}".format(msgType))
                context.update(msgs[0])

            print msgIdx

    def summarize(self):
        return {
            'ice-unhandled-messages': self.__unhandledMessages,
            'ice-translation-entries': len(self.__translation),
            'ice-frames': self.__frameCount,
            'ice-bytes': self.__byteCount,
            'ice-msg-counts': self.__msgCount
        }
