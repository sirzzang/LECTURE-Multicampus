# -*- coding: utf-8 -*-
"""NLP-Seq2Seq-Chatbot-preprocess.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1hFV_9fZKLNQ5JkW-C8gf3-QGWk1KI1TH
"""

# KoNLPy 설치
import os

# KoNLPy 라이브러리 설치
!pip install konlpy

# jdk, JPype1-py3 설치
!apt-get install openjdk-8-jdk-headless -qq > /dev/null
!pip3 install JPype1-py3

# automake 설치
os.chdir('/tmp')
!curl -LO http://ftpmirror.gnu.org/automake/automake-1.11.tar.gz
!tar -zxvf automake-1.11.tar.gz
os.chdir('/tmp/automake-1.11')
!./configure
!make
!make install

# automake 설치 오류 시
os.chdir('/tmp/') 
!wget -O m4-1.4.9.tar.gz http://ftp.gnu.org/gnu/m4/m4-1.4.9.tar.gz
!tar -zvxf m4-1.4.9.tar.gz
os.chdir('/tmp/m4-1.4.9')
!./configure
!make
!make install
os.chdir('/tmp')
!curl -OL http://ftpmirror.gnu.org/autoconf/autoconf-2.69.tar.gz
!tar xzf autoconf-2.69.tar.gz
os.chdir('/tmp/autoconf-2.69')
!./configure --prefix=/usr/local
!make
!make install
!export PATH=/usr/local/bin

# 모듈 불러오기
from konlpy.tag import Okt
import pandas as pd
import re
from sklearn.model_selection import train_test_split
import numpy as np
from tqdm import tqdm
import pickle

# 경로 설정
root_path = "/content/drive/My Drive/멀티캠퍼스/[혁신성장] 인공지능 자연어처리 기반/[강의]/조성현 강사님"
data_path = f"{root_path}/dataset"
chatbot_path = f"{root_path}/Seq2Seq-Chatbot"

# 파일 이름 설정
DATA_PATH = f"{data_path}/6-1.ChatBotData.csv"
VOCABULARY_PATH = f"{data_path}/6-1.vocabulary.voc"

"""## 파라미터 설정

 챗봇을 만들 때는 형태소로 대답하면 안 되니까 `False` 파라미터로 설정한다.
"""

# 데이터 로드를 위한 파라미터 설정
TOKENIZE_AS_MORPH = False # 형태소로 대답하면 안 됨.
ENC_INPUT = 0 # encoder 입력
DEC_INPUT = 1 # decoder 입력
DEC_LABEL = 2 # decoder 출력
MAX_LENGTH = int(input('문장 최대 길이 설정: '))

# 특별 토큰
FILTERS = "([~.,!?\"':;)(])"
PAD = "<PADDING>"
STD = "<START>"
END = "<END>"
UNK = "<UNKNOWN>"

MARKER = [PAD, STD, END, UNK]
CHANGE_FILTER = re.compile(FILTERS)

"""## 데이터 로드"""

# 데이터 로드 함수
def load_data(path):
    data = pd.read_csv(path, header=0)
    question, answer = list(data['Q']), list(data['A'])
    train_input, test_input, train_label, test_label = \
        train_test_split(question, answer, test_size=0.1, random_state=42)
    return train_input, train_label, test_input, test_label

# 데이터 로드 후 확인
train_input, train_label, test_input, test_label = load_data(DATA_PATH)
print(f"Train: {len(train_input)}, {len(train_label)}")
print(f"Sample Train data:\n      Input: {train_input[0]}, Label: {train_label[0]}")
print()
print(f"Test: {len(test_input)}, {len(test_label)}")
print(f"Sample Test data:\n      Input: {test_input[0]}, Label: {test_label[0]}")

"""## 형태소 분석(적용 x)"""

# 형태소 분석 함수
def morphlize_data(tagger, data):
    tagger = tagger()
    result = []
    for sent in tqdm(data):
        morph = " ".join(tagger.morphs(sent.replace(" ", "")))
        result.append(morph)
        
    return result

