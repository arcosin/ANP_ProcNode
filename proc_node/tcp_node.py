
from .msg import Msg
from .node import Node
from .server import Server
from .client import Client
import threading

class NodeEmpty(Exception):
    pass

class TCPNode(Node):
    def __init__(self, id, isServer = True):
        super().__init__(id)
        self.server = None
        self.client = None
        # self.tcpOn = False
        if isServer:
            self.server = Server()
            # threading.Thread(target=self.serverWait)


    def serverWait(self):
        self.server.start()
        while True:
            if self.tcpUpdate():
                break
        # self.tcpOn = True
        

    '''
        Turn on (deploy) the node.
    '''
    def start(self):
        super().start()
        if self.server != None:
            self.serverWait()


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
        if self.server == None:
            try:
                self.client = Client(host, port)
                self.client.start()
                self.conns[id] = self.client
                self.client.send(Msg("conn",self.id))
            except:
                print("fail to connect to server",host,":",port)
        else:
            print("connectTCP method is for non-server object")

    '''
        Turn a present connection into a duplex.
    '''
    def duplexify(self, id):                                                    #TODO: All tcp conns are duplexes, so check if id is a tcp node.
        if not isinstance(self.conns[id],Client) and not isinstance(self.conns[id],Server):                                      #      If so, ignore the call. else, call super version.
            super().duplexify(id)

    '''
        Disconnect the node from node1 with given id.
        If notify is true, node1 will be instructed to disconnect from this node too.
    '''
    def disconnect(self, id, notify = True):                                    #TODO: If id is a tcp node, disconnect in your own way. else, call super version.
        if not isinstance(self.conns[id],Client) and not isinstance(self.conns[id],Server):
            super().disconnect(id, notify = notify)
        else:
            self.conns[id].stop()

    '''
        Quickly handle all updates on the inputLine.
        Node msgs are relocated to the msgQueue.
    '''
    def update(self):                                                           #TODO: Implement for super version and tcp nodes.
        super().update()

    def tcpUpdate(self):
        msg = None
        # print(self.id,"waiting for recv")
        if self.server != None:
            try:
                msg = self.server.recv()
            except:
                pass
        if self.client != None:
            try:
                msg = self.client.recv()
            except:
                pass
        # print(self.id,"recv msg")
        if msg != None:
            # print(self.id," got message ",msg.type)
            if msg.type == "msg":
                self.msgQueue.put(msg)
            if msg.type == "conn":
                id = msg.data
                self.conns[id] = self.server
                return True
        return False


    '''
        Send a node msg to the node indexed by id.
        If the id is not connected, raise a ValueError.
    '''
    def send(self, id, msg):                                                    #TODO: Implement for super version and tcp nodes.
        # print(id,self.conns[id])
        if isinstance(self.conns[id],Server):
            # print(self.id,"server sent msg",msg)
            self.server.send(Msg("msg",msg))
        elif isinstance(self.conns[id],Client):
            # print(self.id,"client sent msg",msg)
            self.client.send(Msg("msg",msg))
        else:
            # print(self.id,"sent msg",msg)
            super().send(id, msg)

    '''
        Gets a node msg.
        If block is true, recv will only return when a msg is found, but will continue to update internally.
        If block is false, recv will finish updating and either return a found msg or raise Empty.
    '''
    def recv(self, block = True):                                               #TODO: Implement for super version and tcp nodes.
        super()._checkNodeOn()
        if block:
            self.update()
            # if self.tcpOn:
            if self.tcpUpdate():
                return
            m = super()._tryGet(self.msgQueue)
            if m is not None:
                # print(self.id,"data:",m.data)
                return m.data
            while True:
                m = self.inputLine.get()
                super()._update(m)
                # if self.tcpOn:
                if self.tcpUpdate():
                    return
                m = super()._tryGet(self.msgQueue)
                if m is not None:
                    # print("data:",m.data)
                    return m.data
        else:
            self.update()
            # if self.tcpOn:
            if self.tcpUpdate():
                return
            m = super()._tryGet(self.msgQueue)
            if m is not None:
                # print("data:",m.data)
                return m.data
            else:
                raise NodeEmpty()






#===============================================================================
