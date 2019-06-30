# 灰度二值化，去燥
# 切割
# 模型判断
import os
from PIL import Image
import cv2
import numpy as np
from keras.models import load_model
import string

CHRS = string.ascii_lowercase + string.digits
def get_bin_table(threshold):
    # 获取灰度转二值的映射table
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    return table
def cut_noise(image):
    rows, cols = image.size  # 图片的宽度和高度
    change_pos = []  # 记录噪声点位置
    change_pos_1=[]  #记录补点位置
    # 遍历图片中的每个点，除掉边缘
    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            # pixel_set用来记录该店附近的黑色像素的数量
            pixel_set = []
            # 取该点的邻域为以该点为中心的九宫格
            for m in range(i - 1, i + 2):
                for n in range(j - 1, j + 2):
                    if image.getpixel((m, n)) != 1:  # 1为白色,0位黑色
                        pixel_set.append(image.getpixel((m, n)))
            # 如果该位置的九宫内的黑色数量小于等于4，则判断为噪声
            if len(pixel_set) <= 3:
                change_pos.append((i, j))
            if len(pixel_set) >6:
                change_pos_1.append((i,j))
    # 对相应位置进行像素修改，将噪声处的像素置为1（白色）
    for pos in change_pos:
        image.putpixel(pos, 1)
    for pos in change_pos_1:
        image.putpixel(pos, 0)
    return image  # 返回修改后的图片
def split_picture(thresh1):
    # 统计符合标准的字符是否是5个
    index=0
    # 用于临时存储图片分割的字符串二维数组
    tempsave=[]
    # 用于分割字符串的排序，记录每个字符的x坐标
    tempindex=[]
    # 提取单个字符
    contours, hierarchy = cv2.findContours(thresh1, 2, 4)
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
        return [tempsave[tempindex.index(tempsort[i])] for i in range(5)]
    return 0

if __name__ == "__main__":
    image = Image.open(r"F:\python_work\tornado\new\checkImage.jpg")
    imgry = image.convert('L')
    table = get_bin_table(140)
    out = imgry.point(table, '1')
    # 去掉图片中的噪声（孤立点）
    out = cut_noise(out)
    gray=np.asarray(out,dtype=np.uint8)*255
    table=split_picture(gray)
    if table!=0:
        table1=np.array(table).reshape(-1,22,19,1)
        cnn=load_model(r"F:\python_work\tornado\result\train.h5")
        y_pre=cnn.predict(table1)
        predictions = np.argmax(y_pre, axis=1)
        print("图片识别结果为:%s"%(''.join([CHRS[predictions[i]] for i in range(5)])))
    else:
        print('图片分割失败')