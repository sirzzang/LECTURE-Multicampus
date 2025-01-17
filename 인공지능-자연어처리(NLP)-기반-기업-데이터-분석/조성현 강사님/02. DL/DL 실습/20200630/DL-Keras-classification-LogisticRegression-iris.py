# -*- coding: utf-8 -*-
"""DL-Keras-classification-LogisticRegression-iris.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1M0IvBartil1wKSrvi-RhkreJMssP-VS5
"""

# module import
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
import numpy as np
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.models import Model
from tensorflow.keras.regularizers import l2
from tensorflow.keras.optimizers import Adam
import matplotlib.pyplot as plt

# load data
iris = load_iris()

# data preprocessing
X_data = iris['data'].astype(np.float32)
y_data = to_categorical(iris['target'], num_classes=len(iris['target_names'])).astype(np.float32)

scaler = StandardScaler()
X_data = scaler.fit_transform(X_data)

# split data
X_train, X_test, y_train, y_test = train_test_split(X_data, y_data, test_size=0.2)
print("Train: {0}, {1} / Test: {2}, {3}".format(X_train.shape, y_train.shape, X_test.shape, y_test.shape))

# layer size
n_input = X_train.shape[1]
n_hidden = int(input('은닉 노드의 수를 설정하세요: '))
n_output = int(input('출력 노드의 수를 설정하세요: '))

"""* Tensorflow 버전과 똑같이 하기 위해 모든 층에 규제항 적용"""

BATCH = int(input('배치 사이즈를 설정하세요: '))
C = float(input('규제항의 크기를 설정하세요: '))
epochs = int(input('학습 epoch 수를 설정하세요: '))

# layers
X_input = Input(batch_shape=[None, n_input])
X_hidden = Dense(n_hidden,
                 kernel_regularizer=l2(C),
                 activation='relu')(X_input)
y_output = Dense(n_output,
                 kernel_regularizer=l2(C),
                 activation='softmax')(X_hidden)

# model
model = Model(X_input, y_output)
model.compile(loss='categorical_crossentropy',
              optimizer=Adam(lr=0.01))
print(model.summary())

# train
hist = model.fit(X_train, y_train,
                 validation_data=(X_test, y_test),
                 batch_size=BATCH,
                 epochs=epochs)

# check
y_hat = model.predict(X_test)
y_hat_pred = np.argmax(y_hat, axis=1)
accuracy = (np.argmax(y_test, axis=1) == y_hat_pred).mean()
print("Test Set Accuracy: %.4f" % accuracy)

# plot
plt.figure(figsize=(10, 4))
plt.plot(hist.history['loss'], label='Train Loss')
plt.plot(hist.history['val_loss'], label='Test Loss')
plt.title('Loss Function_Categorical CrossEntropy')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.show()