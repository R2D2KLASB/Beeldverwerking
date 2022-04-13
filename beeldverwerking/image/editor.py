
import io
import cv2
import numpy as np
from base64 import b64encode, b64decode
import os
from ament_index_python.packages import get_package_share_directory
import beeldverwerking.image.gcode as gcode

def encode(image):
    retval, buffer = cv2.imencode('.jpg', image)
    return b64encode(buffer)

def decode(image):
    image = np.fromstring(b64decode(image), np.uint8)
    return cv2.imdecode(image,cv2.IMREAD_COLOR)

## IMAGE TO EDGE ##
def imageToEdge(image):
    try:
        if isinstance(image, io.BufferedReader):
            image = np.asarray(bytearray(image.read()), dtype=np.uint8)
        else:
            image = np.fromstring(image, np.uint8)

        # ROS2 Package path
        rp = get_package_share_directory('beeldverwerking')

        image = cv2.imdecode(image,cv2.IMREAD_COLOR)

        #Make Image Gray
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
        #Canny Edge Detection
        image = cv2.Canny(image, 30, 200)

        #Invert Image
        image = (255-image)

        #Threshold
        ret, image = cv2.threshold(image, 1, 255, cv2.THRESH_OTSU)

        image = image

        #Find Contours
        contours, heirarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        cv2.drawContours(image, contours, -1, (0,255,0), 1)
        
        return encode(image)
    except:
        return False
    


# Edge TO SVG
def edgeToSVG(image):
    try:
        image = decode(image)

        # ROS2 Package path
        rp = get_package_share_directory('beeldverwerking')
        
        # Save Image
        cv2.imwrite(rp + '/tmp.bmp', image)

        # BMP TO SVG
        os.system("potrace " + rp + "/tmp.bmp --svg -o" + rp + "/tmp.svg")

        with open(rp + "/" + 'tmp.svg', "r") as image_file:
            image = image_file.read()

        return image, rp, 'tmp.svg'
    
    except:
        return False