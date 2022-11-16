#importing libraries
import cv2
import numpy as np
import matplotlib.pyplot as plt
import PIL as image
import math
import sys

#important functions
def gaussian(sigma, x, y):
    return np.exp(-(x**2 + y**2)/(2 * (sigma**2)))/(2*math.pi*(sigma**2))

def gaussian1(sigma, x):
    return np.exp(-np.power(x,2)/(2 * (sigma**2)))/(2*math.pi*(sigma**2))

def distance(i, j, k, l):
    return math.sqrt((i-k)**2 + (j-l)**2)

def weight(diff, i, j, k, l, sig_s, sig_r):
    one = gaussian(sig_s, distance(i,j,k,l))
    two = gaussian(sig_r, diff)
    return one * two

def gaussKernel(ksize, sig):
    kernel = np.zeros(shape = (ksize, ksize))
    ksize = int(ksize/2)
    W = 0
    for i in range(-ksize,ksize + 1):
        for j in range(-ksize,ksize + 1):
            kernel[i + ksize][j + ksize] = gaussian(sig, i, j)
            W += kernel[i + ksize][j + ksize]
    ksize*=2
    for i in range(ksize+1):
        for j in range(i + 1):
            kernel[i][j]/=W
            kernel[i][j] = kernel[j][i]
    return kernel

def bilateral(img, sig_s, sig_r, ksize, mask, iter, bl):
    row = img.shape[0]
    col = img.shape[1]
    
    neigh = math.floor(ksize / 2)
    kernel = gaussKernel(ksize, sig_s)
    new_img = np.zeros(shape = (row, col), dtype = np.uint8)
    if bl == 1:
        row = int(row / 2) - 40
        new_img = img
    c = 0
    while c < iter:
        for i in range(neigh, row-neigh):
            for j in range(neigh, col-neigh):
                if mask[i][j] == False:
                    new_img[i][j] = img[i][j]
                    continue
                one = np.zeros(shape = (ksize, ksize))
                one.fill(img[i][j])
                two = img[i - neigh : i + neigh + 1, j - neigh : j + neigh + 1]
                diff = np.abs(one - two)
                gauss = gaussian1(sig_r, diff)
                w = np.sum(gauss * kernel)
                summ = np.sum(gauss * kernel * two)
                if w == 0:
                    new_img[i][j] = 0
                else:
                    new_img[i][j] = int(summ / w)
        
        for i in range(neigh):
            new_img[i] = img[i]
            new_img[:,i] = img[:,i]
            new_img[row - i - 1] = img[row - i - 1]
            new_img[:, col - i - 1] = img[:, col - i - 1]

        img = new_img
                    
        c+=1
        
    return new_img 

#Reading image
input_string = str(sys.argv[1])
img = cv2.imread(input_string)

if input_string[7] == '1':
    t = 1
else:
    t = 0

row = img.shape[0]
col = img.shape[1]
#Preprocessing for first image -> creating mask for only sky and certain part of the building
if t == 1:
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_mask = img_hsv [:,:,0] > 90
    upper_mask = img_hsv [:,:,0] < 103.01
    mask = upper_mask*lower_mask

#Preprocessing for second image
else:
    mask = np.ones(shape = (row, col), dtype = bool)

final = np.zeros(shape = (row, col, 3), dtype = np.uint8)
#running first image
if t == 1:
    for i in range(2):
        final[:,:,i] = bilateral(img[:,:,i], 0.3, 80, 3, mask, 25, 0)
else:
    for i in range(2):
        final[:,:,i] = bilateral(img[:,:,i], 0.7, 800, 7, mask, 7, 1)

#no need to apply bilateral filter for third channel on any image
final[:,:,2] = img[:,:,2]

#saving file
cv2.imwrite('denoised.jpg', final)