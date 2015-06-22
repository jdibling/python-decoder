from struct import calcsize, unpack_from
StreamIdFmt = '<BBBBH2x'
StreamIdWireBytes = calcsize(StreamIdFmt)


def StreamIdToString(data):
    fields = unpack_from(StreamIdFmt, data)
    if len(fields) is not 5:
        raise ValueError("Internal error decoding StreamId")
    return '{0}.{1}.{2}.{3}:{4}'.format(fields[0], fields[1], fields[2], fields[3], fields[4])

