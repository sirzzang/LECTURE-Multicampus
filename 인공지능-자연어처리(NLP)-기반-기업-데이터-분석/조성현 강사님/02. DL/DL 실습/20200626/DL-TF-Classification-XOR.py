# -*- coding: utf-8 -*-
"""DL-TF-XOR.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/130qBsj_wFD0Dnf4QQnvReM0bCJYsBqCK
"""

# module import
import numpy as np
import tensorflow as tf
from tensorflow.keras.optimizers import Adam

# set data : XOR
X_data = np.array([[0, 0],
                   [0, 1],
                   [1, 0],
                   [1, 1]], dtype=np.float32)
y_data = np.array([[1],
                   [0],
                   [0],
                   [1]], dtype=np.float32)

# layer 설정
n_input = 2 # input layer neuron 개수: X_data.shape[1]
n_hidden = 4 # hidden layer neuron 개수 : 내가 그냥 설정하는 건가?
n_output = 1 # output layer neuron 개수

"""* 은닉 노드: X*W + b -> (4x2) x (2x4) + (4x1) -> 4x4
* 출력 노드: X*W + b -> (4x1) x (1x1) + 1x1
"""

# 그래프 생성

# 은닉 노드
W_hidden = tf.Variable(tf.random.normal([n_input, n_hidden]), dtype=tf.float32)
b_hidden = tf.Variable(tf.zeros([n_hidden]), dtype=tf.float32)

# 출력 노드
W_output = tf.Variable(tf.random.normal([n_hidden, n_output]))
b_output = tf.Variable(tf.zeros([n_output]), dtype=tf.float32)

"""sigmoid 한 번에 적용해 버린다."""

# predict
def predict(x):
    y_hidden = tf.sigmoid(tf.matmul(X_data, W_hidden) + b_hidden)
    y_output = tf.sigmoid(tf.matmul(y_hidden, W_output) + b_output)
    return y_output

# loss function
def loss_CE(x, y):
    y_tmp = predict(x)
    y_clip = tf.clip_by_value(y_tmp, 0.000001, 0.999999)

    CE = -tf.reduce_mean(y*tf.math.log(y_clip) + (1-y)*tf.math.log(1-y_clip))
    return CE

# optimizer
adam = Adam(learning_rate=0.02)

# train
train_loss = []
train_epoch = int(input('학습 횟수를 설정하세요: '))

for epoch in range(train_epoch):
    adam.minimize(lambda: loss_CE(X_data, y_data), var_list = [W_hidden, b_hidden, W_output, b_output])
    train_loss.append(loss_CE(X_data, y_data))
    if epoch % 100 == 0:
        print("%d %4.f" % (epoch, train_loss[-1]))

# 예측
y_hat = predict(X_data).numpy()
y_hat_pred = np.where(y_hat > 0.5, 1, 0)
print('y 추정치')
print(np.round(y_hat_pred, 3))

# 결과 확인
print('===== 은닉층 =====')
print(f"weight: {np.round(W_hidden.numpy(), 3)}, bias: {np.round(b_hidden.numpy(), 3)}")
print('===== 출력층 =====')
print(f"weight: {np.round(W_output.numpy(), 3)}, bias: {np.round(b_output.numpy(), 3)}")