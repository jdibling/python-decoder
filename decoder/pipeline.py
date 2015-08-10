import yaml
import os.path
import sys
import traceback
import signal
import collections
import importlib
from .exceptions import *


def reject_key(d, key):
    """Returns a copy of the dictionary with the specified key removed
    :rtype : dictionary
    """
    ret = dict(d)
    del ret[key]
    return ret


class Pipeline(object):
    """decoder main class"""
    def __init__(self):
        """constructor"""
        self.decoders = []
        self.options = {}
        self.enable_debugging = True
        self.interrupted = False
        self.verbose = False
        self.show_summary = True

    def signal_handler(self, signal, frame):
        self.interrupted = True
        raise InterruptException()

    def run(self, config_filepath):
        """ Run the main application
        :return: none
        :rtype: none
        """
        try:
            signal.signal(signal.SIGINT, self.signal_handler)
            self.parse_config(config_filepath)    # Loads global options & initializes the decoders
            print "*** RUNNING ***"
            self.decoders[0].start()  # Returns when run complete or interrupted

            if self.interrupted:
                print '*** RUN INTERRUPTED ***'
            else:
                print '*** RUN COMPLETE ***'
            # Collect & print a run summary if configured to do so
            if self.show_summary is True:
                summary = collections.OrderedDict()
                print "summarizing"
                for dec in self.decoders:
                    print "summarizing {0}".format(str(dec))
                    summary.update(dec.summarize())
                print 'Run Summary:'
                for stat in summary.keys():
                    print '\t{0}: {1}'.format(stat, summary[stat])
            self.decoders[0].stop()
        except LinkInitError as ex:
            sys.stderr.write("***ERROR***\n")
            sys.stderr.write('An error occurred while initializing a decoder module.\n')
            sys.stderr.write('Error: "{0}"\n'.format(str(ex)))
            sys.stderr.write('Program will terminate.  Correct above errors and try again.\n ')

        except Exception as ex:
            if self.enable_debugging:
                # If debug mode is enabled, print out the full context in which
                # the exception occurred and present a PDB console
                # to enable looking around
                import traceback
                import pdb

                print 'V' * 20
                print 'Exception of type {0} occured.  Arguments: {1}'.format (
                    type (ex), ex.args)

                print 'Traceback:'
                print traceback.format_exc ()

                pdb.post_mortem ()
                print '^' * 20
            else:
                lines = []
                lines.append('***ERROR***\n')
                lines.append('An error occurred while processing.  Program will terminate.\n')
                lines.append('To enable full fidelity of errors, set the "debug" global option to True in your '
                             'config file.\n')
                sys.stderr.writelines(lines)
                raise ex

    def parse_config(self, config_filepath):
        # Find & Load the config
        if not os.path.exists(config_filepath):
            print "*** ERROR*** Config file '{0}' not found.".\
                format(config_filepath)
            sys.exit(2)

        # Parse global configs
        conf = open(config_filepath)
        options = yaml.safe_load(conf)

        self.verbose = options.get('verbose', False)
        self.show_summary = options.get('show-summary', True)
        self.enable_debugging = options.get('debug', False)

        # Create the decoder chain
        for dec in options['decoders']:
            dec_type = dec['type']
            options = reject_key(dec, 'type')
            if self.verbose:
                print "Initialized Decoder: ",\
                    dec_type, "Options: ", options

            package = ".".join(['decoder'] + dec_type.split("/"))
            lib = importlib.import_module(package)

            dec = lib.Decoder(options, None)
            if self.decoders:
                self.decoders[-1].next = dec
            self.decoders.append(dec)

        if self.verbose:
            print 'Initialized decoder chain: {0}'.format(
                str(self.decoders[0]))
            print 'Decoder chain links: {0}'.format(
                len(self.decoders))







