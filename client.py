import xmlrpc.client
from collections import defaultdict
from queue import Queue, Empty
from multiprocessing import Queue as MPQueue
import socket  # import socketserver preinstalled module
import http.server
from node import Node

class client(Node):
    
    def __init__(self , port , id , host):
        super().__init__(id)
        self.portno = port
        self.host = host

     
    def receive(self):
        self.proxy = xmlrpc.client.ServerProxy("http://"+ self.host  +":"+str(self.portno)+"/")
        print("Received from server")
        with open("received_img.jpg", "wb") as handle:
            handle.write((self.proxy.image()).data)  
 

    def returnMsg(self):
        return self.mssg

    
    def sendMsg(self , message):
        HOST = 'data.cs.purdue.edu'
        PORT = self.portno
    
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect(( HOST, PORT))
            print ("Yeah! I'm connected to  : " + str(self.host))
            sock.sendall(bytes(message , 'utf-8'))
            sock.close()