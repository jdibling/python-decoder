from base.field import BasicField, WireField, ComputedField, RepeatingGroup, TrimmedString
from base.descriptor import Descriptor

from base.decoder import Decoder, Verbosity



class Decoder (Decoder):
    """ SeqFwdCpp decoder

    This decoder processes SeqFwdCpp

    """

    def __parse_options (self, opts):
        pass

    def __init__ (self, opts, next_decoder):
        super (Decoder, self).__init__ ('spry/seqfwd-cpp', opts, next_decoder)
        self.__parse_options (opts)
        # init summary data
        self.__frame_sequence = 0
        self.__decodingErrors = 0
        self.__unhandled_messages = {}
        self.__msg_counts = {}

        # init message segment descriptors
        self.__segmentDescriptors = {}
        self.__segmentDescriptors['SeqFwd'] = Descriptor (self.verbosity(), [
            WireField ('seq-num', 'I'),
            WireField ('transaction-type', 'I'),
            WireField ('recv-time', 'Q', type=long),
            WireField ('recv-time', 'Q', type=long),
            WireField ('send-recv-diff', 'Q', type=long),
            WireField ('unscaled-bid', 'I'),
            WireField ('bid-scale', 'I'),
            WireField ('bid-size', 'I'),
            WireField ('unscaled-ask', 'I'),
            WireField ('ask-scale', 'I'),
            WireField ('ask-size', 'I'),
            WireField ('symbol', '12s', type=TrimmedString),
            WireField ('market', '4s', type=TrimmedString)
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
        msgDescriptors = self.__segmentDescriptors['SeqFwd']
        if msgDescriptors:
            # decode non-empty payloads
            decodedMessages, remainingPayload = self.decode_segment (msgDescriptors, payload)

            # pass context & remaining payload to next link in decoder chain
            if decodedMessages:
                for decoded in decodedMessages:
                    decoded.update ({'msg-type-name': 'SeqFwdCpp'})
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


