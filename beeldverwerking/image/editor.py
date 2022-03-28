
import io
import cv2
import numpy as np
from base64 import b64encode
import os
from ament_index_python.packages import get_package_share_directory

## IMAGE EDITOR ##

def encode(image):
    return b64encode(cv2.imencode('.jpg', image)[1].tobytes())

def editImage(image):
    if isinstance(image, io.BufferedReader):
        image = np.asarray(bytearray(image.read()), dtype=np.uint8)
    else:
        image = np.fromstring(image, np.uint8)
    image = cv2.imdecode(image,cv2.IMREAD_COLOR)
    oldImage = image

    #Make Image Gray
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  
    #Canny Edge Detection
    image = cv2.Canny(gray, 30, 200)

    #Invert Image
    image = (255-image)

    #Threshold
    ret, thresh = cv2.threshold(image, 1, 255, cv2.THRESH_OTSU)

    countoursImage = thresh

    #Find Contours
    contours, heirarchy = cv2.findContours(countoursImage, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    cv2.drawContours(countoursImage, contours, -1, (0,255,0), 2)

    # ROS2 Package path
    rp = get_package_share_directory('beeldverwerking')
    

    cv2.imwrite(rp + '/tmp.bmp', countoursImage)

    os.system("potrace " + rp + "/tmp.bmp --svg -o" + rp + "/tmp.svg")

    #Return Images
    return [{
        'name': 'old',
        'image': oldImage,
        'jpg': encode(oldImage)
    },
    {
        'name': 'new',
        'image': image,
        'jpg': encode(image)
    },
    {
        'name': 'contours',
        'image': countoursImage,
        'jpg': encode(countoursImage)
    }]