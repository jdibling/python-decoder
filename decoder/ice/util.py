__author__ = 'blazei'

from decoder.ice.icemsg import segments as ice_segments
import struct

__request_seq_id = 0


def inc_request_seq_id():
    global __request_seq_id
    __request_seq_id += 1
    return __request_seq_id


def is_ice_heartbeat(payload):
    """
    Checks if payload represents an ICE Heartbeat message. Used to identify end of relevant data stream.
    :param payload: bytes representing ICE message payload
    :return: true if MsgType == 'Q', false otherwise
    """
    msg_type = payload[0:1]
    return msg_type == 'Q'


def is_ice_error_response(payload):
    """
    Checks if payload represents an ICE Error Response message. Used to identify if a request was malformed in some way.
    :param payload: bytes representing ICE message payload
    :return: true if MsgType == 'S', false otherwise
    """
    msg_type = payload[0:1]
    return msg_type == 'S'


def make_login_request_payload(username, password, request_seq_id):
    """
    Generates the payload for an ICE TCP Login request given username and password parameters
    :param username: username to ICE TCP server
    :param password: password to ICE TCP server
    :return: LoginRequest payload
    """
    msg_header = ice_segments.MessageHeader
    login_request = ice_segments.LoginRequest

    # already know it's big-endian
    # TODO something more clever?
    # should end up being '>chi30s30sch'
    pack_syms = '>'
    for field in msg_header.fields():
        pack_syms = pack_syms + field.WireFormat()[1:]

    for field in login_request.fields():
        pack_syms = pack_syms + field.WireFormat()[1:]

    msg_type = '1'
    msg_body_length = ice_segments.LoginRequest.WireBytes()
    username = username.ljust(30, '\0')
    password = password.ljust(30, '\0')
    get_strips = 'Y'
    resv = 0

    payload = struct.pack(pack_syms,
                          msg_type,
                          msg_body_length,
                          request_seq_id,
                          username,
                          password,
                          get_strips,
                          resv)
    return payload


def make_product_request_payload(security_type, market_type, request_seq_id):
    msg_header = ice_segments.MessageHeader
    prod_def_req = ice_segments.ProductDefRequest
    pack_syms = '>'

    for field in msg_header.fields():
        pack_syms = pack_syms + field.WireFormat()[1:]

    for field in prod_def_req.fields():
        pack_syms = pack_syms + field.WireFormat()[1:]

    msg_type = '2'
    msg_body_length = ice_segments.ProductDefRequest.WireBytes()
    print 'made prodreq:', msg_type, msg_body_length, request_seq_id, market_type, security_type

    payload = struct.pack(pack_syms, msg_type, msg_body_length, request_seq_id, market_type, security_type)
    return payload


def make_historical_request_payload(ip, port, session_id, seqnum_start, seqnum_end, request_seq_id):
    msg_header = ice_segments.MessageHeader
    hist_req = ice_segments.HistoricalRequest
    pack_syms = '>'

    for field in msg_header.fields():
        pack_syms = pack_syms + field.WireFormat()[1:]
        # print field.name() + ' ' + field.WireFormat()

    for field in hist_req.fields():
        pack_syms = pack_syms + field.WireFormat()[1:]
        # print field.name() + ' ' + field.WireFormat()

    msg_type = '7'
    msg_length = ice_segments.HistoricalRequest.WireBytes()
    ip = ip.ljust(15, '\0')

    print 'made historical_request:', msg_type, msg_length, request_seq_id, ip, port, session_id, seqnum_start, seqnum_end

    payload = struct.pack(pack_syms, msg_type, msg_length, request_seq_id, ip, port, session_id, seqnum_start, seqnum_end)

    return payload
