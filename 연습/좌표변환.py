import pandas as pd

def KATEC_to_wgs84(x, y):
    WGS84 = "+proj=latlong +datum=WGS84 +ellps=WGS84"
    KATEC = "+proj=tmerc +lat_0=38.0 +lon_0=128.0 +x_0=400000.0 +y_0=600000.0 +k=0.9999 +ellps=bessel +a=6377397.155 +b=6356078.9628181886 +units=m +towgs84=-115.80,474.99,674.11,1.16,-2.31,-1.63,6.43"

    KATEC_proj = pyproj.CRS(KATEC)
    WGS84_proj = pyproj.CRS(WGS84)
    trans_func = pyproj.Transformer.from_crs( WGS84_proj, KATEC_proj, always_xy=True)
    return trans_func.transform(y, x)

def To_x(input_point):
    return input_point[0]

def To_y(input_point):
    return input_point[1]

open_csv = pd.read_csv("./school.csv", encoding= 'utf-8-sig')
open_csv['T_X'] = To_x(KATEC_to_wgs84(open_csv['latitude'], open_csv['longitude']))
open_csv['T_Y'] = To_y(KATEC_to_wgs84(open_csv['latitude'], open_csv['longitude']))
open_csv['T_X'] = open_csv['T_X'].apply(lambda x : round(x))
open_csv['T_Y'] = open_csv['T_Y'].apply(lambda x : round(x))
open_csv.to_csv('./school_job.csv', encoding= 'utf-8-sig', index= False)
