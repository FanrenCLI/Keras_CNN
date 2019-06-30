import numpy as np
import os
from keras.utils import np_utils,plot_model
from keras.models import Sequential
from keras.layers.core import Dense,Dropout,Activation,Flatten
from keras.callbacks import EarlyStopping
from keras.layers import Conv2D,MaxPooling2D
from keras import backend as K
from matplotlib import pyplot as plt
import keras
import string
import cv2
from sklearn.model_selection import train_test_split

#输入图片尺寸
image_height=22
image_width=19

# 初始化参数
batch_size=128
epochs=20
#标签值
example_num=0
label_num=36
X=[]
Y=[]
CHRS = string.ascii_lowercase + string.digits
# 获取图片文件
img_dir=r"F:\python_work\tornado\success"
for file in os.listdir(img_dir):
    for inner_file in os.listdir(img_dir+"\\"+str(file)):
        name=str(file).lower()
        gray=cv2.imread(img_dir+'\\'+file+'\\'+inner_file,0)
        ret, thresh1 = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
        X.append(thresh1)
        Y.append(CHRS.index(name))
        example_num=example_num+1
print(example_num)
X=np.array(X).reshape((example_num,22,19,1))
Y=np.array(Y)
input_shape=X[0].shape
Y = np_utils.to_categorical(Y, label_num)
split_point =int(example_num/5*4)
# x_train, y_train, x_test, y_test = X[:split_point], Y[:split_point], X[split_point:], Y[split_point:]
x_train, y_train, x_test, y_test = X, Y, X[split_point:], Y[split_point:]

model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3),
                 activation='relu',
                 input_shape=input_shape))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(label_num, activation='softmax'))

model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.Adadelta(),
              metrics=['accuracy'])
history=model.fit(x_train, y_train,
          batch_size=batch_size,
          epochs=epochs,
          verbose=1,
          validation_data=(x_test, y_test))
score = model.evaluate(x_test, y_test, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])

model.save(r"F:\python_work\tornado\result\train.h5")

val_acc=history.history["val_acc"]
plt.plot(range(len(val_acc)),val_acc,label="CNN model")
plt.title("Validation accuracy on verifycode dataset")
plt.xlabel("epochs")
plt.ylabel("accuracy")
plt.legend()
plt.show()