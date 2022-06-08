import numpy as np
import pandas as pd
import csv
import requests
from urllib.parse import quote_plus
from tqdm import tqdm
import random

def random_survey(number,items):
    style=tqdm(items['style'])
    style=set(style)
    a_list=[]
    for j in style :
        count=0 
        tmp=[0,0,0,0,0] # 가져올 데이터가 담기는 곳
        while count<number : # 데이터 값 중 가져올 데이터의 갯수
            t=random.randrange(0,(items.size/7)-1) # 사이즈가 행의 7배 -> range 뽑기위해 가정
            flag=1
            for i in tmp:
                if i==t: # 중복데이터 넘어가게 하는 코드
                    flag=0 # 데이터 안 뽑음  
            if flag==1 and items.values[t,5] == j : 
                tmp[count]=t
                count=count+1
                a=[csv_test.values[t,0],csv_test.values[t,5],csv_test.values[t,6]]
                a_list.append(a)
    return(a_list)