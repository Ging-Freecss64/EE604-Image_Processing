import numpy as np
from PIL import Image as im
import sys
#if showing PIL not found, install PIL using "pip install pillow"

#creating circles and numbers
def create_circle(k,h,arr):
    for i in range(300):
        for j in range(500):
            if((i - h)**2 + (j - k)**2 <= 25**2):
                arr[i][j] = 255

colLeft = np.array([65, 125, 185])
colRight= np.array([315, 375, 435])
row = np.array([30,90,150,210,270])
left = 0
right = 1

def zero(arr,side):
    if(side == left):
        for i in row:
            create_circle(185,i,arr)
            create_circle(65,i,arr)
        create_circle(125,30,arr)
        create_circle(125,270,arr)
    else:
        for i in row:
            create_circle(435,i,arr)
            create_circle(315,i,arr)
        create_circle(375,30,arr)
        create_circle(375,270,arr)
    
def one(arr,side):
    if(side == right):
        for i in row:
            create_circle(435,i,arr)
    else:
        for i in row:
            create_circle(185,i,arr)

def two(arr,side):
    if(side == right):
        for i in range(3):
            create_circle(435,row[i],arr)
            create_circle(315,row[4 - i],arr)
        create_circle(315,30,arr)
        create_circle(375,30,arr)
        create_circle(315,150,arr)
        create_circle(375,150,arr)
        create_circle(315,270,arr)
        create_circle(375,270,arr)
        create_circle(435,270,arr)
    else:
        for i in range(3):
            create_circle(185,row[i],arr)
            create_circle(65,row[4 - i],arr)
        create_circle(65,30,arr)
        create_circle(125,30,arr)
        create_circle(65,150,arr)
        create_circle(125,150,arr)
        create_circle(65,270,arr)
        create_circle(125,270,arr)
        create_circle(185,270,arr)
    

def three(arr,side):
    if(side == right):
        for i in row:
            create_circle(435,i,arr)
        i = 0
        while(i < 5):
            create_circle(315,row[i],arr)
            create_circle(375,row[i],arr)
            i+=2
    else:
        for i in row:
            create_circle(185,i,arr)
        i = 0
        while(i < 5):
            create_circle(65,row[i],arr)
            create_circle(125,row[i],arr)
            i+=2
        
def four(arr,side):
    if(side == right):
        for i in row:
            create_circle(435,i,arr)
        for i in range(3):
            create_circle(315,row[i],arr)
        create_circle(375,row[2],arr)
    else:
        for i in row:
            create_circle(185,i,arr)
        for i in range(3):
            create_circle(65,row[i],arr)
        create_circle(125,row[2],arr)
        
def five(arr,side):
    if(side == right):
        for i in range(3):
            create_circle(315,row[i],arr)
            create_circle(435,row[4 - i],arr)
        create_circle(315,30,arr)
        create_circle(375,30,arr)
        create_circle(435,30,arr)
        create_circle(315,150,arr)
        create_circle(375,150,arr)
        create_circle(315,270,arr)
        create_circle(375,270,arr)
        create_circle(435,270,arr)
    else:
        for i in range(3):
            create_circle(65,row[i],arr)
            create_circle(185,row[4 - i],arr)
        create_circle(65,30,arr)
        create_circle(125,30,arr)
        create_circle(185,30,arr)
        create_circle(65,150,arr)
        create_circle(125,150,arr)
        create_circle(65,270,arr)
        create_circle(125,270,arr)
        create_circle(185,270,arr)

def six(arr,side):
    if(side == right):
        for i in row:
            create_circle(315,i,arr)
        for i in range(3):
            create_circle(435,row[4 - i],arr)
        create_circle(375,30,arr)
        create_circle(435,30,arr)
        create_circle(315,150,arr)
        create_circle(315,270,arr)
        create_circle(375,row[2],arr)
        create_circle(375,row[4],arr)
    else:
        for i in row:
            create_circle(65,i,arr)
        for i in range(3):
            create_circle(185,row[4 - i],arr)
        create_circle(185,30,arr)
        create_circle(125,30,arr)
        create_circle(65,150,arr)
        create_circle(125,270,arr)
        create_circle(125,row[2],arr)
        create_circle(125,row[4],arr)

def seven(arr,side):
    if(side == right):
        for i in row:
            create_circle(435,i,arr)
        create_circle(315,30,arr)
        create_circle(375,30,arr)
    else:
        for i in row:
            create_circle(185,i,arr)
        create_circle(65,30,arr)
        create_circle(125,30,arr)

def eight(arr,side):
    if(side == right):
        for i in row:
            create_circle(435,i,arr)
            create_circle(315,i,arr)
        create_circle(375,30,arr)
        create_circle(375,150,arr)
        create_circle(375,270,arr)
    else:
        for i in row:
            create_circle(185,i,arr)
            create_circle(65,i,arr)
        create_circle(125,30,arr)
        create_circle(125,150,arr)
        create_circle(125,270,arr)
        
def nine(arr,side):
    if(side == right):
        for i in range(3):
            create_circle(435,row[i],arr)
            create_circle(315,row[i],arr)
        for i in row:
            create_circle(435,i,arr)
        create_circle(315,30,arr)
        create_circle(375,30,arr)
        create_circle(315,150,arr)
        create_circle(375,150,arr)
        create_circle(315,270,arr)
        create_circle(375,270,arr)
    else:
        for i in range(3):
            create_circle(185,row[i],arr)
            create_circle(65,row[i],arr)
        for i in row:
            create_circle(185,i,arr)
        create_circle(65,30,arr)
        create_circle(125,30,arr)
        create_circle(65,150,arr)
        create_circle(125,150,arr)
        create_circle(65,270,arr)
        create_circle(125,270,arr)

#creating black image
arr = np.arange(0,150000,1,np.uint8)
arr = np.reshape(arr, (300,500))
for i in range(300):
    for j in range(500):
        arr[i][j] = 0
       
#printing
def print(arr,side,n):
    if(n == '1'):
        one(arr,side)
    if(n == '2'):
        two(arr,side)
    if(n == '3'):
        three(arr,side)
    if(n == '4'):
        four(arr,side)
    if(n == '5'):
        five(arr,side)
    if(n == '6'):
        six(arr,side)
    if(n == '7'):
        seven(arr,side)
    if(n == '8'):
        eight(arr,side)
    if(n == '9'):
        nine(arr,side)
    if(n == '0'):
        zero(arr,side)

#taking input
#num = str(input("Enter you number: "))
num = str(sys.argv[1])
if(len(num)==2):
    print(arr,left,num[0])
    print(arr,right,num[1])
else:
    print(arr,left,'0')
    print(arr,right,num[0])

#storing image
data = im.fromarray(arr)
data.save('dotmatrix.jpg')


