from decoder.field import *
from decoder.descriptor import Descriptor

from decoder.decoder import Decoder, Verbosity

from decoder.phx.nextgenmsg.field import *

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
    'UsEquityStatus': 0x308,
    'UsEquitySymbolSessionChange': 0x311,
    'UsEquityTimeReference': 0x315,
    'UsEquityImbalance': 0x317,
    'UsEquityFullDepth': 0x319,
    'UsEquityIncrementalDepth': 0x31A,
}

MessageNameIndex = dict((v, k) for k, v in MessageTypeIndex.iteritems())

AppendageTypeIndex = {
    # TotalView Appendage Types
    'TotalViewOrderAdd': 0x100,
    'TotalViewOrderAddAttribution': 0x101,
    'TotalViewOrderCancel': 0x102,
    'TotalViewOrderDelete': 0x103,
    'TotalViewOrderFill': 0x104,
    'TotalViewOrderFillPriced': 0x105,
    'TotalViewOrderReplace': 0x106,
    'TotalViewTrade': 0x107,
    'TotalViewCrossTrade': 0x108,

    # ArcaXDP Appendage Types
    'ArcaXDPOrderAdd': 0x200,
    'ArcaXDPOrderAddAttributed': 0x201,
    'ArcaXDPOrderDelete': 0x202,
    'ArcaXDPOrderFill': 0x203,
    'ArcaXDPOrderRevise': 0x204,
    'ArcaXDPTrade': 0x205,
    'ArcaXDPEquityStatus': 0x208,
    'ArcaXDPImbalance': 0x209,
    'ArcaXDPSymbolSessionChange': 0x20B,
#    'ArcaXDPHeartbeat': 0x20F,

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
            WireField('pico-stream-id', '8s', type=StreamIdToString),
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
            WireField('pico-exchange-seq-num', 'Q', type=int),
            EchoField('sequence-number', 'pico-exchange-seq-num')
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

        self.MessageDesc[MessageTypeIndex['UsEquityStatus']] = Descriptor([
            WireField('pico-market', '4s', type=TrimmedString),
            WireField('pico-ticker', '12s', type=TrimmedString),
            WireField('pico-time', 'Q', type=int),
            WireField('pico-trading-status', 'c')
        ], checksize=4+12+8+1)

        self.MessageDesc[MessageTypeIndex['UsEquityTimeReference']] = Descriptor([
            WireField('pico-market', '4s', type=TrimmedString),
            WireField('pico-ticker', '12s', type=TrimmedString),
            WireField('pico-time', 'Q', type=int),
        ], checksize=4+12+8)

        self.MessageDesc[MessageTypeIndex['UsEquityImbalance']] = Descriptor([
            WireField('pico-market', '4s', type=TrimmedString),
            WireField('pico-ticker', '12s', type=TrimmedString),
            WireField('pico-time', 'Q', type=int),
            WireField('pico-imbalance-size', 'q', type=int),
            WireField('pico-paired-size', 'Q', type=int),
            WireField('pico-rference-price', 'Q', type=int),
            WireField('pico-auction-type', 'c'),
            WireField('pico-imbalance-side', 'c')
        ], checksize=4+12+8+8+8+8+1+1)

        self.MessageDesc[MessageTypeIndex['UsEquitySymbolSessionChange']] = Descriptor([
            WireField('pico-market', '4s', type=TrimmedString),
            WireField('pico-ticker', '12s', type=TrimmedString),
            WireField('pico-time', 'Q', type=int),
        ], checksize=4+12+8)

        self.MessageDesc[MessageTypeIndex['UsEquityFullDepth']] = Descriptor([
            WireField('pico-market', '4s', type=TrimmedString),
            WireField('pico-ticker', '12s', type=TrimmedString),
            WireField('pico-num-bid-levels', 'B', type=int),
            WireField('pico-num-ask-levels', 'B', type=int),
            WireField('pico-level-changed', 'B', type=int),
            WireField('pico-side-changed', 'B', type=int),
            RepeatingGroup([
                WireField('pico-bid-price-unscaled', 'Q', type=int),
                WireField('pico-bid-size', 'Q', type=int),
                WireField('pico-bid-time', 'Q', type=int),
                WireField('pico-bid-orders', 'I', type=int)
            ], RepeatingGroup.ReprCountFromContext('pico-num-bid-levels'), embed_as='pico-bid-depth'),
            RepeatingGroup([
                WireField('pico-ask-price-unscaled', 'Q', type=int),
                WireField('pico-ask-size', 'Q', type=int),
                WireField('pico-ask-time', 'Q', type=int),
                WireField('pico-ask-orders', 'I', type=int)
            ], RepeatingGroup.ReprCountFromContext('pico-num-ask-levels'), embed_as='pico-ask-depth')
        ])

        self.MessageDesc[MessageTypeIndex['UsEquityIncrementalDepth']] = Descriptor([
            WireField('pico-market', '4s', type=TrimmedString),
            WireField('pico-ticker', '12s', type=TrimmedString),
            WireField('pico-level', 'B', type=int),
            WireField('pico-side', 'B', type=int),
            WireField('pico-price-unscaled', 'Q', type=int),
            WireField('pico-size', 'Q', type=int),
            WireField('pico-time', 'Q', type=int),
            WireField('pico-num-orders', 'I', type=int)
        ])



        self.TotalViewCommonApg = [
            WireField('pico-itch-stock-locate', 'H', type=int),
            WireField('pico-itch-tracking-number', 'H', type=int),
        ]

        """ TotalView Appendages
        """
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

        """ Arca appendages
        """
        self.AppendageDesc[AppendageTypeIndex['ArcaXDPOrderAdd']] = Descriptor([
            WireField('pico-xdp-symbol-index', 'I', type=int),
            WireField('pico-xdp-symbol-seq-num', 'I', type=int),
            WireField('pico-xdp-order-duration', 'B', type=int),
            WireField('pico-xdp-order-flags', 'B', type=int)
        ], checksize=4+4+1+1)

        self.AppendageDesc[AppendageTypeIndex['ArcaXDPOrderAddAttributed']] = Descriptor([
            WireField('pico-xdp-symbol-index', 'I', type=int),
            WireField('pico-xdp-symbol-seq-num', 'I', type=int),
            WireField('pico-xdp-order-duration', 'B', type=int),
            WireField('pico-xdp-order-flags', 'B', type=int),
            WireField('pico-xdp-firm-id', '5s', type=int)
        ], checksize=4+4+1+1+5)

        self.AppendageDesc[AppendageTypeIndex['ArcaXDPOrderDelete']] = Descriptor([
            WireField('pico-xdp-symbol-index', 'I', type=int),
            WireField('pico-xdp-symbol-seq-num', 'I', type=int),
            WireField('pico-xdp-order-side', 'B', type=int),
            WireField('pico-xdp-order-duration', 'B', type=int),
            WireField('pico-xdp-reason', 'B', type=int)
        ], checksize=4+4+1+1+1)

        self.AppendageDesc[AppendageTypeIndex['ArcaXDPOrderFill']] = Descriptor([
            WireField('pico-xdp-symbol-index', 'I', type=int),
            WireField('pico-xdp-symbol-seq-num', 'I', type=int),
            WireField('pico-xdp-fill-price-unscaled', 'Q', type=int),
            WireField('pico-xdp-order-duration', 'B', type=int),
            WireField('pico-xdp-reason', 'B', type=int),
            WireField('pico-xdp-trade-id', 'I', type=int)
        ], checksize=4+4+8+1+1+4)

        self.AppendageDesc[AppendageTypeIndex['ArcaXDPOrderRevise']] = Descriptor([
            WireField('pico-xdp-symbol-index', 'I', type=int),
            WireField('pico-xdp-symbol-seq-num', 'I', type=int),
            WireField('pico-xdp-order-side', 'B', type=int),
            WireField('pico-xdp-order-duration', 'B', type=int),
            WireField('pico-xdp-reason', 'B', type=int),
        ], checksize=4+4+1+1+1)

        self.AppendageDesc[AppendageTypeIndex['ArcaXDPTrade']] = Descriptor([
            WireField('pico-xdp-symbol-index', 'I', type=int),
            WireField('pico-xdp-symbol-seq-num', 'I', type=int),
            WireField('pico-xdp-trade-id', 'I', type=int),
            WireField('pico-xdp-trade-cond-1', 'c'),
            WireField('pico-xdp-trade-cond-2', 'c'),
            WireField('pico-xdp-trade-cond-3', 'c'),
            WireField('pico-xdp-trade-cond-4', 'c'),
            WireField('pico-xdp-trade-flags', 'B', type=int),
            WireField('pico-xdp-ask-price-unscaled', 'Q', type=int),
            WireField('pico-xdp-ask-size', 'Q', type=int),
            WireField('pico-xdp-bid-price-unscaled', 'Q', type=int),
            WireField('pico-xdp-bid-size', 'Q', type=int),
        ], checksize=4+4+4+1+1+1+1+1+8+8+8+8)
        self.AppendageDesc[AppendageTypeIndex['ArcaXDPImbalance']] = Descriptor([
            WireField('pico-xdp-symbol-index', 'I', type=int),
            WireField('pico-xdp-symbol-seq-num', 'I', type=int),
            WireField('pico-xdp-imbalance-size', 'Q', type=int),
            WireField('pico-xdp-auction-hour', 'B', type=int),
            WireField('pico-xdp-auction-minute', 'B', type=int),
            WireField('pico-xdp-cont-book-clearing-price-unscaled', 'Q', type=int),
            WireField('pico-xdp-closing-only-price', 'Q', type=int),
            WireField('pico-xdp-ssr-filling-price', 'Q', type=int)
        ], checksize=4+4+8+1+1+8+8+8)

        self.AppendageDesc[AppendageTypeIndex['ArcaXDPSymbolSessionChange']] = Descriptor([
            WireField('pico-xdp-symbol-index', 'I', type=int),
            WireField('pico-xdp-symbol-seq-num', 'I', type=int),
            WireField('pico-xdp-trading-session', 'c')
        ], checksize=4+4+1)

        # self.AppendageDesc[AppendageTypeIndex['ArcaXDPHeartbeat']] = Descriptor([
        #     WireField('pico-xdp-next-sequence', 'I', type=int)
        # ], checksize=4)




        self.AppendageDesc[AppendageTypeIndex['ArcaXDPEquityStatus']] = Descriptor([
            WireField('pico-xdp-symbol-index', 'I', type=int),
            WireField('pico-xdp-symbol-seq-num', 'I', type=int),
            WireField('pico-xdp-security-status', 'B', type=int),
            WireField('pico-xdp-halt-condition', 'B', type=int)
        ], checksize=4+4+1+1)

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
            if self.verbose:
                sys.stderr.write("Unhandled message type: {0}\n".format(messageTypeHex))
            # skip the message body in the payload
            bytes_to_skip = messageHeader['pico-msg-body-length']
            message = {'msg-body-payload': self.toHex(payload[:bytes_to_skip])}
            payload = payload[bytes_to_skip:]
            return (message, payload)
        else:
            messageBodies, payload = self.decode_segment(messageDesc, payload)
            if len(messageBodies) is not 1:
                raise ValueError("Internal error processing NextGen message body")

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
            if self.verbose():
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

    def on_message (self, inputContext, payload):
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
            if len(payload) > 0:
                for appendageNum in range(0, appendageCount):
                    # decode the appendage header & body
                    appendage, payload = self.__decodeAppendageHeader(payload)
                    appendage, payload = self.__decodeAppendageBody(payload, appendage)
                    appendages.append(appendage)


            # pass off to next
            context = dict()
            context.update(packetHeader)
            context.update(inputContext)
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
            'nextgen-msg-types': self.__msg_counts,
            'nextgen-apg-types': self.__apg_counts
        }


