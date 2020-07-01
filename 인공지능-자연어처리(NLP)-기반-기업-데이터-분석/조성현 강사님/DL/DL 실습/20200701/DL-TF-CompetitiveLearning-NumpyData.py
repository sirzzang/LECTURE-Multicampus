# -*- coding: utf-8 -*-
"""20200701-DL-TF-CompetitiveLearning-NumPy.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1HGo2Qd66pgFW5FP95XsGafZsDoRLy6Y0

# 단층 신경망 구성하여 경쟁학습 구현
"""

# module import
import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt

# create Data
def createData(n):
    xy = []
    for i in range(n):
        r = np.random.random()
        
        # r 기준으로 3부류의 데이터 생성
        if r < 0.33:
            x = np.random.normal(0.0, 0.9)
            y = np.random.normal(0.0, 0.9)
        elif r < 0.66:
            x = np.random.normal(1.0, 0.3)
            y = np.random.normal(2.0, 0.3)
        else:
            x = np.random.normal(3.0, 0.6)
            y = np.random.normal(1.0, 0.6)
        
        xy.append([x, y])
    
    return pd.DataFrame(xy, columns = ['x', 'y'])

# winner neuron 찾기
def findWinner(W, X):
    '''
    return:
    '''
    distance = tf.sqrt(
        tf.reduce_sum(
            tf.square(
                tf.subtract(W, tf.transpose(X))
            ), axis=1
        )
    )
    
    winner = tf.argmin(distance, axis=0)
    dist = tf.slice(distance, [winner], [1])

    return dist, winner

# winner neuron의 가중치 업데이트: Hebb's rule
def updateWeights(W, winner, X, alpha):
    '''
    <params>
    W: 초기 가중치
    winner: winner 뉴런 번호
    X: 데이터
    alpha: 헵 학습률
    <return>
    new_weight: 새로이 업데이트된 가중치
    '''
    to_be_updated = tf.gather(W, winner)
    weight_updated = tf.add(to_be_updated, tf.multiply(alpha, tf.subtract(tf.transpose(X), to_be_updated)))
    new_weight = tf.tensor_scatter_nd_update(W, [[winner]], weight_updated)

    return new_weight

# winner takes it all 방식
def winner_takes_all(W, X, n):
    '''
    <params>
    W: 찾아낼 가중치
    X: 입력 데이터
    n: 출력노드 개수.
    <return>
    r: 원핫 벡터
    tf.argmax(r, 0): 클러스터 라벨
    '''
    _, winner = findWinner(W, X)
    r = tf.one_hot(winner, n) # winner 뉴런 찾고, 그걸 원핫 벡터로 바꾼다.
    return r, tf.argmax(r, 0)

# load data
n = int(input('데이터 좌표 수를 설정하세요.: '))
data = createData(n)

input_data = data.values.T.astype(np.float32)

# 필요한 변수 설정
n_input = int(input('입력 뉴런 노드 수를 설정하세요.: '))
n_output = int(input('출력 뉴런 노드 수를 설정하세요.: '))
ALPHA = float(input('헵 학습률을 설정하세요.: '))
epochs = int(input('학습 횟수를 설정하세요.: '))

# 그래프 생성
Wo = tf.Variable(tf.random.uniform([n_output, n_input], 0.0, 1.0), dtype=tf.float32)

# 학습
for epoch in range(epochs):
    error = 0 # 거리 개념

    for k in range(n): # X좌표 각각에 대해 아래의 작업 수행
        X_data = input_data[:, k].reshape([n_input, 1])        
        # winner neuron 찾기
        dist, win = findWinner(Wo, X_data)        
        # winner neuron 가중치 업데이트
        Wo = updateWeights(Wo, win, X_data, ALPHA)
        # 에러 측정: 원래 에러 개념 없지만, 각 중점에 할당된 데이터까지 거리 합으로 정의
        error += dist.numpy()[0]

    print("===== %d-th epoch done. Error: %.8f" % (epoch, error / n)) # 총 에러 n으로 나눠야

# 학습 완료 후 클러스터 결정
cluster = []
for k in range(n):
    data_X = input_data[:, k].reshape([n_input, 1])
    _, label = winner_takes_all(Wo, data_X, n_output)
    cluster.append(label.numpy())

print(cluster)

# 학습이 완료된 weight는 Kmeans의 centroid
centroids = Wo.numpy()
print(centroids)

# plot
clust = np.array(cluster) # array로 만들어서 indexing 편하게 한다.
data = input_data.T # 가로로 되어 있는 애들 세로로 바꾼다
color = plt.cm.rainbow(np.linspace(0, 1, n_output))
plt.figure(figsize=(8, 6))
for i, c in zip(range(n_output), color):
    print(i, c)
    plt.scatter(data[clust==i, 0], data[clust==i, 1],
                s=20, color=c, marker='o',alpha=0.5,
                label=f"cluster-{i}")
plt.scatter(centroids[:, 0], centroids[:, 1],
            s=250, marker='^', color='black', label='centroids')
plt.title('Cluster_Competitive Learning')
plt.legend()
plt.grid(alpha=0.3) 
plt.show()