from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
from collections import defaultdict
from queue import Queue, Empty
from multiprocessing import Queue as MPQueue
from node import Node
import socket
import client , server, filename
import pickle
import os

with open("ans.pickle", "rb") as f:
    # The protocol version used is detected automatically, so we do not
    # have to specify it.
    abc = pickle.load(f)
    print(abc.arr)