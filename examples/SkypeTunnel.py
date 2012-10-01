#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

"""
SkypeTunnel.py

Version 1.0.0

Copyright (c) 2007 Arkadiusz Wahlig
All rights reserved

This script creates a TCP/UDP tunnel over Skype P2P network.

Uses Skype4Py package:
  https://github.com/awahlig/skype4py

Usage:

  $ SkypeTunnel.py --from-port=8888 --to-user=skypename:5

  Binds to port 8888 on localhost and redirects incomming data
  to Skype user 'skypename' using channel 5.

  A channel is an integer that let you distinguish between
  different tunnels running at the same time to the same user.
  If channel is ommited, 0 is used.

  $ SkypeTunnel.py --from-channel=5 --to-host=domain.com:22

  Binds to channel 5 on current Skype user and redirects
  incomming data to domain.com, port 22. Skipping --from-channel
  option binds to channel 0.

For example, if you're behind a NAT and want to put up a server,
start this on your machine:

  $ SkypeTunnel.py --to-host=127.0.0.1:5900

where 5900 is the port of your server (here: VNC).

Then if you want to access the server from a machine that has
Skype and you in the contact list, do this:

  $ SkypeTunnel.py --from-port=8900 --to-user=skypename

Where skypename is your SkypeName and 8900 is the port on local
machine where your server will be made available.

Now you can connect to your server by directing the client to
127.0.0.1:8900.

To create an UDP tunnel, simply append '--udp' option to both
ends of the tunnel.
"""

import socket
import base64
import time
import threading
import pickle
import optparse
import Skype4Py

# commands sent over Skype network (only in TCP connection)
cmdConnect, \
cmdDisconnect, \
cmdData, \
cmdError, \
cmdPing = range(5)

# parse command line options
parser = optparse.OptionParser(version='%prog 1.0.0')

parser.add_option('-p', '--from-port', type='int', metavar='PORT', help='bind to local PORT')
parser.add_option('-u', '--to-user', metavar='USER', help='redirect data from local PORT to Skype USER; append ":CHANNEL" to the USER to redirect to channel other than 0')
parser.add_option('-c', '--from-channel', type='int', metavar='CHANNEL', help='bind to local CHANNEL')
parser.add_option('-a', '--to-addr', metavar='ADDR', help='redirect data from local CHANNEL to ADDR which must be in HOST:PORT format')
parser.add_option('-d', '--udp', action='store_true', help='change the type of the tunnel from TCP to UDP')

opts, args = parser.parse_args()

if args:
    parser.error('unexpected argument(s)')

if opts.from_port != None and opts.to_user != None and opts.from_channel == None and opts.to_addr == None:
    mode = 'client'
    addr = '127.0.0.1', opts.from_port
    a = opts.to_user.split(':')
    user = a[0]
    if len(a) == 1:
        channel = 0
    elif len(a) == 2:
        channel = int(a[1])
    else:
        parser.error('bad value of --to-user')
elif opts.from_port == None and opts.to_user == None and opts.to_addr != None:
    mode = 'server'
    if opts.from_channel != None:
        channel = opts.from_channel
    else:
        channel = 0
    a = opts.to_addr.split(':')
    if len(a) != 2:
        parser.error('bad value of --to-host')
    addr = a[0], int(a[1])
else:
    parser.error('incorrect argument list')

if opts.udp:
    stype = socket.SOCK_DGRAM
else:
    stype = socket.SOCK_STREAM

def StreamRead(stream):
    """Reads Python object from Skype application stream."""
    try:
        return pickle.loads(base64.decodestring(stream.Read()))
    except EOFError:
        return None

def StreamWrite(stream, *obj):
    """Writes Python object to Skype application stream."""
    stream.Write(base64.encodestring(pickle.dumps(obj)))

