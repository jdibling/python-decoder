import collections

from decoder.field import BasicField, WireField, ComputedField, RepeatingGroup, LookupField, TrimmedString
from decoder.descriptor import Descriptor

from decoder.decoder import Decoder, Verbosity


class Decoder(Decoder):
    """ filter module

    This module filters output streams

    """

    def __parse_options(self, opts):
        self.__start_sequence = opts.get('start-sequence', None)
        self.__end_sequence = opts.get('end-sequence', None)
        self.__allow_unsequenced = opts.get('allow-unsequenced', False)
        self.__required_keys = None
        if 'required-keys' in opts:
            self.__required_keys = opts['required-keys'].split(',')
        self.__sent_keys = None
        if 'send-keys' in opts:
            self.__sent_keys = [x.strip() for x in opts['send-keys'].split(',')]
        self.__keyvals = []
        if 'keyvals' in opts:
            for keyval in opts['keyvals'].split(','):
                pair = keyval.split('=')
                self.__keyvals.append(pair)
        self.__allowed_modules = None
        if 'allowed-modules' in opts:
            self.__allowed_modules = opts['allowed-modules'].split(',')
        self.__excluded_modules = None
        if 'excluded-modules' in opts:
            self.__excluded_modules = opts['excluded-modules'].split(',')
        self.__allow_special_keys = opts.get('allow-special-keys', True)

    def __init__(self, opts, next_decoder):
        super(Decoder, self).__init__('output/filter', opts, next_decoder)
        self.__parse_options(opts)
        # init summary data
        self.__filtered_messages = 0
        self.__allowed_messages = 0
        self.__total_messages = 0

    def on_message(self, context, payload):
        """  incoming packet and filter the output

        :rtype : none
        :param context: Message context build by preceding link in decoder chain
        :param payload: Message payload
        """

        self.__total_messages += 1
        allow = True

        # check to see if the sequence number is filtered
        cur_sequence = context.get('sequence-number', None)
        if cur_sequence is not None:
            if self.__start_sequence is not None:
                if cur_sequence < self.__start_sequence:
                    allow = False
            if self.__end_sequence is not None:
                if cur_sequence > self.__end_sequence:
                    allow = False
        else:
            if self.__allow_unsequenced == False:
                allow = False

        # check to see if we're allowing only messages with specific key-value pairs
        if allow == True and len(self.__keyvals) is not 0:
            for key, val in self.__keyvals:
                if key not in context:
                    allow = False
                elif val != context[key]:
                    allow = False

        # check to see if we're allowing only messages with specific keys
        if allow == True and self.__required_keys is not None:
            for key in self.__required_keys:
                if key.strip() not in context:
                    allow = False

        if allow:
            self.__allowed_messages += 1
            # filter in only allowed-keys, if specified
            if self.__sent_keys is not None:
                filteredContext = collections.OrderedDict()
                for key in self.__sent_keys:
                    if key.strip() in context:
                        filteredContext.update({key.strip(): context[key.strip()]})
                context = filteredContext
            # filter in explicitly allowed modules
            if self.__allowed_modules is not None:
                filtered = collections.OrderedDict()
                for key, value in context.iteritems():
                    for allowed_key in self.__allowed_modules:
                        if allowed_key in key:
                            filtered[key] = value
                context = filtered

            # filter out explicitly excluded modules
            if self.__excluded_modules is not None:
                for key, value in context.iteritems():
                    # see if this key is excluded
                    for excluded_key in self.__excluded_modules:
                        if excluded_key in key:
                            # this key is excluded, so remove it from context
                            del context[key]

            # filter in special keys if allowed
            if self.__allow_special_keys:
                if cur_sequence is not None:
                    context['sequence-number'] = cur_sequence

            if context:
                self.dispatch_to_next(context, payload)
        else:
            self.__filtered_messages += 1




    def summarize(self):
        """ Provides summary statistics from this Decoder
        """
        return {
            "filter-filtered": self.__filtered_messages,
            "filter-allowed": self.__allowed_messages,
            "filter-total": self.__total_messages
        }


