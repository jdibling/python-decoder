from decoder.module import *
from decoder.bats.mpitchmsg.segments import *
from decoder.bats.mpitchmsg.constants import *


class Decoder(BasicModule):
    def __init__(self, opts, next_decoder):
        super(Decoder, self).__init__('bats/mpitch', opts, next_decoder)
        self.__parse_options(opts)
        self.__unhandledMessages = dict()
        self.__translation = dict()
        self.__frameCount = 0
        self.__msgCount = dict()
        self.__byteCount = 0
        self.__order_book = dict()

    def __parse_options(self, opts):
        pass

    def on_message(self, inputContext, payload):
        # parse the packet header
        origPayloadLen = len(payload)
        headers, payload = self.decode_segment(UnitHeader, payload)
        if len(headers) is not 1:
            raise ValueError("Internal error processing MPitch packet header")
        header = headers[0]

        # update stats
        self.__byteCount += UnitHeader.WireBytes()
        self.__frameCount += 1

        # process each message
        for msgIdx in range(0, header['mpitch-hdr-count']):
            # decode the common fields from the messsage payload
            commons, payload = self.decode_segment(CommonFields, payload)
            if len(commons) is not 1:
                raise ValueError("Internal error processing MPitch common message fields")
            common = commons[0]

            # grab the message payload & trim the remaining payload
            msgLen = common['mpitch-length'] - CommonFields.WireBytes()
            messagePayload = payload[:msgLen]
            payload = payload[msgLen:]
            # get the msg type
            msgType = common['mpitch-msg-type']

            # decode the message payload
            context = {'sequence-number': header['mpitch-hdr-sequence']+msgIdx}

            # update stats
            self.__byteCount += msgLen
            self.__msgCount[msgType] = self.__msgCount.get(msgType, 0) + 1

            # get the message type & the descriptor for it
            if msgType not in MsgTypes:
                self.__unhandledMessages[msgType] = self.__unhandledMessages.get(msgType, 0) + 1
            else:
                messages, messagePayload = self.decode_segment(MsgTypes[msgType][0], messagePayload)
                if len(messages) is not 1:
                    raise ValueError("Internal error processing MPitch message")
                message = messages[0]

                # get the message type name
                typeName = MsgTypes[msgType][1]

                message['mpitch-message-type'] = typeName
                context.update(message)

                # special handling for add order messages -- update a local order book
                if msgType in AddOrderMsgTypes:
                    order_id = context['mpitch-order-id']
                    order_symbol = context['mpitch-symbol']
                    order_qty = context['mpitch-quantity']
                    order_price = context['mpitch-price']
                    order_side = context['mpitch-side']

                    if order_id in self.__order_book:
                        bk = True

                    self.__order_book[order_id] = {
                        'order-symbol': order_symbol,
                        'order-qty': order_qty,
                        'order-price': order_price,
                        'order-side': order_side
                    }

                # special handling for order executed message
                if msgType == MsgTypeNames['OrderExecutedAtPriceSize']:
                    order_id = context['mpitch-order-id']
                    exec_qty = context['mpitch-quantity']
                    leaves_qty = context['mpitch-remaining-quantity']
                    exec_price = context['mpitch-price']
                    prev_order = self.__order_book.get(order_id, None)
                    if prev_order is not None:
                        for k, v in prev_order.iteritems():
                            key = 'mpitch-orig-{0}'.format(k)
                            context[key] = v
                        prev_qty = prev_order['order-qty']
                        expected_leaves = prev_qty - exec_qty
                        context['mpitch-expected-remaining-quantity'] = expected_leaves
                        if leaves_qty > expected_leaves:
                            context['mpitch-possible-iceberg'] = True

                        if leaves_qty == 0:
                            del(self.__order_book[order_id])

            # send to next
            context.update(inputContext)
            context.update(header)
            context.update(common)
            self.dispatch_to_next(context, messagePayload)

    def summarize(self):
        unhandled = dict([ (MsgTypes[k][1], v) for k,v in self.__unhandledMessages.iteritems()])
        msgCounts = dict([ (MsgTypes[k][1], v) for k,v in self.__msgCount.iteritems()])
        return {
            'mpitch-unhandled-messages': unhandled,
            'mpitch-translation-entries': len(self.__translation),
            'mpitch-frames': self.__frameCount,
            'mpitch-bytes': self.__byteCount,
            'mpitch-msg-counts': msgCounts
        }
