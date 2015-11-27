from decoder.field import BasicField, WireField, ComputedField, RepeatingGroup, TrimmedString, HexArray
from decoder.descriptor import Descriptor

from decoder.module import *


class Decoder(BasicModule):
    """ SeqFwdCpp decoder

    This decoder processes SeqFwdCpp

    """

    def __parse_options (self, opts):
        pass

    def __init__ (self, opts, next_decoder):
        super (Decoder, self).__init__ ('spry/seqfwd-java', opts, next_decoder)
        self.__parse_options (opts)
        # init summary data
        self.__frame_sequence = 0
        self.__decodingErrors = 0
        self.__unhandled_messages = {}
        self.__msg_counts = {}

        # init message segment descriptors
        self.__segmentDescriptors = {}
        self.__segmentDescriptors['SeqFwdJava'] = Descriptor ([
            WireField ('seqfwd-source-id', 'I', type=long),
            WireField ('seqfwd-seq-num', 'I', type=long),
            WireField ('seqfwd-unscaled-bid', 'I', type=long),
            WireField ('seqfwd-bid-scale', 'I', type=long),
            WireField ('seqfwd-bid-size', 'I', type=long),
            WireField ('seqfwd-unscaled-ask', 'I', type=long),
            WireField ('seqfwd-ask-scale', 'I', type=long),
            WireField ('seqfwd-ask-size', 'I', type=long),
            WireField ('seqfwd-symbol', '12s', type=TrimmedString),
            WireField ('seqfwd-market', '4s', type=TrimmedString)

        ])


        # Init message detail dict:q
        
        import string

        ltrs = string.uppercase

    def on_message (self, inputContext, payload):
        """  Process CTA Packet

        :rtype : none
        :param context: Message context build by preceding link in decoder chain
        :param payload: Message payload
        """

        self.__frame_sequence += 1

        # parse the message payload
        msgDescriptors = self.__segmentDescriptors['SeqFwdJava']
        if msgDescriptors:
            # decode non-empty payloads
            decodedMessages, remainingPayload = self.decode_segment (msgDescriptors, payload)

            # pass context & remaining payload to next link in decoder chain
            if decodedMessages:
                for decoded in decodedMessages:
                    decoded.update ({
                        'seqfwd-msg-type-name': 'SeqFwdJava',
                        'sequence-number': decoded['seqfwd-seq-num']})

                    decoded.update (inputContext)
                    self.dispatch_to_next (decoded, remainingPayload)


    def summarize (self):
        """ Provides summary statistics from this Decoder
        """
        return {
            'UnhandledMsgTypeCodes': self.__unhandled_messages,
            'TotalFramesReceived': self.__frame_sequence,
            'MsgTypeCounts': self.__msg_counts
        }


