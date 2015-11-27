from decoder.module import *
from decoder.tmx.cdfmsg.segments import *
from decoder.tmx.cdfmsg.constants import *
from collections import OrderedDict
import re

class Decoder(BasicModule):
    def __init__(self, opts, next_decoder):
        super(Decoder, self).__init__('tmx/cdf', opts, next_decoder)
        self.__parse_options(opts)
        self.__unhandledMessages = dict()
        self.__translation = dict()
        self.__frameCount = 0
        self.__msgCount = dict()
        self.__byteCount = 0

    def __parse_options(self, opts):
        pass

    def __camel_to_dict(self, name):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1-\2', s1).lower()


    def on_message(self, inputContext, payload):
            # decode the transport header
            transport_headers, payload = self.decode_segment(TransportHeader, payload)
            if len(transport_headers) != 1:
                raise ValueError("Internal error processing tmx/cdf transport header")
            transport_header = transport_headers[0]
            msg_len = transport_header['cdf-th-length'] - TransportHeader.WireBytes()
            msg_payload = payload[:msg_len]
            payload = payload[msg_len:]

            message = dict()
            # handle heartbeats
            if transport_header['cdf-th-msg-type'] == 'V':
                message['cdf-heartbeat'] = msg_payload
            else:
                # strip off the leading SOH
                msg_payload = msg_payload[1:]
                # the CDF protocol is an ASCII representation of key/value pairs
                # each key/value pair is delimited by a CdfFieldChar (0x1E)
                # the delimited between the key and value is '='
                # Let's build a dictionary of key/value pairs in this message

                # let's build a dictionary for this message payload

                for pair in msg_payload.split(CdfFieldChar):
                    pair = pair.strip(''.join([CdfControlTrailerChar, CdfBusinessContentChar]))
                    if not pair:
                        continue

                    key_val = pair.split('=')
                    cdf_field_id = key_val[0]
                    if '.' in cdf_field_id:
                        id_idx = cdf_field_id.split('.')
                        cdf_field_id = int(id_idx[0])
                        cdf_field_idx = int(id_idx[1])
                    else:
                        cdf_field_id = int(cdf_field_id)
                        cdf_field_idx = None

                    cdf_field_name = CdfFields[cdf_field_id]
                    output_field_name = 'cdf-{0}'.format(self.__camel_to_dict(cdf_field_name))
                    if cdf_field_idx is not None:
                        cdf_field_name = '{0}-{1}'.format(output_field_name, cdf_field_idx)
                    cdf_field_value = key_val[1]

                    message[output_field_name] = cdf_field_value

            # handle sequence numbering
            if 'cdf-sequence-number' in message:
                message['sequence-number'] = int(message['cdf-sequence-number'])

            # send to next
            context = OrderedDict()
            context.update(message)
            context.update(transport_header)
            context.update(inputContext)
            self.dispatch_to_next(context, payload)

    def summarize(self):
        return {
            'bbo-unhandled-messages': self.__unhandledMessages,
            'bbo-translation-entries': len(self.__translation),
            'bbo-frames': self.__frameCount,
            'bbo-bytes': self.__byteCount,
            'bbo-msg-counts': self.__msgCount
        }
