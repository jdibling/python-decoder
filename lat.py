#!/usr/bin/python
from __future__ import division
import sys
import numpy
import argparse
from numpy import *

from dateutil import tz

# dependencies:  python-argparse 

def nonblank_lines(f):
  for l in f:
    line = l.rstrip()
    if line:
      yield line

parser = argparse.ArgumentParser()

skipFirst = True
first = True

parser.add_argument('-v', dest='verbose', action='store_true', help="Verbose output")
parser.add_argument('-x', dest='filter', help="filter latencies higher that this as bad samples", default=sys.maxint)
parser.add_argument('-f', dest='sourceFile', help="source latency file", default="ticks.csv")
parser.add_argument('-g', dest='histogram', action='store_true', help="show histogram", default=False)
parser.add_argument('-n', dest='bins', help="number of bins in histogram", default=10) 
parser.add_argument('-t', dest='title', help="Histogram Title", default="Untitled")
parser.add_argument('-c', dest='col', help="Column number to extract", default=None)
# parser.add_argument('-s', dest='skipFirst', help='Skip first row in result set', default=False)
args = parser.parse_args()

posLats = []
negLats = []

with open(args.sourceFile) as f:
  for line in nonblank_lines(f):
    if skipFirst and first:
      first = False
      continue;

    toks = line.split(",")
    print len(toks)
    curr = float(toks[int(args.col)])
    if curr >= 0:
	posLats.append(curr)
    else:
	negLats.append(curr)
    if args.verbose:
        print '{0}'.format(curr)

print "### POSITIVE VALUES ###"
if(len(posLats) > 1):
  npNums = numpy.array(posLats)

  pctBins = []
  for pct in [99, 99.9, 99.99, 99.999, 99.9999]:
    pctBins.append((pct, numpy.percentile(npNums, pct)))

  print "   mean =", npNums.mean()
  print " median =", numpy.median(npNums)
  for (pct, lat) in pctBins:
    print '  {0}%:\t{1}'.format(pct, lat)

  print " 50%     ", numpy.percentile(npNums, 50)
  print " stdDev =", npNums.std()
  print "    min =", npNums.min()
  print "    max =", npNums.max()
  print "  count =", len(npNums)
  print "dropped =", dropped

  if args.histogram == True: 
    import matplotlib.pyplot as plt
    plt.hist(npNums, bins=int(args.bins))
    plt.title(args.title);
    plt.xticks(range(0,npNums.max(),50))
    count = 0;
    colors = ['g','r','c','m','y']

    for (pct, lat) in pctBins:
      ypos = len(npNums)-((len(npNums)/10)*count)
      color = colors[count]
      plt.annotate('{0}%\n{1} mics'.format(pct, int(lat)), xy=(lat,ypos), color=color)
      plt.vlines(lat, 0, len(npNums), linestyles=u'dashed', color=color)
      count += 1
    plt.xlabel('Microseconds')
    plt.ylabel('Count')
    plt.show()

else:
  print "Unable to locate any samples that match the request."

