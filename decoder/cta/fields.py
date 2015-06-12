from base.field import BasicField

class FreeFormTextField(BasicField):
    def __init__(self, field_name, **kwargs):
        super(FreeFormTextField, self).__init__(field_name, **kwargs)
        pass
    def eval(self, payload, contexts):
        return (payload, [])

