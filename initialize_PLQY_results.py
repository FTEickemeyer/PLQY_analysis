#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import shutil

from FTE_analysis_libraries import General as gen

working_dir = os.getcwd()
source_dir = os.path.join(working_dir, 'PLQY_results - template')
destination_dir = os.path.join(working_dir, 'PLQY_results')


# In[2]:


# delete all files in source_dir

for root, dirs, files in os.walk(destination_dir):
    for file in files:
        filepath = os.path.join(root, file)
        try:
            os.remove(gen.win_long_fp(filepath))
            #print(f'removed: {file}')
        except OSError as error:
            #print(error)
            pass


# In[3]:


# now delete all directories

for i in range(3): # We have 3 directory layers
    for root, dirs, files in os.walk(destination_dir):
        for directory in dirs:
            directory = os.path.join(root, directory)
            try:
                os.rmdir(gen.win_long_fp(directory))
                #print("Directory '% s' has been removed successfully" % directory)
            except OSError as error:
                #print(error)
                #print("Directory '% s' can not be removed" % directory)
                pass


# In[4]:


# copy directories

for root, dirs, files in os.walk(source_dir):
    rel_root = gen.win_long_fp(os.path.relpath(root, source_dir))
    for directory in dirs:
        dir_new = gen.win_long_fp(os.path.join(destination_dir, rel_root, directory))
        if not os.path.exists(dir_new):
            os.mkdir(dir_new)


# In[5]:


# copy files

for root, dirs, files in os.walk(source_dir):
    rel_root = gen.win_long_fp(os.path.relpath(root, source_dir))
    for file in files:
        fp_dst = gen.win_long_fp(os.path.join(destination_dir, rel_root, file))
        if not os.path.exists(fp_dst):
            fp_src = gen.win_long_fp(os.path.join(root, file))
            shutil.copyfile(fp_src, fp_dst)


# In[ ]:




