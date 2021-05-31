import numpy as np
from skimage.measure import approximate_polygon, find_contours

import cv2
import numpy


img = cv2.imread('SegmentationTest.png', cv2.IMREAD_COLOR)
img.shape
width = img.shape[0]
height = img.shape[1]

color_map = []
image_hash = {}

for i in range(width):
    for j in range(height):
        color_val = "_".join([ str(k) for k in img[i][j]])
        if color_val == '255_255_255':
            continue
        if color_val not in color_map:
            print(color_val)
            color_map.append(color_val)
            new_img = numpy.zeros((width+2,height+2),numpy.uint8)
            image_hash[color_val] = new_img
        image_hash[color_val][i+1][j+1] = 255

#color_map.remove('255_255_255')
print( color_map )

for color_key in color_map:
    cv2.imwrite(color_key+".png",image_hash[color_key])



def process_contour( image, factor=1):

    l_img = image #cv2.imread(img_key + '.png', 0)
    print("image shape:", l_img.shape )
    
    contours = find_contours(l_img, 0)
    result_contour = np.zeros((l_img.shape[0]*factor,l_img.shape[1]*factor)+(3,), np.uint8)
    #result_polygon1 = np.zeros((l_img.shape[0]*2,l_img.shape[1]*2)+(3,), np.uint8)
    #print("contour image shape:", result_contour.shape )

    for contour in contours:
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
        result_contour = cv2.fillPoly(result_contour,pts=np.int32([np_contour]),color=(255,255,255))

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

    return result_contour
    #cv2.imwrite(img_key + '_contour_lines.png', result_contour)
    #cv2.imwrite(img_key + '_polygon1_lines.png', result_polygon1)

processed_image_hash = {}

factor = 2

for k in image_hash.keys():
    print("process:", k)
    processed_image = process_contour( image_hash[k], factor )
    #processed_image_hash[k] = processed_image
    cv2.imwrite(k+"_processed.png",processed_image)


factor = 2

combined_image = numpy.ones((width*factor,height*factor,3),numpy.uint8)*255

white_value = numpy.array([255,255,255])
print(white_value)
for k in image_hash.keys():
    part_image = cv2.imread(k+"_processed.png")
    print(part_image.shape)
    print("processing image for color value:", k )
    #processed_image_hash[k]
    color_val = k.split("_")
    for i in range(width*factor):
        for j in range(height*factor):
            #if "_".join([str(x) for x in part_image[i+1][j+1]]) == "255_255_255":
            #print( part_image[i+1][j+1], type(part_image[i+1][j+1]), white_value, type(white_value))
            if (part_image[i+1][j+1] == white_value).all():
                #print( part_image[i+1][j+1], white_value )
                #break
                combined_image[i][j] = color_val
    cv2.imwrite( "combined.png",combined_image)

cv2.imwrite( "combined.png",combined_image)