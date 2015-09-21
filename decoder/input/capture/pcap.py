from decoder.field import *
from decoder.descriptor import Descriptor

from decoder.decoder import Decoder, Verbosity

from struct import calcsize, unpack_from, pack

import os

import sys
import time
import datetime
import socket

class IpAddrField(WireField):
    def __init__(self):
        self.__orig_data = 0L
        self.__rendered = "NotRendered"
    def __call__(self, data):
        self.__orig_data = data
        self.__render()
        return self.__str__()
    def __str__(self):
        return self.__rendered
    def __repr__(self):
        return "IpAddrField ({0}): {1}".format(self.__orig_data, self.__rendered)
    def __render(self):
        self.__rendered = socket.inet_ntoa(pack('!L', self.__orig_data))
    def as_int(self):
        return self.__orig_data

class Decoder (Decoder):
    """ pcap decoder

    This decoder processes pcaps

    """

    def __parse_options (self, opts):
        self.__file_size = os.stat(opts['filename']).st_size
        self.pcap = self.open_file(opts['filename'])
        self.destAddrWhite = None
        if 'dest-addrs-allow' in opts:
            self.destAddrWhite = (opts['dest-addrs-allow']).split(",;")
        self.destAddrBlack = None
        if 'dest-addrs-disallow' in opts:
            self.destAddrBlack = str(opts['dest-addrs-disallow']).split(",;")
        self.destPortWhite = None
        if 'dest-ports-allow' in opts:
            self.destPortWhite = [int(x) for x in str(opts['dest-ports-allow']).split(",")]
        self.destPortBlack = None
        if 'dest-ports-disallow' in opts:
            self.destPortBlack = str(opts['dest-ports-disallow']).split(",;")
        if 'progress' in opts:
            self.__pbar_widgets = [self.__fname, Percentage(), ' ', FileTransferSpeed(), ' ', ETA()]
            self.__pbar = ProgressBar(widgets=self.__pbar_widgets, maxval=self.__file_size)
            self.__pbar.start()


    def read(self, bytes):
        payload = self.pcap.read(bytes)
        if len(payload) != bytes:
            raise EOFError()
        self.__total_bytes += bytes
        #DELETE ME!!! if self.__total_bytes == 1806500:
        #    bk = True
        return payload
        

    def __init__ (self, opts, next_decoder):
        super (Decoder, self).__init__ ('capture/pcapngmsg', opts, next_decoder)
        self.__pbar = None
        self.__pbar_widgets = None
        self.__parse_options (opts)
        # init summary data
        self.__frame_count = 0
        self.__total_bytes = 0
        self.__first_recv_timestamp = None
        self.__last_recv_timestamp = None

        # init message segment descriptors
        self.PcapDescriptor = {}
        self.PcapDescriptor['MagicNumber'] = Descriptor([
            WireField('pcap-magic-number', 'I', type=int),
        ])

        self.PcapDescriptor['GlobalHeader'] = Descriptor([
            WireField('pcap-magic-number', 'I', type=int),
            WireField('pcap-version-major', 'H', type=int),
            WireField('pcap-version-minor', 'H', type=int),
            WireField('pcap-thiszone', 'i', type=int),
            WireField('pcap-sigfigs', 'I', type=int),
            WireField('pcap-snaplen', 'I', type=int),
            WireField('pcap-datalinktype', 'I', type=int)
        ])

        self.PcapDescriptor['PacketHeader'] = Descriptor([
            WireField('pcap-time-whole', 'I', type=int),
            WireField('pcap-time-frac', 'I', type=int),
            WireField('pcap-incl-len', 'I', type=int),
            WireField('pcap-orig-len', 'I', type=int)
        ])

        self.NetDescriptor = {}
        self.NetDescriptor['EthernetHeader'] = Descriptor([
            WireField('pcap-dest-mac', '6s', type=HexArray),
            WireField('pcap-source-mac', '6s', type=HexArray),
            WireField('pcap-eth-protocol', 'H', type=int)
        ])

        self.NetDescriptor['VlanTag'] = Descriptor([
            WireField('pcap-vlan-id', '2s', type=HexArray),
            WireField('pcap-eth-protocol', 'H', type=int) # this will overwrite the pcap-eth-protocol extracted in EtherNetHeader
        ])

        self.NetDescriptor['IpHeader'] = Descriptor([
            WireField('pcap-ip-version', 'B', type=int),
            WireField('pcap-ip-services', 'B', type=int),
            WireField('pcap-ip-total-length', 'H', type=int),
            WireField('pcap-ip-identification', 'H', type=int),
            WireField('pcap-ip-flags', 'B', type=int),
            WireField('pcap-ip-fragment-offset', 'B', type=int),
            WireField('pcap-ip-ttl', 'B', type=int),
            WireField('pcap-ip-protocol', 'B', type=int),
            WireField('pcap-ip-header-checksum', 'H', type=int),
            WireField('pcap-ip-source-addr', 'L', type=IpAddrField()),
            WireField('pcap-ip-dest-addr', 'L', type=IpAddrField()),
        ])

        self.NetDescriptor['UdpHeader'] = Descriptor([
            WireField('pcap-udp-source-port', 'H', type=int),
            WireField('pcap-udp-dest-port', 'H', type=int),
            WireField('pcap-udp-length', 'H', type=int),
            WireField('pcap-udp-checksum', 'H', type=int),
        ])

        self.NetDescriptor['TcpHeader'] = Descriptor([
            WireField('pcap-tcp-source-port', 'H'),
            WireField('pcap-tcp-dest-port', 'H'),
            WireField('pcap-tcp-seqnum', 'I'),
            WireField('pcap-tcp-ack-num', 'I'),
            WireField('pcap-tcp-data-flags', 'I'),
            WireField('pcap-tcp-checksum', 'B'),
            WireField('pcap-tcp-urgent-ptr', 'B'),
            ConstantField('tcp-packet', True),
            EchoField('tcp-stream-id', 'pcap-tcp-dest-port')
        ])

    def on_message (self, context, payload):
        """  Process pcap Packet

        :rtype : none
        :param context: Message context build by preceding link in decoder chain
        :param payload: Message payload
        """
        filtered_out = False
        payloadProtocol = None

        # grab the ethernet header & pull out the protocol type
        ethernetHeaders, payload = self.decode_segment(self.NetDescriptor['EthernetHeader'], payload)
        if len(ethernetHeaders) is not 1:
            raise ValueError("Internal Error (1)")
        header = ethernetHeaders[0]
        ethProto = header['pcap-eth-protocol']

        # if tagged vlan,
        if ethProto == 0x8100:
            vlanHeaders, payload = self.decode_segment(self.NetDescriptor['VlanTag'], payload)
            if len(vlanHeaders) is not 1:
                raise ValueError("Internal Error (2)")
            header.update(vlanHeaders[0])
            ethProto = header['pcap-eth-protocol']

        # grab the IP header
        if ethProto == 0x0800:
            ipHeaders, payload = self.decode_segment(self.NetDescriptor['IpHeader'], payload)
            if len(ipHeaders) is not 1:
                raise ValueError("Internal Error (3)")
            header.update(ipHeaders[0])
        else:
            if self.verbose():
              print 'Unhandled ethernet protocol: {0}'.format(hex(ethHeaderProtocol))
            return

        # see if the dest-addr is either white-listed or black-listed
        if self.destAddrWhite is not None:
            destAddr = str(header['pcap-ip-dest-addr'])
            if destAddr not in self.destAddrWhite:
                filtered_out = True
        if self.destAddrBlack is not None:
            destAddr = str(header['pcap-ip-dest-addr'])
            if destAddr in self.destAddrBlack:
                filtered_out = True

        # unpack the UDP or TCP header
        payloadProtocol = header['pcap-ip-protocol']
        if payloadProtocol == 0x11:
            # unpack the UDP header
            udpHeaders, payload = self.decode_segment(self.NetDescriptor['UdpHeader'], payload)
            if len(udpHeaders) is not 1:
                raise ValueError("Internal Error (4)")
            pcap_ip_destination_address_index = 10
            stream_id = self.NetDescriptor['IpHeader'].fields()[pcap_ip_destination_address_index].\
                _BasicField__renderer._IpAddrField__orig_data
            stream_id <<= 16;
            stream_id = stream_id | udpHeaders[0]['pcap-udp-dest-port']
            udpHeaders[0]['pcap-udp-stream-id'] = stream_id#NamedField('pcap-udp-stream-id', type=int)
            header.update(udpHeaders[0])
        elif payloadProtocol == 0x06:
            # unpack the TCP header
            tcpHeaders, payload = self.decode_segment(self.NetDescriptor['TcpHeader'], payload)
            if len(tcpHeaders) is not 1:
                raise ValueError("Internal Error decoding TCP Header")
            tcpHeader = tcpHeaders[0]
            src_port = tcpHeader['pcap-tcp-source-port']
            dst_port = tcpHeader['pcap-tcp-dest-port']
            data_offset = int(tcpHeader['pcap-tcp-data-flags'])
            db = bin(data_offset)
            data_offset = (data_offset & 0xF0000000) >> (32-4)
            data_offset_idx = data_offset * 4 # 32-bit words
            # advance the payload beyond the rest of the tcp header
            adv_len = data_offset_idx - self.NetDescriptor['TcpHeader'].WireBytes()
            payload = payload[adv_len:]
            header.update(tcpHeader)
        else:
            if self.verbose():
              print "Unhandled payload protocol:{0}".format(hex(payloadProtocol))
            return

        # see if the dest port is either whitelisted or blacklisted
        if self.destPortWhite is not None:
            destPort = header['pcap-udp-dest-port']
            if destPort not in self.destPortWhite:
                filtered_out = True
        if self.destPortBlack is not None:
            destPort = str(header['pcap-udp-dest-port'])
            if destPort in self.destPortBlack:
                filtered_out = True

        # if this packet isn't filtered out, send it down the line
        header.update(context)
        if not filtered_out:
          self.dispatch_to_next (header, payload)

        # in any case, count it
        if self.__first_recv_timestamp is None:
            self.__first_recv_timestamp = header['pcap-recv-timestamp']
        self.__last_recv_timestamp = header['pcap-recv-timestamp']

    def __SetPcapLittleEndian(self):
        for (descName, desc) in self.PcapDescriptor.iteritems():
            desc.SetLittleEndian()
        self.__endianness = "Little"
    def __SetPcapBigEndian(self):
        for (descName, desc) in self.PcapDescriptor.iteritems():
            desc.SetBigEndian()
        self.__endianness = "Big"
    def __GetPcapEndian(self):
        return self.__endianness

    def __processGlobalHeader(self):
        # extract the global header from the file
        headerBytes = self.PcapDescriptor['GlobalHeader'].WireBytes()
        headerPayload = self.read(headerBytes)
        # get the magic number & determine endianness of the file
        magicNumberContexts, dummyPayload = self.decode_segment(self.PcapDescriptor['MagicNumber'], headerPayload, peek=True)
        magicNumber = magicNumberContexts[0]['pcap-magic-number']
        if magicNumber == 0xa1b2c3d4:
            # little endian
            self.__SetPcapLittleEndian()
            self.__nanosecond = False

        elif magicNumber == 0xd4c3b2a1:
            # big endian
            self.__SetPcapBigEndian()
            self.__nanosecond = False
        elif magicNumber == 0xa1b23c4d:
            # little endian microsecond resolution
            self.__SetPcapLittleEndian()
            self.__nanosecond = True
        elif magicNumber == 0x4d3cb2a1:
            # big enddian microsecond resolution
            self.__SetPcapBigEndian()
            self.__nanosecond = True
        else:
            mnHex = '%0x' % magicNumber
            raise ValueError('Invalid/corrupt pcap file. (Unexpected magic number {0})'.format(mnHex))

        # now get the global header
        globalHeaders, headerPayload = self.decode_segment(self.PcapDescriptor['GlobalHeader'], headerPayload)
        self.__globalHeader = globalHeaders[0]
        magicNumber = self.__globalHeader['pcap-magic-number']
        if magicNumber != 0xa1b2c3d4 and magicNumber != 0xa1b23c4d:
            mnHex = '%0x' % magicNumber
            raise ValueError('Invalid/corrupt pcap file processing. (Unexpected magic number {0})'.format(mnHex))
        self.__snapLen = self.__globalHeader['pcap-snaplen']

    def run(self):
        try:
            # load & process the file header
            self.__processGlobalHeader()
            if self.verbose():
                if self.__nanosecond is True:
                    resol = "Nanosecond"
                else:
                    resol = "Microsecond"
                print "Pcap: {0} endian, {1} resolution".format(self.__GetPcapEndian(), resol)

            # process each packet in the file
            packetHeaderDesc = self.PcapDescriptor['PacketHeader']
            packetHeaderBytes = packetHeaderDesc.WireBytes()

            for netDescName, netDesc in self.NetDescriptor.iteritems():
                netDesc.SetBigEndian()
            while True:
                # rad & process the packet header
                packetHeaderPayload = self.read(packetHeaderBytes)
                if len(packetHeaderPayload) < packetHeaderDesc.WireBytes():
                    # end of file
                    break
                self.__frame_count += 1

                packetHeaders, packetHeaderPayload = self.decode_segment(self.PcapDescriptor['PacketHeader'], packetHeaderPayload)
                if len(packetHeaders) is not 1:
                    raise ValueError("Internal Error")
                packetHeader = packetHeaders[0]
                packetBytes = packetHeader['pcap-incl-len']
                if packetHeader['pcap-orig-len'] != packetBytes:
                    sys.stderr.write("*** WARNING: pcap packet truncated from {0} bytes to {1} bytes!".format(packetHeader['pcap-orig-len'], packetHeader['pcap-incl-len']))

                # compute the packet timestamp
                timeWhole = packetHeader['pcap-time-whole']
                timeFrac = packetHeader['pcap-time-frac']
                (secs, nanos) = (timeWhole, timeFrac)
                if self.__nanosecond is False:
                    nanos *= 1000
                dt = datetime.datetime.fromtimestamp(secs)
                dt.replace(microsecond=(nanos/1000))
                packetHeader['pcap-recv-timestamp'] = dt
                packetHeader['pcap-recv-time-sec'] = '{0}.{1:09d}'.format(secs, nanos)

                 # read the packet payload frrom the file & send to next link in chain
                packetPayload = self.read(packetBytes)
                self.on_message(packetHeader, packetPayload)
        except EOFError as ex:
            return

    def summarize (self):
        """ Provides summary statistics from this Decoder
        """
        return {
            'pcap-total-bytes': self.__total_bytes,
            'pcap-frame-count': self.__frame_count,
            'pcap-first-recv-timestamp': self.__first_recv_timestamp,
            'pcap-last-recv-timestamp': self.__last_recv_timestamp
        }


