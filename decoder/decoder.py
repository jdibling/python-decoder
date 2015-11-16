from .exceptions import *
from .verbosity import Verbosity
import gzip


class Decoder(object):
    """  Decoder base class

        In order to implement a new Decoder class,
        you must provide implementations for:

         1)  on_message
         2)  summarize

         In order to implement a new Head Decoder class,
         (eg, the first link in a decoder chain),
         you must also implement:

         1) run

         In order to implement a new Tail Decoder class,
         (eg, the last link in a decoder chain),
         you must also implement:

         1) summarize (can also be implemented by any Decoder)

        Your Decoder class must call the __init__ function
        in the Base class once, at construction.  This
        is needed in order to build the decoder chain.
    """

    def toHex (self, x):
        return ' '.join ([hex (ord (c))[2:].zfill (2) for c in x])

    def toCHex (self, x):
        return ", ".join ([hex (ord (c)) for c in x])

    def __init__(self, kind, opts, next_decoder):
        self.__parse_basic_module_options(opts)
        self.kind = kind
        self.next = next_decoder
        self._last_decoded_recv_time = None

    def __parse_basic_module_options (self, opts):
        self.__verbosity = Verbosity.Normal
        if 'verbose' in opts:
            self.__verbosity = True if opts.get ('verbose', False) == True  else False
        elif 'verbosity' in opts:
            if opts['verbosity'].lower() not in Verbosity.Names:
                legitValues = ','.join(key for (key,val) in Verbosity.Names.iteritems())
                errorStr = "Error:  Verbosity '{0}' not understood.  Use one of: {1}".format(opts['verbosity'], legitValues)
                raise LinkInitError(errorStr)
            else:
                self.__verbosity = Verbosity.Names[opts['verbosity'].lower()]
        self.__show_payloads = opts.get ('show-payloads', False)

    @property
    def verbosity(self):
        return self.__verbosity
    @property
    def verbose(self):
        return self.verbosity == Verbosity.Verbose
    @property
    def show_payloads(self):
        return self.__show_payloads

    def __str__(self):
        if self.next is not None:
            return '[' + self.kind + ']' + ' -> ' + str(self.next)
        else:
            return '[' + self.kind + ']'

    def decode_segment(self, fields, payload, **kwargs):
        # if we are peeking, copy the payload
        origPayload = None
        if kwargs.get('peek', False) is True:
            origPayload = payload
        # decode each field individually
        decodedContexts = [{}]
        for field in fields:
            # decode this field
            (payload, decodedContexts) = field.eval(payload, decodedContexts, **kwargs)

        # if we are peeking, return the original payload
        if origPayload is not None:
            return decodedContexts, origPayload
        else:
            return decodedContexts, payload

    def on_message(self, msg, payload):
        """  Packet processor

          Packets are decoded by a "decoder chain."  Each link in the chain
          handles a different type of data.  For example, when doing
          gap-checking on an ArcaXDBBBO pcapngmsg file, there are three links
          in the chain:

              1)  A pcapngmsg decoder
              2)  An XDP decoder
              3)  A gap-check psudo-decoder

          Each link in the chain does some processing of the inbound data,
          saves the processed fields in a dictionary, and then passes
          both that dictionary and whatever unprocessed data remaines (the payload)
          to the next link in the chain.  The chains are agnositic in the sense
          that they don't care who the next link in the chain is, or even if
          there is a next link in the chain.

          A single message processed by one link in the chain can result in
          many subsequent messages processed by the next link.  For example,
          one XDP Packet consists of one or more XDP Messages.  The XDP decoder
          handles the XDP Common Header, and then calls the next link in the
          chain for each XDP message within that XDP Packet.

          :rtype : none
          :param context: Message context build by preceding link in decoder chain
          :param payload: Message payload
          """
        pass

    def start(self):
        try:
            self.run()
        except InterruptException:
            return

    def stop(self):
        if self.next is not None:
            self.next.stop()

    def dispatch_to_next(self, context, payload):
        self._last_decoded_recv_time = context.get('packet-recv-time-gmt', None)

        if self.next is not None:
            self.next.on_message(context, payload)

class InputDecoder(Decoder):
    def __init__(self, kind, opts, next_decoder):
        super(InputDecoder, self).__init__(kind, opts, next_decoder)
        self.__parse_input_module_options(opts)
        # set up some summary vars
        self.__read_bytes = 0
        self.__raw_bytes_read = 0

    @property
    def raw_bytes_read(self):
        return self.__raw_bytes_read
    @property
    def bytes_read(self):
        return self.__read_bytes

    @property
    def file_name(self):
        return self.__file_name

    def __check_required_arguments(self, required_args, opts):
        missing_args = []
        for arg in required_args:
            if arg not in opts:
                missing_args += arg

        if missing_args:
            # get the module name
            mod_name = opts[type]
            import sys
            for missing in missing_args:
                sys.stderr.write("Missing required argument '{0}' for decoder module '{1}'\n".format(missing, mod_name))
            raise TypeError("At least one missing argument in config.")

    def __parse_input_module_options(self, opts):
        self.__check_required_arguments(['filename'], opts)

        # open the raw file & see how big it is
        self.__file_name = opts['filename']
        self.__raw_file = open(self.__file_name, 'rb')
        self.__raw_file.seek(0,2) # seek to the end
        self.__raw_file_size = self.__raw_file.tell() # get the file size
        self.__raw_file.seek(0,0) # rewind back to the beginning

        # if we're using compression, allow for decompression
        self.__decomp_file = None
        if opts.get('compressed', False) is True:
            import gzip
            self.__decomp_file = gzip.GzipFile(None, None, None, self.__raw_file)

        # start the progbar
        if opts.get('progress', False) is True:
            from thirdparty.progressbar23.progressbar import Percentage, FileTransferSpeed, ETA, ProgressBar
#            from progressbar import Percentage, FileTransferSpeed, ETA, ProgressBar
            self.__pbar_widgets = [self.file_name, Percentage(), ' ', FileTransferSpeed(), ' ', ETA()]
            self.__pbar = ProgressBar(widgets=self.__pbar_widgets, maxval=self.__raw_file_size)
            self.__pbar.start()
        else:
            self.__pbar = None

    def __input_file(self):
        return self.__decomp_file or self.__raw_file

    def read_from_input_file(self, bytes):
        payload = self.__input_file().read(bytes)
        self.__read_bytes += bytes
        self.__raw_bytes_read = self.__raw_file.tell()
        # update the prog bar
        if self.__pbar is not None:
            self.__pbar.update(self.raw_bytes_read)
        return payload








