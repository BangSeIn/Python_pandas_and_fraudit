# import the Fraudit libraries
from fraudit import *

# import commonly-needed built-in libraries
import string, sys, re, random, os, os.path
# import data handling libraries
import pandas as pd
import numpy as np

from pandas import Series, DataFrame

df_merged = 분개장.toDF()

# 1. 프로딧 서머라이즈 
res1 = Grouping.summarize_by_value(분개장, "전표일자", "전표번호", 차변합계="sum(group['차변금액'])")

# 1-1. 인덱스칼럼 삽입
res1.insert_index("S_INDEX")

# 1-2. 상세분석 칼럼 삽입
res1.insert_calculated_static(0, "상세분석", str, "0")


# 2. 프로딧 group
res2 = Grouping.stratify_by_value(분개장, 0, "전표일자", "전표번호")

# 2-1. 상세 그룹 테이블 작성
상세분석_리스트 = [i[1] for i in zip(res1['상세분석'],res1['S_INDEX']) if i[0] == "1"]


상세_프로딧 = TableArray()

for i in 상세분석_리스트:
    상세_프로딧 = 상세_프로딧 + TableArray(res2[i])
    
if len(상세_프로딧) == 0 :
    del 상세_프로딧




#=========================================================================


# 2.판다스 서머라이즈
gb_1 = df_merged.groupby(['전표일자', "전표번호"])

df_res1 = DataFrame({'차변합계' : gb_1['차변금액'].sum(),
                    }
                   ).reset_index()
                   
# 2-1. 인덱스칼럼 삽입
df_res1 = df_res1.reset_index()
df_res1 = df_res1.rename(columns = {"index" : "S_INDEX"})

서머라이즈 = Table(data = df_res1)

서머라이즈.insert_calculated_static(0, "상세분석", str, "0")




# 4.판다스 group
gb_1 = df_merged.groupby(['전표일자', "전표번호"])

df_merged['S_INDEX'] = gb_1.ngroup()

# 4-1. ['그룹_인덱스'] 칼럼 순서 맨 앞으로
cols = list(df_merged.columns)
인덱스 = df_merged.columns.get_loc('S_INDEX')
cols.pop(인덱스)
cols.insert(0,'S_INDEX')

df_merged = df_merged[cols]
     
# 4-2. df_merged 소팅
df_merged = df_merged.sort_values('S_INDEX')

# 4-3. 프로딧 res1에 상세분석 칼럼에 분석하고자하는 groupby 테이블에 '1' 기입

상세분석_리스트 = [i[1] for i in zip(서머라이즈['상세분석'],서머라이즈['S_INDEX']) if i[0] == "1"]

# 4-4. 상세테이블 작성
상세_df = TableArray()

for i in 상세분석_리스트:
    상세_df = 상세_df + TableArray(Table(data = df_merged[df_merged['S_INDEX']==i]))
    
if len(상세_df) == 0 :
    del 상세_df


   
    