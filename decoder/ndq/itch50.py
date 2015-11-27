from decoder.module import *
from decoder.ndq.mold.segments import *
from decoder.ndq.itch.segments import *
from decoder.ndq.itch.constants import *

class Decoder(BasicModule):
    def __init__(self, opts, next_decoder):
        super(Decoder, self).__init__('ndq/itchp50', opts, next_decoder)
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
        packets, payload = self.decode_segment(MoldPacketHeader, payload)
        if len(packets) is not 1:
            raise ValueError("Internal error processing Itch50 packet header")
        packet = packets[0]

        # update stats
        self.__byteCount += MoldPacketHeader.WireBytes()
        self.__frameCount += 1

        # process each message
        for msgIdx in range(0, packet['mold-message-count']):
            # decode the message header
            headers, payload = self.decode_segment(MoldMessageHeader, payload)
            if len(headers) is not 1:
                raise ValueError("Internal error processing Itch messsage header")
            header = headers[0]

            # grab the message payload & trim the remaining payload
            msgLen = header['mold-message-length']
            messagePayload = payload[:msgLen]
            payload = payload[msgLen:]

            # peek the common fields, get the msg type
            commons, messagePayload = self.decode_segment(ItchCommonSegment, messagePayload, peek=True)
            if len(commons) is not 1:
                raise ValueError("Internal error processing Itch message common segment")
            common = commons[0]
            msgType = common['itch-msg-type']

            # decode the message payload
            context = {'sequence-number': packet['mold-sequence-number']+msgIdx}

            if msgType not in MsgTypes:
                self.__unhandledMessages[msgType] = self.__unhandledMessages.get(msgType, 0) + 1
            else:
                messages, messagePayload = self.decode_segment(MsgTypes[msgType][0], messagePayload)
                if len(messages) is not 1:
                    raise ValueError("Internal error processing Itch message")
                message = messages[0]

                # update stats
                self.__msgCount[msgType] = self.__msgCount.get(msgType, 0) + 1
                self.__byteCount += header['mold-message-length'] + MoldMessageHeader.WireBytes()

                # handle translations
                stockLocate = message.get('itch-stock-locate', None)
                if stockLocate is None:
                    raise ValueError("Internal error: No stock locate in itch message")
                if 'itch-symbol' not in message and stockLocate in self.__translation:
                    # add this symbol to translation
                    message['itch-symbol'] = self.__translation[stockLocate]
                elif stockLocate not in self.__translation and 'itch-symbol' in message:
                    # pull the symbol from translation
                    self.__translation[stockLocate] = message['itch-symbol']

                # get the message type name
                typeName = MsgTypes[msgType][1]
                message['itch-message-type'] = typeName
                context.update(message)

            # send to next
            context.update(inputContext)
            context.update(packet)
            context.update(header)
            self.dispatch_to_next(context, messagePayload)

    def summarize(self):
        return {
            'itch-unhandled-messages': self.__unhandledMessages,
            'itch-translation-entries': len(self.__translation),
            'itch-frames': self.__frameCount,
            'itch-bytes': self.__byteCount,
            'itch-msg-counts': self.__msgCount
        }
