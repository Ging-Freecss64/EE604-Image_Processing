import cv2
import numpy as np
from PIL import Image
from PIL import ImageEnhance
import matplotlib.pyplot as plt
from numpy import asarray
import sys

input_string = str(sys.argv[1])

img = cv2.imread(input_string)

#a failed attempt to write gaussian blur function
def padding(img, size):
    row = img.shape[0]
    col = img.shape[1]
    new_img = np.zeros(shape = (row + size, col + size))
    size = int(size/2)
    for i in range(size,row+size):
        for j in range(size,col+size):
            new_img[i][j] = img[i-size][j-size]
    new_img = new_img.astype(int)
    return new_img
    
def convolve(img, kernel):
    row = img.shape[0]
    col = img.shape[1]
    temp_img = padding(img, kernel.shape[0] - 1)
    result = np.zeros(shape = (row, col))
    size = kernel.shape[0]
    for i in range(row):
        for j in range(col):
            matrix = temp_img[i:i+size,j:j+size]
            result[i][j] = np.sum(np.multiply(matrix,kernel))
    return result
    
    
def gauss_blur(img, gamma, ksize):
    kernel = np.array([[0.00291502, 0.01306423, 0.02153928, 0.01306423, 0.00291502],
[0.01306423, 0.05854983, 0.09653235, 0.05854983, 0.01306423],
[0.02153928, 0.09653235, 0.15915494, 0.09653235, 0.02153928],
[0.01306423, 0.05854983, 0.09653235, 0.05854983, 0.01306423],
[0.00291502, 0.01306423, 0.02153928, 0.01306423, 0.00291502]])
    blur_img = convolve(img, kernel)
    return blur_img
    
#result = gauss_blur(img,157,5)

#creating pseudo self-image that cast shadows of greed-ego
result = cv2.GaussianBlur(img,(201,201),31)

row = img.shape[0]
col = img.shape[1]

#following the enlightened beings like Buddha
tt = np.zeros(shape = (row, col, 3))
for i in range(row):
    for j in range(col):
        for k in range(3):
            tt[i][j][k] = 1.0 * (1/result[i][j][k]) * img[i][j][k]
            
#enhancing our spirit
tt = cv2.normalize(tt,None, alpha=50, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)

def adjust_brightness(input_image, factor):
    enhancer_object = ImageEnhance.Brightness(input_image)
    out = enhancer_object.enhance(factor)
    return out

tt = Image.fromarray(tt)
tt = adjust_brightness(tt, 1.1)
tt = asarray(tt)
cv2.imwrite('cleaned-gutter.jpg', tt)
