from decoder.field import BasicField, WireField, ComputedField, RepeatingGroup, LookupField, TrimmedString
from decoder.descriptor import Descriptor

from decoder.decoder import Decoder, Verbosity

from decoder.cta.constants import  InstrumentType, CancelErrorAction
from decoder.cta.types import TimeStamp, DecDiv, PriceDenominator
from decoder.cta.fields import FreeFormTextField


class Decoder(Decoder):
    """ cqs Decoder

    This decoder processes cqs packets.

    """

    def __parse_options(self, opts):
        self.showAdminMessages = bool(opts.get('show-admin-messages', False))
        self.showLineIntegrity = bool(opts.get('show-line-integrity-messages', False))

    def __init__(self, opts, next_decoder):
        super(Decoder, self).__init__('cta/cqs', opts, next_decoder)
        self.__parse_options(opts)
        # init summary data
        self.__frame_sequence = 0
        self.__decodingErrors = 0
        self.__unhandled_messages = {}
        self.__msg_counts = {}

        # init message segment descriptors
        self.__segmentDescriptors = {}
        self.__segmentDescriptors['MsgHeader'] = Descriptor([
            WireField('cqs-msg-cat', 'c'),
            WireField('cqs-msg-typ', 'c'),
            WireField('cqs-msg-network', 'c'),
            WireField('cqs-retran-requestor', '2s'),
            WireField('cqs-header-id', 'c'),
            WireField('resv', '2s', hidden=True),
            WireField('cqs-seq-num', '9s', type=long),
            WireField('cqs-participant-id', 'c'),
            WireField('cqs-timestamp', '6s')
        ])

        self.__segmentDescriptors['MsgHeaderExpansion'] = Descriptor([
            WireField('cqs-timestamp-1', '6s', type=TimeStamp()),
            WireField('cqs-timestamp-2', '6s', type=TimeStamp()),
            WireField('cqs-trans-id-part-b', '9s')
        ])
        """  TRADES
        """
        self.__segmentDescriptors['LongTrade'] = Descriptor([
            WireField('cqs-symbol', '11s', type=TrimmedString),
            WireField('cqs-temporary-suffix', 'c'),
            WireField('cqs-test-msg-indic', 'c'),
            WireField('cqs-trade-reporting-facility', 'c'),
            WireField('cqs-primary-listing-market', 'c'),
            WireField('resv', 'c', hidden=True),
            WireField('cqs-financial-status', 'c'),
            WireField('cqs-currency', '3s'),
            WireField('cqs-held-trade', 'c'),
            LookupField('cqs-inst-type', 'c', InstrumentType),
            WireField('cqs-seller-sale-days', '3s'),
            WireField('cqs-sale-condition', '4s'),
            WireField('cqs-trade-thru-exempt', 'c'),
            WireField('resv', '2s', hidden=True),
            WireField('cqs-price-denom', 'c', type=PriceDenominator, verbosity=Verbosity.Verbose),
            WireField('cqs-trade-price-unscaled', '12s', type=long, verbosity=Verbosity.Verbose),
            ComputedField('cqs-trade-price', DecDiv ('cqs-trade-price-unscaled', 'cqs-price-denom')),
            WireField('cqs-trade-volume', '9s', type=long),
            WireField('cqs-cons-high-low-last', 'c'),
            WireField('cqs-part-open-high-low-last', 'c'),
            WireField('resv', 'c', hidden=True),
            WireField('cqs-stop-stock', 'c'),
        ])

        self.__segmentDescriptors['ShortTrade'] = Descriptor([
            WireField('cqs-symbol', '3s', type=TrimmedString),
            WireField('cqs-sale-condition', 'c'),
            WireField('cqs-trade-volume', '4s'),
            WireField('cqs-price-denom', 'c', type=PriceDenominator, verbosity=Verbosity.Verbose),
            WireField('cqs-trade-price-unscaled', '8s', type=long, verbosity=Verbosity.Verbose),
            ComputedField('cqs-trade-price', DecDiv ('cqs-trade-price-unscaled', 'cqs-price-denom')),
            WireField('cqs-cons-high-low-last', 'c'),
            WireField('cqs-part-open-high-low-last', 'c'),
            WireField('resv', 'c', hidden=True),
        ])

        self.__segmentDescriptors['PriorDayTrade'] = Descriptor([
            WireField('cqs-trade-date', '6s'),
            WireField('resv', '2s', hidden=True),
            WireField('cqs-trade-time', '3s', type=TimeStamp()),
            WireField('cqs-symbol', '11s', type=TrimmedString),
            WireField('cqs-temporary-suffix', 'c'),
            WireField('cqs-financial-status', 'c'),
            WireField('cqs-currency', '3s'),
            WireField('cqs-trade-thru-exempt', 'c'),
            LookupField('cqs-inst-type', 'c', InstrumentType),
            WireField('cqs-seller-sale-days', '3s', type=int),
            WireField('cqs-sale-condition', '4s'),
            WireField('cqs-price-denom', 'c', type=PriceDenominator, verbosity=Verbosity.Verbose),
            WireField('cqs-trade-price-unscaled', '12s', type=long, verbosity=Verbosity.Verbose),
            ComputedField('cqs-trade-price', DecDiv ('cqs-trade-price-unscaled', 'cqs-price-denom')),
            WireField('cqs-trade-volume', '9s', type=long),
            WireField('cqs-stop-stock', 'c'),
            WireField('cqs-trade-reporting-facility', 'c'),
            WireField('cqs-primary-listing-market', 'c'),
            WireField('cqs-short-sale', 'c'),
            WireField('resv', '10s', hidden=True)
        ])


        self.__segmentDescriptors['PriorDayCancelError'] = Descriptor([
            WireField('cqs-symbol', '11s', type=TrimmedString),
            WireField('cqs-temporary-suffix', 'c'),
            WireField('cqs-financial-status', 'c'),
            WireField('cqs-currency', '3s'),
            LookupField('cqs-inst-type', 'c', InstrumentType),
            LookupField('cqs-cancel-error-action', 'c', CancelErrorAction),
            WireField('cqs-trade-reporting-facility', 'c'),
            WireField('cqs-primary-listing-market', 'c'),
            WireField('resv', '12s', hidden=True),
            WireField('cqs-prior-day-trade-date', '6s'),
            WireField('resv', '2s', hidden=True),
            WireField('cqs-prior-day-trade-time', '3s', type=TimeStamp()),
            WireField('cqs-sellers-sale-days', '3s'),
            WireField('cqs-sale-condition', '4s'),
            WireField('cqs-price-denom', 'c', type=PriceDenominator, verbosity=Verbosity.Verbose),
            WireField('cqs-trade-price-unscaled', '12s', type=long, verbosity=Verbosity.Verbose),
            ComputedField('cqs-trade-price', DecDiv ('cqs-trade-price-unscaled', 'cqs-price-denom')),
            WireField('cqs-trade-volume', '9s', type=long),
            WireField('cqs-stop-stock', 'c'),
            WireField('cqs-trade-thru-exempt', 'c'),
            WireField('cqs-short-sale-exempt', 'c'),
            WireField('resv', '11s', hidden=True)
        ])
            

        """ TRADING STATUS
        """
        self.__segmentDescriptors['TradingStatus'] = Descriptor([
            WireField('cqs-symbol', '11s', type=TrimmedString),
            WireField('cqs-temporary-suffix', 'c'),
            WireField('resv', '4s', hidden=True),
            WireField('cqs-financial-status', 'c'),
            WireField('cqs-currency', '3s'),
            LookupField('cqs-inst-type', 'c', InstrumentType),
            WireField('cqs-security-status', 'c'),
            WireField('cqs-halt-reason', 'c'),
            WireField('cqs-due-to-related-security-indicator', 'c'),
            WireField('cqs-in-view-of-common-indicator', 'c'),
            WireField('cqs-last-price-denom', 'c', type=PriceDenominator, verbosity=Verbosity.Verbose),
            WireField('cqs-last-price-unscaled', '12s', type=long, verbosity=Verbosity.Verbose),
            ComputedField('cqs-last-price', DecDiv ('cqs-last-price-unscaled', 'cqs-last-price-denom')),
            WireField('cqs-status-indicator', 'c'),
            WireField('cqs-high-price-denom', 'c', type=PriceDenominator, verbosity=Verbosity.Verbose),
            WireField('cqs-high-price-unscaled', '12s', type=long, verbosity=Verbosity.Verbose),
            ComputedField('cqs-high-price', DecDiv ('cqs-high-price-unscaled', 'cqs-high-price-denom')),
            WireField('cqs-low-price-denom', 'c', type=PriceDenominator, verbosity=Verbosity.Verbose),
            WireField('cqs-low-price-unscaled', '12s', type=long, verbosity=Verbosity.Verbose),
            ComputedField('cqs-low-price', DecDiv ('cqs-low-price-unscaled', 'cqs-low-price-denom')),
            WireField('resv', 'c', hidden=True),
            WireField('cqs-buy-volume', '9s', type=int),
            WireField('cqs-sell-volume', '9s', type=int),
            WireField('cqs-short-sale-restriction', 'c'),
            WireField('cqs-limit-up-limit-down', 'c'),
            WireField('resv', '4s', hidden=True)
        ])


        """ ADMIN
        """
        self.__segmentDescriptors['FreeFormText'] = Descriptor([
            FreeFormTextField('cqs-text')
        ])

        self.__segmentDescriptors['EmptyPayload'] = Descriptor([])

        """ SUMMARIES
        """
        self.__segmentDescriptors['ParticipantStartOfDaySummary'] = Descriptor([
            # general
            WireField('cqs-symbol', '11s', type=TrimmedString),
            WireField('cqs-temporary-suffix', 'c'),
            WireField('cqs-financial-status', 'c'),
            WireField('cqs-currency', '3s'),
            WireField('cqs-instrument-type', 'c'),
            WireField('resv', '11s', hidden=True),
            # consolidated data
            WireField('cqs-consolidated-participant-id', 'c'),
            WireField('cqs-consolidated-prev-close-price-denom', 'c', type=PriceDenominator, verbosity=Verbosity.Verbose),
            WireField('cqs-consolidated-prev-close-price-unscaled', '12s', verbosity=Verbosity.Verbose),
            ComputedField('cqs-consolidated-prev-close-price', DecDiv ('cqs-consolidated-prev-close-price-unscaled', 'cqs-consolidated-prev-close-price-denom')),
            WireField('cqs-consolidated-prev-close-price-date', '6s'),
            WireField('resv', '10s', hidden=True),
            # number of participant data iterations
            RepeatingGroup([
                # participant data
                WireField('cqs-participant-id', 'c'),
                WireField('cqs-participant-prev-close-price-denom', 'c', type=PriceDenominator),
                WireField('cqs-participant-prev-close-price-unscaled', '12s', verbosity=Verbosity.Verbose),
                ComputedField('cqs-participant-prev-close--price', DecDiv ('cqs-participant-prev-close-price-unscaled', 'cqs-participant-prev-close-price-denom')),
                WireField('cqs-participant-prev-close-price-date', '6s'),
                WireField('resv', '10s', hidden=True),
            ], RepeatingGroup.ReprCountFromPayload('2s')),
        ])

        self.__segmentDescriptors['ConsolidatedEndOfDaySummary'] = Descriptor([
            WireField('cqs-symbol', '11s', type=TrimmedString),
            WireField('cqs-temporary-suffix', 'c'),
            WireField('cqs-financial-status', 'c'),
            WireField('cqs-currency', '3s'),
            LookupField('cqs-instrument-type', 'c', InstrumentType),
            WireField('cqs-short-sale-restriction', 'c'),
            WireField('resv', '10s', hidden=True),
            WireField('cqs-last-participant-id', 'c'),
            WireField('cqs-last-price-denom', 'c', type=PriceDenominator),
            WireField('cqs-last-price-unscaled', '12s', verbosity=Verbosity.Verbose),
            ComputedField('cqs-last-price', DecDiv ('cqs-last-price-unscaled', 'cqs-last-price-denom')),
            WireField('cqs-prev-close-price', '6s'),
            WireField('cqs-high-price-denom', 'c', type=PriceDenominator),
            WireField('cqs-high-price-unscaled', '12s', verbosity=Verbosity.Verbose),
            ComputedField('cqs-high-price', DecDiv ('cqs-high-price-unscaled', 'cqs-high-price-denom')),
            WireField('cqs-low-price-denom', 'c', type=PriceDenominator),
            WireField('cqs-low-price-unscaled', '12s', verbosity=Verbosity.Verbose),
            ComputedField('cqs-low-price', DecDiv ('cqs-low-price-unscaled', 'cqs-low-price-denom')),
            WireField('cqs-total-volume', '11s', type=int),
            WireField('resv', '11s', hidden=True),
            WireField('cqs-num-participants', '2s', type=int)
        ])
            

        """  MWCB
        """
        self.__segmentDescriptors['MwcbDeclineLevelStatus'] = Descriptor([
            WireField('cqs-price-denom', 'c', type=PriceDenominator, verbosity=Verbosity.Verbose),
            WireField('cqs-level-1-price-unscaled', '12s', verbosity=Verbosity.Verbose),
            ComputedField('cqs-level-1-price', DecDiv('cqs-level-1-price-unscaled', 'cqs-price-denom')),
            WireField('resv', '3s', hidden=True),
            WireField('cqs-level-2-price-unscaled', '12s', verbosity=Verbosity.Verbose),
            ComputedField('cqs-level-2-price', DecDiv ('cqs-level-2-price-unscaled', 'cqs-price-denom')),
            WireField('resv', '3s', hidden=True),
            WireField('cqs-level-3-price-unscaled', '12s',verbosity=Verbosity.Verbose),
            ComputedField('cqs-level-3-price', DecDiv ('cqs-level-3-price-unscaled', 'cqs-price-denom')),
            WireField('resv', '3s', hidden=True)
        ])

        """ MARKET STATUS
        """
        self.__segmentDescriptors['StartOfMostActiveIssues'] = Descriptor([
            WireField('cqs-number-of-most-active-issues', 'H', type=int)
        ])

        self.__segmentDescriptors['ClosingTradePrices'] = Descriptor([
            WireField('cqs-symbol', '11s', type=TrimmedString),
            WireField('cqs-temporary-suffix', 'c'),
            WireField('cqs-trade-volume', '11s', type=int),
            WireField('cqs-open-price-denom', 'c', type=PriceDenominator),
            WireField('cqs-open-price-unscaled', '12s', verbosity=Verbosity.Verbose),
            ComputedField('cqs-open-price', DecDiv ('cqs-open-price-unscaled', 'cqs-open-price-denom')),
            WireField('cqs-high-price-denom', 'c', type=PriceDenominator),
            WireField('cqs-high-price-unscaled', '12s', verbosity=Verbosity.Verbose),
            ComputedField('cqs-high-price', DecDiv ('cqs-high-price-unscaled', 'cqs-high-price-denom')),
            WireField('cqs-low-price-denom', 'c', type=PriceDenominator),
            WireField('cqs-low-price-unscaled', '12s', verbosity=Verbosity.Verbose),
            ComputedField('cqs-low-price', DecDiv ('cqs-low-price-unscaled', 'cqs-low-price-denom')),
            WireField('cqs-last-price-denom', 'c', type=PriceDenominator),
            WireField('cqs-last-price-unscaled', '12s', verbosity=Verbosity.Verbose),
            ComputedField('cqs-last-price', DecDiv ('cqs-last-price-unscaled', 'cqs-last-price-denom')),
            WireField('cqs-net-change-tick', 'c'),
            WireField('cqs-net-change-denom', 'c', type=PriceDenominator),
            WireField('cqs-net-change-unscaled', '12s', verbosity=Verbosity.Verbose),
            ComputedField('cqs-net-change', DecDiv ('cqs-net-change-unscaled', 'cqs-net-change-denom')),
            WireField('cqs-resv', 'c', hidden=True),
            WireField('cqs-financial-status', 'c'),
            WireField('cqs-short-sale-restriction', 'c'),
            WireField('cqs-resv', 'c', hidden=True)
        ])
        self.__segmentDescriptors['MostActiveIssues'] = Descriptor([
            WireField('cqs-symbol', '11s', type=TrimmedString),
            WireField('cqs-temporary-suffix', 'c'),
            WireField('cqs-trade-volume', '11s', type=int),
            WireField('cqs-open-price-denom', 'c', type=PriceDenominator),
            WireField('cqs-open-price-unscaled', '12s', verbosity=Verbosity.Verbose),
            ComputedField('cqs-open-price', DecDiv ('cqs-open-price-unscaled', 'cqs-open-price-denom')),
            WireField('cqs-high-price-denom', 'c', type=PriceDenominator),
            WireField('cqs-high-price-unscaled', '12s', verbosity=Verbosity.Verbose),
            ComputedField('cqs-high-price', DecDiv ('cqs-high-price-unscaled', 'cqs-high-price-denom')),
            WireField('cqs-low-price-denom', 'c', type=PriceDenominator),
            WireField('cqs-low-price-unscaled', '12s', verbosity=Verbosity.Verbose),
            ComputedField('cqs-low-price', DecDiv ('cqs-low-price-unscaled', 'cqs-low-price-denom')),
            WireField('cqs-last-price-denom', 'c', type=PriceDenominator),
            WireField('cqs-last-price-unscaled', '12s', verbosity=Verbosity.Verbose),
            ComputedField('cqs-last-price', DecDiv ('cqs-last-price-unscaled', 'cqs-last-price-denom')),
            WireField('cqs-net-change-tick', 'c'),
            WireField('cqs-net-change-denom', 'c', type=PriceDenominator),
            WireField('cqs-net-change-unscaled', '12s', verbosity=Verbosity.Verbose),
            ComputedField('cqs-net-change', DecDiv ('cqs-net-change-unscaled', 'cqs-net-change-denom')),
            WireField('cqs-resv', 'c', hidden=True),
            WireField('cqs-financial-status', 'c'),
            WireField('cqs-short-sale-restriction', 'c'),
            WireField('cqs-resv', 'c', hidden=True)
        ])
        # Init message detail dict
        import string
        ltrs = string.uppercase
        self.__msgDetail = {}
        # Admin messages (cat A)
        self.__msgDetail['AA'] = ("StartOfEndOfDaySummary", 'EmptyPayload', True)
        self.__msgDetail['AB'] = ("EndOfEndOfDaySummary", 'EmptyPayload', True)
        self.__msgDetail['AC'] = ("StartOfStartOfDaySummary", 'EmptyPayload', True)
        self.__msgDetail['AD'] = ("EndOfStartOfDaySummary", 'EmptyPayload', True)
        self.__msgDetail['AH'] = ("AdminMessage", 'FreeFormText', self.showAdminMessages)
        # Bond messages (cat B)
        self.__msgDetail['BB'] = ("BondLongTrade", 'LongTrade', True)
        self.__msgDetail['BF'] = ("BondTradingStatus", 'TradingStatus', True)
        self.__msgDetail['BI'] = ("BondShortTrade", 'ShortTrade', True)
        self.__msgDetail['BJ'] = ("BondPriorDay", 'PriorDayTrade', True)
        self.__msgDetail['BO'] = ("BondStartOfDaySummary", 'StartOfDaySummary', True)
        # Control messages (cat C)
        self.__msgDetail['CI'] = ("StartOfDay", 'EmptyPayload', True)
        self.__msgDetail['CL'] = ("ResetMessageSequenceNumber", 'EmptyPayload', True)
        self.__msgDetail['CM'] = ("StartTestCycle", 'EmptyPayload', self.showLineIntegrity)
        self.__msgDetail['CN'] = ("EndTestCycle", 'EmptyPayload', self.showLineIntegrity)
        self.__msgDetail['CT'] = ("LineIntegrity", 'EmptyPayload', self.showLineIntegrity)
        self.__msgDetail['CZ'] = ("EndOfTransmission", 'EmptyPayload', True)
        # Listed Equity messages (cat E)
        self.__msgDetail['EB'] = ("EquityLongTrade", 'LongTrade', True)
        self.__msgDetail['EF'] = ("EquityTradingStatus", 'TradingStatus', True)
        self.__msgDetail['EI'] = ("EquityShortTrade", 'ShortTrade', True)
        self.__msgDetail['EJ'] = ("EquityPriorDay", 'PriorDayTrade', True)
        self.__msgDetail['EL'] = ("EquityPriorDayCancelError", 'PriorDayCancelError', True)
        self.__msgDetail['EO'] = ("EquityParticipantStartOfDaySummary", 'ParticipantStartOfDaySummary', True)
        self.__msgDetail['ES'] = ("EquityConsolidatedEndOfDaySummary", 'ConsolidatedEndOfDaySummary', True)
        # Local Issue messages (cat L)
        # Market Summary messages (cat M)
        self.__msgDetail['MB'] = ("StartOfMostActiveIssues", 'StartOfMostActiveIssues', True)
        self.__msgDetail['MC'] = ("MostActiveIssues", 'MostActiveIssues', True)
        self.__msgDetail['MD'] = ("EndOfMostActiveIssues", 'EmptyPayload', True)
        self.__msgDetail['ME'] = ("StartOfClosingTradePrices", 'EmptyPayload', True)
        self.__msgDetail['MF'] = ("ClosingTradePrices", 'ClosingTradePrices', True)
        self.__msgDetail['MG'] = ("EndOfClosingTradePrices", 'EmptyPayload', True)
        self.__msgDetail['MK'] = ("MwcbDeclineLevelStatus", 'MwcbDeclineLevelStatus', True)
        # Index mesages (cat Y)


    def isWireField(self, fieldName):
        NON_WIRE_PREFIX = [
            '!', # calculated field
            '@'  # payload field
        ]

        return fieldName[0] not in NON_WIRE_PREFIX

    def on_message(self, inputContext, inPayload):
        """  Process CTA Packet

        :rtype : none
        :param context: Message context build by preceding link in decoder chain
        :param payload: Message payload
        """

        self.__frame_sequence += 1

        # split the incoming payload in to multiple messages
        dividers = [
            # SOH
            0x01,
            # US
            0x1f,
            # ETX
            0x03
            ]

        payloads = []
        for c in inPayload:
            co = ord(c)
            if co in dividers:
                payloads.append("")
            else:
                payloads[-1] += c
        payloads.pop(-1)    # the last element should just be and empty string because of the trailing ETX, so dump it

        # parse each message in the payload
        for payload in payloads:
            # decode the common header
            headers, payload = self.decode_segment(self.__segmentDescriptors['MsgHeader'], payload)
            if len(headers) is not 1:
                sys.stderr.write("ERROR: CTA common header decoded in to {0} bodies\n".format(len(commonHeaders)))
                self.__decodingErrors += 1
                return

            header = headers[0]
            header.update({'$frame-sequence': self.__frame_sequence})
            header['cqs-msg-type'] = header['cqs-msg-cat']+header['cqs-msg-typ']

            # decode the message body, if we can
            msgTypeCode = header['cqs-msg-type']
            self.__msg_counts[msgTypeCode] = self.__msg_counts.get(msgTypeCode, 0) + 1

            processThisMessage = True
            messages = None
            if msgTypeCode not in self.__msgDetail:
                self.__unhandled_messages[msgTypeCode] = self.__unhandled_messages.get(msgTypeCode, 0) + 1
                if self.verbosity() >= Verbosity.Verbose:
                    print 'Unhandled MsgType: {0} Decoded context: {1}, Remaining Payload: {2}'.format(msgTypeCode, commonHeaderContext, self.toHex(payload))
            else:
                # decode the message. decodedMessages ends up being an array of decoded contexts
                msgDetail = self.__msgDetail[msgTypeCode]
                msgIsFilteredOut = not msgDetail[2]
                if not msgIsFilteredOut:
                    messageDesc = self.__segmentDescriptors[msgDetail[1]]
                    if messageDesc:
                        # decode non-empty payloadsp
                        messages, payload = self.decode_segment(messageDesc, payload)

                        for message in messages:
                            context = dict()
                            context.update(inputContext)
                            context.update(header)
                            context.update(message)
                            context.update ({'cqs-msg-type-name': msgDetail[0]})
                            self.dispatch_to_next(context,payload)

    def summarize(self):
        """ Provides summary statistics from this Decoder
        """
        return {
            'UnhandledMsgTypeCodes': self.__unhandled_messages,
            'TotalFramesReceived': self.__frame_sequence,
            'MsgTypeCounts': self.__msg_counts
        }


