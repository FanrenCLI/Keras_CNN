import os
from PIL import Image
from collections import defaultdict


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


def OCR_lmj(img_path):
    arr=img_path.split("\\")
    image = Image.open(img_path)
    imgry = image.convert('L')
    # imgry.show()
    # 将图片进行二值化处理
    table = get_bin_table(150)
    out = imgry.point(table, '1')
    # out.show()
    # 去掉图片中的噪声（孤立点）
    out = cut_noise(out)
    # out.show()
    # 保存图片
    result= r'C:\Users\FanrenCLI\Desktop\1\onetwo\\'+arr[6]
    out.save(result)


def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        print(files)
    return files


path = r'C:\Users\FanrenCLI\Desktop\1\new'
for name in file_name(path):
    OCR_lmj(path+"\\"+name)

