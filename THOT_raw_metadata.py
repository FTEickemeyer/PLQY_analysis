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

from FTE_analysis_libraries import PLQY as lqy


# In[ ]:


# Initializes Thot project
db = ThotProject( dev_root = 'PLQY_results/PLQY' )
root = db.find_container( { '_id': db.root } )


# In[ ]:


# Generate new sample and calibration assets with metadata
asset_type = ''
container_ids = root.children
for container_id in container_ids:
    container = db.find_container( { '_id': container_id } )
    lqy.raw_to_asset_with_metadata(
        container,
        asset_type,
        db,
        show_FN = ( False and db.dev_mode() ),
        show_new_asset = ( False and db.dev_mode() )
    )


# In[ ]:




