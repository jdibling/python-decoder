from base.field import BasicField, WireField, ComputedField, RepeatingGroup, TrimmedString
from base.descriptor import Descriptor

from base.decoder import Decoder, Verbosity

import sys

MessageTypeIndex = {

    'DropMessage': 0x201,


    'UsEquityBboQuote': 0x300,
    'UsEquityDepthQuote': 0x301,
    'UsEquityOrderAdd': 0x302,
    'UsEquityOrderDelete': 0x303,
    'UsEquityOrderFill': 0x304,
    'UsEquityOrderReplace': 0x305,
    'UsEquityOrderRevise': 0x306,
    'UsEquityTrade': 0x307,
}

MessageNameIndex = dict((v, k) for k, v in MessageTypeIndex.iteritems())

AppendageTypeIndex = {
    'TotalViewOrderAdd': 0x100,
    'TotalViewOrderAddAttribution': 0x101,
    'TotalViewOrderCancel': 0x102,
    'TotalViewOrderDelete': 0x103,
    'TotalViewOrderFill': 0x104,
    'TotalViewOrderFillPriced': 0x105,
    'TotalViewOrderReplace': 0x106,
    'TotalViewTrade': 0x107,
    'TotalViewCrossTrade': 0x108
}

AppendageNameIndex = dict((v, k) for k, v in AppendageTypeIndex.iteritems())


