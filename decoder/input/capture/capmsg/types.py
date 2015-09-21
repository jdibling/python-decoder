import datetime

class HiResTimeStamp(object):
    def __init__(self, dataField):
        super(HiResTimeStamp, self).__init__()
        self.__dataField = dataField
        self.__epoch = 1262304000 # seconds from unix epoch to 1/1/2010
    def __call__(self, context):
        if self.__dataField not in context:
            raise ValueError("Context does not have expected '{0}' field: {1}".format(self.__dataField, context))
        hiRes = float(context[self.__dataField])
        whole = int(hiRes)
        mics = int((hiRes-whole)*1000000)
        whole += self.__epoch
        dt = datetime.datetime.fromtimestamp(whole).replace(microsecond=mics)
        return dt

