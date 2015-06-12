import datetime

class XdpTimeStamp(object):
    def __init__(self, secFieldName, nanoFieldName):
        super(XdpTimeStamp, self).__init__()
        self.__secField = secFieldName
        self.__nanoField = nanoFieldName
    def __call__(self, context):
        sec = int(context[self.__secField])
        mic = int(context[self.__nanoField]) / 1000
        dt = datetime.datetime.fromtimestamp(sec)
        dt = dt.replace(microsecond=mic)
        return dt
