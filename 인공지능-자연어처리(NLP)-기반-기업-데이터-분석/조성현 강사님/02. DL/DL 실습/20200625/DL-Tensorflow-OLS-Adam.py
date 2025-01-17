# -*- coding: utf-8 -*-
"""Untitled3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1H-zWEoiw9WfPlnA-ovNQIOaGRFhDqGek
"""

# module import
import numpy as np
import tensorflow as tf
from tensorflow.keras.optimizers import Adam
import matplotlib.pyplot as plt

# 샘플 데이터 생성
def createData(a, b, n):
    result_X, result_Y = [], []
    for i in range(n):
        x = np.random.normal(0.0, 0.5)
        y = a * x + b + np.random.normal(0.0, 0.05) # 잔차
        result_X.append(x)
        result_Y.append(y)
    return result_X, result_Y

# 입력 데이터 식: y = 0.1*x + 0.3 + e
x, y = createData(0.1, 0.3, 2000) # 2000개

# 선형 회귀 식 정의: y = w*X + b
W = tf.Variable(tf.random.uniform([1], -1.0, 1.0), name='weight')
b = tf.Variable(tf.zeros([1]), name='bias')

# optimizer 정의
optimizer = Adam(learning_rate=0.05)

# loss function 정의
def loss(x):
    H = tf.add(tf.multiply(W, x), b)
    return tf.reduce_mean(tf.square(H-y))

# 학습
train_loss = []
for i in range(300):
    optimizer.minimize(lambda: loss(x), var_list = [W, b])
    train_loss.append(loss(x))
    if i % 10 == 0:
        print("epoch : %d %f" %(i, train_loss[-1]))

# 결과 확인
y_hat = W.numpy() * x + b.numpy() # real 추정치
print("======= 회귀직선의 방정식(OLS) =======")
print("y = %.4f * x + %.4f" % (W.numpy(), b.numpy()))

# plot
fig = plt.figure(figsize=(10, 4))
p1 = fig.add_subplot(1, 2, 1)
p2 = fig.add_subplot(1, 2, 2)

p1.plot(x, y, 'ro', markersize=1.5)
p1.plot(x, y_hat)

p2.plot(train_loss, color='red', linewidth=1)
p2.set_title('Loss Function')
p2.set_xlabel('epoch')
p2.set_ylabel('loss')
plt.show()