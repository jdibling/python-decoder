from base.field import BasicField, WireField, ComputedField, RepeatingGroup, LookupField, TrimmedString
from base.descriptor import Descriptor

from base.decoder import Decoder, Verbosity

from decoder.cta.constants import  InstrumentType, CancelErrorAction
from decoder.cta.types import TimeStamp, DecDiv, PriceDenominator
from decoder.cta.fields import FreeFormTextField
from decoder.cta.cqsmsg.constants import *
from decoder.cta.cqsmsg.segments import *

class Decoder(Decoder):
    """ cqs Decoder

    This decoder processes cqs packets.

    """

    def __parse_options(self, opts):
        self.showAdminMessages = bool(opts.get('show-admin-messages', False))
        self.showLineIntegrity = bool(opts.get('show-line-integrity-messages', False))

    def __init__(self, opts, next_decoder):
        super(Decoder, self).__init__('cta/cqs', opts, next_decoder)
        self.__parse_options(opts)
        # init summary data
        self.__frame_sequence = 0
        self.__decodingErrors = 0
        self.__unhandled_messages = {}
        self.__msg_counts = {}

    def on_message(self, inputContext, inPayload):
        """  Process CTA Packet

        :rtype : none
        :param context: Message context build by preceding link in decoder chain
        :param payload: Message payload
        """

        self.__frame_sequence += 1

        # split the incoming payload in to multiple messages
        payloads = []
        for c in inPayload:
            co = ord(c)
            if co in PayloadSeperators:
                payloads.append("")
            else:
                payloads[-1] += c
        payloads.pop(-1)    # the last element should just be and empty string because of the trailing ETX, so dump it

        # parse each message in the payload
        for payload in payloads:
            # decode the common header
            headers, payload = self.decode_segment(MsgHeader, payload)
            if len(headers) is not 1:
                self.__decodingErrors += 1
                raise ValueError("Internal error decoding CQS message header")

            header = headers[0]
            msgCat = header['cqs-msg-cat']
            msgTyp = header['cqs-msg-typ']
            msgTypeCode = msgCat+msgTyp
            header['cqs-msg-type'] = msgTypeCode

            # decode the message body, if we can
            self.__msg_counts[msgTypeCode] = self.__msg_counts.get(msgTypeCode, 0) + 1
            descriptor = GetDescriptor(msgCat, msgTyp)

            if descriptor is None:
                context = dict(inputContext)
                context.update(header)
                context.update({'cqs-msg-type-name': 'unhandled'})
                self.dispatch_to_next(context, payload)
                self.__unhandled_messages[msgTypeCode] = self.__unhandled_messages.get(msgTypeCode, 0) + 1
                continue

            messages, payload = self.decode_segment(descriptor, payload)
            if len(messages) is not 1:
                raise ValueError("Error decoding CQS message payload")
            message = messages[0]

            message['cqs-msg-type-name'] = GetMessageName(msgCat, msgTyp)

            # handle processing of NBBO data
            nbboIndic = message.get('cqs-nbbo', 0)
            nbbo = None
            if nbboIndic == 4 or nbboIndic == 6:
                nbbos = None
                if nbboIndic == 4:
                    nbbos, payload = self.decode_segment(LongNBbo, payload)
                elif nbboIndic == 6:
                    nbbos, payload = self.decode_segment(ShortNBbo, payload)
                if len(nbbos) is not 1:
                    raise ValueError("Internal Error processing Long NBBO Appendage")
                nbbo = nbbos[0]
            elif nbboIndic == 1:
                nbbo = {'cqs-quote-is-nbbo': True}

            # handle processing of FINRA BBO data
            fbboIndic = message.get('cqs-finra-ice', 0)
            fbbo = None
            if fbboIndic == 3:
                fbbos, payload = self.decode_segment(FinraBbo, payload)
                if len(fbbos) is not 1:
                    raise ValueError("Internal error processing FINRA BBO appendage")
                fbbo = fbbos[0]
            elif fbboIndic == 1:
                fbbo = {'cqs-quote-if-finra-ice': True}

            context = dict(inputContext)
            context.update(header)
            context.update(message)
            if nbbo is not None:
                context.update(nbbo)
            if fbbo is not None:
                context.update(fbbo)
            if header.get('cqs-seq-num', None) is not None:
                context.update({'sequence-number': int(header['cqs-seq-num'])})
            self.dispatch_to_next(context, payload)

    def summarize(self):
        """ Provides summary statistics from this Decoder
        """
        return {
            'UnhandledMsgTypeCodes': self.__unhandled_messages,
            'TotalFramesReceived': self.__frame_sequence,
            'MsgTypeCounts': self.__msg_counts
        }


