# -*- coding: utf-8 -*-
"""[20200625] DL-Equation-Keras-Rmsprop.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1KpF9odB-QrxTg278uF2gjW8cxkw5lkji
"""

# module import
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential
from tensorflow.keras import optimizers
import numpy as np
import matplotlib.pyplot as plt

# x, y 데이터 생성
x = np.array(np.arange(-5, 5, 0.1))
y = 2*x*x + 3*x + 5
X_data = np.stack([x*x, x]).T # x*x, x 자리에 차례로 들어갈 2차원 array

# 그래프 생성
model = Sequential()
model.add(Dense(1, input_dim=2))
model.compile(loss='mse', optimizer=optimizers.RMSprop(lr=0.05))
print(model.summary())

# train
h = model.fit(X_data, y, batch_size=10, epochs=300)

# 학습 결과
parameters = model.layers[0].get_weights()
parameters
print('==== 추정 결과 ====')
print('     w1 = %.2f' % parameters[0][0][0])
print('     w1 = %.2f' % parameters[0][1][0])
print('     b0 = %.2f' % parameters[1][0])

# plot history
plt.plot(h.history['loss'], color='red', linewidth=1)
plt.title('Loss Function')
plt.xlabel('epoch')
plt.ylabel('loss')
plt.show()

model.layers[0]

model.layers[0].get_weights()