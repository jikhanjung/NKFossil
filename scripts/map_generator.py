from PIL import Image
import os

def make_transparent(img):
    img = img.convert("RGBA")
    datas = img.getdata()

    newData = []
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    img.putdata(newData)
    return img



# Opens a image in RGB mode
im_src = Image.open(r"data/KoreaGeolMap3.png")
im = im_src.rotate(0.3)

factor = 1.5
orig_width = int( 2066 * factor )
orig_height = int( 2066 * factor )

padding = orig_width

p_width, p_height = im.size
new_width = p_width + 2 * padding
new_height = p_height + 2 * padding
padded_img = Image.new(im.mode, (new_width, new_height), (255,255,255))
padded_img.paste(im, (padding, padding))

# Setting the points for cropped image

orig_left = int( 1483 * factor ) - 4 + padding
orig_bottom = int( 3282 * factor ) + 16 + padding + 3 * padding

right = orig_left + orig_width
top = orig_bottom + orig_height
  
# Cropped image of above dimension
# (It will not change orginal image)
if( not os.path.isdir('map_tiles') ):
    os.mkdir( 'map_tiles' )
for level in range(13,5,-1):
    mult = 2**(13 - level)
    width = orig_width / mult
    height= orig_height / mult
    level_dir = "map_tiles/{0}".format(level)
    print("level:", level)
    if( not os.path.isdir(level_dir) ):
        os.mkdir( level_dir )
    for i in range(2 * mult):
        for j in range(5 * mult):
            left = orig_left + i * width
            right = left + width
            bottom = orig_bottom - j * height
            top = bottom - height
            cropped_image = padded_img.crop((left, top, right, bottom)).resize((256,256))
            transparent_image = make_transparent( cropped_image )
            transparent_image.save("map_tiles/{0}/{1}_{2}.png".format(level,i,j))
            
#im1 = padded_img.crop((left, top, right, bottom)).resize((256,256))
  
# Shows the image in image viewer
#display(im1)