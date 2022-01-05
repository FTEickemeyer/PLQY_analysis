#!/usr/bin/env python
# coding: utf-8

# # **PLQY_individual**
# 
# _by Felix Eickemeyer_
# 
# Calibration and correction has to be done before. 

# In[1]:


import os
from os import getcwd, listdir
import thot
from thot import ThotProject
import importlib
from importlib import reload

from FTE_analysis_libraries import PLQY as lqy
from FTE_analysis_libraries import Spectrum as spc
from FTE_analysis_libraries.General import f1240, Vsq, V_loss, QFLS


# In[2]:


#Perovskite
#which_sample = 'Haizhou-FAPbI3'
which_sample = 'FAPbI3'

#DSC
#which_sample = 'Yameng DSC'
#which_sample = 'dye on TiO2'
#which_sample = 'dye on Al2O3'
#which_sample = 'Coumarin 153'
#which_sample = 'MS5'
#which_sample = 'XY1b'

param = lqy.exp_param(which_sample = which_sample, excitation_laser = None, PL_left = None, PL_right = None, PL_peak = None, corr_offs_left = 40, corr_offs_right = 50, PL_peak_auto = False, eval_Pb = False)
#Schawaller, Salathe
#param = lqy.exp_param(which_sample = None, excitation_laser = 657, PL_left = 705, PL_right = 1000, PL_peak = 720, corr_offs_left = 0, corr_offs_right = 10, PL_peak_auto = False, eval_Pb = False)


# In[3]:


# Initializes Thot project
db = ThotProject( dev_root = r'PLQY_results' )


# In[2]:


<<<<<<< REMOTE CELL DELETED >>>>>>>
# Initializes Thot project
db = ThotProject( dev_root = '../double_perovskite_temperature_dependence/trial-06' )
root = db.find_container( { '_id': db.root } )


# In[4]:


samples = db.find_assets({'type' : 'calibrated PL spectrum'})
names = list({sample.metadata['name'] for sample in samples})
<<<<<<< local
if 'no sample' in names:
    raise RuntimeError( 'No sample data not found.' )

if 'exclude' in root.metadata:
    for exc in root.metadata[ 'exclude' ]:
        names.remove(exc)

if db.dev_mode():
    print( names )
=======
names.remove('no sample')
names
>>>>>>> remote


# In[12]:


La = lqy.find({'metadata.name' : 'no sample', 'metadata.em_filter' : param.laser_marker}, samples, show_details = True)
Pa = lqy.find({'metadata.name' : 'no sample', 'metadata.em_filter' : param.PL_marker}, samples, show_details = True)


# In[6]:


for idx in range(len(names)):
    show_details = True
    sample_name = names[idx]
    
    print('____________________________')
    print(sample_name)
    
    group = thot.filter({'metadata.name' : sample_name}, samples)
    Lb = lqy.find({'metadata.em_filter' : param.laser_marker, 'metadata.inboob' : 'outofbeam'}, group, show_details = show_details)
    Lc = lqy.find({'metadata.em_filter' : param.laser_marker, 'metadata.inboob' : 'inbeam'}, group, show_details = show_details)
    Pb = lqy.find({'metadata.em_filter' : param.PL_marker, 'metadata.inboob' : 'outofbeam'}, group, show_details = show_details)
    Pc = lqy.find({'metadata.em_filter' : param.PL_marker, 'metadata.inboob' : 'inbeam'}, group, show_details = show_details)
    fs = lqy.find({'metadata.em_filter' : param.PL_marker, 'metadata.fsip' : 'fs'}, group, show_details = show_details)

    show_details = True

    sPL = lqy.PLQY_dataset(db, La, Lb, Lc, Pa, Pb, Pc, fs, sample_name, param)
    #sPL.fs.plot(yscale = 'linear', title = sPL.fs_asset.metadata['orig_fn'])
    #sPL.P.plot()

    sPL.find_PL_peak()
    sPL.inb_adjust(adj_factor = None, show_adjust_factor = False, show = show_details)
    sPL.calc_abs(what = 'inb', show_details = show_details)

    #sPL.oob_adjust(adj_factor = None, show_adjust_factor = True, show = True)
    #sPL.calc_abs(what = 'oob', show_details = show_details)

    sPL.calc_PLQY(show = show_details, show_lum = 'linear')

    sPL.abs_pf_spec(nsuns = 1)

    sPL.save_asset()


# In[ ]:




