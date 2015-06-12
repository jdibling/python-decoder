import os.path
from sys import exit
import decimal

import decoder.base


class Decoder(decoder.base.Base):
    """  gap-check meta decoder

            gap-check is a meta-decoder that finds sequence gaps
            in a stream.  Gaps are identified as they are found,
            and printed to stdout.  There's also an option to write
            a file with every gapped packet.  That file will contain
            the msg sequence number that was gapped, along with the
            timstamp of the next packet we got.  (We have no way
            of knowing what time a packet was sent if we never got
            it.  ha ha)

            A "meta-decocer" is a class that implements the
            Decoder interface, but it doesn't actually process
            raw data.

            Instead, it's intended to be the last link in the
            decoder chain, and compute some statistics gathered
            from the links before it.
    """

    def __init__(self, opts, next_decoder):
        super(Decoder, self).__init__('gap-check', next_decoder)
        self.opts = opts
        self.last_packet = None  # last packet seen, used to detect gaps
        self.ttl_processed = 0  # total messages processed
        self.ttl_gapped = 0  # total packets gtapped
        self.gaps_file = None  # file to write all gaps to (optional, enabled with 'gaps-file')
        self.__process_options()

    def __process_options(self):
        gaps_filename = self.opts.get('gaps-file', None)
        if gaps_filename is not None:
            gaps_filename = os.path.abspath(gaps_filename)
            if not os.path.isdir(os.path.dirname(gaps_filename)):
                print "***ERROR***: "\
                    "In gap-check config, gaps-filename path does not exist. "\
                    "Path: {0}"\
                    .format(os.path.dirname(gaps_filename))
                exit(2)
            self.gaps_file = open(gaps_filename, 'w')

    def on_message(self, context, payload):
        """
        :param context:  message processed by preceding link in decoder chain
        :type context:  dictionary
        :param payload: remaining unprocessed bytes in message
        :type payload:  string
        :return: none
        :rtype:  none
        """
        if 'msg-seq-num' not in context:
            return

        msg_seq_num = context['msg-seq-num']
        expected_seq_num = None

        # Compute the expected next sequence number by looking
        # at the seqnum of the last message we got.
        # If we've never gotten a message before, assume
        # we're gap-free. :)
        if self.last_packet is not None:
            expected_seq_num = self.last_packet['msg-seq-num'] + 1

        # If there is a gap, report how many packets were lost and at what time
        if (expected_seq_num is not None) and (expected_seq_num != msg_seq_num):
            cur_time = context['recv-timestamp']
            gapped = msg_seq_num - expected_seq_num
            self.ttl_gapped += gapped

            print '*SEQUENCE GAP* lost {0} packets at {1}'.format(
                gapped, str(cur_time))
            if self.gaps_file is not None:
                for gap in range(expected_seq_num, msg_seq_num):
                # print '*GAP*\t{0}: {1}'.format(gap, str(cur_time))
                    self.gaps_file.write('msg-seq-num={0},time={1}\n'.format(gap, str(cur_time)))
                self.gaps_file.flush()



        # Update summary stats
        self.ttl_processed += 1
        self.last_packet = dict(context)

    # print '\t{0}'.format(msg_seq_num)

    def summarize(self):
        return {
            'gapcheck-ttl-messages': self.ttl_processed,
            'gapcheck-ttl-gaps': self.ttl_gapped,
            'gapcheck-pct-gaps': '{0:.5f}%'.format(
                (decimal.Decimal(self.ttl_gapped) / decimal.Decimal(self.ttl_processed))
            )
        }




