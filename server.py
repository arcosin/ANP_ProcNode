from queue import Queue, Empty
from multiprocessing import Queue as MPQueue
from multiprocessing.connection import Listener
import socket
from subprocess import getoutput

class Server:

    def __init__(self, port):
        self.host = getoutput("hostname -I").split()[0]
        self.address = ((self.host, port))
        self.port = port
        print("Sever Address: "+socket.gethostbyname(socket.gethostname())+":"+str(port))
        self.listener = Listener(self.address) 
        self.conn = None

    def start(self):
        if self.conn == None:
            print("Start Waiting for Client")
            self.conn = self.listener.accept()
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
    


    

