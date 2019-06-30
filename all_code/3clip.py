
import os
import uuid
import cv2
from PIL import Image
import numpy as np

def split_picture(imagepath,file):
    # 统计符合标准的字符是否是5个
    index=0
    # 用于临时存储图片分割的字符串二维数组
    tempsave=[]
    # 用于分割字符串的排序，记录每个字符的x坐标
    tempindex=[]
    # 以灰度模式读取图片
    gray = cv2.imread(imagepath, 0)
    # 将图片的边缘变为白色
    height, width = gray.shape
    # print(height,width)
    for i in range(width):
        gray[0, i] = 255
        gray[height-1, i] = 255
    for j in range(height):
        gray[j, 0] = 255
        gray[j, width-1] = 255
    # 二值化
    ret, thresh1 = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
    # 提取单个字符
    contours, hierarchy = cv2.findContours(thresh1, 2, 4)
    # print(len(contours))
    for cnt in contours:
        # 最小的外接矩形
        x, y, w, h = cv2.boundingRect(cnt)
        if x != 0 and y != 0 and w*h>=50 and h>10:
            # print((x,y,w,h))
            if w <= 19:
                # 保存图片  并将图片尺寸统一大小 height 22 width 19
                thresh1_result=np.zeros((22, 19), dtype=np.int)
                for i in range(22):
                    for j in range(19):
                        thresh1_result[i,j]=255
                thresh1_1 = thresh1[y:y + h, x:x + w]
                for m in range(thresh1_1.shape[0]):
                    for n in range(thresh1_1.shape[1]):
                        thresh1_result[m][n]=thresh1_1[m,n]
                tempsave.append(thresh1_result)
                tempindex.append(x)
                index+=1
    if(index==5):
        tempsort=tempindex.copy()
        tempsort.sort()
        for i in range(5):
            if not os.path.exists(r'F:\python_work\tornado\success\%s' % (file[i:i+1])):
                os.mkdir(r'F:\python_work\tornado\success\%s' % (file[i:i+1]))
            cv2.imwrite(r'F:\python_work\tornado\success\%s\%s.jpg' % (file[i:i+1],uuid.uuid1()),
                tempsave[tempindex.index(tempsort[i])])

if __name__ == '__main__':
    dir = r"F:\python_work\tornado\onetwo"
    for file in os.listdir(dir):
        imagepath = dir+'\\'+file
        split_picture(imagepath,file.split(".")[0])







