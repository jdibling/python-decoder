from base.field import *

class FreeFormTextField(NamedField):
    def __init__(self, field_name, **kwargs):
        super(FreeFormTextField, self).__init__(field_name, **kwargs)
        pass
    def eval(self, payload, contexts):
        return (payload, [])

