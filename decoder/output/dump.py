import os.path

import decoder.decoder
from decoder.decoder import Verbosity
from decoder.exceptions import LinkInitError


class Decoder(decoder.decoder.Decoder):
    def __init__(self, opts, next_decoder):
        super(Decoder, self).__init__('dump', opts, next_decoder)
        self.out_file = None
        self.__parse_options(opts)
        self.msg_type_counts = {}
            
    def __parse_options(self, opts):
        # Get the output file
        out_filename = opts.get('filename', None)
        if out_filename is not None:
            out_filename = os.path.abspath(out_filename)
            if not os.path.isdir(os.path.dirname(out_filename)):

                print "***ERROR***: "\
                    "In dump config, filename path does not exist. "\
                    "Path: {0}"\
                    .format(os.path.dirname(out_filename))
                exit(2)

            # if we're compressing...
            if (opts.get('compress', False) == True) or (opts.get('compressed', False) == True):
                import gzip
                self.out_file = gzip.open(out_filename, 'w')
            else:
                self.out_file = open(out_filename, 'w')

        # See if we're squelching keys
        self.squelch_key = bool(opts.get('squelch-keys', False))
        self.show_remaining = bool(opts.get('show-remaining-payload', False))

        # Process any filters
        self.excludeAll = False
        self.inclusions = []
        self.exclusions = []

        filters = opts.get('filter', '').split()
        for filter in filters:
            op = str(filter[0])
            key = ''
            for ix, c in enumerate(filter[1:]):
                if c == '_':
                    key += '-'
                else:
                    key += c.lower()

            if key == '*':
                # special handling for wildcard
                self.excludeAll = op == '-'
            elif op == '-':
                self.exclusions.append(key)
            elif op == '+':
                self.inclusions.append(key)

        self.sortByKey = bool(opts.get('sort-by-key', False))

    def on_message(self, context, payload):
        """ Dump all processed packets in human-readable fomat
        """
        values = []

        if len(payload):
            if self.show_remaining:
                context['remaining-payload'] = self.toHex(payload)

        if self.sortByKey:
            keyList = sorted(context.keys())
        else:
            keyList = context.keys()

        for key in keyList:
            if key[0] == '$' or key[0] == '#':
                continue

            excluded = self.excludeAll

            if key in self.exclusions:
                excluded = True
            if key in self.inclusions:
                excluded = False

            if not excluded:
                if not self.squelch_key:
                    values.append('{0}={1}'.format(key, context[key]))
                else:
                    values.append('{0}'.format(context[key]))

        if len(values):
            line = ','.join(values)
            if self.out_file is not None and len(line) > 0:
                self.out_file.write('{0}\n'.format(line))
                self.out_file.flush()
                if self.verbosity() >= Verbosity.Verbose:
                    print line
            else:
                print line

        self.dispatch_to_next(context, payload)

    def stop(self):
        # send the stop up the chain first
        super(Decoder, self).stop()
        if self.out_file is not None:
            self.out_file.flush()
            self.out_file.close()
            self.out_file = None

    def summarize(self):
        return dict()


