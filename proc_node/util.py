
import multiprocessing

try:
    from setproctitle import setproctitle
    PROCTITLE_LOADED = True
except ImportError:
    PROCTITLE_LOADED = False



def connectAll(nodeList):
    for i in range(len(nodeList)):
        for j in range(len(nodeList)):
            if i != j:
                nodeList[i].connect(nodeList[j], duplex = False)



def setProcName(name):
    if PROCTITLE_LOADED:
        setproctitle(name)
        return True
    else:
        return False



def buildNodeProcess(node, target, group = None, name = None, argDict = dict(), daemon = None):
    a = (node, argDict)
    pr = multiprocessing.Process(group = group, target = target, name = name, args = a, daemon = daemon)
    return pr





#===============================================================================
