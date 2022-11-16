import cv2
import numpy as np
from PIL import Image
from PIL import ImageEnhance
import matplotlib.pyplot as plt
from numpy import asarray
import math
import sys
from pathlib import Path

input_string = str(sys.argv[1])
img = cv2.imread(input_string)
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#defination of the required functions
#1. dilation
def dilation(img):
    row = img.shape[0]
    col = img.shape[1]
    arr = np.zeros(shape = (row, col))
    dx = np.array([0,0,1,1,1,-1,-1,-1])
    dy = np.array([1,-1,0,1,-1,0,1,-1])
    for i in range(1,row-1):
        for j in range(1,col-1):
            count = 0
            for k in range(8):
                if img[i + dx[k]][j + dy[k]] == 255:
                    count += 1
            if count > 0:
                arr[i][j] = 255
    arr = arr.astype(int)
    return arr

#2. subtraction
def subtract(img1, img2):
    row = img.shape[0]
    col = img.shape[1]
    arr = np.zeros(shape = (row, col))
    for i in range(row):
        for j in range(col):
            arr[i][j] = abs(img1[i][j] - img2[i][j])
    arr = arr.astype(int)
    return arr
    
#3. radian conversion
def rad(x):
    return (x * math.pi)/180

#smothening filter
#The code I have written for gaussian blur was giving unnecessary boundary in the final image, i couldn't figure out the real reason behing it so used the library function
smooth = cv2.GaussianBlur(gray_img,(7,7),1.5)
#why using adaptive thresholding?
#As we were taught codes for only global thresholding methods which weren't good for the given images, but using adaptive thresholding was giving really good results so I've used cv2 library for that
img_thresh = cv2.adaptiveThreshold(smooth, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 8)
kernel = np.array([[1,1,1],[1,1,1],[1,1,1]])
dilated_img = dilation(img_thresh) #increases bright area according to kernel
diff = subtract(dilated_img, img_thresh)
thresh = 255 - diff

row = thresh.shape[0]
col = thresh.shape[1]
diag = int(math.sqrt(row**2 + col**2)) + 50 #maximum size of parameter rho

accum = np.zeros(shape = (360, diag))#initialising accumulator function
for i in range(row):
    for j in range(col):
        if thresh[i][j] == 0:
            for k in range(360):
                val = i * math.cos(rad(k-180)) + j * math.sin(rad(k-180))
                if val > 0 and val < diag:
                    accum[k][int(val)]+=1

accum_norm = cv2.normalize(accum, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)#normalize to fit our condtn
row = img.shape[0]
col = img.shape[1]

for i in range(360):
    for j in range(diag):
        if accum_norm[i][j] >= 255*0.38:
            a = math.cos(rad(i-180))
            b = math.sin(rad(i-180))
            rho = j
            for k in range(row):
                for l in range(col):
                    val = a * k + b * l
                    if val >= rho - 0.6 and val <= rho + 0.6:
                        img[k][l][0] = 0
                        img[k][l][1] = 0
                        img[k][l][2] = 255
                        
cv2.imwrite('robolin-' + input_string + '.jpg', img)
