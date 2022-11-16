import cv2
from PIL import Image
from PIL import ImageEnhance
import numpy as np
import matplotlib.pyplot as plt
from numpy import asarray
import sys
from pathlib import Path

input_string = str(sys.argv[1])
img = cv2.imread(input_string,0)
#using gamma correction
def enhance(gamma, img):
    row = img.shape[0]
    col = img.shape[1]
    for i in range(row):
        for j in range(col):
            img[i][j] = ((img[i][j] / 255) ** gamma) * 255
    return img

temp = enhance(0.6,img)
#temp = cv2.GaussianBlur(temp,(3,3),1)
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
    
    
def gauss_blur(img):
    kernel = np.array([[0.075,0.124,0.075],
                        [0.124,0.204,0.124],
                        [0.075,0.124,0.075]])
    blur_img = convolve(img, kernel)
    return blur_img
    
temp = gauss_blur(img)

#using linear transformation for increasing brightness and contrast of the image
def BandC(img,a,b):
    row = img.shape[0]
    col = img.shape[1]
    result = np.zeros(shape = (row,col))
    for i in range(row):
        for j in range(col):
            result[i][j] = img[i][j] * a + b
    result = result.astype(int)
    return result

final = BandC(temp,2,-20)
cv2.imwrite('enhanced-' + input_string, final)
