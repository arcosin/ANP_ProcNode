
from collections import defaultdict
from queue import Queue, Empty
from multiprocessing import Queue as MPQueue

from .msg import Msg




class NodeEmpty(Exception):
    pass

class NodeOff(Exception):
    pass


class Node:
    def __init__(self, id):
        super().__init__()
        self.id = id
        self.inputLine = MPQueue()
        self.conns = dict()
        self.msgQueue = None
        self.on = False

    '''
        Turn on (deploy) the node.
    '''
    def start(self):
        self.msgQueue = Queue()
        self.on = True

    '''
        Turn off (undeploy) the node.
    '''
    def stop(self, disconnect = True):
        if disconnect:
            for id in list(self.conns.keys()):
                self.disconnect(id, notify = False)
        self.msgQueue = None
        self.on = False

    '''
        Connect an undeployed node to this one directly through meemory.
        If duplex is true, the given node will also be connected to this one.
    '''
    def connect(self, node, duplex = True):
        self._connectConn(node)
        if duplex:
            node._connectConn(self)

    '''
        Connect an undeployed node to a neighbor node directly through meemory.
    '''
    def connectIndexed(self, node, id):
        try:
            indexedRec = self.conns[id]
            node.conns[id] = indexedRec
        except KeyError:
            raise ValueError("[ProcNode]: Error. ID %s not found." % str(id))

    '''
        Connect a neibor node (id1) to another (id2) through connection line.
        If duplex is true, node 2 will also be connected to node 1.
    '''
    def connectProxy(self, id1, id2, duplex = True):
        try:
            connRec1 = self.conns[id1]
            connRec2 = self.conns[id2]
            msg = (id2, connRec2)
            self._send(connRec1, Msg("conn", msg))
            if duplex:
                msg = (id1, connRec1)
                self._send(connRec2, Msg("conn", msg))
        except KeyError:
            raise ValueError("[ProcNode]: Error. IDs (%s, %s) not found." % (str(id1), str(id2)))

    '''
        Turn a present connection into a duplex.
    '''
    def duplexify(self, id):
        try:
            indexedRec = self.conns[id]
            msg = (self.id, self._buildConnRec(self))
            self._send(indexedRec, Msg("conn", msg))
        except KeyError:
            raise ValueError("[ProcNode]: Error. ID %s not found." % str(id))

    '''
        Disconnect the node from node1 with given id.
        If notify is true, node1 will be instructed to disconnect from this node too.
    '''
    def disconnect(self, id, notify = True):
        try:
            oldRec = self.conns.pop(id)
            if notify:
                self._send(oldRec, Msg("disc", self.id))
        except KeyError:
            raise ValueError("[ProcNode]: Error. ID %s not found." % str(id))

    '''
        Return a list of all currently connected node IDs.
    '''
    def listConnectedNodes(self):
        return list(self.conns.keys())

    '''
        Quickly handle all updates on the inputLine.
        Node msgs are relocated to the msgQueue.
    '''
    def update(self):
        self._checkNodeOn()
        while not self.inputLine.empty():
            m = self._tryGet(self.inputLine)
            if m is not None:
                self._update(m)
            else:
                break

    '''
        Send a node msg to the node indexed by id.
        If the id is not connected, raise a ValueError.
    '''
    def send(self, id, msg):
        self._checkNodeOn()
        try:
            connRec = self.conns[id]
            self._send(connRec, Msg("msg", msg))
        except KeyError:
            raise ValueError("[ProcNode]: Error. ID %s not found." % str(id))

    '''
        Gets a node msg.
        If block is true, recv will only return when a msg is found, but will continue to update internally.
        If block is false, recv will finish updating and either return a found msg or raise Empty.
    '''
    def recv(self, block = True):
        self._checkNodeOn()
        if block:
            self.update()
            m = self._tryGet(self.msgQueue)
            if m is not None:
                return m.data
            while True:
                m = self.inputLine.get()
                self._update(m)
                m = self._tryGet(self.msgQueue)
                if m is not None:
                    return m.data
        else:
            self.update()
            m = self._tryGet(self.msgQueue)
            if m is not None:
                return m.data
            else:
                raise NodeEmpty()

    def _connectConn(self, node):
        connRec = self._buildConnRec(node)
        self.conns[node.id] = connRec

    def _tryGet(self, q):
        try:
            m = q.get(block = False)
            return m
        except Empty:
            return None

    def _update(self, msg):
        if msg.type == "msg":
            self.msgQueue.put(msg)
        elif msg.type == "conn":
            id, rec = msg.data
            self.conns[id] = dict(rec)
        elif msg.type == "disc":
            id = msg.data
            self.conns.pop(id, None)

    def _send(self, connRec, msg):
        if connRec["type"] == "proc":
            connRec["line"].put(msg)

    def _buildConnRec(self, node):
        connRec = dict()
        connRec["line"] = node.inputLine
        connRec["type"] = "proc"
        return connRec

    def _checkNodeOn(self):
        if not self.on:
            raise NodeOff("[ProcNode]: Node is turned off.")




#===============================================================================
