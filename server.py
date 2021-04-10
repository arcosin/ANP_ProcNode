from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
from collections import defaultdict
from queue import Queue, Empty
from multiprocessing import Queue as MPQueue
from node import Node
import socket
class Server(Node):

    def __init__(self , port , name ,id):
        super().__init__(id)
        self.server = SimpleXMLRPCServer(("data.cs.purdue.edu", port))
        self.item = name
        self.portno = port
        print("Listening on port "+str(port)+" ...")
    
    def image(self):
        with open(self.item, "rb") as handle:
            return handle.read()

    def createProxy(self):
        self.server.register_function(self.image, 'image')

    def start(self):    
        self.msgQueue = Queue()
        self.on = True
        self.server.serve_forever()

      
    def startServer(self):
        HOST = 'data.cs.purdue.edu'
        PORT = self.portno
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            while True:
                (clientsocket, address) = s.accept()
                print (address)
                data = clientsocket.recv(1024)
                print ('client connected')
                print( data)
                self.mssg = data
            
            clientsocket.close()
    

    def returnMsg(self):
        return self.mssg

    
    # def buildClientSocket(self , portno):
    #     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     return s
    
    # def startClient(self, s  , portno):
    #     s.connect(('localhost', portno))
    #     print ("Yeah! I'm connected :")
    #     s.close()