"""## 인코더, 디코더용 데이터 만들기
- 사전: 원래는 빈도별로 해야 하는데 그렇게 안 함. 가나다 순.
- 전처리
    - 형태소 분석
    - OOV 처리
"""

# 토크나이징
def tokenize_data(data):
    words = []
    for sentence in data:
        sentence = re.sub(CHANGE_FILTER, "", sentence)
        for word in sentence.split():
            words.append(word)
            
    return [word for word in words if word]

# 사전 파일 만들기
def make_vocabulary(path, tokenize_as_morph=TOKENIZE_AS_MORPH):
    data = pd.read_csv(path, encoding='utf-8')
    question, answer = list(data['Q']), list(data['A'])
    
    # 형태소 분석
    if TOKENIZE_AS_MORPH:  
        question = morphlize_data(Okt, question)
        answer = morphlize_data(Okt, answer)
    
    # 어휘집 생성: 앞에 특별 토큰 추가
    sentences = []
    sentences.extend(question)
    sentences.extend(answer)
    words = tokenize_data(sentences)
    words = list(set(words)) # 중복 단어 제거
    words[:0] = MARKER

    word2idx = {word: idx for idx, word in enumerate(words)}
    idx2word = {idx: word for idx, word in enumerate(words)}
    
    return word2idx, idx2word

def preprocess_data(data, dictionary, dataType, tokenize_as_morph=TOKENIZE_AS_MORPH, filter=CHANGE_FILTER, maxlen=MAX_LENGTH):
    # 형태소 토크나이징 여부
    if tokenize_as_morph:
        data = morphlize_data(data)
    
    sequences_input_index = []
    for sequence in data:
        sequence = re.sub(filter, "", sequence) # 구둣점 제거

        # 디코더 입력: <START>로 시작
        if dataType == DEC_INPUT: 
            sequence_index = [dictionary[STD]]
        else:
            sequence_index = []

        # OOV: <unknown>
        for word in sequence.split():
            if dictionary.get(word) is not None:
                sequence_index.append(dictionary[word])
            else:
                sequence_index.append(dictionary[UNK])

            # 문장 단어 수 제한
            if len(sequence_index) >= maxlen:
                break
        
        # 디코더 출력: <END>로 끝
        if dataType == DEC_LABEL:
            if len(sequence_index) < maxlen:
                sequence_index.append(dictionary[END])
            else:
                sequence_index[len(sequence_index)-1] = dictionary[END]
        
        # 패딩: maxlen보다 작을 경우
        sequence_index += (maxlen - len(sequence_index))*[dictionary[PAD]]
        sequences_input_index.append(sequence_index)
    
    return np.asarray(sequences_input_index)

# 사전 생성
word2idx, idx2word = make_vocabulary(DATA_PATH)
print(f"word-index : {list(word2idx.items())[:20]}")
print(f"Vocab Size: {len(word2idx)}")

# 학습 데이터 : 인코더 입력, 디코더 입력, 디코더 출력
train_input_E = preprocess_data(train_input, word2idx, ENC_INPUT)
train_input_D = preprocess_data(train_label, word2idx, DEC_INPUT)
train_label_D = preprocess_data(train_label, word2idx, DEC_LABEL)

# 평가 데이터 : 인코더 입력, 디코더 입력, 디코더 출력
test_input_E = preprocess_data(test_input, word2idx, ENC_INPUT)
test_input_D = preprocess_data(test_label, word2idx, DEC_INPUT)
test_label_D = preprocess_data(test_label, word2idx, DEC_LABEL)

"""## 결과 저장"""

# vocabulary 저장
with open(f"{chatbot_path}/vocabulary.pickle", 'wb') as f:
    pickle.dump([word2idx, idx2word], f, pickle.HIGHEST_PROTOCOL)

# train data 저장
with open(f"{chatbot_path}/train.pickle", 'wb') as f:
    pickle.dump([word2idx, idx2word], f, pickle.HIGHEST_PROTOCOL)

# test data 저장
with open(f"{chatbot_path}/train.pickle", 'wb') as f:
    pickle.dump([word2idx, idx2word], f, pickle.HIGHEST_PROTOCOL)
