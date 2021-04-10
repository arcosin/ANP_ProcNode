import  client , server , TCPNode
 
def main():
    print("start")
    portno =  61619
    name = "Naruto.jpg"
    type = "client"
    id = "B"
    s1 = TCPNode.TCPNode(id , name, type, portno)
    s1.start()
    s1.recv()



    
if __name__ == '__main__':
    main()