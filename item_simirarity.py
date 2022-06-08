import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
#from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
fit={
    1 : '스키니',
    1.5: '스키니슬림',
    2:'슬림',
    2.5:'슬림레귤러',
    3:'레귤러',
    3.5: '레귤러루즈',
    4:'루즈',
    4.5: '루즈오버사이즈',
    5: '오버사이즈'
    }
seasons = ['spring', 'summer', 'autumn', 'winter']

def filter_data(data, column, values):
    condition = pd.Series([False]*len(data))
    for value in values:
        condition |= data[column]==value
    return data[list(condition)]

def item_string(data, columns):
    string_data = ['']*len(data)
    for i in range(len(data)):
        row = data.iloc[i]
        for column in columns:
            if column == 'fit':
                string_data[i] += f"{fit[row[column]]} "
            elif column in seasons:
                if row[column] == 1:
                    string_data[i] += f"{column} "
            else:
                string_data[i] += f" {row[column]}"
    data['string_data'] = string_data
    return data['string_data']
                
                
            
def item_cosine_similarity(data, columns, tfidf_vector = TfidfVectorizer()):
    data = item_string(data, columns)
    tfidf_matrix = tfidf_vector.fit_transform(data).toarray()
    #tfidf_matrix_feature = tfidf_vector.get_feature_names_out()
    #tfidf_matrix = pd.DataFrame(tfidf_matrix, columns=tfidf_matrix_feature)
    cosine_sim = cosine_similarity(tfidf_matrix)
    return tfidf_matrix

def index_dict(data):
    idx_dict = dict()
    for i, idx in enumerate(data['clothesId']):
        idx_dict[idx] = i
    return idx_dict
        
def genre_recommendations(target_title, data, columns, tfidf_vector = TfidfVectorizer(), k=5):
    sim_matrix = item_cosine_similarity(data, columns, tfidf_vector = TfidfVectorizer())
    idx_dict = index_dict(data)
    target = idx_dict[target_title]
    recom_idx = sim_matrix[target].reshape(1, -1).argsort()[:, ::-1].flatten()[1:k+1]
    recoms = [data.iloc[idx]['clothesId'] for idx in recom_idx]
    return recoms