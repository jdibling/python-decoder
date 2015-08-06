from .field import *
from .types import *
from .verbosity import *

class Descriptor(object):
    def __init__(self, fields, **kwargs):
        self.__verbosity = kwargs.get('verbosity', Verbosity.Normal)
        self.__fields = fields

        # set fields
        for field in self.fields():
            # determine if we should show this field based on the field's verbosity setting
            # and the runtime parameters of the decoder
            #field.set_shown(self.verbosity() >= field.verbosity())

            # NOTE:  This doesn't really work because set_shown(False) means
            # the field won't even be in the resulting context.  As such,
            # dependencies on those elided fields will fail.  For example,
            # if a computed field depends on another field which has been
            # elided, then evaluation of the computed field will crash
            # with a KeyError.
            # The ultimate fix will be to have evaluate() return two contexts
            # instead of just one -- one for the un-hidden fields and one for
            # the hidden.
            # For now, we'll just disable this feature and display everything
            field.set_shown(True)

        # set endianness
        if 'endian' in kwargs:
            endianness = kwargs['endian'].lower()
            if endianness == 'big':
                self.SetBigEndian()
            elif endianness == 'little':
                self.SetLittleEndian()
            else:
                raise ValueError("Unexpected value passed for 'endian=' argument on Descriptor: '{0}'".format(kwargs['endian']))

        # check actual size against expected size
        if 'checksize' in kwargs:
            if self.WireBytes() != int(kwargs['checksize']):
                raise RuntimeError("Descriptor expected size of {0} but has an actual size of {1}".format(kwargs['checksize'], self.WireBytes()))

    def __iter__ (self):
        return iter(self.fields())
    def fields(self):
        return self.__fields
    def verbosity(self):
        return self.__verbosity
    def WireBytes(self):
        ttl=0
        for field in self.__fields:
            WireBytesOp = getattr(field, "WireBytes", None)
            if callable(WireBytesOp):
                ttl += field.WireBytes()
        return ttl
    def SetLittleEndian(self):
        for field in self.fields():
            try:
                field.SetLittleEndian()
            except NotImplementedError:
                pass
            except AttributeError:
                pass
    def SetBigEndian(self):
        for field in self.fields():
            try:
                field.SetBigEndian()
            except NotImplementedError:
                pass
            except AttributeError:
                pass
    # def GetEndian(self):
    #     return self.fields()[0].GetEndian()

