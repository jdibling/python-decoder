from decoder.module import InputDecoder
from decoder.input.capture.pcapngmsg.constants import *
from decoder.exceptions import *
import gzip
import time

class Decoder(InputDecoder):
    def __init__(self, opts, next_decoder):
        super(Decoder, self).__init__('input/capture/pcapng', opts, next_decoder)
        self.__parse_options(opts)
        self.__frame_count = 0
        self.__total_bytes = 0
        self.__first_recv_timestamp = None
        self.__last_recv_timestamp = None
        # set up the jump table
        self.jumpTable = {}
        self.jumpTable[BlockTypeIndex['SectionHeader']] = self.__processSectionHeader
        self.jumpTable[BlockTypeIndex['InterfaceDefinition']] = self.__processInterfaceDescription
        self.jumpTable[BlockTypeIndex['EnhancedPacket']] = self.__processEnhancedPacket

    def __parse_options(self, opts):
        self.destAddrWhite = None
        if 'dest-addrs-allow' in opts:
            self.destAddrWhite = (opts['dest-addrs-allow']).split(",;")
        self.destAddrBlack = None
        if 'dest-addrs-disallow' in opts:
            self.destAddrBlack = str(opts['dest-addrs-disallow']).split(",;")
        self.destPortWhite = None
        if 'dest-ports-allow' in opts:
            self.destPortWhite = str(opts['dest-ports-allow']).split(",;")
        self.destPortBlack = None
        if 'dest-ports-disallow' in opts:
            self.destPortBlack = str(opts['dest-ports-disallow']).split(",;")

    def __decodeBlock(self):
        # first decode the block header

        headerPayload = self.read_from_input_file(BlockHeader.WireBytes())

        headers, headerPayload = self.decode_segment(BlockHeader, headerPayload)
        if len(headers) is not 1:
            raise ValueError("Internal error decoding pcap-ng block header")
        header = headers[0]

        # get some basic info about this block
        blockType = header['pcap-block-type']
        if blockType & (1 << 31):
            # pcap internal block type
            return (None, None, None)
        totalBlockLen = header['pcap-block-total-length']
        blockTuple = BlockTypes.get(blockType, None)
        if blockTuple is None:
            raise ValueError("Internal error processing pcap-ng block:  unhandled block type {0}".format(blockType))
        blockDesc = blockTuple[0]
        blockTypeName = blockTuple[1]

        # decode the block body

        blockPayloadLen = blockDesc.WireBytes()
        blockPayload = self.read_from_input_file(blockPayloadLen)
        bodies, blockPayload = self.decode_segment(blockDesc, blockPayload)
        if len(bodies) is not 1:
            raise ValueError("Internal error decoding pcap block body type {0} ('{1}')".format(self.toHex(blockType), blockTypeName ))
        body = bodies[0]

        # if there is a variable-length data field in the block, decode it
        capLen = body.get('pcap-captured-length', 0)
        capWireBytes = capLen
        if capLen != 0:
            # see if there are padding bytes
            paddingBytes = (capLen % 4)
            if paddingBytes > 0:
                paddingBytes = 4-paddingBytes
            # pull the data from the capfile
            capWireBytes = capLen + paddingBytes
            fieldPayload = self.read_from_input_file(capWireBytes)
            fieldPayload = fieldPayload[:capLen] # we can just discard the padding bytes; it's garbage
            # store the packet data
            body.update({'pcap-packet-data': fieldPayload})

        # decode the block options
        optionsPayloadLen = totalBlockLen
        optionsPayloadLen -= BlockHeader.WireBytes() # already processed
        optionsPayloadLen -= capWireBytes # already processed
        optionsPayloadLen -= blockDesc.WireBytes() # already processed
        optionsPayloadLen -= BlockFooter.WireBytes() # will process
        optionsPayload = self.read_from_input_file(optionsPayloadLen)
        options = self.__decodeBlockOptions(blockType, optionsPayload)

        # decode the block footer & verify
        footerPayloadLen = BlockFooter.WireBytes()
        footerPayload = self.read_from_input_file(footerPayloadLen)
        footers, footerPayload = self.decode_segment(BlockFooter, footerPayload)
        if len(footers) is not 1:
            raise ValueError("Internal error decoding block footer")
        footer = footers[0]
        totalBlockLenCheck = footer['pcap-block-total-length-check']
        if totalBlockLen != totalBlockLenCheck:
            raise ValueError("Internal error decoding block:  checksum failure")

        # call the block processor, if there is one
        blockProcessor = self.jumpTable.get(blockType, None)
        if blockProcessor is not None:
            blockProcessor(body, header, options)
        else:
            self.__unhandledMessages[blockType] = self.__unhandledMessages.get(blockType, 0) + 1

        return (body, header, options)

    def __decodeBlockOptions(self, blockType, payload):
        opt = dict()
        blockOptions = BlockOptionTypes.get(blockType, None)
        if blockOptions is None:
            return []

        while payload:
            # decode the option header
            if len(payload) < OptionHeader.WireBytes():
                bk = True
            headers, payload = self.decode_segment(OptionHeader, payload)
            if len(headers) is not 1:
                raise ValueError("Internal error processing block option header")
            header = headers[0]
            optValLen = header['pcap-option-length']
            optType = header['pcap-option-code']
            optValPayload = payload[:optValLen]
            paddingBytes = (optValLen % 4)
            if paddingBytes > 0:
                paddingBytes = 4-paddingBytes
            payload = payload[optValLen+paddingBytes:]
            optionTuple = blockOptions.get(optType, None)
            if optionTuple is not None:
                optName = optionTuple[0]
                optType = optionTuple[1]
                if optType is not None:
                    opt[optName] = optType(optValPayload)
        return opt

    def __processSectionHeader(self, body, header, options):
        self.ifc = []
        return

    def __processInterfaceDescription(self, body, header, options):
        # decode the tsresol option
        payload = options['tsresol']
        resolOpts, payload = self.decode_segment(TsResolOption, payload)
        if len(resolOpts) is not 1:
            raise ValueError("Internal error decoding 'tsresol' optional field in InterfaceDescription block in pcapngmsg file")
        resolOpt = resolOpts[0]
        resolution = resolOpt['pcap-tsresol']
        resolutionNanos = 1000000000 / pow(10,resolution)
        print 'PcapNG Interface {0} timestamp resolution: {1} ({2} nanoseconds)'.format(len(self.ifc), resolution, resolutionNanos)

        self.ifc.append( (options, resolutionNanos) )
        return

    def __processEnhancedPacket(self, body, header, options):
        # build a 64-bit timestamp from the packet
        packetPayload = body['pcap-packet-data']
        timestamp = body['pcap-timestamp-high']
        timestamp <<= 32
        timestamp += body['pcap-timestamp-low']
        # determine the 'units' of the timestamp (how many nanos one unit represents)
        ifcIdx = body['pcap-ifc-id']
        timestampUnits = self.ifc[ifcIdx][1]
        # compute the timestamp in nanos since epoch
        timestampInNanos = timestamp * timestampUnits
        body['pcapng-recv-nanos'] = timestampInNanos
        timestampInNanosStr = str(timestampInNanos)
        tsWhole = timestampInNanosStr[:-9]
        tsFrac = timestampInNanosStr[len(timestampInNanosStr)-len(tsWhole)+1:]
        body['pcap-recv-time-sec'] = float('{0}.{1}'.format(tsWhole, tsFrac))
        body['packet-recv-time-gmt'] = body['pcap-recv-time-sec']

        # compute the parts of the timestamp
        tv = timestampInNanos

        nanos = tv % 1000000000
        micros = int(nanos / 1000)
        tv /= 1000000000

        ts = datetime.datetime.fromtimestamp(tv)
        ts = ts.replace(microsecond=micros)
        s = str(ts)

        # construct a context & pass to next
        context = dict()
        context.update(body)
        context.update({'pcap-recv-timestamp': ts})
        del context['pcap-packet-data']

        self.on_message(context, packetPayload)

    def on_message (self, context, payload):
        """  Process pcapngmsg Packet

        :rtype : none
        :param context: Message context build by preceding link in decoder chain
        :param payload: Message payload
        """
        self.__frame_count += 1
        filtered_out = False
        payloadProtocol = None

        # grab the ethernet header & pull out the protocol type
        ethernetHeaders, payload = self.decode_segment(EthernetHeader, payload)
        if len(ethernetHeaders) is not 1:
            raise ValueError("Internal Error (1)")
        header = ethernetHeaders[0]
        ethProto = header['pcap-eth-protocol']

        # if tagged vlan,
        if ethProto == 0x8100:
            vlanHeaders, payload = self.decode_segment(VlanTag, payload)
            if len(vlanHeaders) is not 1:
                raise ValueError("Internal Error (2)")
            header.update(vlanHeaders[0])
            ethProto = header['pcap-eth-protocol']

        # grab the IP header
        if ethProto == 0x0800:
            ipHeaders, payload = self.decode_segment(IpHeader, payload)
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

        # unpack the UDP header
        payloadProtocol = header['pcap-ip-protocol']
        if payloadProtocol == 0x11:
            udpHeaders, payload = self.decode_segment(UdpHeader, payload)
            if len(udpHeaders) is not 1:
                raise ValueError("Internal Error (4)")
            header.update(udpHeaders[0])
        else:
            if self.verbose():
              print "Unhandled payload protocol:{0}".format(hex(payloadProtocol))
            return

        # see if the dest port is either whitelisted or blacklisted
        if self.destPortWhite is not None:
            destPort = str(header['pcap-udp-dest-port'])
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


    def run(self):
        # now keep processing blocks until we run out of file
        try:
            cont = True
            while cont:
                body, header, options = self.__decodeBlock()
        except EOFError as ex:
            # reached end of file -- just stop
            print "End Of File"


    def summarize(self):
        return {
            'pcapng-total-bytes': self.__total_bytes,
            'pcapng-frame-count': self.__frame_count,
            'pcapng-first-recv-timestamp': self.__first_recv_timestamp,
            'pcapng-last-recv-timestamp': self.__last_recv_timestamp
        }
