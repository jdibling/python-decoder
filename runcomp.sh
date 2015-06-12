#!/bin/bash

echo "decoding ingress & egress files..."
outdir=/tmp/

in_file="$outdir/ingress-auto.txt"
out_file="$outdir/egress-auto.txt"

echo -e $in_config > $outdir/ingress-auto.conf

echo "Decoded ingress file: $in_file"
echo "Decoded egress file: $out_file"

echo "Forking ingress decoder..."
./decode.py ingress-auto.conf & pid_in_decode=$!
echo "pid=$pid_in_decode"

echo "Forking egress decoder..."
./decode.py egress-auto.conf & pid_eg_decode=$!
echo "pid=$pid_eg_decode"

wait
echo "Decoding complete..."

echo "Sorting results..."
sort -n -k2 -t',' /tmp/ingress-auto.txt > /tmp/ingress-auto-sorted.txt
sort -n -k2 -t',' /tmp/egress-auto.txt > /tmp/egress-auto-sorted.txt

echo "Joining results..."
join -1 1 -2 2 -t',' /tmp/ingress-auto-sorted.txt /tmp/egress-auto-sorted.txt > /tmp/joined-auto.txt

echo "Computing differences..."
echo "SeqNum,IngressRecv,EgressRecv,RecvDelta" > /tmp/joined-diff-auto.txt
awk 'BEGIN {FS = ","} {printf "%d,%f,%f,%1.6f\n", $1, $2, $3, $3-$2 }' /tmp/joined-auto.txt >> /tmp/joined-diff-auto.txt

echo "Plotting histogram..."
./lat.py -f /tmp/joined-diff-auto.txt -c 3 -g -n 100 -t "Latency: INET in to MDPacket out"
