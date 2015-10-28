from base.decoder import Decoder
from decoder.opra.details import segments
from decoder.opra.details import constants

class Decoder(Decoder):
    def __init__(self, opts, next_decoder):
        super(Decoder, self).__init__('opra/binary', opts, next_decoder)
        self.__parse_options(opts)
        self.__unhandledMessages = dict()
        self.__translation = dict()
        self.__frameCount = 0
        self.__msgCount = dict()
        self.__byteCount = 0

    def __parse_options(self, opts):
        pass

    def on_message(self, inputContext, payload):
            # decode the block header
            blocks, payload = self.decode_segment(segments.BlockHeader, payload)
            if len(blocks) != 1:
                raise ValueError("Malformed Opra Binary BlockHeader")
            block = blocks[0]

            # decode the appropriate message header
            msgHeaders, payload = self.decode_segment(constants.MsgHeadersByVersion[block['opra-block-ver']], payload)
            if len(msgHeaders) != 1:
                raise ValueError("Malformed Opra Binary MessageHeader v {0}".format(block['opra-block-ver0']))
            msgHeader = msgHeaders[0]


            # send to next
            if block['sequence-number'] == 36399374:
                bk = True
            context = {}
            context.update(block)
            context.update(msgHeader)
            context.update(inputContext)
            self.dispatch_to_next(context, payload)

    def summarize(self):
        return {
            'opra-unhandled-messages': self.__unhandledMessages,
            'opra-translation-entries': len(self.__translation),
            'opra-frames': self.__frameCount,
            'opra-bytes': self.__byteCount,
            'opra-msg-counts': self.__msgCount
        }
