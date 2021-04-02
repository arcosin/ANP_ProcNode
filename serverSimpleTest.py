from client import Client
from server import Server
from PIL import Image

def main():
    port =  61619
    s = Server(port)
    s.start()
    name = "Naruto.jpg"
    image = Image.open(name)
    s.send(image)
    message = s.recv()
    print("message from client: ",message)


    
if __name__ == '__main__':
    main()