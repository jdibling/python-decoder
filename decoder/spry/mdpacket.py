from decoder.spry.mdpacketmsg.segments import *
from struct import unpack_from, calcsize
import traceback
import decimal

from decoder.field import BasicField, WireField, ComputedField, RepeatingGroup, TrimmedString
from decoder.descriptor import Descriptor

from decoder.module import *


def toHex (x):
    return ' '.join ([hex (ord (c))[2:].zfill (2) for c in x])


def toCHex (x):
    return ", ".join ([hex (ord (c)) for c in x])

from decoder.spry.fids import Fids
from decoder.spry.field_types import FieldTypeNames, FieldTypes
from decoder.spry.transaction_types import TransactionTypes, TransactionTypeNames

def bin(x, b=1):
    return ''.join(x & (1 << i) and '1' or '0' for i in range((8*b)-1,-1,-1))

FidNames = dict([(v,k) for (k,v) in Fids.items()])

NativeTypes = {
    FidNames['sku']: FieldTypeNames['sku'],

    FidNames['last']: FieldTypeNames['price'],
    FidNames['open']: FieldTypeNames['price'],
    FidNames['high']: FieldTypeNames['price'],
    FidNames['low']: FieldTypeNames['price'],
    FidNames['bid']: FieldTypeNames['price'],
    FidNames['ask']: FieldTypeNames['price'],
    FidNames['best-bid']: FieldTypeNames['price'],
    FidNames['best-ask']: FieldTypeNames['price'],
    FidNames['ice-bid']: FieldTypeNames['price'],
    FidNames['ice-ask']: FieldTypeNames['price'],

    FidNames['last-size']: FieldTypeNames['uint32'],
    FidNames['bid-size']: FieldTypeNames['uint32'],
    FidNames['ask-size']: FieldTypeNames['uint32'],
    FidNames['ice-bid-size']: FieldTypeNames['uint32'],
    FidNames['ice-ask-size']: FieldTypeNames['uint32'],
    FidNames['best-bid-size']: FieldTypeNames['uint32'],
    FidNames['best-ask-size']: FieldTypeNames['uint32'],
    FidNames['transaction-type']: FieldTypeNames['uint32'],
    FidNames['transaction-sequence']: FieldTypeNames['uint32'],
    FidNames['source-content']: FieldTypeNames['uint32'],
    FidNames['entitlement']: FieldTypeNames['uint32'],
    FidNames['volume']: FieldTypeNames['uint32']
}

def GetNativeType(fieldId):
    return NativeTypes[fieldId]

