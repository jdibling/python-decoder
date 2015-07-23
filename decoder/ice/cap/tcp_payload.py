import time
from base.decoder import Decoder
from decoder.ice.icemsg.segments import  *
from decoder.ice.icemsg.constants import *
import scripts.seq_checkers.bytestostring as stream_id_converter

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
        historical_dict = dict()

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
                historical_dict['ice-session-id'] = response['ice-session-id']

                # stream id is used downstream by the JSON outputter to separate files based on mcast
                stream_id = stream_id_converter.addrToStreamId(response['ice-multicast-group-addr'],
                                                               response['ice-multicast-port'])
                historical_dict['pcap-udp-stream-id'] = stream_id

            # dispatch packet payload to next
            if self.__frames >= self.__msgOffset:
                context = dict()
                context.update(header)
                context.update(historical_dict)
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


