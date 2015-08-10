#!/usr/bin/python

import sys
from decoder._version import __version__
from decoder.pipeline import Pipeline

if __name__ == '__main__':
    print "Decoder version {0}".format(__version__)
    if len(sys.argv) < 2:
        print "***ERROR*** No config file specified."
        sys.exit(1)

    app = Pipeline()
    app.run(sys.argv[1])

    print 'Finished'