class Decoder(BasicModule):
    """ MDPacket processor

    """

    def __init__(self, opts, next_decoder):
        try:
            super(Decoder, self).__init__('spry/mdpacket', opts, next_decoder)
            self.__parseOptions(opts)
            self.__packetCount = 0
            self.__packetTransactions = {}

            """ Initialize the FID header decoder jump table
            """
            self.fieldHeaderJumpTable = [self.__decodeFidHeaderUndefined for n in range (0,16)]

            self.fieldHeaderJumpTable[0] = self.__decodeFidHeaderCompact
            self.fieldHeaderJumpTable[1] = self.__decodeFidHeaderShort
            self.fieldHeaderJumpTable[2] = self.__decodeFidHeaderLong

            """  Initialize the FID body decoder jump table
            """
            self.fieldBodyJumpTable = [self.__decodeFieldBodyUndefined for n in range (0,1024)]

            self.fieldBodyJumpTable[FieldTypeNames['uint32']] = self.__decodeFieldBodyUInt32
            self.fieldBodyJumpTable[FieldTypeNames['uint64']] = self.__decodeFieldBodyUInt64
            self.fieldBodyJumpTable[FieldTypeNames['entitlement']] = self.__decodeFieldBodyUInt32
            self.fieldBodyJumpTable[FieldTypeNames['source-content']] = self.__decodeFieldBodyUInt32
            self.fieldBodyJumpTable[FieldTypeNames['sku']] = self.__decodeFieldBodySku
            self.fieldBodyJumpTable[FieldTypeNames['order-sku']] = self.__decodeFieldBodyOrderSku
            self.fieldBodyJumpTable[FieldTypeNames['price']] = self.__decodeFieldBodyPrice

            """ Initialize the value-decoder lookup table
                This is used to re-interpret the value that was decoded
                by FieldType.  We will use a different dictionary object that
                maps value to a human-readable string; there will be one of
                these dictionaries for each FID that can be re-interpreted.
                If there is no such dictionary for a given FID, then
                no re-interpretation takes place
            """
            self.fieldValueTranslationDictionary = []
            for i in range(0,len(Fids)):
                self.fieldValueTranslationDictionary.append(None)

            self.fieldValueTranslationDictionary[FidNames['transaction-type']] = TransactionTypes

            # For TCP reassembly
            self.__tcp_streams = dict()

        except Exception as ex:
            print 'V'*20
            print 'Exception of type {0} occured.  Arguments: {1}'.format(
                type(ex), ex.args)
            print 'Traceback:'
            print traceback.format_exc()
            import pdb
            pdb.post_mortem()
            print '^'*20

    def __parseOptions(self, opts):
        self.verbose = bool(opts.get('verbose', False))
        self.showUnhandled = bool(opts.get('show-unhandled', True))
        self.showPayloads = bool(opts.get('show-payloads', False))
        self.decodePrices = bool(opts.get('decode-prices', False))

    def __valid_signature(self, x):
        if x == 0x4239:
            return True
        return False

    """ Decoders for specific FID Templates
    """
    def __decodeFidHeaderUndefined(self, context, payload):
        print '+++ undefined or unhandled FID Template: {0} @ {1}'.format('0x%2x' % context['$md-fid-template'], context['recv-timestamp'] )
        context['$md-field-template-name'] = 'Undefined'
        print '+++ current context: {0}'.format(context)
        print '+++ current payload: {0}'.format(toHex(payload))
        return []

    def __decodeFidHeaderCompact(self, context, payload):
        fid_compact_fmt = '<H' # this is a bitField we're going to have to decode
        fid_compact_fmt_bytes = calcsize(fid_compact_fmt)
        fid_compact_fields = unpack_from(fid_compact_fmt, payload)

        bitField = fid_compact_fields[0]
        fidTemplate = bitField & 0b11
        fieldId = (bitField & 0b1111111100) >> 2
        fieldLength = (bitField & 0b1111110000000000) >> (8+2)
        fieldType = GetNativeType(fieldId)

        context['$md-field-length'] = fieldLength
        context['$md-fid-template'] = fidTemplate
        context['$md-field-id'] = fieldId
        context['$md-field-name'] = Fids[fieldId]
        context['$md-field-type'] = fieldType
        context['$md-field-type-name'] = FieldTypes[fieldType]
        context['$md-field-template-name'] = 'Compact'

        payload = payload[fid_compact_fmt_bytes:]

        return payload

    def __decodeFidHeaderShort(self, context, payload):
        fid_short_fmt = '<I' # this is a bitField we're going to have to decode
        fid_short_fmt_bytes = calcsize(fid_short_fmt)
        fid_short_fields = unpack_from(fid_short_fmt, payload)

        bitField = fid_short_fields[0]
        # total 32 bits
        fidTemplate = bitField & 0b11 # 2 bits
        fieldType = (bitField & (0b11111111 << 2)) >> 2 # 8 bits
        fieldId = (bitField & (0b111111111111 << (2+8))) >> (2+8) # 12 bits
        fieldLength = (bitField & (0b1111111111 << (2+8+12))) >> (2+8+12) # 10 bits


        context['$md-fid-template'] = fidTemplate
        context['$md-field-type'] = fieldType
        context['$md-field-id'] = fieldId
        context['$md-field-name'] = Fids[fieldId]
        context['$md-field-length'] = fieldLength
        context['$md-field-template-name'] = 'Short'

        payload = payload[fid_short_fmt_bytes:]

        return payload

    def __decodeFidHeaderLong(self, context, payload):
        """     This format uses the MD_MESSAGE_FID structure fromi mean the actual field id, not the
                MDMessage.h
        """
        fid_long_fmt = '<II' # this is a bitField we're going to have to decode
        fid_long_fmt_bytes = calcsize(fid_long_fmt)
        fid_long_fields = unpack_from(fid_long_fmt, payload)

        bitField = fid_long_fields[0]
        fidTemplate = bitField & 0b11 # 2 bits
        fieldType = (bitField & (0b111111111 << 2)) >> 2 # 9 bits
        fieldId = (bitField & (0b1111111111111111 << (2+9))) >> (2+9) # 16 bits
        fieldLength = fid_long_fields[1]

        context['$md-fid-template'] = fidTemplate
        context['$md-field-type'] = fieldType
        context['$md-field-id'] = fieldId
        context['$md-field-name'] = Fids[fieldId]
        context['$md-field-length'] = fieldLength
        context['$md-field-template-name'] = 'Long'

        payload = payload[fid_long_fmt_bytes:]

        return payload

    """  Fid Body Decoders
    """
    def __decodeFieldBodyUndefined(self, context, payload):
        fieldLength = context['$md-field-length']
        fieldTypeName =  FieldTypes[context['$md-field-type']]

        fieldPayload = payload[:fieldLength]
        payload = payload[fieldLength:]

        if self.showUnhandled == True:
            context['$md-field-value'] = 'Unhandled FieldType: {0}.  {1} Unprocessed Bytes'.format(fieldTypeName, fieldLength)

        return payload

    def __decodeFieldBodyUInt32(self, context, payload):
        fieldLength = context['$md-field-length']

        context['$md-field-type-name'] = 'uint32'
        
        field_fmt = '<L'
        field_fmt_bytes = calcsize(field_fmt)
        field_values = unpack_from(field_fmt, payload[:fieldLength])

        context['$md-field-value'] = field_values[0]

        return payload [fieldLength:]

    def __decodeFieldBodyUInt64(self, context, payload):
        fieldLength = context['$md-field-length']

        context['$md-field-type-name'] = 'uint64'

        field_fmt = '<Q'
        field_fmt_bytes = calcsize(field_fmt)
        field_values = unpack_from(field_fmt, payload[:fieldLength])

        context['$md-field-value'] = field_values[0]

        return payload [fieldLength:]

    def __decodeDateTime(self, value):
        # A DateTime object contains either a date or a time.
        # If the date bit is set (0x40000000), then it's a date.

        if value & 0x40000000 != 0:
            # This is a date.
            year = (value >> 16) & 0x3ff
            month = (value >> 8) & 0xff
            day = value & 0xff

            retval = '{0}/{1}/{2}'.format(month, day, year)
        else:
            milli = (value & 0xffff) % 1000
            second = (value & 0xffff) / 1000
            minute = (value >> 16) & 0xff
            hour = (value >> 24) & 0x3f

            retval = "{0}:{1}:{2}.{3}".format(hour, minute, second, milli)

        return retval

    def __decodeFieldBodyPrice(self, context, payload):
        try:
            fieldLength = context['$md-field-length']
            fieldPayload = payload[:fieldLength]

            fieldFmt = '<'
            fieldFmt += 'I' # 0 price value
            fieldFmt += 'H' # 1 price type
            fieldFmt += '2s' # 2 market code
            fieldFmt += 'I' # 3 date time

            fields = unpack_from(fieldFmt, fieldPayload)

            if self.decodePrices:
                price = decimal.Decimal(fields[0]) / decimal.Decimal(10 ** fields[1])
            else:
                price = fields[0]
            market = fields[2]
            dateTime = self.__decodeDateTime(fields[3])

            context['$md-field-value'] = '{0}{1} {2}'.format(price, market, dateTime)

            return payload[fieldLength:]

        except Exception as ex:
            # This should never happen.  It is here for debugging while I learn Python better...
            print 'V' * 20
            print 'Exception of type {0} occured.  Arguments: {1}'.format (
                type (ex), ex.args)
            print 'Traceback:'
            print traceback.format_exc ()
            import pdb

            pdb.post_mortem ()
            print '^' * 20

    def __decodeFieldBodyOrderSku(self, context, payload):
        fieldLength = context['$md-field-length']
        fieldPayload = payload[:fieldLength]

        field_fmt = '<'
        field_fmt += 'H' # product
        field_fmt += 'I' # Source content
        field_fmt += 'I' # Value
        field_fmt += 'H' # Value price type
        field_fmt += '12s' # IDn

        fields = unpack_from(field_fmt, fieldPayload)

        fieldValue = '{0}.{1}.{2}.{3}.{4}'.format(fields[0], fields[1], fields[2], fields[3], fields[4].strip(' \t\r\n\0'))

        context['$md-field-value'] = fieldValue

        return payload[fieldLength:]

    def __decodeFieldBodySku(self, context, payload):
        fieldPayload = payload[:context['$md-field-length']]

        symbol = ''
        country = ''
        market = ''
        mmid = ''

        sku_fmt = '<'
        sku_fmt += '24s' # symbol
        if len(fieldPayload) > 24:
            sku_fmt += '2s' # country
        if len(fieldPayload) > (24+2):
            sku_fmt += '2s' # market
        if len(fieldPayload) > (24+2+2):
            sku_fmt += '4s' # mmid
        sku_bytes = calcsize(sku_fmt)
        sku_fields = unpack_from(sku_fmt, payload)

