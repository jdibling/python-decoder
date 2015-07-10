#!/usr/bin/python

import SocketServer
import struct
from decoder.ice.ice.segments import *

loginrequest='>chi30s30sch'

def ReadHeader( packet ):
    msg_header = MessageHeader
    unpack_str = ">"

    for field in msg_header.fields():
        unpack_str = unpack_str + field.WireFormat()[1:]
    print "here is the raw data " + packet
    print "unpacking with " + unpack_str

    data = struct.unpack( unpack_str, packet[0:3] )
    return (data[0], data[1])
    


    

class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    def handle(self):
        # self.request is the TCP socket connected to the client
        #self.allow_reuse_address = true

        self.data = self.request.recv(1024).strip()

        msg_type, msglen = ReadHeader(self.data)
        if msg_type == '1': #Login message
            self.ProcessLogin()
        elif msg_type == '2': #Product Definition
            pass
        elif msg_type == '7': #Historical Replay
            pass
        elif msg_type == '5': #Debug
            pass
        elif msg_type == '6': #Logout
            pass

        print msg_type, " ", msglen
        msg = struct.unpack(loginrequest, self.data)
        print msg
        print "{} wrote:".format(self.client_address[0])
        print self.data
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())
    def ProcessLogin():
        req = LoginRequest
         
        

if __name__ == "__main__":
    HOST, PORT = "10.3.2.73", 9999
    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
