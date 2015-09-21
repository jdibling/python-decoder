from struct import calcsize, unpack_from
from .decoder import Verbosity
from .types import *


class BasicField(object):
    def __init__(self, **kwargs):
        self.__renderer = kwargs.get('type', None)
        self.__decoder = kwargs.get('decode_function', self.eval)
        self.__verbosity = kwargs.get ('verbosity', Verbosity.Normal)
        if kwargs.get ('hidden', False) == True:
            self.__verbosity = Verbosity.Silent
        self.__shown = True
    def __repr__(self):
        return "BasicField"
    def eval(self, payload, contexts):
        pass

    def render(self, value):
#        return value

        if self.__renderer is None:
            return value
        return self.__renderer(value)
    def decoder(self):
        return self.__decoder
    def shown(self):
        return self.__shown
    def set_shown(self, is_shown=True):
        self.__shown = is_shown
    def verbosity(self):
        return self.__verbosity

class NamedField(BasicField):
    def __init__(self, fieldName, **kwargs):
        super(NamedField, self).__init__(**kwargs)
        self.fieldName = fieldName
    def name(self):
        return self.fieldName
    def __repr__(self):
        return "{0}.NamedField: '{1}'".format(super(NamedField, self).__repr__(), self.fieldName)

""" EchoField

    This field simply creates a new field with the same value
    of another field already in-context.

    The value may be converted using a 'type=' argument

    Construction:
        EchoField(newField, oldField, [args])
            The new field is named 'newField'.
            The value for 'newField' is taken 'oldField'
            from existing context.  Any type conversion specified
            in [args] is applied to the new field.

"""
class EchoField(NamedField):
    def __init__(self, fieldName, echoFieldName, **kwargs):
        super(EchoField, self).__init__(fieldName, **kwargs)
        self.echoFieldName = echoFieldName
    def eval(self, payload, contexts, **kwargs):
        fieldVal = self.render(contexts[-1][self.echoFieldName])
        contexts[-1].update({self.name(): fieldVal})
        return (payload, contexts)

class WireField(NamedField):
    def __init__(self, field_name, wire_format, **kwargs):
        super(WireField, self).__init__(field_name, **kwargs)
        self.__base_format = wire_format
        self.__format = None
        self.__wireBytes = None
        self.SetLittleEndian()

    def SetLittleEndian(self):
        self.__format = "<{0}".format(self.__base_format)
        self.__wireBytes = calcsize(self.WireFormat())
    def SetBigEndian(self):
        self.__format = ">{0}".format(self.__base_format)
        self.__wireBytes = calcsize(self.WireFormat())
    def WireFormat(self):
        return self.__format
    def WireBytes(self):
        return self.__wireBytes

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
        payload = payload[self.__wireBytes:]
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

class MapLookupField(NamedField):
  def __init__(self, field_name, value_field, lookup_map, **kwargs):
        super(MapLookupField, self).__init__(field_name, **kwargs)
        self.__lookup_map = lookup_map
        self.__value_field = value_field

  def eval(self, payload, contexts, **kwargs):
        decoded = contexts[-1][self.__value_field]
        translated = self.__lookup_map[decoded]
        contexts[-1].update({self.name(): translated})
        return (payload, contexts)


class ConstantField(NamedField):
    def __init__(self, field_name, value, **kwargs):
        super(ConstantField, self).__init__(field_name, **kwargs)
        self.__value = value
    def eval(self, payload, contexts, **kwargs):
        decoded = contexts
        decoded[-1].update({self.name(): self.__value})
        return (payload, decoded)

class ComputedField(NamedField):
    def __init__(self, field_name, computation, **kwargs):
        super(ComputedField, self).__init__(field_name, **kwargs)
        self.__computer = computation

    def eval(self, payload, contexts):
        computed_context = {self.name(): self.__computer(contexts[-1])}
        contexts[-1].update (computed_context)
        return (payload, contexts)

class RepeatingGroup(BasicField):
    class ReprCountFromPayload(object):
        def __init__(self, fieldFmt):
            super(RepeatingGroup.ReprCountFromPayload, self).__init__()
            self.fmt = fieldFmt
            self.fmtBytes = calcsize(self.fmt)
        def GetCount(self, payload, context):
            fields = unpack_from(self.fmt, payload)
            if len(fields) is not 1:
                raise ValueError("Internal error decoding ReprCount of RepeatingGroup from wire data")
            return (int(fields[0]), payload[self.fmtBytes:])
    class ReprCountFromContext(object):
        def __init__(self, field):
            super(RepeatingGroup.ReprCountFromContext, self).__init__()
            self.field = field
        def GetCount(self, payload, context):
            reprCount = context.get(self.field, None)
            if reprCount is None:
                raise ValueError("Internal error extracting ReprCount for RepeatingGroup:  '{0}' field not found in context".format(self.field))

            return int(reprCount), payload

    def __init__(self, sub_fields, reprCounter, **kwargs):
        super(RepeatingGroup,self).__init__(**kwargs)
        self.__sub_fields= sub_fields
        self.__embed = kwargs.get('embed', True)
        self.reprCounter = reprCounter
        self.embeddedFieldName = kwargs.get('embed_as', None)

    def eval(self, payload, contexts):
        # get the repr count
        repCount, payload = self.reprCounter.GetCount(payload, contexts[-1])

        decodedGroups = []
        # decode the repeating group
        for rep in range(0,repCount):
            decodedFields = [dict()]
            # decode each field
            for sub_field in self.__sub_fields:
                (payload, decodedFields) = sub_field.eval(payload, decodedFields)
            # append the decoded fields in this element of the repr group
            # to an array of decoded elements
            decodedGroups.append(decodedFields[-1])

        # if we're embedding the decoding repeating group,
        # then add it to the last context...
        if self.embeddedFieldName is not None:
            contexts[-1].update({self.embeddedFieldName: decodedGroups})
        # otherwise, create a new context for each element of
        # the repeating group, replacing the initial context
        # that was passed in
        else:
            baseContext = dict()
            baseContext.update(contexts[-1])
            retContexts = []
            for groupElement in decodedGroups:
                newContext = dict()
                newContext.update(baseContext)
                newContext.update(groupElement)
                retContexts.append(newContext)
            contexts = retContexts
        # we're done
        return (payload, contexts)


