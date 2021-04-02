from client import Client
from server import Server
from PIL import Image
import time
import picamera
from picamera.array import PiRGBArray
import cv2

def main():
    port =  6000
    server = Server(port)
    server.start()
    width=480
    height=480

    camera =  picamera.PiCamera(
            sensor_mode=7, # https://picamera.readthedocs.io/en/release-1.12/fov.html#camera-modes 
                            # Good to choose mod with binning (Binning increase the readout speed)
                            # Each mod have the minimal resolution recieved from the camera
                            # FoV represent the range of image captured from the camera
                            # If possible it is best to use Full FoV, 2x2 or 4x4 binning (higher = faster), mimimum resolution higher than requirement
                            # frame rates are also limited by each mode
                            # Please check if the camera is v1 or v2
            resolution=str(width)+'x'+str(height),
            framerate=60)
    time.sleep(0.1) # let the camera warm up and set gain/white balance
    stream = PiRGBArray(camera, size=(width, height))

    for frame in camera.capture_continuous(stream,'bgr',use_video_port=True): # https://picamera.readthedocs.io/en/release-1.13/recipes1.html?highlight=start_recording#capturing-to-a-network-stream
            image = frame.array
            server.send(image)
            stream.truncate(0)
    
if __name__ == '__main__':
    main()

