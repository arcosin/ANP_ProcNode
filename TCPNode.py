from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
from collections import defaultdict
from queue import Queue, Empty
from multiprocessing import Queue as MPQueue
from node import Node
import socket
import client , server, filename


class TCPNode(Node):
    
    def __init__(self, id , object , type ,port):
        super().__init__(id)
        self.portno = 61619
        self.type = type
        self.rname = filename.filename
        if (self.type == "server"):
            self.item = object.attribute
        
        self.host = 'data.cs.purdue.edu'

    def reader(self):
        with open(self.item, "rb") as handle:
            return handle.read()

    def createProxy(self):
        self.server.register_function(self.reader, 'reader')

    def serverStart(self):    
        self.msgQueue = Queue()
        self.on = True
        self.server = SimpleXMLRPCServer(("data.cs.purdue.edu", self.portno))
        print("Listening on port "+str(self.portno)+" ...")
        self.server.serve_forever()

    '''
        Turn on (deploy) the node.
    '''
    def start(self):
        super().start()


    def startTCPServer(self):
        self.server = SimpleXMLRPCServer(("data.cs.purdue.edu", self.portno))
        self.createProxy()
        print("Listening on port "+str(self.portno)+" ...")
        self.server.serve_forever()

    def startTCPClient(self):
        self.proxy = xmlrpc.client.ServerProxy("http://"+ self.host  +":"+str(self.portno)+"/")
    

    '''
        Turn off (undeploy) the node.
    '''
    def stop(self, disconnect = True):
        super().stop()

    '''
        Connect an undeployed node to this one directly through memory.
        If duplex is true, the given node will also be connected to this one.
    '''
    def connectTCP(self, id, host, port):                                       #TODO: add code to connect to a remote TCPNode at host:port.
        self._connectConn(node)

                                                                                #      Store info in self.conns dict to map the id to the connection object.
                                                                                #      Make sure you can internally distinguish between tcp and local conns.

   
    def _connectConn(self, node):
        connRec = self._buildConnRec(node)
        self.conns[node.id] = connRec
        
    
    def _buildConnRec(self, node , type):
        connRec = dict()
        connRec["line"] = node.inputLine
        connRec["type"] = type
        return connRec
   

    def send(self, id, msg):
        self._checkNodeOn()
        try:
            connRec = self.conns[id]
            self._send(connRec, Msg("msg", msg))
        except KeyError:
            raise ValueError("[ProcNode]: Error. ID %s not found." % str(id))

    
    def _send(self, connRec, msg):
        if connRec["type"] == "server":
            HOST = 'data.cs.purdue.edu'
            PORT = self.portno
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect(( HOST, PORT))
                print ("Yeah! I'm connected to  : " + str(self.host))
                sock.sendall(bytes(message , 'utf-8'))
                sock.close()
        
        if connRec["type"] == "client":
            HOST = 'data.cs.purdue.edu'
            PORT = self.portno
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect(( HOST, PORT))
                print ("Yeah! I'm connected to  : " + str(self.host))
                sock.sendall(bytes(message , 'utf-8'))
                sock.close()
            
        else:
            connRec["line"].put(msg)
    '''
        Turn a present connection into a duplex.
    '''
    def duplexify(self, id):                                                    #TODO: All tcp conns are duplexes, so check if id is a tcp node.
        raise NotImplementedError                                               #      If so, ignore the call. else, call super version.
        super().duplexify(id)

    '''
        Disconnect the node from node1 with given id.
        If notify is true, node1 will be instructed to disconnect from this node too.
    '''
    def disconnect(self, id, notify = True):                                    #TODO: If id is a tcp node, disconnect in your own way. else, call super version.
        raise NotImplementedError
        super().disconnect(id, notify = notify)

    '''
        Quickly handle all updates on the inputLine.
        Node msgs are relocated to the msgQueue.
    '''
    def update(self):                                                           #TODO: Implement for super version and tcp nodes.
        raise NotImplementedError
        super().update()

    '''
        Send a node msg to the node indexed by id.
        If the id is not connected, raise a ValueError.
    '''
    # def send(self, id, msg):                                                    #TODO: Implement for super version and tcp nodes.
    #     raise NotImplementedError
    #     super().send(id, msg)

    '''
        Gets a node msg.
        If block is true, recv will only return when a msg is found, but will continue to update internally.
        If block is false, recv will finish updating and either return a found msg or raise Empty.
    '''
    def recv(self, block = True):                                               #TODO: Implement for super version and tcp nodes.
        
        if self.type == "server":
            self.proxy = xmlrpc.client.ServerProxy("http://"+ self.host  +":"+str(self.portno)+"/")
            print("Received from server")
            with open("received_img.jpg", "wb") as handle:
                handle.write((self.proxy.reader()).data)  
        
        elif self.type == "client":
            # ob = (self.proxy.reader()).data
            with open(self.rname, "wb") as handle:
                handle.write((self.proxy.reader()).data)
 
        else:
            super().recv(block = block)






#===============================================================================