class Decoder (Decoder):
    """ SeqFwdCpp decoder

    This decoder processes SeqFwdCpp

    """

    def __parse_options (self, opts):
        self.showAppendages = opts.get('show-appendages', True)
        pass

    def __init__ (self, opts, next_decoder):
        super (Decoder, self).__init__ ('phx/nextgen', opts, next_decoder)
        self.__parse_options (opts)
        # init summary data
        self.__frame_sequence = 0
        self.__decodingErrors = 0
        self.__unhandled_messages = {}
        self.__msg_counts = {}
        self.__unhandled_appendages = {}
        self.__apg_counts = {}

        # init message segment descriptors
        self.PacketHeaderDesc = Descriptor([
            WireField('pico-packet-length', 'H', type=int),
            WireField('pico-packet-header-length', 'B', type=int),
            WireField('pico-stream-id', 'Q', type=int),
            WireField('pico-current-chunk', 'B', type=int),
            WireField('pico-msg-count', 'B', type=int),
            WireField('pico-ingress-timestamp', 'Q', type=int),
            WireField('pico-bitfield', 'B', type=int),
            WireField('pico-reserved', 'H', hidden=True)
        ])

        self.CommonMessageHeaderDesc = Descriptor([
            WireField('pico-msg-block-length', 'H', type=int),
            WireField('pico-msg-header-length', 'B', type=int),
            WireField('pico-msg-body-length', 'H', type=int),
            WireField('pico-msg-type', 'H', type=long),
            WireField('pico-msg-appendage-count', 'B', type=int)
        ])

        self.BusinessMessageHeaderDesc = Descriptor([
            WireField('pico-source-content', 'H', type=int),
            WireField('pico-exchange-seq-num', 'Q', type=int)
        ])

        self.AppendageHeaderDesc = Descriptor([
            WireField('pico-appendage-length', 'H', type=int),
            WireField('pico-appendage-header-length', 'B', type=int),
            WireField('pico-appendage-type', 'H', type=int)
        ])

        # init message descriptors
        self.MessageDesc = dict()

        # admin messages
        self.MessageDesc[MessageTypeIndex['DropMessage']] = Descriptor([
            WireField('pico-reserved', 'H', type=int)
        ])

        # business messages
        self.MessageDesc[MessageTypeIndex['UsEquityOrderAdd']] = Descriptor([
            WireField('pico-market', '4s', type=TrimmedString),
            WireField('pico-ticker', '12s', type=TrimmedString),
            WireField('pico-time', 'Q', type=int),
            WireField('pico-order-id', 'Q', type=int),
            WireField('pico-price', 'Q', type=int),
            WireField('pico-size', 'Q', type=int),
            WireField('pico-side', 'B', type=int)
        ])

        self.MessageDesc[MessageTypeIndex['UsEquityOrderDelete']] = Descriptor([
            WireField('pico-market', '4s', type=TrimmedString),
            WireField('pico-ticker', '12s', type=TrimmedString),
            WireField('pico-time', 'Q', type=int),
            WireField('pico-order-id', 'Q', type=int)
        ])

        self.MessageDesc[MessageTypeIndex['UsEquityOrderFill']] = Descriptor([
            WireField('pico-market', '4s', type=TrimmedString),
            WireField('pico-ticker', '12s', type=TrimmedString),
            WireField('pico-time', 'Q', type=int),
            WireField('pico-order-id', 'Q', type=int),
            WireField('pico-size', 'Q', type=int)
        ])

        self.MessageDesc[MessageTypeIndex['UsEquityOrderReplace']] = Descriptor([
            WireField('pico-market', '4s', type=TrimmedString),
            WireField('pico-ticker', '12s', type=TrimmedString),
            WireField('pico-time', 'Q', type=int),
            WireField('pico-prev-order-id', 'Q', type=int),
            WireField('pico-repl-order-id', 'Q', type=int),
            WireField('pico-new-price', 'Q', type=int),
            WireField('pico-new-size', 'Q', type=int)
        ])

        self.MessageDesc[MessageTypeIndex['UsEquityOrderRevise']] = Descriptor([
            WireField('pico-market', '4s', type=TrimmedString),
            WireField('pico-ticker', '12s', type=TrimmedString),
            WireField('pico-time', 'Q', type=int),
            WireField('pico-order-id', 'Q', type=int),
            WireField('pico-revise-action', 'c', type=TrimmedString),
            WireField('pico-price', 'Q', type=int),
            WireField('pico-size', 'Q', type=int)
        ])

        self.MessageDesc[MessageTypeIndex['UsEquityTrade']] = Descriptor([
            WireField('pico-market', '4s', type=TrimmedString),
            WireField('pico-ticker', '12s', type=TrimmedString),
            WireField('pico-time', 'Q', type=int),
            WireField('pico-price', 'Q', type=int),
            WireField('pico-volume', 'Q', type=int),
            WireField('pico-regional-bitfield', 'B', type=int),
            WireField('pico-composite-bitfield', 'B', type=int),
        ])

        self.TotalViewCommonApg = [
            WireField('pico-itch-stock-locate', 'H', type=int),
            WireField('pico-itch-tracking-number', 'H', type=int),
        ]

        self.AppendageDesc = dict()
        self.AppendageDesc[AppendageTypeIndex['TotalViewOrderAdd']] = Descriptor(
            self.TotalViewCommonApg
        )

        self.AppendageDesc[AppendageTypeIndex['TotalViewOrderAddAttribution']] = Descriptor(
            self.TotalViewCommonApg + [
            WireField('pico-itch-attribution', '4s', type=TrimmedString)
        ])

        self.AppendageDesc[AppendageTypeIndex['TotalViewOrderCancel']] = Descriptor(
            self.TotalViewCommonApg + [
        ])

        self.AppendageDesc[AppendageTypeIndex['TotalViewOrderDelete']] = Descriptor(
            self.TotalViewCommonApg + [
        ])

        self.AppendageDesc[AppendageTypeIndex['TotalViewOrderFill']] = Descriptor(
            self.TotalViewCommonApg + [
            WireField('pico-itch-order-match-id', 'Q', type=int)
        ])

        self.AppendageDesc[AppendageTypeIndex['TotalViewOrderFillPriced']] = Descriptor(
            self.TotalViewCommonApg + [
            WireField('pico-itch-order-match-id', 'Q', type=int),
            WireField('pico-itch-fill-price', 'Q', type=int),
            WireField('pico-itch-fill-size', 'Q', type=int),
            WireField('pico-itch-fill-printable', 'c', type=TrimmedString)
        ])

        self.AppendageDesc[AppendageTypeIndex['TotalViewOrderReplace']] = Descriptor(
            self.TotalViewCommonApg + [
        ])

        self.AppendageDesc[AppendageTypeIndex['TotalViewTrade']] = Descriptor(
            self.TotalViewCommonApg + [
            WireField('pico-itch-order-match-id', 'Q', type=int)
        ])

        self.AppendageDesc[AppendageTypeIndex['TotalViewCrossTrade']] = Descriptor(
            self.TotalViewCommonApg + [
            WireField('pico-itch-order-match-id', 'Q', type=int),
            WireField('pico-itch-order-cross-type', 'c', type=TrimmedString)
        ])

    def __decodePacketHeader(self, payload):
        packetHeaders, payload = self.decode_segment(self.PacketHeaderDesc, payload)
        if len(packetHeaders) is not 1:
            self.__decodingErrors += 1
            errStr = "NextGen packet header decoded in to {0} bodies".format(len(packetHeaders))
            sys.stderr.write(errStr)
            sys.stderr.flush()
            raise ValueError(errStr)
        return packetHeaders[0], payload

    def __decodeCommonMessageHeader(self, payload):
        messageHeaders, payload = self.decode_segment(self.CommonMessageHeaderDesc, payload)
        if len(messageHeaders) is not 1:
            self.__decodingErrors += 1
            errStr = "NextGen common message header decoded in to {0} bodies".format(len(messageHeaders))
            sys.stderr.write(errStr)
            sys.stderr.flush()
            raise ValueError(errStr)

        messageHeader = messageHeaders[0]
        msgTypeHex = '0x{0}'.format(('%x' % messageHeader['pico-msg-type']).zfill(4))
        messageHeader['pico-msg-type-hex'] = msgTypeHex

        return messageHeader, payload

    def __decodeBusinessMessageHeader(self, payload):
        messageHeaders, payload = self.decode_segment(self.BusinessMessageHeaderDesc, payload)
        if len(messageHeaders) is not 1:
            self.__decodingErrors += 1
            errStr = "NextGen business message header decoded in to {0} bodies".format(len(messageHeaders))
            sys.stderr.write(errStr)
            sys.stderr.flush()
            raise ValueError(errStr)
        return messageHeaders[0], payload

    def __decodeMessageBody(self, payload, messageHeader):
        messageType = messageHeader['pico-msg-type']
        messageTypeHex = messageHeader['pico-msg-type-hex']
        self.__msg_counts[messageTypeHex] = self.__msg_counts.get(messageTypeHex, 0) + 1

        messageDesc = self.MessageDesc.get(messageType, None)
        if messageDesc is None:
            # unhandled message -- report it and skip the payload
            self.__unhandled_messages[messageTypeHex] = self.__unhandled_messages.get(messageTypeHex, 0) + 1
            sys.stderr.write("Unhandled message type: {0}\n".format(messageTypeHex))
            # skip the message body in the payload
            bytes_to_skip = messageHeader['pico-msg-body-length']
            message = {'msg-body-payload': self.toHex(payload[:bytes_to_skip])}
            payload = payload[bytes_to_skip:]
            return (message, payload)
        else:
            messageBodies, payload = self.decode_segment(messageDesc, payload)
            if len(messageBodies) is not 1:
                self.__decodingErrors += 1
                errStr = "NextGen message body decoded in to {0} bodies".format(len(messageBodies))
                sys.stderr.write(errStr)
                sys.stderr.flush()
                raise ValueError(errStr)

            messageBody = messageBodies[0]
            messageBody['pico-msg-type-name'] = MessageNameIndex[messageType]
            return messageBody, payload

    def __decodeAppendageHeader(self, payload):
        appendageHeaders, payload = self.decode_segment(self.AppendageHeaderDesc, payload)
        if len(appendageHeaders) is not 1:
            self.__decodingErrors += 1
            raise ValueError("Internal error (apg header)")
        appendageHeader = appendageHeaders[0]
        apgTypeHex = '0x{0}'.format(('%x' % appendageHeader['pico-appendage-type']).zfill(4))
        appendageHeader['pico-appendage-type-hex'] = apgTypeHex
        return appendageHeader, payload

    def __decodeAppendageBody(self, payload, appendage):
        appendageType = appendage['pico-appendage-type']
        appendageTypeHex = appendage['pico-appendage-type-hex']
        self.__apg_counts[appendageTypeHex] = self.__apg_counts.get(appendageTypeHex, 0) + 1

        appendageDesc = self.AppendageDesc.get(appendageType, None)
        if appendageDesc is None:
            # unhandled message -- report it and skip the payload
            self.__unhandled_appendages[appendageTypeHex] = self.__unhandled_appendages.get(appendageTypeHex, 0) + 1
            sys.stderr.write("Unhandled appendage type: {0}\n".format(appendageTypeHex))
            # skip the message body in the payload
            headerLength = appendage['pico-appendage-header-length']
            bodyLength = appendage['pico-appendage-length']
            bytes_to_skip = bodyLength-headerLength
            appendage['pico-appendage-payload'] = self.toHex(payload[:bytes_to_skip])
            payload = payload[bytes_to_skip:]
        else:
            appendageBodies, payload = self.decode_segment(appendageDesc, payload)
            if len(appendageBodies) is not 1:
                self.__decodingErrors += 1
                raise ValueError("Internal error: apg body")
            appendageBodies[0]['pico-appendage-type-name'] = AppendageNameIndex[appendageType]
            appendage.update(appendageBodies[0])

        return appendage, payload

    def on_message (self, context, payload):
        """  Process CTA Packet

        :rtype : none
        :param context: Message context build by preceding link in decoder chain
        :param payload: Message payload
        """

        self.__frame_sequence += 1

        # parse the packet header
        packetHeader, payload = self.__decodePacketHeader(payload)

        # Parse each message in the packet
        packetMessageCount = packetHeader['pico-msg-count']
        for messageNum in range(0, packetMessageCount):
            # decode the common message header
            messageHeader, payload = self.__decodeCommonMessageHeader(payload)

            msgType = messageHeader['pico-msg-type']
            msgTypeHex = messageHeader['pico-msg-type-hex']

            # If this is a business message, decode the bus message header
            if msgType >= 0x300:
                businessMessageHeader, payload = self.__decodeBusinessMessageHeader(payload)
                messageHeader.update(businessMessageHeader)

            # decode the message body
            messageBody, payload = self.__decodeMessageBody(payload, messageHeader)

            # decode each appendage
            appendageCount = messageHeader['pico-msg-appendage-count']
            appendages = []
            for appendageNum in range(0, appendageCount):
                # decode the appendage header & body
                appendage, payload = self.__decodeAppendageHeader(payload)
                appendage, payload = self.__decodeAppendageBody(payload, appendage)
                appendages.append(appendage)


            # pass off to next
            context.update(messageHeader)
            context.update(messageBody)
            context.update({'appendages': appendages})
            self.dispatch_to_next(context,payload)

    def summarize (self):
        """ Provides summary statistics from this Decoder
        """
        return {
            'nextgen-unhandled-msg-types': self.__unhandled_messages,
            'nextgen-unhandled-apg-types': self.__unhandled_appendages,
            'nextgen-ttl-frames': self.__frame_sequence,
            'nextgen-msg_types': self.__msg_counts,
            'nextgen-apg-types': self.__apg_counts
        }


