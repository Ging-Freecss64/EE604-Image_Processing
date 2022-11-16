#importing libraries
import cv2
import numpy as np
import matplotlib.pyplot as plt
import PIL as image
import math
import sys

# Note:
# 1. I have assumed that only gray buildings will be fed to my program, as mentioned in the research paper
# 2. I have tried many methods on my own apart from the research paper, but given that the research paper 
# is made after lots of experiments I went with it
# 3. Some of my experiments included converting image into HSV and Lab format and segregrating few classes
# based on channel values

#Reading image
input_string = str(sys.argv[1])
img = cv2.imread(input_string)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

#Calculating important parameters
row = img.shape[0]
col = img.shape[1]
gb = 0
rg = 0
rb = 0
g2rb = 0
for i in range(row):
    for j in range(col):
        gb+=abs(int(img[i][j][1]) - int(img[i][j][2]))
        g2rb+=abs(2 * int(img[i][j][1]) - int(img[i][j][2]) - int(img[i][j][0]))
        rb+=abs(int(img[i][j][0]) - int(img[i][j][2]))
        rg+=abs(int(img[i][j][0]) - int(img[i][j][1]))
#normalising
gb = gb/(row * col)
g2rb = g2rb/(row * col)
rg = rg/(row * col)
rb = rb/(row * col)

#categorising
#1 -> building, 2 -> grass, 3 -> road
#I have used range of values provided in the research paper to estimate the class
#I have observed that it is very easy to classify an image into class 1 and 3, then we can use the else
#for classifying into the last category
if gb >= 0 and gb <= 6.2:
    if g2rb >= 0.8 and g2rb <= 8.2:
        print('1')
    else:
        print('2')
elif gb >= 5.9 and gb <= 20.2:
    if g2rb >= 0 and g2rb <= 12.2:
        print('3')
    else:
        print('2')
else:
    print('2')