import time
from decoder.decoder import Decoder
from decoder.ice.icemsg.segments import  *
from decoder.ice.icemsg.constants import *
import decoder.ice.util as ice_util
import decoder.util as decoder_util


class Decoder(Decoder):
    """ SpryWare Capture File Decoder
    """

    def __parse_options(self, opts):
        self.__cap_file = None
        self.__mmapped_cap_file = None

        # open the cap file
        self.__fname = opts.get('filename', None)
        self.__cap_file = open(opts.get('filename', None), 'rb')
        # if mmapped mode enabled, get a file mapping
        if opts.get('mapped-mode', False) is True:
            import mmap
            self.__mapped_cap_file = mmap.mmap(self.__cap_file.fileno(), 0, prot=mmap.PROT_READ)

        self.__max_packet_count = opts.get('max-packets', None)
        self.__fileOffset = opts.get('file-offset', 0)
        self.__read(self.__fileOffset)
        self.__msgOffset = opts.get('msg-offset', 0)
        self.__login = opts.get('login', False)
        self.__tcp_group = str(opts.get('tcp-group', None))
        self.__prod_def = opts.get('prod-def', False)

    def cap_file(self):
        if self.__mmapped_cap_file is not None:
            return self.__mmapped_cap_file
        else:
            return self.__cap_file

    def __init__(self, opts, next_decoder):
        super(Decoder, self).__init__('ice/cap/tcp_payload', opts, next_decoder)
        # init summary data
        self.__frames = 0
        self.__bytes = 0
        self.__startTime = time.clock()
        self.__endTime = None
        self.__parse_options(opts)

    def on_message(self, inputContext, inPayload):
        """  Process ice tcp capture

        :rtype : none
        :param context: Message context build by preceding link in decoder chain
        :param payload: Message payload
        """

    def __read(self, bytes):
        payload = self.cap_file().read(bytes)
        self.__bytes += bytes
        return payload

    def run(self):
        # main loop
        cont = True
        hdr_bytes = MessageHeader.WireBytes()
        extra_context = dict()

        while cont:
            # read the record header
            payload = self.__read(hdr_bytes)
            if len(payload) is 0:
                # end of file
                cont = False
                continue

            headers, payload_rest = self.decode_segment(MessageHeader, payload)
            if len(headers) is not 1:
                raise ValueError("Internal error processing capture file header")
            header = headers[0]
            # print header

            # read the rest of the body
            body_length = header['ice-msg-body-length']
            payload += self.__read(body_length)

            # if this is a historical response, then populate some additional fields for context
            #  response messages don't have session or seqnum, so gotta add those using response
            if header['ice-msg-type'] == '8':
                responses, _ = self.decode_segment(HistoricalResponse, payload[MessageHeader.WireBytes():])
                response = responses[0]
                extra_context['ice-session-id'] = response['ice-session-id']

                # stream id is used downstream by the JSON outputter to separate files based on mcast
                stream_id = decoder_util.addrToStreamId(response['ice-multicast-group-addr'],
                                                        response['ice-multicast-port'])
                extra_context['pcap-udp-stream-id'] = stream_id

            # if this is a prod def message the streamid must be populated from the known values of the tcp ip/port
            if self.__prod_def:
                [ip, port, _, _] = ice_util.request_tcp_map[self.__tcp_group]
                stream_id = decoder_util.addrToStreamId(ip, port)
                extra_context['pcap-udp-stream-id'] = stream_id

            # dispatch packet payload to next
            if self.__frames >= self.__msgOffset:
                context = dict()
                context.update(header)
                context.update(extra_context)
                # check for login and that the message isn't a login message
                if self.__login or \
                        (header['ice-msg-type'] != '1' and header['ice-msg-type'] != 'A'):
                    self.dispatch_to_next(context, payload)

            # update stats
            self.__frames += 1

            if self.__max_packet_count is not None:
                if self.__frames >= self.__max_packet_count:
                    cont = False

        self.__endTime = time.clock()

    def summarize(self):
        """ Provides summary statistics from this Decoder
        """
        return {
            'cap-frames': self.__frames,
            'cap-bytes': self.__bytes,
            'decode-start-time': self.__startTime,
            'decode-end-time': self.__endTime
        }


