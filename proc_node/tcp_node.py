
from .msg import Msg



class TCPNode(Node):
    def __init__(self, id):
        super().__init__(id)

    '''
        Turn on (deploy) the node.
    '''
    def start(self):
        super().start()


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
        raise NotImplementedError                                               #      Store info in self.conns dict to map the id to the connection object.
                                                                                #      Make sure you can internally distinguish between tcp and local conns.

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
    def send(self, id, msg):                                                    #TODO: Implement for super version and tcp nodes.
        raise NotImplementedError
        super().send(id, msg)

    '''
        Gets a node msg.
        If block is true, recv will only return when a msg is found, but will continue to update internally.
        If block is false, recv will finish updating and either return a found msg or raise Empty.
    '''
    def recv(self, block = True):                                               #TODO: Implement for super version and tcp nodes.
        raise NotImplementedError
        super().recv(block = block)






#===============================================================================
