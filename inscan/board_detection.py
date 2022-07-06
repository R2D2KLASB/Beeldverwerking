import cv2
import math
from matplotlib.pyplot import hlines
import numpy as np
import scipy.spatial as spatial
import scipy.cluster as cluster
from scipy import ndimage
from collections import defaultdict
from statistics import mean

# # Load image
baord_original = cv2.imread('board.jpeg')
baord_original_resized = cv2.resize(baord_original, (540, 960))

# Get a 2d view of the board


def get_perspective(img, location, height=900, width=900):
    pts1 = np.float32([location[0], location[3], location[1], location[2]])
    pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])

    # Apply Perspective Transform Algorithm
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    result = cv2.warpPerspective(img, matrix, (width, height))
    return result

# Gray_scale + Bilateral + canny filters


def detect_board(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # gaussian_smoothed = scipy.ndimage.convolve(gray_image, gaussian_smooth_mask)
    bilateral_filtered = cv2.bilateralFilter(gray_image, 13, 20, 20)
    canny_filtered = cv2.Canny(bilateral_filtered, 30, 180)
    return canny_filtered

# Hough transformation(array)


def hough_transform(image):
    line_hough = cv2.HoughLines(image, 1, np.pi / 180, 200, None, 0, 0)
    line_hough = np.reshape(line_hough, (-1, 2))
    return line_hough


# filter the vertical and horizontal lines
def line_separator(lines):
    h_lines, v_lines = [], []
    for rho, theta in lines:
        if theta < np.pi / 4 or theta > np.pi - np.pi / 4:
            v_lines.append([rho, theta])
        else:
            h_lines.append([rho, theta])
    return h_lines, v_lines

# check the intersetion of the vertical line and het horizontal line put them in a array


def line_intersections(h_lines, v_lines):
    points = []
    for r_h, t_h in h_lines:
        for r_v, t_v in v_lines:
            a = np.array([[np.cos(t_h), np.sin(t_h)],
                         [np.cos(t_v), np.sin(t_v)]])
            b = np.array([r_h, r_v])
            inter_point = np.linalg.solve(a, b)
            points.append(inter_point)
    return np.array(points)

#  van af hier testen rest werkt
#  Cluster verzameling van intersect points
def cluster_points(points):
    dists = spatial.distance.pdist(points)
    single_linkage = cluster.hierarchy.single(dists)
    flat_clusters = cluster.hierarchy.fcluster(single_linkage, 15, 'distance')
    cluster_dict = defaultdict(list)
    for i in range(len(flat_clusters)):
        cluster_dict[flat_clusters[i]].append(points[i])
    cluster_values = cluster_dict.values()
    clusters = map(lambda arr: (np.mean(np.array(arr)[:, 0]), np.mean(
        np.array(arr)[:, 1])), cluster_values)
    return sorted(list(clusters), key=lambda k: [k[1], k[0]])

# Soortert de cluster in array om ze te gebruiken en te zeten in 2d array
def augment_points(points):
    points_shape = list(np.shape(points))
    augmented_points = []
    for row in range(int(points_shape[0] / 11)):
        start = row * 11
        end = (row * 11) + 10
        rw_points = points[start:end + 1]
        rw_y = []
        rw_x = []
        for point in rw_points:
            x, y = point
            rw_y.append(y)
            rw_x.append(x)
        y_mean = mean(rw_y)
        for i in range(len(rw_x)):
            point = (rw_x[i], y_mean)
            augmented_points.append(point)
    augmented_points = sorted(augmented_points, key=lambda k: [k[1], k[0]])
    return augmented_points

#  image cropper werkt nog niet verder naar kijken later.
def write_crop_images(img, points, img_count=0, folder_path='./Data/raw_data/'):
    num_list = []
    shape = list(np.shape(points))
    start_point = shape[0] - 14

    if int(shape[0] / 11) >= 8:
        range_num = 8
    else:
        range_num = int((shape[0] / 11) - 2)

    for row in range(range_num):
        start = start_point - (row * 11)
        end = (start_point - 8) - (row * 11)
        num_list.append(range(start, end, -1))

    for row in num_list:
        for s in row:
            # ratio_h = 2
            # ratio_w = 1
            base_len = math.dist(points[s], points[s + 1])
            bot_left, bot_right = points[s], points[s + 1]
            start_x, start_y = int(bot_left[0]), int(
                bot_left[1] - (base_len * 2))
            end_x, end_y = int(bot_right[0]), int(bot_right[1])
            if start_y < 0:
                start_y = 0
            cropped = img[start_y: end_y, start_x: end_x]
            img_count += 1
            cv2.imwrite("data/"+  str(img_count) + '.jpeg', cropped)
            # print(folder_path + 'data' + str(img_count) + '.jpeg')
    return img_count


board = detect_board(baord_original_resized)
board_array = hough_transform(board)

# result = hough_draw_lines(board_array, board)

h_line, v_line = line_separator(board_array)
intersect_array = line_intersections(h_line, v_line)
points = cluster_points(intersect_array)
points = augment_points(points)

x_list = write_crop_images(board, points, 0)
# print(points)
cv2.imshow("Board", board)
cv2.waitKey()
