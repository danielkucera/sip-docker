#!/usr/bin/env python
#This plugin includes example functions that are triggered by events in sip.py

from blinker import signal
import gv

from socket import *
import threading
import sys
 
HOST = '0.0.0.0'
PORT = 20000

def get_byte():
    print(gv.srvals) #  This shows the state of the zones.
    byte = 0
    for i in range(0, 8):
        byte = byte << 1
        byte += gv.srvals[7-i]
    print(byte)
#    return "\x51"+chr(byte)
    return (""+chr(byte)).encode()

class TcpServer(threading.Thread):
        def __init__(self):
                    threading.Thread.__init__(self)
                    ADDR = (HOST, PORT)
                    serversock = socket(AF_INET, SOCK_STREAM)
                    serversock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
                    serversock.bind(ADDR)
                    serversock.listen(5)
                    self.serversock = serversock
                    self.clients = []
                    zones = signal('zone_change')
                    zones.connect(self.notify_zone)
                    self.notify_timer()
                    print('TCP event initialized')

        def run(self):
            while 1:
                try:
                    print('waiting for connection...')
                    clientsock, addr = self.serversock.accept()
                    print('...connected from:', addr)
                    #clientsock.send(get_byte()) #may throw exception when client discon and breaks loop
                    clientsock.setblocking(0)
                    self.clients.append(clientsock)
                except:
                    print("Unexpected error:", sys.exc_info()[0])
                    pass

        def notify_zone(self, name, **kw):
            self.notify()

        def notify_timer(self):
            threading.Timer(30, self.notify_timer, ()).start()
            self.notify()

        def notify(self):
            print("refreshing TCP clients", self.clients)
            byte = get_byte()
            for clientsock in self.clients:
                clientsock.settimeout(5)
                try:
                    clientsock.send(byte)
                except:
                    print("Unexpected error:", sys.exc_info()[0])
                    print("removing stale connection")
                    self.clients.remove(clientsock)
                    #remove sock
            print("TCP refresh finished")

thread1 = TcpServer()
thread1.start()

