import pandas as pd


#open_csv = pd.read_csv("./aptlist.csv", encoding= 'utf-8-sig')
#open_csv['T_X'] = To_x(KATEC_to_wgs84(open_csv['latitude'], open_csv['longitude']))
#open_csv['T_Y'] = To_y(KATEC_to_wgs84(open_csv['latitude'], open_csv['longitude']))
#open_csv['T_X'] = open_csv['T_X'].apply(lambda x : round(x))
#open_csv['T_Y'] = open_csv['T_Y'].apply(lambda x : round(x))
#open_csv.to_csv('./aptlist_table.csv', encoding= 'utf-8-sig', index= False)

open_csv1 = pd.read_csv("./school_table.csv", encoding= 'utf-8-sig', usecols=[0, 19, 20])
open_csv2 = pd.read_csv("./aptlist_table.csv", encoding= 'utf-8-sig', usecols=[0, 18, 19])

result = open_csv1['T_X'] -  open_csv2['T_X']
print(result)