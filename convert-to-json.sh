#!/bin/bash

DECODER_ROOT=/home/rkulseth/stash/decoder
DECODER_CONFIG=/etc/pico/ice.conf
ZIP_TOOL=gzip


pypy $DECODER_ROOT/decode.py $DECODER_CONFIG | $ZIP_TOOL > /mnt/t5gv0/picoraw/solar_capture.p2p2.20150630-171306.json.gz 
