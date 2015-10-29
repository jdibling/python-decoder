import datetime

from decoder.decoder import Decoder

from decoder.arca.integratedmsg.constants import *
from decoder.arca.integratedmsg.segments import *


class Decoder(Decoder):

    def __parseOptions (self, opts):
        pass

    def __init__(self, opts, next_decoder):
        super(Decoder, self).__init__('arca/integrated', opts, next_decoder)
        self.__parseOptions(opts)
        self.__unhandledMessages = dict()
        self.__translation = dict()
        self.__symbolIndex = dict()
        self.__timeRefIndex = dict()
        self.__frameCount = 0
        self.__msgCount = 0
        self.__byteCount = 0

    def on_message(self, context, payload):
        """  Process XDP/BBO Message
        """
        self.__frameCount += 1
        self.__byteCount += len(payload)

        # parse the XDP packet header
        packets, payload = self.decode_segment(BboSegment[BboMsgTypeId['XdpPacketHeader']], payload)
        if len(packets) is not 1:
            raise ValueError("Internal error parsing XdpBboPacketHeader")
        packet = packets[0]

        msgCount = packet['xdp-number-msgs']

        # if there are no messages or no remaining payload, nothing further to do
        if msgCount is 0 or len(payload) is 0:
            # ship it
            #self.dispatch_to_next(packet, payload)
            return

        self.__msgCount += msgCount

        # process each message in packet
        for msgIdx in range(0, msgCount):
            # peek at the common header, grab the msg size & type
            commonHeaders, payload = self.decode_segment(BboSegment[BboMsgTypeId['XdpCommonHeader']], payload, peek=True)
            if len(commonHeaders) is not 1:
                raise ValueError("Internal error parsing XDP CommonHeader")
            commonHeader = commonHeaders[0]
            xdpMsgType = commonHeader['xdp-msg-type']
            xdpMsgSize = commonHeader['xdp-msg-size']

            # get the descriptor to decode this message
            segment = BboSegment.get(xdpMsgType, None)
            if segment is None:
                self.__unhandledMessages[xdpMsgType] = self.__unhandledMessages.get(xdpMsgType, 0) + 1
                payload = payload[xdpMsgSize:]
                unhandled = commonHeader
                unhandled['xdp-msg-type-name'] = 'unhandled'
                self.dispatch_to_next(unhandled, payload)
                continue

            # get the message payload & trim the remaining payload
            messagePayload = payload[:xdpMsgSize]
            payload = payload[xdpMsgSize:]

            # decode the message
            messages, messagePayload = self.decode_segment(BboSegment[xdpMsgType], messagePayload)
            if len(messages) is not 1:
                raise ValueError("Internal error parsing XdpBboMessage type {0}: {1}".format(xdpMsgType, BboMsgType[xdpMsgType]))
            message = messages[0]
            message['xdp-msg-type-name'] = BboMsgType[xdpMsgType]

            symbolIdx = message.get('xdp-symbol-index', None)

            # business logic: handle time reference
            if xdpMsgType == BboMsgTypeId['XdpSourceTimeReference']:
                timeRef = int(message['xdp-time-reference'])
                self.__timeRefIndex[symbolIdx] = timeRef

            # business logic: add a translation if this is a symbol index mapping
            if xdpMsgType == BboMsgTypeId['XdpSymbolIndexMapping']:
                symbol = message['xdp-symbol']
                venue = message['xdp-exchange-code']
                roundLot = message['xdp-round-lot-size']

                self.__translation[symbolIdx] = (symbol, venue, roundLot)
                self.__symbolIndex[symbolIdx] = symbol

            # business logic: resolve translations & time references
            if symbolIdx is not None:
                # handle translations
                symbol = self.__symbolIndex.get(symbolIdx, None)
                if symbol is not None:
                    message['xdp-symbol'] = symbol
                # handle time references
                timeRef = self.__timeRefIndex.get(symbolIdx, None)
                nano = message.get('xdp-source-time-nano-part', None)
                if timeRef is not None and nano is not None:
                    mic = int(nano) / 1000
                    dt = datetime.datetime.fromtimestamp(timeRef)
                    dt = dt.replace(microsecond=mic)
                    message['xdp-timestamp'] = dt


#                message['xdp-symbol-len'] = len(symbol)
#                message['xdp-symbol-hex'] = self.toHex(symbol)


            # see if we should send this message down the chain
            if segment.verbosity() <= self.verbosity():
                # build context
                context.update(packet)
                context.update(message)
                # compute sequence-number
                sequence = packet.get('xdp-seq-num', None)
                if sequence is not None:
                    sequence_number = int(sequence) + msgIdx
                    context.update({'sequence-number': sequence_number})
                # send the context
                self.dispatch_to_next(context, messagePayload)






    def summarize(self):
        """ Provides summary statistics from this Decoder
        """
        return {
            'xdp-unhandled-messages': self.__unhandledMessages,
            'xdp-num-translations': len(self.__translation)
        }








