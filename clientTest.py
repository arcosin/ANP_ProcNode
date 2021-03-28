import client , server
 
def main():
    portno =  61619
    id = "client"
    host = "data.cs.purdue.edu"
    message = "Message from client"
    c1 = client.client(portno , id , host)
    c1.sendMsg(message)
    c1.receive()
    
if __name__ == '__main__':
    main()