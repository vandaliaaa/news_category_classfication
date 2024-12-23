import pickle
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from keras.utils import to_categorical
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from keras.models import load_model

# 데이터 로드
# 특정 CSV 파일에서 데이터를 로드하고 중복 제거 및 인덱스를 재정렬
df = pd.read_csv('./crawling_data/naver_headline_news20241223.csv')
df.drop_duplicates(inplace=True)  # 중복 데이터를 제거
df.reset_index(drop=True, inplace=True)  # 인덱스를 리셋
print(df.head())  # 데이터의 첫 5행 출력
df.info()  # 데이터 유형 및 통계 정보 출력
print(df.category.value_counts())  # 카테고리별 데이터 수 출력

# X에 기사 제목, Y에 카테고리 레이블 저장
X = df['titles']
Y = df['category']

with open('./models/encoder.pickle', 'rb') as f:
    encoder = pickle.load(f)  # 인코더를 파일로 저장

label = encoder.classes_  # 레이블 목록 확인
print(label)  # 레이블 출력

#라벨이 이미 있을 경우 transform을 쓴다면 라벨링을 할 수 있다
#빈 encoder를 사용하여 라벨링 할때는 fit_transform
labeled_y = encoder.transform(Y)

# 원-핫 인코딩(One-hot encoding)
onehot_Y = to_categorical(labeled_y)  # 카테고리를 원-핫 벡터로 변환
print(onehot_Y)  # 변환 결과 출력

okt = Okt()

# 형태소 분석 (모든 문장에 대해 처리)
for i in range(len(X)):
    X[i] = okt.morphs(X[i], stem=True)  # 어간 추출 적용

# 불용어(stopwords) 로드
stopwords = pd.read_csv('stopwords/stopwords.csv', index_col=0)  # 불용어 데이터 로드
print(stopwords)  # 불용어 목록 확인

# 불용어 제거 및 핵심 단어 필터링
for sentence in range(len(X)):
    words = []
    for word in range(len(X[sentence])):
        if len(X[sentence][word]) > 1:  # 길이가 1 이하인 단어는 제거
            if X[sentence][word] not in list(stopwords['stopword']):  # 불용어에 포함되지 않은 단어만 추가
                words.append(X[sentence][word])
    X[sentence] = ' '.join(words)  # 최종 결과를 문자열로 변환

print(X[:5])  # 전처리가 완료된 5개의 문장 출력

# 토크나이저(tokenizer) 초기화 및 텍스트 시퀀스화
token = Tokenizer()
token.fit_on_texts(X)  # 텍스트를 기반으로 토크나이저 학습
tokened_x = token.texts_to_sequences(X)  # 문장을 시퀀스(숫자 리스트)로 변환
wordsize = len(token.word_index) + 1  # 전체 단어 크기 저장 (패딩 포함)
print(wordsize)  # 단어 개수 출력

print(tokened_x[:5])  # 시퀀스로 변환된 첫 5문장 출력

# 가장 긴 문장의 길이(max)를 계산
max = 0
for i in range(len(tokened_x)):
    if max < len(tokened_x[i]):
        max = len(tokened_x[i])  # 최대 길이 갱신
print(max)  # 최대 길이 출력

with open('./models/news_token.pickle', 'rb') as f:
    token = pickle.load(f)
tokened_X = token.texts_to_sequences(X)
print(tokened_X[:5])

for i in range(len(tokened_X)):
    if len(tokened_X[i]) > 16:
        tokened_X[i] = tokened_X[i][:16]
X_pad = pad_sequences(tokened_X, max)

print(X_pad[:5])

model_path = './models/news_category_classfication_model_1.0.h5'
model = load_model(model_path)  # 모델 로드
preds = model.predict(X_pad, batch_size=32)

predicts = []
for pred in preds:
    most = label[np.argmax(pred)]
    pred[np.argmax(pred)] = 0
    second = label[np.argmax(pred)]
    predicts.append([most, second])
df['predict'] = predicts

print(df.head(30))

score = model.evaluate(X_pad, onehot_Y)
print(score[1])

df['OX'] = 0
for i in range(len(df)):
    if df.loc[i, 'category'] in df.loc[i, 'predict']:
            df.loc[i, 'OX'] = 1
print(df.OX.mean())
#dd

