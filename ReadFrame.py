import urllib2
from datetime import datetime
import pandas as pd
import numpy as np
import os
def read_to_frame(directory):
    import re
    allfiles = os.listdir(directory)
    #filter all files
    allfiles = filter(lambda x: x.startswith('vhi_'), allfiles)
    #create empty main frame
    main_frame = pd.DataFrame({'year':[],'week':[],'SMN':[],'SMT':[],'VCI':[],'TCI':[],'VHI':[],'province_id':[]})
    for file in allfiles:
        df = pd.read_table('%s/%s'%(directory, file),
                           names=['year','week','SMN','SMT','VCI','TCI','VHI'],
                           sep='[ ,]+',
                           engine = 'python')
        #get ID with file name
        province_id = re.search(r'\d+', file).group(0)
        df['province_id'] = setNewProvinceIndex(int(province_id))
        #add main frame to df
        main_frame = pd.concat([main_frame,df], ignore_index=True)
    return main_frame
def setNewProvinceIndex(old_index):
    reindex = {
        1:22,
        2:24,
        3:23,
        4:25,
        5:3,
        6:4,
        7:8,
        8:19,
        9:20,
        10:21,
        11:9,
        12:26,
        13:10,
        14:11,
        15:12,
        16:13,
        17:14,
        18:15,
        19:16,
        20:27,
        21:17,
        22:18,
        23:6,
        24:1,
        25:2,
        26:7,
        27:5
            }
    if old_index in reindex:
        return reindex[old_index]
    return np.nan