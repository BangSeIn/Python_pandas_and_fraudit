# import the Fraudit libraries
from fraudit import *

# import commonly-needed built-in libraries
import string, sys, re, random, os, os.path
# import data handling libraries
import pandas as pd
import numpy as np

df = GL_Detail.toDF()
df_log = log_file.toDF()

# 한 컬럼 기준으로 데이터프레임의 중복값 없애기
df_1 = df.drop_duplicates(subset=['컬럼이름'])

# data type이 object일 때 int로 치환
df_1['Journal_ID'] = pd.to_numeric(df_1['Journal_ID'])
df_1['ID_Shift'] = df_1['Journal_ID'].shift(1)
df_1['ID_Shift'] = df_1['ID_Shift'].fillna(0)
df_1['ID_Shift'] = df_1['ID_Shift'].astype('int64')

# 두 컬럼의 차이값을 나타내는 컬럼를 생성
df_1['diff'] = df_1['Journal_ID'] - df_1['ID_Shift']

# 컬럼값이 1이 아닌 것들만 필터링하여 새로운 데이터프레임 생성
df_2 = df_1[df_1['diff'] != 1]

# 프로딧의 Join과 같음
df_조인 = pd.merge(df_log,df,  
                  how='left', 
                  left_on = ['Journal_ID','Amount_Credit_Debit_Indicator'], 
                  right_on = ['Journal_ID','Amount_Credit_Debit_Indicator'], 
                  suffixes=('', '_df'))
# 차변금액, 대변금액 컬럼을 새로 생성
df = GL_Detail.toDF()
df = df.astype({'Amount' : np.float64})
df['차변금액'] = df.apply(lambda x : x['Amount'] 
                                   if x['Amount_Credit_Debit_Indicator'] == 'S'
                                   else 0, axis =1)
                                   
df['대변금액'] = df.apply(lambda x : x['Amount'] 
                                   if x['Amount_Credit_Debit_Indicator'] == 'H'
                                   else 0, axis =1)
                                   
                                   
# 프로딧의 그룹바이,서머라이즈 과정
gb_1 = df.groupby(['Journal_ID'])

from pandas import DataFrame

SM = DataFrame({'차변합계':gb_1['차변'].sum(),
                '대변합계':gb_1['대변'].sum()
                }
              ).reset_index()
              
              
SM['차이'] = SM ['차변합계'] == SM['대변합계']

# '차이'행의 값이 0이 아닌 컬럼 필터링하여 새로운 DF 생성
SM_필터 = SM[SM['차변'] != 0]

df['차변라운드'] = df.apply(lambda x : 1
                                   if x['차변금액']%1000 == 0 and x['차변금액'] > 0
                                   else 0, axis =1)  
                                   
df['대변라운드'] = df.apply(lambda x : 1
                                   if x['대변금액']%1000 == 0 and x['대변금액'] > 0
                                   else 0, axis =1)   
                                   
# 차대변 라운드 금액이 0이 아닌 경우만 필터링하여 DF 생성
df_ÇÊÅÍ¸µ = df[(df['차변라운드'] > 0) | (df['대변라운드'] > 0)]    
