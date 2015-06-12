from struct import calcsize, unpack_from
from base.decoder import  Verbosity
from base.types import *

class BasicField(object):
    def __init__(self, fieldName, **kwargs):
        self.__fieldName = fieldName
        self.__renderer = kwargs.get('type', TrimmedString)
        self.__decoder = kwargs.get('decode_function', self.eval)
        self.__verbosity = kwargs.get ('verbosity', Verbosity.Normal)
        if kwargs.get ('hidden', False) == True:
            self.__verbosity = Verbosity.Silent
        self.__shown = True

    def __repr__ (self):
        return "{0}:'{1}'".format (super (BasicField, self).__repr__ (), self.name())

    def eval(self, payload, contexts):
        pass

    def name(self):
        return self.__fieldName
    def renderer(self):
        return self.__renderer
    def render(self, value):
        return self.renderer()(value)
    def decoder(self):
        return self.__decoder
    def shown(self):
        return self.__shown
    def set_shown(self, is_shown=True):
        self.__shown = is_shown
    def verbosity(self):
        return self.__verbosity
    def WireBytes(self):
        return 0
    def SetBigEndian(self):
        pass
    def SetLittleEndian(self):
        pass
    def GetEndian(self):
        return "None"

class WireField(BasicField):
    def __init__(self, field_name, wire_format, **kwargs):
        super(WireField, self).__init__(field_name, **kwargs)
        self.__wire_format = wire_format
        self.SetLittleEndian()

    def SetLittleEndian(self):
        self.__endian_format = '<'
    def SetBigEndian(self):
        self.__endian_format = '>'
    def GetEndian():
        if self.__endian_format == '<':
            return "Little"
        elif self.__endian_format == '>':
            return "Big"
        else:
            return "Void"

    def WireFormat(self):
        return "{0}{1}".format(self.__endian_format, self.__wire_format)

    def WireBytes(self):
        return calcsize(self.WireFormat())

    def eval(self, payload, contexts, **kwargs):
        payload, decodedField = self._extract(payload, **kwargs)
        payload, contexts = self._finalize(payload, decodedField, contexts, **kwargs)
        return (payload, contexts)

    def _finalize(self, payload, decoded_field, contexts, **kwargs):
        # update our context
        if self.shown():
            contexts[-1].update({self.name(): decoded_field})
        # done
        return (payload, contexts)

    def _extract(self, payload, **kwargs):
        # extract the payload
        if not payload:
            raise ValueError('Payload not specified for WireField')
        dataFields = unpack_from(self.WireFormat(), payload)
        if len(dataFields) is not 1:
            raise ValueError('Something went terribly wrong here!')
        # decode the field
        fieldData = dataFields[0]
        decodedField = self.render(fieldData)
        # trim the payload
        payload = payload[self.WireBytes():]
        # return
        return (payload, decodedField)

class LookupField(WireField):
    def __init__(self, field_name, wire_format, lookup_map, **kwargs):
        super(LookupField, self).__init__(field_name, wire_format, **kwargs)
        self.__lookup_map = lookup_map

    def eval(self, payload, contexts, **kwargs):
        (payload, decoded) = self._extract(payload, **kwargs)
        translated = self.__lookup_map[decoded]
        return self._finalize(payload, translated, contexts, **kwargs)

class ConstantField(BasicField):
    def __init__(self, field_name, value, **kwargs):
        super(ConstantField, self).__init__(field_name, **kwargs)
        self.__value = value
    def eval(self, payload, contexts, **kwargs):
        decoded = contexts
        decoded[-1].update({self.name(): self.__value})
        return (payload, decoded)

class ComputedField(BasicField):
    def __init__(self, field_name, computation, **kwargs):
        super(ComputedField, self).__init__(field_name, **kwargs)
        self.__computer = computation

    def eval(self, payload, contexts):
        computed_context = {self.name(): self.__computer(contexts[-1])}
        contexts[-1].update (computed_context)
        return (payload, contexts)

class RepeatingGroup(BasicField):
    def __init__(self, field_name, repr_format, sub_fields, **kwargs):
        super(RepeatingGroup,self).__init__(field_name, **kwargs)
        self.__sub_fields= sub_fields
        self.__send_initial = kwargs.get('send_initial', False)
        self.__repr_format = repr_format
        self.__repr_bytes = calcsize(self.__repr_format)

    def WireBytes(self):
        return self.__repr_bytes

    def eval(self, payload, contexts):
        repCountFields = unpack_from(self.__repr_format, payload)
        if len(repCountFields) is not 1:
            raise ValueError("Decoding {0} did not yield a single repCount field".format(self.__toHex(payload[0:self.fieldBytes])))
        repCount = int(repCountFields[0])
        payload = payload[self.__repr_bytes:]
        # grab the initial context where the repeating group exists
        initial = contexts[-1]
        # trim the initial from the rest of the contexts (we'll add it back in later)
        contexts = contexts[0:-1] # this will usually be empty now
        # if sendInitial, add what we already have back in
        if self.__send_initial:
            contexts.append(initial)
        # decode the repeating group
        for rep in range(0,repCount):
            # start with a new context based off of initial
            base = [initial.copy()]
            # decode each field
            for sub_field in self.__sub_fields:
                (payload, base) = sub_field.eval(payload, base)
            # add the new context(s) back in to the return value
            contexts.append(base[-1])
        # we're done
        return (payload, contexts)

    def __update_context(self, decoded_field, retval):
        if not retval:
            retval = [{}]
        if self.shown():
            retval[-1].update({self.name(): str(decoded_field)})
        return retval


