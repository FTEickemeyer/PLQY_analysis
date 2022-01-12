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
root = db.find_container( { '_id': db.root } )


# In[2]:


exch_dir = os.path.join(
    db.root,
    root.metadata.get( 'share_dir', 'exchange' )
)

try:
    os.makedirs( exch_dir, exist_ok = True )
    
except OSError as error:
    raise RuntimeError( f'Directory {exch_dir} can not be created.' )

# collect assets for extraction
abs_pl = db.find_assets( { 'type': 'absolute PL spectrum' } )  # extract all absolute PL spectra
tagged = db.find_assets( { 'tags': { '$in': [ 'share' ] } } )  # extract all tagged assets

# copy files into share folder
for sample in [ *abs_pl, *tagged ]:
    src = sample.file
    FN = os.path.basename( sample.file )
    dst =  os.path.join( exch_dir, FN )
    shutil.copyfile( src, dst )


# In[ ]:




