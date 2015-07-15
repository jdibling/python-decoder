from base.exceptions import *
from base.verbosity import Verbosity
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

    def __parse_basic_options (self, opts):
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
        self.__compression_format = opts.get('compression', None)

    def __init__(self, kind, opts, next_decoder):
        self.__parse_basic_options(opts)
        self.kind = kind
        self.next = next_decoder

    def verbosity(self):
        return self.__verbosity
    def verbose(self):
        return self.verbosity() == Verbosity.Verbose
    def compression(self):
        if self.__compression_format is None:
            return None
        return self.__compression_format.lower()

    def open_file(self, fileName):
        # open the file accounting for whatever compression
        return {
            None: open(fileName, 'rb'),
            'gzip':  gzip.open(fileName, 'rb')
        }[self.compression()]


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
          gap-checking on an ArcaXDBBBO pcapng file, there are three links
          in the chain:

              1)  A pcapng decoder
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
        if self.next is not None:
            self.next.on_message(context, payload)
