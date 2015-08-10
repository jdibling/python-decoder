from decoder.decoder import Decoder

import socket
from struct import pack

class Decoder(Decoder):
    def __init__(self, opts, next_decoder):
        super(Decoder, self).__init__('input/capture/pcapng', opts, next_decoder)
        self.__parse_options(opts)
        self.__frame_count = 0
        self.__total_bytes = 0

    def __parse_options(self, opts):
        self.group = opts.get('group', None)
        self.port = opts.get('port', None)
        self.interface = opts.get('interface', None)
        if self.group is None or self.port is None or self.interface is None:
            raise ValueError("'group', 'port' and 'interface' are required in the udp module")

    def on_message (self, context, payload):
        self.__frame_count += 1
        self.__total_bytes += len(payload)
        self.dispatch_to_next(context, payload)
      
    def run(self):
        # open the udp socket & read packets until we're killed
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
        sock.bind( (self.group, self.port) )
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        mreq = pack('4s4s', socket.inet_aton(self.group), socket.inet_aton(self.interface))
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        while True:
            payload = sock.recv(4*1024)
            if self.verbose():
                print 'Recieved {0} bytes: {1}'.format(len(payload), self.toHex(payload))
            context = dict()
            self.on_message(context, payload)
            #self.dispatch_to_next(context, payload)




    def summarize(self):
        return {
            'udp-total-bytes': self.__total_bytes,
            'udp-frame-count': self.__frame_count
        }

