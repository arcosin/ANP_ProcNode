import  client , server , TCPNode , filename , util ,time

import multiprocessing




def procBCode(node):                                     # Echo process.
    node.start()
    node.recv()
    node.recv()
   

def procCCode(node):                                     # Echo process.
    node.start()
    print("\n\n")
    node.recv()
    # node.startTCPServer()
   

def procACode(node , _):                                        # User process.
    node.start()
    node.startTCPServer()
    node.send("B", "SENDING IPC MESSAAGE")
    node.send("B" , filename.obj)
    node.send("C" , "FROM A TO C")
    
    # node.stop()


def main():
    print("start")
    portno =  61619  
    I1 = filename.obj
    type = "server"
    id = "A"
    msg = "This was sent by the server"
    
    s1 = TCPNode.TCPNode(id , I1, type, portno)
    s2 = TCPNode.TCPNode("B", None ,"TCP",portno)
    s3 = TCPNode.TCPNode("C", None ,"TCP",portno)
    s1.connectTCP(s2)
    s1.connectTCP(s3)
    s3.connectTCP(s1)

    
    pb = util.buildNodeProcess(s1 , procACode)       # Make process A with this utility function.
    pb.start()                                    # Start process A.
    time.sleep(0.5)                               # Wait a bit to make sure pb is set up before we start A code.
    procBCode(s2)                              # Start process B code.
    procCCode(s3)



def func():
    return copy
   




if __name__ == '__main__':
    main()