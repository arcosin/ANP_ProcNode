
from queue import Queue, Empty
from multiprocessing import Queue as MPQueue
from multiprocessing.connection import Client as mClient
import socket

 
class Client:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.address = ((self.host, self.port))
        print("Sever Address: "+host+":"+str(port))
        self.conn = None
        self.on = False

    def start(self):
        if self.conn == None:
            print("Connecting to the server")
            self.conn = mClient(self.address)
            print("Server Connected")
        self.on = True

    def stop(self, disconnect = True):
        if disconnect:
            self.conn.close()
            self.conn = None
        self.on = False
    
    def send(self, msg):
        if self.on:
            self.conn.send(msg)

    def recv(self):
        if self.on:
            return self.conn.recv()
    


    

