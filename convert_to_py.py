# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 12:54:32 2021

@author: dreickem
"""
import os
import os.path
import time

os.system('jupyter nbconvert --to script *.ipynb')

fns = os.listdir(os.getcwd())
for fn in fns:
    extension = os.path.splitext(fn)[1]
    #print(extension)
    if (fn[0:4] == 'THOT') and (extension == '.py'):
        new_fn = fn.split(' ')[0]+'.py'
        os.rename(fn, new_fn)
