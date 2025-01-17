# -*- coding: utf-8 -*-
"""20200702-DL-Keras-Sine(bidirectional, many-to-one)-practice.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16-NnFcYd0EyavBIhkwuds16BNpGd5SDu
"""

# module import
import numpy as np
from tensorflow.keras.layers import Input, Dense, LSTM, Bidirectional
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
import matplotlib.pyplot as plt

# create Data
def createData(X_data, step):
    m = np.arange(len(X_data) - step)

    x, y = [], []
    for i in m:
        a = X_data[i:i+step]
        x.append(a)
        b = X_data[i+1:i+1+step]
        y.append(b[-1])

    X = np.array(x).reshape([len(m), step, 1])
    Y = np.array(y).reshape([len(m), 1])
    return X, Y

# 시계열 sine 데이터 생성
data = np.arange(1001)*0.001 + np.sin(2*np.pi*0.03*np.arange(1001)) + np.random.random(1001)
plt.plot(data)

# 파라미터 설정
n_input = 1 # input feature
n_output = 1 # output feature
n_step = int(input('시계열 step 주기를 설정하세요: '))
n_hidden = int(input('FFN 히든 뉴런의 개수를 설정하세요: '))

# 학습 데이터 생성
x, y = createData(data, n_step)

# LSTM 모델 생성
x_Input = Input(batch_shape=(None, n_step, n_input))
x_Lstm = Bidirectional(LSTM(n_hidden), merge_mode='concat')(x_Input)
y_output = Dense(n_output)(x_Lstm)
model = Model(x_Input, y_output)
latent = Model(x_Input, x_Lstm)
latent_feature = latent.predict(x[0].reshape(1, 20, 1))
print(f"latent feature 확인: {latent_feature}") # (1, 100)이 된다. 

model.compile(loss='mse', optimizer=Adam(lr=0.01))
print(model.summary())

# 학습
EPOCHS = int(input('학습 횟수를 설정하세요.: '))
BATCH = int(input('배치 사이즈를 설정하세요.: '))

hist = model.fit(x, y,
                 epochs=EPOCHS,
                 shuffle=True,
                 batch_size=BATCH)

# plot loss history
plt.figure(figsize=(8, 3))
plt.plot(hist.history['loss'])
plt.title('Loss History')
plt.xlabel('Epochs')
plt.ylabel('Train Loss')
plt.show()

# 예측
n_future = int(input('예측하고자 하는 기간을 설정하세요.: '))

# 마지막 100개 데이터 활용
if len(data) > 100:
    last_data = np.copy(data[-100:])
else:
    last_data = np.copy(data)

X_pred = np.copy(last_data)
estimate = [X_pred[-1]]

# 예측
for _ in range(n_future):
    x = X_pred[-n_step:].reshape(1, n_step, 1) # 마지막에 들어가기 위해서
    y_hat = model.predict(x)[0][0]
    estimate.append(y_hat)
    X_pred = np.insert(X_pred, len(X_pred), y_hat)

ax1 = np.arange(1, len(last_data)+1)
ax2 = np.arange(len(last_data), len(last_data) + len(estimate))
plt.figure(figsize=(8, 3))
plt.plot(ax1, last_data, 'b-o', color='blue', markersize=3, label='Original Time Series', linewidth=1)
plt.plot(ax2, estimate, 'b-o', color='red', markersize=3, label='Estimates')
plt.axvline(x=ax1[-1], linestyle='dashed', linewidth=1)
plt.legend()
plt.show()