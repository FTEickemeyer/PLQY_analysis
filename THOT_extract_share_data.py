#!/usr/bin/env python
# coding: utf-8

# # Extract share data
# Pull all data to be sahred into it's own directory

# In[ ]:


import os
import shutil
from thot import ThotProject


# In[ ]:


# Initializes Thot project
db = ThotProject(dev_root = 'PLQY_results')

samples = db.find_assets( { 'type': 'absolute PL spectrum' } )


# In[ ]:


exch_dir = os.path.join( db.root, 'exchange' )

try:
    os.makedirs( exch_dir, exist_ok = True )
    
except OSError as error:
    print( f'Directory {exch_dir} can not be created.' )

# PLQY.csv
src = asset_filepath
FN = os.path.basename( asset_filepath )
dst =  os.path.join( exch_dir, FN )
shutil.copyfile( src, dst )

# absolute PL spectra
for sample in samples:
    src = sample.file
    FN = os.path.basename( sample.file )
    dst =  os.path.join( exch_dir, FN )
    shutil.copyfile( src, dst )
    
# all graph linear and semilog
filepath = os.path.join( exch_dir, FN_lin )
all_graph.savefig( filepath )

filepath = os.path.join( exch_dir, FN_log )
all_graph_log.savefig( filepath )

