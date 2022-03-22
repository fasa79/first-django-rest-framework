# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 10:03:17 2022

@author: FaSa79_
"""

import pandas as pd
import numpy as np
import sqlalchemy as db

engine = db.create_engine('mysql+mysqldb://root:@localhost:3306/thd', echo = False)
connection = engine.connect()
metadata = db.MetaData()

thd_data = pd.read_excel('THD_Din.xlsx', sheet_name='THD_Din', index_col='ThdID')

# convert = {'ServiceID': int, 'ComplaintLocationLatitude': float, 'RFSdate': np.datetime64(), 'NONRFS': np.datetime64(), 'SiteLat': float}
# thd_data = thd_data.astype(convert)

thd_data.to_sql(name='api_thd', con=engine, if_exists = 'append')