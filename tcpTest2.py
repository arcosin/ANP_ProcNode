import  client , server , TCPNode ,filename


def main():
    print("start")
    portno =  61619
    name = ""
    type = "client"
    id = "B"
    s1 = TCPNode.TCPNode(id , name, type, portno)
    s1.startTCPClient()
    s1.recv()



    
if __name__ == '__main__':
    main()