
import cv2
import numpy as np
from base64 import b64encode
  
## IMAGE EDITOR ##

def encode(image):
    return b64encode(cv2.imencode('.jpg', image)[1].tobytes())

def editImage(image):
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