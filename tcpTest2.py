import  client , server , TCPNode ,filename


def main():
    print("start")
    portno =  61619
    name = ""
    type = "TCP"
    id = "B"
    s1 = TCPNode.TCPNode(id , name, type, portno)
    # s1.serverStart()
    s1.recv()
    # s1.recv()
    


    
if __name__ == '__main__':
    main()