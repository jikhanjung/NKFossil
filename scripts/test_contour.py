import numpy as np
from skimage.measure import approximate_polygon, find_contours

import cv2
import numpy


img = cv2.imread('data/contour_test.png', cv2.IMREAD_COLOR)
result_contour = np.zeros((img.shape[0],img.shape[1])+(3,), np.uint8)

imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(imgray,125,255,0)

contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
print(contours)
print(hierarchy)

for idx in range(len(contours)):
    cnt = contours[idx]
    hi = hierarchy[0][idx]
    a_color = [255,255,255]
    border_color = a_color
    if hi[3] != -1:
        fill_color = [0,0,0]
    else:
        fill_color = a_color

    result_contour = cv2.fillPoly(result_contour,pts=[cnt],color=fill_color)

    result_contour = cv2.drawContours(result_contour, [cnt], 0, border_color, 1)  # blue

cv2.imwrite( "data/contour_test_result.png",result_contour)
