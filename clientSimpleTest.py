from client import Client
from server import Server

def main():
    host = "127.0.1.1"
    port =  61619
    c = Client(host, port)
    c.start()
    image = c.recv()
    image.show()
    c.send(b"Hi Server Image is well recieved")


    
if __name__ == '__main__':
    main()