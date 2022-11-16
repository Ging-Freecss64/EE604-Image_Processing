#importing libraries
import cv2
import numpy as np
import matplotlib.pyplot as plt
import PIL as image
import math
import sys

#reading arguments
inputY = str(sys.argv[1])
inputCb = str(sys.argv[2])
inputCr = str(sys.argv[3])

#reading images as gray values since we only need one channel of information
Y = cv2.imread(inputY,0)
Cb = cv2.imread(inputCb,0)
Cr = cv2.imread(inputCr,0)

#Defining important libraries
def gaussian(sigma, x, y):
    return np.exp(-(x**2 + y**2)/(2 * (sigma**2)))/(2*math.pi*(sigma**2))

def gaussian1(sigma, x):
    return np.exp(-np.power(x,2)/(2 * (sigma**2)))/(2*math.pi*(sigma**2))

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

def resize(img, factor):
    r = img[:,:]
    row = img.shape[0]
    col = img.shape[1]
    new_img = np.zeros(shape = (int(row * factor), int(col * factor)))
    k = 0
    i = 0
    while i < row * factor:
        j = 0
        l = 0
        while j < col * factor:
            for m in range(factor):
                for n in range(factor):
                    new_img[i + m][j + n] = img[k][l]
            j += factor
            l += 1
        i += factor
        k += 1
    
    return new_img

def bilateral(S, imgBar, sig_s, sig_r, ksize):
    row = S.shape[0]
    col = S.shape[1]
    
    neigh = math.floor(ksize / 2)
    kernel = gaussKernel(ksize, sig_s)

    new_img = np.zeros(shape = (row, col), dtype = np.uint8)
    
    for i in range(neigh, row-neigh):
        for j in range(neigh, col-neigh):
            
            
            one = np.zeros(shape = (ksize, ksize), dtype = np.uint8)
            one.fill(imgBar[i][j])
            two = imgBar[i-neigh : i+neigh + 1, j-neigh : j+neigh + 1]
            three = S[i-neigh : i+neigh + 1, j-neigh : j+neigh + 1]
            diff = np.abs(one - two)
            gauss = gaussian1(sig_r, diff)
            w = np.sum(gauss * kernel)
            summ = np.sum(gauss * kernel * three)
            if w == 0:
                new_img[i][j] = 0
            else:
                new_img[i][j] = int(summ / w)
    for i in range(neigh):
        new_img[i] = S[i]
        new_img[:,i] = S[:,i]
        new_img[row - i - 1] = S[row - i - 1]
        new_img[:, col - i - 1] = S[:, col - i - 1]
        
    return new_img       

#The idea which I have used here is to double the small image and half the large image and apply bilateral filter using large image as guide to estimate the lost informations
def upsampler(small, large):
    factor = int(np.round(math.log2(large.shape[0]/small.shape[0])))
    for i in range(factor):
        sml = resize(small, factor)
        lrg = cv2.resize(large, (sml.shape[1], sml.shape[0]))
        small = sml
        small[:,:] = bilateral(sml[:,:], lrg[:,:], 3, 5, 7) 
        small = small.astype('int')
    return small

#upsampling both the channels using the large Y as a guide image
Cr_ = upsampler(Cr, Y)
Cb_ = upsampler(Cb, Y)

row = Y.shape[0]
col = Y.shape[1]
final = np.zeros(shape = (row, col, 3), dtype=np.uint8)
final[:,:,0] = Y[:,:]
final[:,:,2] = Cr_[0:622,:]
final[:,:,1] = Cb_[0:622,:]

finall = cv2.cvtColor(final, cv2.COLOR_YCrCb2RGB)
cv2.imwrite('flyingelephant.jpg',finall)

