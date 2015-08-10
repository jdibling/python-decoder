from decoder.field import *
from decoder.descriptor import Descriptor

from decoder.decoder import Decoder, Verbosity

from decoder.spry.seqfwd_cppmsg.constants import *



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
        self.__segmentDescriptors['SeqFwd'] = Descriptor ( [
            WireField ('seqfwd-seq-num', 'I'),
            WireField ('seqfwd-transaction-type', 'I'),
            WireField ('seqfwd-recv-time', 'Q', type=long),
            WireField ('seqfwd-send-time', 'Q', type=long),
            WireField ('seqfwd-send-recv-diff', 'Q', type=long),
            WireField ('seqfwd-unscaled-bid', 'I'),
            WireField ('seqfwd-bid-scale', 'I'),
            WireField ('seqfwd-bid-size', 'I'),
            WireField ('seqfwd-unscaled-ask', 'I'),
            WireField ('seqfwd-ask-scale', 'I'),
            WireField ('seqfwd-ask-size', 'I'),
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