class TCPTunnel(threading.Thread):
    """Tunneling thread handling TCP tunnels. An instance of this class in
    created on both ends of the tunnel. Clients create at after a connection
    is detected on the main socket. Servers create it after a connection is
    made in Skype application."""

    # A dictionary of all currently running tunneling threads. It is used
    # to convert tunnel IDs (comming from Skype application stream) to the
    # threads handling them.
    threads = {}

    def __init__(self, sock, stream, n=None):
        """Initializes the tunelling thread.

        sock - socket bound to this tunnel (either from incoming or outgoing
               connection)

        stream - stream object connected to the appropriate user

        n - stream ID, if None a new ID is created which is then sent to
            the other end of the tunnel
        """
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.sock = sock
        self.stream = stream

        # master is True if we are on the side that initiated the connection
        self.master = (n==None)

        # master should generate the tunnel ID
        if self.master:
            n = 0
            while n in TCPTunnel.threads:
                n += 1
        self.n = n
        assert n not in TCPTunnel.threads

        # store this thread in threads dictionary
        TCPTunnel.threads[n] = self

    def run(self):
        # master initiates the connection on the other side
        if self.master:
            # the tunnel ID is sent and it will be stored on the
            # other side so if multiple tunnels are open, data
            # sent using the same stream will get to apropriate
            # tunnels
            StreamWrite(self.stream, cmdConnect, self.n)

        print 'Opened new connection (%s)' % self.n

        try:
            # main loop reading data from socket and sending them
            # to the stream
            while True:
                data = self.sock.recv(4096)
                if not data:
                    break
                StreamWrite(self.stream, cmdData, self.n, data)
        except socket.error:
            pass

        self.close()

        # master closes the connection on the other side
        if self.master:
            StreamWrite(self.stream, cmdDisconnect, self.n)

        print 'Closed connection (%s)' % self.n

        del TCPTunnel.threads[self.n]

    def send(self, data):
        """Sends data to the socket bound to the tunnel."""

        try:
            self.sock.send(data)
        except socket.error:
            pass

    def close(self):
        """Closes the tunnel."""

        try:
            self.sock.shutdown(socket.SHUT_RDWR)
            self.sock.close()
        except socket.error:
            pass

class SkypeEvents:
    """This class gathers all Skype4Py event handlers."""

    def ApplicationReceiving(self, app, streams):
        """Called when the list of streams with data ready to be read changes."""

        # we should only proceed if we are in TCP mode
        if stype != socket.SOCK_STREAM:
            return

        # handle all streams
        for stream in streams:
            # read object from the stream
            obj = StreamRead(stream)
            if obj:
                if obj[0] == cmdData:
                    # data were received, reroute it to the tunnel based on the tunnel ID
                    try:
                        TCPTunnel.threads[obj[1]].send(obj[2])
                    except KeyError:
                        pass
                elif obj[0] == cmdConnect:
                    # a connection request received, connect the socket
                    n = obj[1]
                    sock = socket.socket(type=stype)
                    try:
                        sock.connect(addr)
                        # start the tunnel thread
                        TCPTunnel(sock, stream, n).start()
                    except socket.error, e:
                        # connection failed, send an error report back through the stream
                        print 'error (%s): %s' % (n, e)
                        StreamWrite(stream, cmdError, n, tuple(e))
                        StreamWrite(stream, cmdDisconnect, n)
                elif obj[0] == cmdDisconnect:
                    # an disconnection request received, close the tunnel
                    try:
                        TCPTunnel.threads[obj[1]].close()
                    except KeyError:
                        pass
                elif obj[0] == cmdError:
                    # connection failed on the other side, display the error
                    print 'error (%s): %s' % obj[1:2]

    def ApplicationDatagram(self, app, stream, text):
        """Called when a datagram is received over a stream."""

        # we should only proceed if we are in UDP mode
        if stype != socket.SOCK_DGRAM:
            return

        # decode the data
        data = base64.decodestring(text)

        # open an UDP socket
        sock = socket.socket(type=stype)

        # send the data
        try:
            sock.sendto(data, addr)
        except socket.error, e:
            print 'error: %s' % e

# create a Skype object instance and register our event handlers
skype = Skype4Py.Skype(Events=SkypeEvents())

# attach to the Skype client running in background
skype.Attach()

# create a proxy object for Skype application object (an app2app protocol handling object)
app = skype.Application('SkypeTCPTunnel.%s' % channel)

# create the object in Skype
app.Create()

# main loop
try:
    # if we are in client mode
    if mode == 'client':
        # in client mode, we wait for connections on local port so we
        # create a listening socket
        gsock = socket.socket(type=stype)
        gsock.bind(addr)

        # if we are in TCP mode
        if stype == socket.SOCK_STREAM:
            gsock.listen(5)

            # loop waiting for incoming connections
            while True:
                sock, raddr = gsock.accept()
                # connection on socket accepted, now connect to the user
                # and start the tunnel thread which will take care of the
                # rest
                stream = app.Connect(user, True)
                TCPTunnel(sock, stream).start()

        # if we are in UDP mode
        else:
            # loop waiting for incoming datagrams
            while True:
                data, addr = gsock.recvfrom(4096)
                # data received, connect to the user and send the data;
                # since UDP is connection-less, no tunnel thread is
                # created
                stream = app.Connect(user, True)
                stream.SendDatagram(base64.encodestring(data))

    # if we are in server mode
    elif mode == 'server':
        # loop forever pinging all opened streams every minute; this is
        # needed because Skype automatically closes streams which idle
        # for too long
        while True:
            time.sleep(60)
            for stream in app.Streams:
                StreamWrite(stream, cmdPing)

except KeyboardInterrupt:
    print 'Interrupted'
