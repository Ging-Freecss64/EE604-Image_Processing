from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb
import cv2

img = Image.open("jigsaw.jpg")

width, height = img.size

left = 0
right = width/4 - 9.6
bottom = height/2 - 10
top = 0
left_top = img.crop((left,top,right,bottom))

left = 0
right = width/4 - 8.8
bottom = height - 10.6
top = height/2 - 11
left_bottom = img.crop((left,top,right,bottom))

left = width * 4 / 6 - 16.8
right = width - 96.5
bottom = height - 90
top = height/3 + 9.3
right_top = img.crop((left,top,right,bottom))

left = width / 2 - 29
right = width
bottom = height
top = height - 51.5
right_bottom = img.crop((left,top,right,bottom))

right_bottom = img.crop((left,top,right,bottom))

left_bottom = left_bottom.transpose(Image.Transpose.ROTATE_180)

left_bottom = left_bottom.transpose(Image.Transpose.FLIP_LEFT_RIGHT)

right_top = right_top.transpose(Image.Transpose.FLIP_LEFT_RIGHT)

right_bottom = right_bottom.transpose(Image.Transpose.FLIP_TOP_BOTTOM)

bird = np.array(left_top)

hsv_bird = cv2.cvtColor(bird, cv2.COLOR_RGB2HSV)
hue = hsv_bird[:,:,0]

h = 160
t = 5
min_hue = np.array([h - t])
max_hue = np.array([h + t])
mask_hue = cv2.inRange(hue, min_hue, max_hue)
inv_mask = cv2.bitwise_not(mask_hue)

hue[mask_hue > 0] = hue[mask_hue > 0] + 36
hue[inv_mask > 0] = hue[inv_mask > 0] + 20

h = 185
t = 5
min_hue = np.array([h - t])
max_hue = np.array([h + t])

mask_hue = cv2.inRange(hue, min_hue, max_hue)
hue[mask_hue > 0] = hue[mask_hue > 0] + 8.2

h = 147
t = 5
min_hue = np.array([h - t])
max_hue = np.array([h + t])

mask_hue = cv2.inRange(hue, min_hue, max_hue)

hue[mask_hue > 0] = hue[mask_hue > 0] + 170

hh = hsv_bird
hh[:,:,0] = hue

imt = cv2.cvtColor(hh, cv2.COLOR_HSV2RGB)
im = Image.fromarray(imt)

img.paste(im, (0,200))
img.paste(left_bottom)
img.paste(right_bottom, (370,370))
img.paste(right_top, (515,150))

left = 0
right = width/4 - 9.6
bottom = height - 21
top = height - 26
up = img.crop((left,top,right,bottom))
bottom = height - 6
top = height - 11
dw = img.crop((left,top,right,bottom))

imd = dw.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
imu = up.transpose(Image.Transpose.FLIP_TOP_BOTTOM)

img.paste(imu, (0,height-21))
img.paste(imd, (0,height-16))

#right = width/4 - 10
#left = right - 2
#bottom = height
#top = 0
#temp = img.crop((left,top,right,bottom))
#img.paste(temp, (190,0))

img.save('jigsolved.jpg')
