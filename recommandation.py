import item_simirarity as ism
import user_simirarity as usm
from import_data import database
import pandas as pd
from collections import defaultdict

def recommandation(user, db, clothes):
    clothes_columns = ['clothesId', 'fit', 'spring', 'summer', 'autumn', 'winter', 'subCategory', 'mainCategory']
    prefrence_columns = ['uid', 'codiId']
    codi_clothes_columns = ['codiId', 'clothesId']
    
    clothes_data = pd.DataFrame(db.select_columns('musinsacloset', clothes_columns), columns=clothes_columns)
    preference_data = pd.DataFrame(db.select_columns('preference', prefrence_columns), columns=['userId', 'codiId'])
    codi_clothes_data = pd.DataFrame(db.select_columns('codi_clothes', codi_clothes_columns), columns=codi_clothes_columns)
    
    
    recommand_codies = usm.find_nearest_users(preference_data, user)
    clothes_data = clothes_data.set_index('clothesId', drop=False)
    codi_clothes_data = codi_clothes_data.set_index('codiId', drop=False)
    recommand_codi_clothes_data = pd.DataFrame(columns = codi_clothes_data.columns)
    for codi in recommand_codies:
        try:
            recommand_codi_clothes_data = pd.concat([recommand_codi_clothes_data, codi_clothes_data.loc[codi]])
        except:
            continue
    codi_clotes_dict = defaultdict(list)
    
    for i in range(len(codi_clothes_data)):
        data = codi_clothes_data.iloc[i].values
        codi_clotes_dict[data[0]].append(data[1])
    
    for codi in codi_clotes_dict.keys():
        category = clothes_data.loc[codi_clotes_dict[codi][0]]['mainCategory']
        if  category == '스커트' or category == '바지':
            codi_clotes_dict[codi][0], codi_clotes_dict[codi][1] = codi_clotes_dict[codi][1], codi_clotes_dict[codi][0]
    
    clothes_dict = defaultdict(int)
#     #item = 580958
    category = clothes_data.loc[clothes]['mainCategory']
    candidates = [clothes]
    if category == '스커트' or category == '바지':
        category_idx, recommand_idx = 1, 0
    else:
        category_idx, recommand_idx = 0, 1
    for item in codi_clotes_dict.values():
        clothes_dict[item[category_idx]] = item[recommand_idx]
        candidates.append(item[category_idx])

    candidates_data = clothes_data.loc[candidates]
    
    recommandations = ism.genre_recommendations(clothes, candidates_data, clothes_columns)
    recommandations = [clothes_dict[item] for item in recommandations]

    return recommandations