#        payloadHex = toHex(payload[:sku_bytes])
        symbol = sku_fields[0].strip(' \t\r\n\0')
        if len(sku_fields) > 1:
            country = sku_fields[1].strip(' \t\r\n\0')
        if len(sku_fields) > 2:
            market = sku_fields[2].strip(' \t\r\n\0')
        if len(sku_fields) > 3:
            mmid = sku_fields[3].strip(' \t\r\n\0')

        # Start building the return value
        fieldValue = '{0}.{1}'.format(symbol, market)
        if len(mmid) > 0:
            fieldValue += '.{0}'.format(mmid)

        context['$md-field-value'] = fieldValue

        return payload[sku_bytes:]


    def __decodeField(self, context, payload, fieldNum, offset):
        try:
            if fieldNum == 6:
                foo = 'bar'
            origPayload = payload
            fid_fmt = ''
            fid_fmt += '<B' # fid templaten
            fid_fmt_bytes = calcsize(fid_fmt)

            # Parse the first byte of the fid header, to get the template id
            fid_fields = unpack_from(fid_fmt, payload)

            """ Decode the Field Header
            """
            fid_template = fid_fields[0] & 0x03

            fieldContext = {'$md-fid-template': fid_template, '#field-num': fieldNum}
            fnDecodeFieldHeader = self.fieldHeaderJumpTable[fid_template]
            payload = fnDecodeFieldHeader(fieldContext, payload)

            if self.verbose:
                print 'Field: {0}\tID:{1}\tLen:{2}\tType:{3}'.format(fieldContext['$md-field-template-name'], fieldContext['$md-field-id'], fieldContext['$md-field-length'], fieldContext['$md-field-type'])

            # Make sure we were able to decode this fid header
            if '$md-field-type' not in fieldContext:
                print '+++ unable to parse field header.  skipping remaining payload'
                return []
            fieldType = fieldContext['$md-field-type']
            fieldLength = fieldContext['$md-field-length']
            fieldName = fieldContext['$md-field-name']
            fieldId = fieldContext['$md-field-id']

            """ Decode the field body
            """
            if self.showPayloads:
                fieldContext['$md-field-payload'] = toHex(payload[:fieldLength])
            fnDecodeFieldBody = self.fieldBodyJumpTable[fieldType]
            payload = fnDecodeFieldBody(fieldContext, payload)

            """ Append a possibly re-interpreted field value
                to the resulting context
            """
            if '$md-field-value' in fieldContext:
                fieldValue = fieldContext['$md-field-value']

                # Re-interpret the field value based on the FID
                valueDict = self.fieldValueTranslationDictionary[fieldId]
                if valueDict is not None:
                    fieldValue = valueDict[fieldValue]

                # Append this field to the message context
                context[fieldName] = fieldValue

            return payload

        except Exception as ex:
            # This should never happen.  It is here for debugging while I learn Python better...
            print 'V'*20
            print 'Exception of type {0} occured.  Arguments: {1}'.format(
                type(ex), ex.args)
            print 'Traceback:'
            print traceback.format_exc()
            import pdb
            pdb.post_mortem()
            print '^'*20

    def reassemble_tcp(self, context, payload):

        if context.get('tcp-packet', False) is False:
            return context, payload
        # this is a tcp packet that needs to be reassembled
        # each dest port is a distinct data stream
        # If we have never seen data for a given stream
        # (indicated by the lack of entry in the dict below)
        # then we need to throw data away until we find the
        # beginning of a packet, indicated by the presence
        # of the magic numnber in the packet header.
        # If we have seen data for the stream, then we keep
        # appending data to the stream until we accumulate
        # all the bytes for the packet, then we send that
        # back to on_message()

        # grab the tcp stream id
        stream_id = context['tcp-stream-id']

        if self.__tcp_streams.get(stream_id, None) is None:
            # we haven't seen this stream yet
            # decode what should be the packet header
            # add this payload to the stream buffer
            pkt_hdrs, payload = self.decode_segment(PacketHeader, payload, peek=True)
            if len(pkt_hdrs) is not 1:
                raise ValueError("Internal error decoding MDPacket header during TCP reconstruction")
            pkt_hdr = pkt_hdrs[0]
            if not self.__valid_signature(pkt_hdr['md-signature']):
                # this is not the beginning of a packet
                # we will do nothing
                return None, None
            else:
                # this is the beginning of a new packet
                # add it to the stream buffer
                self.__tcp_streams[stream_id] = (pkt_hdr['md-total-length'], payload)
        else:
            # we have seen this stream before
            # add the data to the buffer
            if self.__valid_signature(pkt_hdr['md-signature']):
                # this is the beginning of a packet
                self.__tcp_streams[stream_id] = (pkt_hdr['md-total-length'], payload)
            else:
                # a continuation packet -- just append the payload
                self.__tcp_streams[stream_id][1].append(payload)

        # now check to see if we have a full packet
        bytes_expected = self.__tcp_streams[stream_id][0]
        bytes_recieved = len(self.__tcp_streams[stream_id][1])
        if bytes_recieved >= bytes_expected:
            # send those bytes & remove them from the buffer
            send_payload = self.__tcp_streams[stream_id][1][0:bytes_expected]
            remain_payload = self.__tcp_streams[stream_id][1][bytes_expected:]
            if len(remain_payload) > 0:
                # peel open the next header
                next_headers, remain_payload = self.decode_segment(PacketHeader, remain_payload, peek=True)
                if len(next_headers) is not 1:
                    raise ValueError("Internal error while decoding MDPacket header for TCP Reconstruction of remaining payload")
                next_header = next_headers[0]
                self.__tcp_streams[stream_id] = (next_header['md-total-length'], remain_payload)
            else:
                self.__tcp_streams[stream_id] = None
            return context, send_payload
        else:
            # we still need more bytes...
            return None, None



    def on_message(self, context, payload):
        try:
            # if we need to reassemble tcp packets...
            context, payload = self.reassemble_tcp(context, payload)
            if context is None:
                # we need more data
                return

            if self.showPayloads:
                context['msg-payload-length'] = len (payload)
                context['msg-payload'] = toHex (payload[0:])

            if self.verbose:
                print "=== MESSAGE ===================================" 
            # Peel open the MD_MESSAGE_HEADER
            md_headers, payload = self.decode_segment(PacketHeader, payload)
            if len(md_headers) is not 1:
                raise ValueError("Internal error decoding MDPacket Header")
            md_header = md_headers[0]

            # Hack -- peel open the fid table
            fieldNum = 0
            offset = 0
            while len(payload) > 0:
                prevLen = len(payload)
                payload = self.__decodeField(context, payload, fieldNum, offset)
                postLen = len(payload)
                offset += prevLen-postLen
                fieldNum += 1

            # gather stats
            self.__packetCount += 1
            api = context.get('transaction-type', -1)
            self.__packetTransactions[api] = self.__packetTransactions.get(api, 0) + 1

            # Pass of to next decoder
            self.dispatch_to_next (context, payload)
            return

        except Exception as ex:
            # This should never happen.  It is here for debugging while I learn Python better...
            print 'V'*20
            print 'Exception of type {0} occured.  Arguments: {1}'.format(
                type(ex), ex.args)
            print 'Traceback:'
            print traceback.format_exc()
            import pdb
            pdb.post_mortem()
            print '^'*20


    def summarize(self):
        """ Provides summary statistics from this Decoder
        """
        return {
            'md-packet-count': self.__packetCount,
            'md-transaction-count': self.__packetTransactions
        }








