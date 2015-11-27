from __future__ import absolute_import

import os.path
import datetime
import decoder.types
from decoder.module import *
from decoder.exceptions import LinkInitError
import json
import sys
from decoder.util import *
import os
import gzip

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decoder.types.HexArray):
            return obj.__str__()
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y%m%d-%H:%M:%S.%f')
        return json.JSONEncoder.default(self, obj)

def mark_file_done(file_name):
    if file_name.endswith('.tmp'):
        os.rename(file_name, file_name.rstrip('.tmp'))

def finalize_file(file):
    file.flush()
    name = file.name
    file.close()
    mark_file_done(name)

class Decoder(BasicModule):
    def __init__(self, opts, next_decoder):
        print "json.dump(1)"
        super(Decoder, self).__init__('json', opts, next_decoder)
        self.__parse_options(opts)
        self.msg_type_counts = {}

    def __finalize_files(self):
        if self.separate_by_channel:
            for f in self.out_files:
                finalize_file(self.out_files[f])
        else:
            finalize_file(self.out_file)

    def __parse_options(self, opts):
        # Get the output file
        out_filename = opts.get('filename', None)
        self.compressed = (opts.get('compress', False) == True) or (opts.get('compressed', False) == True)

        self.separate_by_channel = bool(opts.get('separate-by-channel', False))
        if self.separate_by_channel:
            self.out_files = {}
            self.root = str(opts.get('output-root', "normalized"))
            self.venue = str(opts.get('output-venue', 'ice'))
            self.date = str(opts.get('output-date'))
            self.time = str(opts.get('output-time'))

        elif out_filename is not None:
            out_filename = os.path.abspath(out_filename)
            if not os.path.isdir(os.path.dirname(out_filename)):

                print "***ERROR***: "\
                    "In json config, filename path does not exist. "\
                    "Path: {0}"\
                    .format(os.path.dirname(out_filename))
                exit(2)

            # if we're compressing...
            if (self.compressed):
                self.out_file = gzip.open(out_filename, 'w')
            else:
                self.out_file = open(out_filename, 'w')
        else:
            self.out_file = sys.stdout
        # See if we're squelching keys
        self.squelch_key = bool(opts.get('squelch-keys', False))
        self.show_remaining = bool(opts.get('show-remaining-payload', False))
        self.suffix = opts.get('suffix', '')

        # Process any filters
        self.excludeAll = False
        self.inclusions = []
        self.exclusions = []

        filters = opts.get('filter', '').split()
        for filt in filters:
            op = str(filt[0])
            key = ''
            for ix, c in enumerate(filt[1:]):
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

    def open_channel_file(self, channel):
        ip = bytesToAddr(channel)
        ip = ip.replace(":", "-")
        file = self.date + "-" + self.time + self.suffix + ".json"
        out_filename = os.path.join(self.root, "json", self.venue, self.date, ip, file)
        if not os.path.exists(os.path.dirname(out_filename)):
            os.makedirs(os.path.dirname(out_filename))
        if self.compressed:
            out_filename += ".gz.tmp"
            self.out_file = gzip.open(out_filename, 'w')
        else:
            out_filename += ".tmp"
            self.out_file = open(out_filename, 'wb')
        return self.out_file

    def on_message(self, context, payload):
        """ Dump all processed packets in json
        """
        if len(payload):
            if self.show_remaining:
                context['remaining-payload'] = self.toHex(payload)

        if self.separate_by_channel:
            channel_id = context['pcap-udp-stream-id']
            self.out_file = self.out_files.get(channel_id, None)
            if self.out_file is None:
                print "making new file ", channel_id
                self.out_file = self.open_channel_file(channel_id)
                self.out_files[channel_id] = self.out_file
        #json.dump(context, self.out_file, cls=CustomEncoder)
        print >>self.out_file, json.dumps(context, cls=CustomEncoder)

        self.dispatch_to_next(context, payload)

    def stop(self):
        # send the stop up the chain first
        super(Decoder, self).stop()
        self.__finalize_files()

    def summarize(self):
        return dict()


