from queue import Queue, Empty
from multiprocessing import Queue as MPQueue
from multiprocessing.connection import Listener
import socket, random
from subprocess import getoutput

class Server:

    def __init__(self):
        self.host = getoutput("hostname -I").split()[0]
        while True:
            try:
                self.port = random.randint(1024,65536)
                self.address = ((self.host, self.port))
                self.listener = Listener(self.address) 
                break
            except:
                continue
        print("Sever Address:",self.host,":",self.port)
        self.conn = None
        self.wait = False
        self.on = False

    def start(self):
        if self.conn == None and self.wait == False:
            print("Start Waiting for Client")
            self.wait = True
            self.conn = self.listener.accept()
            self.wait = False
            print("Client Connected from: ",self.listener.last_accepted)
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
    


    

