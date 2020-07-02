# -*- coding: utf-8 -*-
"""DL-Keras-Sine(bidirectional, many-to-many)-practice

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1kHO9Dcaj8JhoEUgIzjsEzyK8U7jW0Koe
"""

# module import
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.layers import Input, Dense, LSTM, TimeDistributed, Bidirectional
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam

def createData(X_data, step):
    m = np.arange(len(X_data) - step)

    x, y = [], []
    for i in m:
        a = X_data[i:i+step]
        x.append(a)
        b = X_data[i+1:i+1+step]
        y.append(b)
    X = np.reshape(np.array(x), (len(m), step, 1))
    Y = np.reshape(np.array(y), (len(m), step, 1))
    
    return X, Y

# Sine
data = np.arange(1001) * 0.01 + np.sin(2*np.pi*0.02*np.arange(1001)) + np.random.random(1001)

# parameters
n_input = 1
n_output = 1
n_step = 20
n_hidden = 50

EPOCHS = 100
BATCH = 100

n_futures = 20

# x, y data
x, y = createData(data, n_step)

# LSTM 모델 생성
x_Input = Input(batch_shape=(None, n_step, 1))
x_Lstm = Bidirectional(LSTM(n_hidden, return_sequences=True), merge_mode='concat')(x_Input)
y_Output = TimeDistributed(Dense(n_output))(x_Lstm)

model = Model(x_Input, y_Output)
model.compile(loss='mse', optimizer=Adam(lr=0.01))

# 모델 구조 확인
print(model.summary())

# 학습
hist = model.fit(x, y, epochs=EPOCHS, batch_size=BATCH, shuffle=True)

# plot loss
plt.figure(figsize=(8, 3))
plt.plot(hist.history['loss'])
plt.xlabel('Epochs')
plt.ylabel('Train Loss')
plt.show()

# 예측
last_data = data[-100:]

X_pred = last_data.copy()
estimate = [X_pred[-1]]

for _ in range(n_futures):
    x = X_pred[-n_step:].reshape(1, n_step, 1)
    y_hat = model.predict(x)[0][-1][0]
    estimate.append(y_hat)
    X_pred = np.insert(X_pred, len(X_pred), y_hat)

# plot
ax1 = np.arange(1, len(last_data) + 1)
ax2 = np.arange(len(last_data), len(last_data)+len(estimate))
plt.figure(figsize=(8,3))
plt.plot(ax1, last_data, 'b-o', color='blue', markersize=3, label='Original Time Series', linewidth=1)
plt.plot(ax2, estimate, 'b-o', color='red', markersize=3, label='Estimate')
plt.axvline(x=ax1[-1], linestyle='dashed', linewidth=1)
plt.legend()
plt.show()

