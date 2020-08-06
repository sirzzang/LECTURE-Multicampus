# -*- coding: utf-8 -*-
"""[과제]NLP-Keras-PredictNextWord-Alice-multilabel.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1gfrbvoajiweCs3i8gwPmXSGGr1yCyd-8
"""

# 모듈 불러오기
from collections import Counter
import nltk
nltk.download('punkt')
from nltk import word_tokenize
from tensorflow.keras.layers import Input, Dense, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam, RMSprop
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras import backend as K
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import string
import matplotlib.pyplot as plt
import random


# 경로 설정
root_path = "/content/drive/My Drive/멀티캠퍼스/[혁신성장] 인공지능 자연어처리 기반/[강의]/조성현 강사님"
data_path = f"{root_path}/dataset"

# 데이터 로드
with open(f"{data_path}/alice_in_wonderland.txt", "r") as f:
    content = f.read()

# 구둣점 제거
text = " ".join("".join([" " if char in string.punctuation else char for char in content]).split())

# 토큰화
tokens = word_tokenize(text)
tokens = [word.lower() for word in tokens if len(word) >= 2]

# N그램 생성 및 데이터 형태 변환
N = int(input('N 개수 설정: '))
quads = list(nltk.ngrams(tokens, N)) # 처음에 5개로 생성
new_text = [] # 학습 데이터
for q in quads:
    temp = " ".join(q)
    new_text.append(temp)

# 3-gram, 2-gram 형태로 변환
X_trigram = []
y_bigram = []
for text in new_text:
    x_str = " ".join(text.split()[0:N-2]) # 앞의 3단어
    y_str = " ".join(text.split()[N-2:]) # 뒤에 나와야 할 2단어
    X_trigram.append(x_str)
    y_bigram.append(y_str)

# 빈도 기반 수치화
vectorizer = CountVectorizer()
X_trigram_mat = vectorizer.fit_transform(X_trigram).todense()
y_bigram_mat = vectorizer.fit_transform(y_bigram).todense()

# 어휘집
word2idx = vectorizer.vocabulary_
idx2word = {v:k for k, v in word2idx.items()}

# 데이터 준비
X = np.array(X_trigram_mat)
y = np.array(y_bigram_mat)

# train, test 분리
X_train, X_test, y_train, y_test, X_train_tg, X_test_tg = train_test_split(X, y, X_trigram,
                                                                           test_size=0.3,
                                                                           random_state=42)
print(f"Train: {X_train.shape}, {y_train.shape}")
print(f"Test: {X_test.shape}, {y_test.shape}")
print(f"Train Trigram: {len(X_train_tg)}, {len(X_test_tg)}")

# 모델 파라미터 설정
EPOCHS = int(input('학습 에폭 수 설정: '))
BATCH = int(input('배치 사이즈 설정: '))

# FFN 네트워크 구성
X_input = Input(shape=(X_train.shape[1], ))
X_dense_1 = Dense(256, activation='relu')(X_input)
X_dense_1 = Dropout(0.2)(X_dense_1)
X_dense_2 = Dense(128, activation='relu')(X_dense_1)
X_dense_3 = Dense(256, activation='relu')(X_dense_2)
X_dense_3 = Dropout(0.3)(X_dense_3)
y_output = Dense(y_train.shape[1], activation='sigmoid')(X_dense_3)

# 모델 구성
K.clear_session()

model = Model(X_input, y_output)
model.compile(optimizer=RMSprop(learning_rate=0.01), loss='binary_crossentropy')
print("======= 모델 전체 구조 ======")
print(model.summary())

# 모델 훈련
es = EarlyStopping(monitor='val_loss', patience=5, verbose=1)
hist = model.fit(X_train, y_train,
                 batch_size=BATCH,
                 epochs=EPOCHS,
                 callbacks=[es],
                 validation_split=0.2)

# loss 시각화
plt.plot(hist.history['loss'], label='Train Loss')
plt.plot(hist.history['val_loss'], label='Test Loss')
plt.title('Loss Trajectory')
plt.legend()
plt.show()

# 결과 확인
y_pred = model.predict(X_test)
print(y_pred)

# 출력값 잘 나왔는지 시각화: 가장 높은 거 한 개만
temp = np.argmax(y_pred, axis=1)
max_list = []
for i in range(len(y_pred)):
    max_list.append(y_pred[i, temp[i]])

plt.plot(max_list)
plt.show()

# 가장 높은 2개 인덱스 반환
indices_pred = y_pred.argsort()[:,::-1][:, :2]
indices_test = y_test.argsort()[:, ::-1][:, :2]

# 랜덤하게 예측된 라벨과 정답 확인
print ("인덱스 | bigram | Actual | Predicted\n")
NUM_DISPLAY = int(input('확인할 라벨 수 설정: '))
for i in random.sample(range(len(X_test_tg)), NUM_DISPLAY):
    print(i, X_test_tg[i], "|", " ".join([idx2word[indices_test[i][j]] for j in range(2)]), "|", " ".join([idx2word[indices_pred[i][j]] for j in range(2)]))