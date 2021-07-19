import numpy as np
from skimage.measure import approximate_polygon, find_contours

import cv2
import numpy

temp_dir = 'data/tmp3/'

#img = cv2.imread('data/KoreaGeolMapLithoOnly2.png', cv2.IMREAD_COLOR)
img = cv2.imread('data/SegmentationTest.png', cv2.IMREAD_COLOR)

img.shape
width = img.shape[0]
height = img.shape[1]

print("width:",width,"height:",height)

color_map = []
image_hash = {}

import time

start = time.time()

def crop_background( a_img ):

    l_grayscale = cv2.cvtColor(a_img, cv2.COLOR_BGR2GRAY)
    #print(type(l_grayscale))

    ret, l_thresholded = cv2.threshold(l_grayscale, 0, 255, cv2.THRESH_OTSU)
    #print(type(l_thresholded))
    #print(ret)

    l_bbox = cv2.boundingRect(l_thresholded)

    l_x, l_y, l_w, l_h = l_bbox

    l_foreground = img[l_y:l_y+l_h, l_x:l_x+l_w]
    #print(type(l_thresholded))
    #print(l_x,l_y,l_w,l_h)
    #cv2.imwrite("data/tmp/thre.png",l_foreground)

    return l_bbox, l_foreground

bbox, foreground = crop_background(~img)
x,y,w,h = bbox


for i in range(y,y+h):
    for j in range(x,x+w):
        color_val = "_".join([ str(k) for k in img[i][j]])
        if color_val == '255_255_255':
            continue
        if color_val not in color_map:
            print(color_val)
            color_map.append(color_val)
            new_img = numpy.zeros((width,height),numpy.uint8)
            image_hash[color_val] = new_img
        image_hash[color_val][i][j] = 255
#color_map.remove('255_255_255')
print( color_map )

end = time.time()
print("elapsed time 1:",end - start)

for color_key in color_map:
    cv2.imwrite(temp_dir+color_key+".png",image_hash[color_key])



def process_contour( image, a_color,factor=1):

    w, h = image.shape[0], image.shape[1]
    print("in image shape:", image.shape )
    l_img = numpy.zeros((w+2,h+2),numpy.uint8)
    l_img[1:-1,1:-1] = image #cv2.imread(img_key + '.png', 0)
    print("working image shape:", l_img.shape )


    contours, hierarchy = cv2.findContours(l_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #contours = find_contours(l_img, 0)

    result_contour = np.zeros((image.shape[0]*factor,image.shape[1]*factor)+(3,), np.uint8)
    #result_polygon1 = np.zeros((l_img.shape[0]*2,l_img.shape[1]*2)+(3,), np.uint8)
    #print("contour image shape:", result_contour.shape )
    #print("contour no:",len(contours),"hierarchy:",hierarchy)
    #return


    for idx in range(len(contours)):
        cnt = contours[idx]
        hi = hierarchy[0][idx]
    #for cnt, hi in contours, hierarchy:
        print("cnt:",len(cnt),type(cnt),hi,type(hi))
        cnt = cnt - 1
        cnt = cnt * factor
        if hi[3] != -1:
            l_color = [0,0,0]
        else:
            l_color = a_color
        
        result_contour = cv2.fillPoly(result_contour,pts=[cnt],color=l_color)
        result_contour = cv2.drawContours(result_contour, [cnt], 0, a_color, 1)  # blue

    """
    for contour in contours:
        print(a_color,contour[0:3])
        #print('Contour shape:', contour.shape)
        #polygon1 = approximate_polygon(contour, tolerance=0.5)

        contour = contour.astype(int).tolist()
        #polygon1 = polygon1.astype(int).tolist()
        #print("length:",len(contour), len(polygon1))

        for idx, coords in enumerate(contour):
            contour[idx] = [ coords[0]*factor,coords[1]*factor ]

        # fill contour
        #print(contour)
        np_contour = np.array(contour,np.int32)
        for idx, coords in enumerate(np_contour):
            np_contour[idx] = [ coords[1],coords[0] ]
        #print(np_contour)
        result_contour = cv2.fillPoly(result_contour,pts=np.int32([np_contour]),color=a_color)

        # draw contour lines
        for idx, coords in enumerate(contour[:-1]):
            #print(idx,coords)
            y1, x1, y2, x2 = coords + contour[idx + 1]
            #print(x1,y1,x2,y2)
            result_contour = cv2.line(result_contour, (x1, y1), (x2, y2),(0, 0, 0), 1)


        # draw polygon 1 lines
        #for idx, coords in enumerate(polygon1[:-1]):
        #    y1, x1, y2, x2 = coords + polygon1[idx + 1]
        #    result_polygon1 = cv2.line(result_polygon1, (x1*2, y1*2), (x2*2, y2*2),
        #                               (0, 255, 0), 1)
    """
    return result_contour
    #cv2.imwrite(img_key + '_contour_lines.png', result_contour)
    #cv2.imwrite(img_key + '_polygon1_lines.png', result_polygon1)

processed_image_hash = {}

factor = 2

for k in image_hash.keys():
    print("process:", k)
    processed_image = process_contour( image_hash[k], [int(x) for x in k.split("_")],factor )
    #processed_image_hash[k] = processed_image
    cv2.imwrite(temp_dir+k+"_processed.png",processed_image)


combined_image = numpy.zeros((width*factor,height*factor,3),numpy.uint8)

white_value = numpy.array([255,255,255])
print(white_value)
idx=1
for k in image_hash.keys():
    part_image = cv2.imread(temp_dir+k+"_processed.png")

    combined_image = cv2.add(combined_image,part_image)
    cv2.imwrite( temp_dir+"combined"+str(idx)+".png",combined_image)
    idx+=1
    continue

    l_bbox, l_foreground = crop_background(part_image)
    l_x,l_y,l_w,l_h = l_bbox
    print(l_bbox)

    print(part_image.shape,combined_image.shape)
    print("processing image for color value:", k )
    #processed_image_hash[k]

    color_val = k.split("_")
    for i in range(l_y,l_y+l_h):
        for j in range(l_x,l_x+l_w):
            #if "_".join([str(x) for x in part_image[i+1][j+1]]) == "255_255_255":
            #print( part_image[i+1][j+1], type(part_image[i+1][j+1]), white_value, type(white_value))
            #print(i,j)#
            if (part_image[i][j] == white_value).all():
                #print( part_image[i+1][j+1], white_value )
                #break
                combined_image[i][j] = color_val
    cv2.imwrite( "data/combined.png",combined_image)

cv2.imwrite( "data/combined.png",combined_image)

end = time.time()
print("total time:",end - start)
