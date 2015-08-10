import os.path

import decoder.decoder
from decoder.decoder import Verbosity
from decoder.exceptions import LinkInitError


class Decoder(decoder.decoder.Decoder):
    def __init__(self, opts, next_decoder):
        super(Decoder, self).__init__('null', opts, next_decoder)
        self.__parse_options(opts)
        self.msg_type_counts = {}
            
    def __parse_options(self, opts):
        pass

    def on_message(self, context, payload):
        pass

    def summarize(self):
        return dict()

