
import io
import cv2
import numpy as np
from base64 import b64encode
import os
from ament_index_python.packages import get_package_share_directory
from svg_to_gcode.svg_parser import parse_file
from svg_to_gcode.compiler import Compiler, interfaces
import simp

def svg2gcode(path, name):
    gcode_compiler = Compiler(interfaces.Gcode, movement_speed=100, cutting_speed=100, pass_depth=0)

    curves = parse_file(path + "/" + name) # Parse an svg file into geometric curves

    gcode_compiler.append_curves(curves) 
    gcode_compiler.compile_to_file(path + "/" + "tmp.gcode", passes=2)


## IMAGE EDITOR ##

def encode(image):
    return b64encode(cv2.imencode('.svg', image).tobytes())

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
    
    # Save Image
    cv2.imwrite(rp + '/tmp.bmp', countoursImage)

    # BMP TO SVG
    os.system("potrace " + rp + "/tmp.bmp --svg -o" + rp + "/tmp.svg")

    # SVG TO GCODE
    svg2gcode(rp, 'tmp.svg')

    with open(rp + "/" + 'tmp.svg', "r") as image_file:
        image = image_file.read()

    with open(rp + "/" + 'tmp.gcode', "r") as gcode_file:
        gcode = gcode_file.read()

    #Return Image and Gcode
    return {
        'image': image,
        'gcode': gcode,
    }