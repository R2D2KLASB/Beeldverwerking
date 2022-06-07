import cv2
import imutils
import numpy as np
import scipy
from scipy import ndimage

# # Load image
baord_original = cv2.imread('border.jpg')
baord_original2 = cv2.imread('border2.jpg')
baord_original3 = cv2.imread('border3.jpg')
boot_original = cv2.imread('boot1_crop.jpg')
boot_original2 = cv2.imread('boot1.jpg')
sudoku = cv2.imread('sudoku1.jpg')

def get_perspective(img, location, height = 800, width = 800):
    loc_index = list(range(4))

    x = 0
    y = 1

    top_left = 0
    top_right = 0
    bot_left = 0
    bot_right = 0
    
    max_sum = location[0][0][x] + location[0][0][y]
    min_sum = location[0][0][x] + location[0][0][y]

    # find top left and bottom right
    for i in loc_index:
        if location[i][0][x] + location[i][0][y] >= max_sum:
            max_sum = location[i][0][x] + location[i][0][y]
            bot_right = i
        if location[i][0][x] + location[i][0][y] <= min_sum:
            min_sum = location[i][0][x] + location[i][0][y]
            top_left = i
    
    # pop index of found loc_index
    if top_left > bot_right:
        loc_index.pop(top_left)
        loc_index.pop(bot_right)
    else:
        loc_index.pop(bot_right)
        loc_index.pop(top_left)

    # find top right and bottom left with the two leftover loc_index
    if location[loc_index[0]][0][y] >= location[loc_index[1]][0][y]:
        bot_left = loc_index[0]
        top_right = loc_index[1]
    else:
        bot_left = loc_index[1]
        top_right = loc_index[0]


    pts1 = np.float32([location[top_left], location[top_right], location[bot_left], location[bot_right]])
    pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])

    # Apply Perspective Transform Algorithm
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    result = cv2.warpPerspective(img, matrix, (width, height))
    return result

def detect_board(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # gaussian_smoothed = scipy.ndimage.convolve(gray_image, gaussian_smooth_mask)
    bilateral_filtered = cv2.bilateralFilter(gray_image, 13, 20, 20)
    canny_filtered = cv2.Canny(bilateral_filtered, 30, 180)
    
    contours, hierarchy = cv2.findContours(canny_filtered.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # contours = imutils.grab_contours(contours)
    contour_image = cv2.drawContours(image = image.copy(), contours = contours, contourIdx = -1, color = (0, 255, 0), thickness = 1)

    cv2.imshow("Board", contour_image)
    cv2.waitKey()

    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:15]
    location = None
    # Finds rectangular contour

    for contour in contours:
        approx = cv2.approxPolyDP(contour, 15, True)
        if len(approx) == 4:
            location = approx
            break
    result = get_perspective(image, location)
    cv2.imshow('board', result)
    cv2.waitKey()
    return result, location

def split_boxes(board):
    """Takes an image of the board and split it into 100 cells (10 x 10).
    each cell contains an element of that board is either occupied or an empty cell."""
    rows = np.vsplit(board,10)
    boxes = []
    for row in rows:
        cols = np.hsplit(row,10)
        for box in cols:
            # cv2.imshow("Splitted block", box)
            # cv2.waitKey()
            boxes.append(box)
    return boxes

def create_2D_field(boxes):
    field = np.arange(100)
    field = field.reshape((10, 10))
    field = np.zeros_like(field)
    index = 0

    for box in boxes:
        total_pixels = len(box) * len(box[0])
        pixels_filled = 0
        blur = cv2.GaussianBlur(box,(5,5),0)
        for y in range(len(box)):
            for x in range(len(box[y])):
                if box[y][x] >= 70:
                    box[y][x] = 255
                else:
                    box[y][x] = 0
                    pixels_filled += 1
        pixel_ratio = ((pixels_filled / total_pixels) * 100)
        if pixel_ratio > 90:
            field[index // 10][index % 10] = 1
        index += 1
        # cv2.imshow('box', box)
        # cv2.waitKey()
    return field

def get_boats(field):
    coorinates_checked = []
    boats = []
    for y in range(len(field)):
        for x in range(len(field[y])):
            length = 1
            if field[y][x] == 1:
                if ([y, x] in coorinates_checked):
                    pass
                else:
                    boat = []
                    coorinates_checked.append([y, x])
                    boat.append([y, x])
                    if field[y + length][x] == 1:
                        while field[y + length][x] == 1:
                            coorinates_checked.append([y + length, x])
                            boat.append([y + length, x])
                            length += 1
                    elif field[y][x + length] == 1:
                        while field[y][x + length] == 1:
                            coorinates_checked.append([y, x + length])
                            boat.append([y, x + length])
                            length += 1
                    boats.append(boat)
    return boats

board, location = detect_board(boot_original)
gray_image = cv2.cvtColor(board, cv2.COLOR_BGR2GRAY)
boxes = split_boxes(gray_image)
field = create_2D_field(boxes)
boat_list = get_boats(field)
# cv2.imshow("Board", board)
# cv2.waitKey()
