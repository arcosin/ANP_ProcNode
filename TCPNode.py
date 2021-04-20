from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
from collections import defaultdict
from queue import Queue, Empty
from multiprocessing import Queue as MPQueue
from node import Node
import socket
import client , server, filename , CustomObject as c1
from collections import namedtuple


class TCPNode(Node):
    
    def __init__(self, id , object , type ,port):
        super().__init__(id)
        self.portno = port
        self.type = type
        self.rname = filename.filename
        self.host = 'data.cs.purdue.edu'
        self.object = object

    def reader(self):
        return self.object

    def createProxy(self):
        self.server.register_function(self.reader, 'reader')

   
    def serverStart(self):    
        self.server = SimpleXMLRPCServer((self.host, self.portno))
        self.createProxy()
        print("Listening on port "+str(self.portno)+" ...")
        self.server.handle_request()

    '''
        Turn on (deploy) the node.
    '''
    def start(self):
        super().start()


    def startTCPServer(self):
        self.server = SimpleXMLRPCServer(("data.cs.purdue.edu", self.portno))
        # self.createProxy()
        # print("Listening on port "+str(self.portno)+" ...")
        # self.server.handle_request()

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
    def connectTCP(self, node):                                       #TODO: add code to connect to a remote TCPNode at host:port.
        self._connectConn(node)

                                                                                #      Store info in self.conns dict to map the id to the connection object.
                                                                                #      Make sure you can internally distinguish between tcp and local conns.
 
   
    def _connectConn(self, node):
        connRec = self._buildConnRec(node)
        self.conns[node.id] = connRec
        
    
    def _buildConnRec(self, node ):
        connRec = dict()
        connRec["line"] = node.inputLine
        connRec["type"] = node.type
        return connRec
   

    def send(self, id, msg):
        self._checkNodeOn()
        try:
            connRec = self.conns[id]
            self._send(connRec, msg)
        except KeyError:
            raise ValueError("[ProcNode]: Error. ID %s not found." % str(id))


    def _send(self, connRec, msg):
        if connRec["type"] == "TCP":
            self.object = msg
            self.createProxy()
            print("Listening on port "+str(self.portno)+" ...")
            self.server.handle_request()
        
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
        print("IN NODE :"+str(self.id))
        flag = 0
        if self.type == "TCP":
            self.proxy = xmlrpc.client.ServerProxy("http://"+ self.host  +":"+str(self.portno)+"/")
            dictionary = self.proxy.reader()
            a1 = c1.CustomObject(**dictionary) 
            print(a1.returnList())
            print(a1.returnStr())
            print(a1.returnDic())
              

        else:
            super().recv(block = block)










#===============================================================================