from decoder.module import *
from decoder.opra.binarymsg import segments
from decoder.opra.binarymsg import constants

class Decoder(BasicModule):
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
            msg_version = block['opra-block-version']

            # decode the appropriate message header
            headers, payload = self.decode_segment(segments.MessageHeader[msg_version], payload)
            if len(headers) != 1:
                raise ValueError("Malformed Opra Binary MessageHeader v {0}".format(block['opra-block-ver0']))
            header = headers[0]

            msg_cat = header['opra-msg-cat']
            msg_type = header['opra-msg-type']

            # send to next
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
