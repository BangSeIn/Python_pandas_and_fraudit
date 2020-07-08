# import the Fraudit libraries
from fraudit import *

# import commonly-needed built-in libraries
import string, sys, re, random, os, os.path
# import data handling libraries
import pandas as pd
import numpy as np

#https://wikidocs.net/46759
from DataFrame import pandas
df = 분개장예제_2.toDF()

결과 = pd.DataFrame({ '차변합계' : df.groupby(['전표일자','전표번호'])['차변금액'].sum()})
#********결과 = 결과.reset_index()	#인덱스 붙여주기 잊지 말기!*************

#통계함수는 sum, count, mean, median(=중간값), std, var, min, max, prod(전체곱=), first,last(=그룹의 첫번째,마지막값) 가능
"""
gb = df.groupby(['A','B'])	#프로딧 그룹바이
df2 = DataFrame({'A합계' : 이름['A'].sum()})  #프로딧 서머라이즈바이
df['A합계'] = gb_1['A'].transform("sum")   #트랜스폼
df['인덱스'] = gb_1.ngroup()	#프로딧의 그룹바이했을 때 그룹 인덱스를 삽입해줌
"""

"""
#데이터프레임에서 특정 열 A를 맨 앞으로 옮기는 법
df = 분개장.toDF()	
cols = list(df.columns)
A인덱스 = df.columns.get_loc('A열')
del cols[A인덱스]
cols.insert(0,'A열') ##0 대신 1,2,를 넣으면 앞에서 둘째, 셋째 행에 삽입할 수 있음!
df = df[cols]	#바뀐 columns 리스트로 업데이트하여 순서 바꿈
"""

#전표일자, 전표번호별로 그룹바이하기
gb_1 = df.groupby(['전표일자','전표번호'])

#그룹 인덱스를 df에 추가하기
df['인덱스'] = gb_1.ngroup()

#'인덱스'행을 맨 앞으로 끌어오기
cols = list(df.columns)
인덱스 = df.columns.get_loc('인덱스')
del cols[인덱스]
cols.insert(0,'인덱스')
df = df[cols]

#res1은 프로딧의 그룹바이밸류, res2는 프로딧의 서머라이즈밸류(차변금액의 최대) 후 res2에 S_INDEX 삽입  (+++res1과 res2는 모두 ['전표일자','전표번호']로 그룹핑하였음!+++)
#이후 res2의 차변금액 최대를 내림차순 정렬 후 상세분석 열을 추가하여 맨 위 10개 행만 1로 표기했을 때(1인 것만 뽑아내도록),
#새로운 테이블 res3에 맨 위 10개 행에 대한 res1의 그룹들만 넣어 표시하는 방법은 아래와 같음
#헷갈리면 직접해보기
li = [res2[i]['S_INDEX'] for i in range(len(res2)) if res2[i]['상세분석'] == '1']
res3 = TableArray( [res1[i] for i in li] )  #res1[i]는 '테이블' 타입임
