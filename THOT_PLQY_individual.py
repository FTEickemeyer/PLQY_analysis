#!/usr/bin/env python
# coding: utf-8

# # **PLQY_individual**
# 
# _by Felix Eickemeyer_
# 
# PLQY
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


# Initializes Thot project
db = ThotProject( dev_root = '../hong-sn' )
root = db.find_container( { '_id': db.root } )


# In[3]:


# Perovskite
if 'sample_type' in root.metadata:
    which_sample = root.metadata[ 'sample_type' ]

else:
    # default sample type
    which_sample = 'FAPbI3'

    #DSC
    #which_sample = 'Yameng DSC'
    #which_sample = 'dye on TiO2'
    #which_sample = 'dye on Al2O3'
    #which_sample = 'Coumarin 153'
    #which_sample = 'MS5'
    #which_sample = 'XY1b'

param = lqy.exp_param(
    which_sample = which_sample,
    excitation_laser = None,
    PL_left = None,
    PL_right = None,
    PL_peak = None,
    corr_offs_left = 40,
    corr_offs_right = 50,
    PL_peak_auto = False,
    eval_Pb = False
)


# In[4]:


samples = db.find_assets({'type' : 'calibrated PL spectrum'})
names = list({sample.metadata['name'] for sample in samples})
names.remove('no sample')
if 'exclude' in root.metadata:
    for exc in root.metadata[ 'exclude' ]:
        names.remove(exc)

if db.dev_mode():
    print( names )


# In[5]:


La = lqy.find(
    {
        'metadata.name' : 'no sample',
        'metadata.em_filter' : param.laser_marker
    }, 
    samples, 
    show_details = ( True and db.dev_mode() )
)

Pa = lqy.find(
    {
        'metadata.name' : 'no sample',
        'metadata.em_filter' : param.PL_marker
    },
    samples,
    show_details = ( True and db.dev_mode() )
)


# In[6]:


for sample_name in names:
    show_details = True and db.dev_mode()
    print( sample_name )
    group = thot.filter({'metadata.name' : sample_name}, samples)
    Lb = lqy.find({'metadata.em_filter' : param.laser_marker, 'metadata.inboob' : 'outofbeam'}, group, show_details = show_details)
    Lc = lqy.find({'metadata.em_filter' : param.laser_marker, 'metadata.inboob' : 'inbeam'}, group, show_details = show_details)
    Pb = lqy.find({'metadata.em_filter' : param.PL_marker, 'metadata.inboob' : 'outofbeam'}, group, show_details = show_details)
    Pc = lqy.find({'metadata.em_filter' : param.PL_marker, 'metadata.inboob' : 'inbeam'}, group, show_details = show_details)
    fs = lqy.find({'metadata.em_filter' : param.PL_marker, 'metadata.fsip' : 'fs'}, group, show_details = show_details)

    show_details = True and db.dev_mode()

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




