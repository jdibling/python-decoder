from decoder.module import *
from .icemsg.segments import *
from .icemsg.constants import *


class Decoder(BasicModule):
    def __init__(self, opts, next_decoder):
        super(Decoder, self).__init__('ice/ice', opts, next_decoder)
        self.__parse_options(opts)
        self.__unhandledMessages = dict()
        self.__translation = dict()
        self.__frameCount = 0
        self.__msgCount = dict()
        self.__byteCount = 0

    def __parse_options(self, opts):
        self.__deblock = opts.get('deblock', True)

    def decode_message(self, context, payload):
        # grab the message header (first two fields of every message')
        headers, payload = self.decode_segment(MessageHeader, payload)

        if len(headers) is not 1:
            raise ValueError("Internal error decoding ICE message header")
        context.update(headers[0])

        # extract the message payload
        msgBodyLen = context['ice-msg-body-length']
        msgPayload = payload[:msgBodyLen]

        #if len(msgPayload) !=  msgBodyLen:
        #    raise "Length does not match!"

        # parse the message body
        msgType = context['ice-msg-type']
        if msgType not in MsgTypeIndex:
            self.__unhandledMessages[msgType] = self.__unhandledMessages.get(msgType, 0) + 1
        else:
            msgs, msgPayload = self.decode_segment(MsgTypeIndex[msgType][0], msgPayload)
            if len(msgs) is not 1:
                raise ValueError("Internal error decoding ICE message type {0}".format(msgType))
            context.update(msgs[0])

        return context, payload

    def on_message(self, inputContext, payload):
        # default message count is None for the non-deblock case
        num_msgs = 1
        msgBlock = {}
        if self.__deblock:
            # parse the packet header
            msgBlocks, payload = self.decode_segment(MessageBlock, payload)
            if len(msgBlocks) is not 1:
                raise ValueError("Internal error processing ICE message block")
            msgBlock = msgBlocks[0]

            # update stats
            self.__byteCount += MessageBlock.WireBytes()
            self.__frameCount += 1

            num_msgs = msgBlock['ice-num-msgs']

        # process each message
        for msgIdx in xrange(0, num_msgs):
            origPayload = payload
            context = dict(inputContext)

            # if deblock is True, add the deblocked info to context
            if self.__deblock:
                context.update(msgBlock)

            # decode the individual message
            context, payload = self.decode_message(context, payload)

            msgBodyLen = context['ice-msg-body-length']
            msgType = context['ice-msg-type']

            # trim the remaining unprocessed payload, send the decoded stuff to the next link & loo
            payload = origPayload[3+msgBodyLen:]
            self.dispatch_to_next(context, payload)

            # update stats
            self.__byteCount += MessageHeader.WireBytes() + msgBodyLen
            self.__msgCount[msgType] = self.__msgCount.get(msgType, 0) + 1

    def summarize(self):
        return {
            'ice-unhandled-messages': self.__unhandledMessages,
            'ice-translation-entries': len(self.__translation),
            'ice-frames': self.__frameCount,
            'ice-bytes': self.__byteCount,
            'ice-msg-counts': self.__msgCount
        }
