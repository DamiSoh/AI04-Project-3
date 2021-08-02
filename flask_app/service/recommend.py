import pandas as pd
from sklearn.preprocessing import OrdinalEncoder
from sklearn.ensemble import RandomForestClassifier
from itertools import product

#연령, 성별, 계절에 따른 화장품 종류 선호도 예측
cols = ['age', 'sex', 'season', 'prod_type']
young = ["10대", "20대", "30대"]
old = ["40대", "50대이상"]
male =["남성"]
female =['여성']
season = ["봄", "여름", "가을", "겨울"]

#타겟 Value 
skin = [0] #기초
color = [1] #색조

#e.g. 10대, 20대 여성이라면 전 계절에 걸쳐 "색조" 제품을 선호할 것이다. 
#e.g. 40대 이상의 여성이라면 
#e.g. 혹은 전 연령의 남성이라면 "색조 외" 제품을 선호할 것이다.

first = [young, female, season, color]
first = list(product(*first))

second = [old, female, season, skin]
second = list(product(*second))

third = [young+old, male, season, skin]
third = list(product(*third))

base_date = first + second + third

#Encoding 진행 
df = pd.DataFrame(base_date, columns=cols)
train = df[cols[:3]]
target = df['prod_type']
enc = OrdinalEncoder()
train = enc.fit_transform(train)

#모델 학습 
model = RandomForestClassifier()
model.fit(train, target)

def prediction(spec):
  spec = [spec]
  spec = enc.transform(spec)
  recommend = model.predict(spec)
  if recommend[0] == 0:
    return "기초"
  else:
    return "색조"
