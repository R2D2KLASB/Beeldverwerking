import cv2
import numpy as np
from matplotlib import pyplot as plt
# Import object + grey scale
img_rgb = cv2.imread('mario_coin.jpg')
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
# import + grey scale img
template = cv2.imread('mario.jpg',0)
# Get hight + widht of img
w, h = template.shape[::-1]

# Search for object's in the img
res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
threshold = 0.8
# locate objects
loc = np.where( res >= threshold)
# Draw box around object positions
for pt in zip(*loc[::-1]):
    cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

cv2.imwrite('res.jpg',img_rgb)
