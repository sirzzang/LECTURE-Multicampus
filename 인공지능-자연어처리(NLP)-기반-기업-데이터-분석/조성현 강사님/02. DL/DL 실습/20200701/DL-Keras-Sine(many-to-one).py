# -*- coding: utf-8 -*-
"""DL-Keras-LSTM-Sine(many to one)-practice의 사본

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_uJpIJaOxeL81IlXeCkpVHf4NPB4uBtU
"""

# module import
from tensorflow.keras.layers import Dense, Input, LSTM
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
import numpy as np
import matplotlib.pyplot as plt

# 1차원 배열의 시계열 데이터로 학습용 배치 파일 생성
def createData(X_data, step):
    '''
    <params>
        X_data: 생성할 시계열 데이터
        step: 시계열
    <return>
        batch_X : RNN 입력 데이터
        batch_Y : RNN 출력 데이터
    '''

    m = np.arange(len(X_data) - step) 

    x, y = [], []

    for i in m:
        # 입력데이터 생성
        a = X_data[i:(i+step)] 
        x.append(a)
        # 라벨데이터 생성
        b = X_data[i+1:(i+1+step)]
        y.append(b[-1])
        
    batch_X = np.reshape(np.array(x), (len(m), step, 1)) 
    batch_y = np.reshape(np.array(y), (len(m), 1)) 

    return batch_X, batch_y

# 시계열 데이터 생성을 위한 X좌표(noise 포함해서 생성)
data = np.arange(1001)*0.01 + np.sin(2 * np.pi * 0.03 * np.arange(1001)) + np.random.random(1001)

# parameters
n_input = 1 # feature 개수
n_output = 1 # 라벨 몇 개인지
n_step = int(input('분석할 step(기간) 수를 설정하세요: '))
n_hidden = int(input('hidden node 뉴런 수를 설정하세요: '))

EPOCHS = int(input('학습 횟수를 설정하세요: '))
BATCH = int(input('배치 사이즈를 설정하세요: '))

# 시계열 데이터 생성
x, y = createData(data, n_step)
print(f"X 데이터: {x.shape}, y 데이터: {y.shape}")

# LSTM 모델 생성
x_Input = Input(batch_shape=(None, n_step, 1))
x_Lstm = LSTM(n_hidden)(x_Input)
x_Output = Dense(n_output)(x_Lstm)
model = Model(x_Input, x_Output)
model.compile(loss='mse',
              optimizer=Adam(lr=0.01))
print(model.summary())

# 학습
hist = model.fit(x, y, epochs=EPOCHS, batch_size=BATCH, shuffle=True)

# plot history
plt.figure(figsize=(8, 4))
plt.plot(hist.history['loss'])
plt.title('Train Loss History')
plt.xlabel('Epochs')
plt.ylabel('Train Loss')
plt.show()

# 처음에 너무 loss 커서 빼고 그린다.
plt.figure(figsize=(8, 4))
plt.plot(hist.history['loss'][1:])
plt.title('Train Loss History from Epoch 1')
plt.xlabel('Epochs from 1')
plt.ylabel('Train Loss from Epoch 1')
plt.show()

# 예측 기간 수
n_future = int(input('예측할 미래 기간 수를 설정하세요: '))

# 마지막 100일에 대해서만 시계열 plot
if len(data) > 100:
    last_data = np.copy(data[-100:])
else:
    last_data = np.copy(data)

# 예측에 사용할 데이터
X_pred = np.copy(last_data)

# 예측값 저장 배열
estimate = [X_pred[-1]] 

# n_future 기간 만큼의 예측
for _ in range(n_future):
    x = X_pred[-n_step:].reshape(1, n_step, 1) # LSTM input 형태
    y_hat = model.predict(x)[0][0] 
    estimate.append(y_hat)
    X_pred = np.insert(X_pred, len(X_pred), y_hat) # 예측 후 데이터 업데이트

# plot
ax1 = np.arange(1, len(last_data)+1) # 원래 데이터
ax2 = np.arange(len(last_data), len(last_data) + len(estimate)) # 예측 데이터

plt.figure(figsize=(8, 3))
plt.plot(ax1, last_data, 'b-o', color='blue', markersize=3, label='Original Time Series', linewidth=1)
plt.plot(ax2, estimate, 'b-o', color='red', markersize=3, label='Estimates')
plt.axvline(x=ax1[-1], linestyle='dashed', linewidth=1) # 수직선으로 구분
plt.legend()
plt.show()