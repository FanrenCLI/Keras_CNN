from keras.models import load_model
import numpy as np
import os
import cv2
import string
CHRS = string.ascii_lowercase + string.digits
table=[]
index=0
img_dir=r'F:\python_work\tornado\success\a'
for file in os.listdir(img_dir):
    imagepath = img_dir+'\\'+file
    # 以灰度模式读取图片
    gray = cv2.imread(imagepath, 0)
    # 二值化
    ret, thresh1 = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
    table=np.array([thresh1]).reshape(-1,22,19,1)
    break
cnn=load_model(r"F:\python_work\tornado\result\train.h5")
y_pre=cnn.predict(table)
predictions = np.argmax(y_pre, axis=1)
print("图片识别结果为:%s"%(CHRS[predictions[0]]))