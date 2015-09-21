from decoder.decoder import Decoder
from decoder.input.capture.capmsg.segments import *
from progressbar import *
from os import stat

class Decoder(Decoder):
    """ SpryWare Capture File Decoder
    """

    def __parse_options(self, opts):
        self.__cap_file = None
        self.__mmapped_cap_file = None

        # open the cap file
        self.__fname = opts.get('filename', None)
        self.__file_size = os.stat(self.__fname).st_size
        self.__cap_file = open(opts.get ('filename', None), 'r')
        # if mmapped mode enabled, get a file mapping
        if opts.get('mapped-mode', False) is True:
            import mmap
            self.__mapped_cap_file = mmap.mmap(self.__cap_file.fileno(), 0, prot=mmap.PROT_READ)

        self.__max_packet_count = opts.get('max-packets', None)
        self.__frame_count = 0
        self.__pbar = None
        if opts.get('progress', False) is True:
            self.__pbar_widgets = [self.__fname, Percentage(), ' ', FileTransferSpeed(), ' ', ETA()]
            self.__pbar = ProgressBar(widgets=self.__pbar_widgets, maxval=self.__file_size)
            self.__pbar.start()

    def cap_file(self):
        if self.__mmapped_cap_file is not None:
            return self.__mmapped_cap_file
        else:
            return self.__cap_file

    def __init__(self, opts, next_decoder):
        super(Decoder, self).__init__('input/capture/cap', opts, next_decoder)
        self.__parse_options(opts)
        # init summary data
        self.__frames = 0
        self.__bytes = 0
        self.__startTime = None
        self.__endTime = None

    def on_message(self, inputContext, inPayload):
        """  Process spryware capture packet

        :rtype : none
        :param context: Message context build by preceding link in decoder chain
        :param payload: Message payload
        """

    def __read(self, bytes):
        payload = self.cap_file().read(bytes)
        self.__bytes += bytes
        return payload

    def run(self):
        # decode the file header
        wireBytes = FileHeader.WireBytes()
        payload = self.__read(wireBytes)

        headers, payload = self.decode_segment(FileHeader, payload)
        if len(headers) is not 1:
            raise ValueError("Internal error processing capture file header")
        header = headers[0]

        self.__cap_creation_date = header['cap-file-creation-date']
        self.__cap_creation_time = header['cap-file-creation-time']

        # check the file signature
        sig = header['cap-file-signature']
        if sig != 'V2CAN':
            raise ValueError("Invalid cap file signature")
        if self.verbose():
            print "{0} is a valid SpryWare-format capture file".format(self.__fname)

        # main loop
        recordHeaderBytes = RecordHeader.WireBytes()
        packetHeaderBytes = PacketHeader.WireBytes()
        packetFooterBytes = PacketFooter.WireBytes()
        cont = True
        while cont:
            # read the record header
            payload = self.__read(recordHeaderBytes)
            if len(payload) is 0:
                # end of file
                cont = False
                continue
            records, payload = self.decode_segment(RecordHeader, payload)
            if len(records) is not 1:
                raise ValueError("Internal error processing capture file record header")
            record = records[0]

            # read the packet header
            payload = self.__read(packetHeaderBytes)
            packets, payload = self.decode_segment(PacketHeader, payload)
            if len(packets) is not 1:
                raise ValueError("Internal Error processing capture packet header")
            packet = packets[0]

            # read the packet payload

            payloadBytes = record['cap-packet-length'] - packetHeaderBytes
            packetPayload = self.__read(payloadBytes)

            # read the packet footer
            payload = self.__read(packetFooterBytes)
            if len(payload) is not packetFooterBytes:
                raise ValueError("Internal error reading capture packet footer")
            footers, payload = self.decode_segment(PacketFooter, payload)
            if len(footers) is not 1:
                raise ValueError("Internal error processing capture packet footer")
            footer = footers[0]
            if footer['cap-packet-length-check'] != record['cap-packet-length']:
                raise ValueError("CRC error processing capture packet")

            # dispatch packet payload to next
            context = dict()
            self.__frame_count += 1
            context['cap-frame-num'] = self.__frame_count
            context.update(record)
            context.update(packet)
            context.update(footer)
            self.dispatch_to_next(context, packetPayload)

            # update stats
            self.__frames += 1
            if self.__startTime is None:
                self.__startTime = context['cap-packet-timestamp']
            self.__endTime = context['cap-packet-timestamp']

            if self.__max_packet_count is not None:
                if self.__frames >= self.__max_packet_count:
                    cont = False

            if self.__pbar is not None:
                self.__pbar.update(self.__bytes)


    def summarize(self):
        """ Provides summary statistics from this Decoder
        """
        return {
            'cap-frames': self.__frames,
            'cap-bytes': self.__bytes,
            'cap-start-time': self.__startTime,
            'cap-end-time': self.__endTime,
            'cap-create-date': self.__cap_creation_date,
            'cap-create-time': self.__cap_creation_time
        }


