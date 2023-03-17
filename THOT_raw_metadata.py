#!/usr/bin/env python
# coding: utf-8

# # **THOT raw metadata**
# 
# _by Felix Eickemeyer_
# 
# Transforms raw data from Andor to data with meta data.

# In[ ]:


import os
import sys
from thot import ThotProject
from IPython import embed
from importlib import reload

from FTE_analysis_libraries import PLQY as lqy


# In[ ]:


# Initializes Thot project
db = ThotProject( dev_root = r'PLQY_results\PLQY' )
#db = ThotProject( dev_root = r'PL' )
root = db.find_container(dict(_id = db.root))


# In[ ]:


# Generate new sample and calibration assets with metadata
asset_type = ''
container_ids = root.children
for container_id in container_ids:
    container = db.find_container( { '_id' : container_id} )
    lqy.raw_to_asset_with_metadata(container, asset_type, db, show_FN = True, show_new_asset = True)


# In[ ]:




