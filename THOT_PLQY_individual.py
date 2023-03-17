#!/usr/bin/env python
# coding: utf-8

# # **PLQY_individual**
# 
# _by Felix Eickemeyer_
# 
# Calculation of PLQY for each sample.

# In[ ]:


import sys
import warnings

import thot
from thot import ThotProject

from FTE_analysis_libraries import PLQY as lqy

if False:
    import importlib
    from importlib import reload
    reload(lqy)


# In[ ]:


# Initializes Thot project
db = ThotProject( dev_root = r'PLQY_results' )
root = db.find_container( dict(_id = db.root) )


# In[ ]:


#Perovskite

if 'sample_type' in root.metadata:
    which_sample = root.metadata[ 'sample_type' ]

else:
    # default sample type
    # which_sample = 'Haizhou-FAPbI3'
    which_sample = 'FAPbI3'

    #DSC
    #which_sample = 'Yameng DSC'
    #which_sample = 'dye on TiO2'
    #which_sample = 'dye on Al2O3'
    #which_sample = 'Coumarin 153'
    #which_sample = 'MS5'
    #which_sample = 'XY1b'

param = lqy.exp_param(which_sample=which_sample,
                      excitation_laser=None,
                      PL_left=None,
                      PL_right=None,
                      PL_peak=None,
                      corr_offs_left=20,
                      corr_offs_right=30,
                      PL_peak_auto=False,
                      eval_Pb=False)

param2 = lqy.exp_param(which_sample=None,
                      excitation_laser=422,
                      PL_left=470,
                      PL_right=600,
                      PL_peak=None,
                      corr_offs_left=20,
                      corr_offs_right=30,
                      PL_peak_auto=True,
                      eval_Pb=False)


# In[ ]:


if False:
    param.corr_offs_left = 20 #50
    param.corr_offs_right = 30 #60


# In[ ]:


samples = db.find_assets({'type' : 'calibrated PL spectrum'})
names = list({sample.metadata['name'] for sample in samples})
names.remove('no sample')
if 'exclude' in root.metadata:
    for exc in root.metadata[ 'exclude' ]:
        names.remove(exc)
#Select samples
if False:
    # select = [i for i in range(len(names)) if (i in [3, 4, 6, 7, 8])]
    # names = [names[select[idx]] for idx in range(len(select))]
    names = [name for name in names if ('-Au_' in name)]
if db.dev_mode():
    for idx, name in enumerate(names):
        print(f'{idx:2}: {name}')


# In[ ]:


La = lqy.find({'metadata.name' : 'no sample', 'metadata.em_filter' : param.laser_marker}, samples, show_details = ( True and db.dev_mode() ))
Pa = lqy.find({'metadata.name' : 'no sample', 'metadata.em_filter' : param.PL_marker}, samples, show_details = ( True and db.dev_mode() ))


# In[ ]:


# You can change maxNumberOutputs in settings: click on Menu bar → Settings → Advanced Settings Editor → Notebook → set maxNumberOutputs in the User Preferences tab, like:
# {
#     "maxNumberOutputs": 0
# }

#idx = 0
#param.eval_Pb = True
skip_inb_adjust = False

show_details = ( False and db.dev_mode() )
show_inbeam_correction = ( True and db.dev_mode() )

save_plots = ( False or not db.dev_mode() )


for idx in range(len(names)):

    sample_name = names[idx]


    print(f'\n{idx:}____________________________')
    print(sample_name)

    group = thot.filter({'metadata.name' : sample_name}, samples)
    Lb = lqy.find({'metadata.em_filter' : param.laser_marker, 'metadata.inboob' : 'outofbeam'}, group, show_details = show_details)
    Lc = lqy.find({'metadata.em_filter' : param.laser_marker, 'metadata.inboob' : 'inbeam'}, group, show_details = show_details)
    Pb = lqy.find({'metadata.em_filter' : param.PL_marker, 'metadata.inboob' : 'outofbeam'}, group, show_details = show_details)
    Pc = lqy.find({'metadata.em_filter' : param.PL_marker, 'metadata.inboob' : 'inbeam'}, group, show_details = show_details)
    fs = lqy.find({'metadata.em_filter' : param.PL_marker, 'metadata.fsip' : 'fs'}, group, show_details = show_details)

    if ( Lb is None ) or ( Lc is None ) or (fs is None) or ( Pc is None ) or ( (Pb is None) and (param.eval_Pb == True) ):
        warnings.warn("Attention: One or more of the necessary data is missing, PLQY can't be evaluated!")
        continue

    sPL = lqy.PLQY_dataset(db, La, Lb, Lc, Pa, Pb, Pc, fs, sample_name, param)
    # sPL.fs.plot(yscale = 'linear', title = sPL.fs_asset.metadata['orig_fn'])

    sPL.find_PL_peak()
    print(f'PL peak: {sPL.PL_peak:.0f} nm')

    if skip_inb_adjust:
        sPL.Pc_corrfac = 1
        sPL.adj_factor = 1
    else:
        sPL.inb_adjust(adj_factor = None, show_adjust_factor = False, save_plots = save_plots, show_plots = show_details, show_inbeam_correction=show_inbeam_correction)
        sPL.calc_abs(what = 'inb', save_plots = show_details, show_plot = show_details)

    if param.eval_Pb is True:
        sPL.oob_adjust(adj_factor = None, show_adjust_factor = True, save_plots = save_plots, show_plots = show_details)
        sPL.calc_abs(what = 'oob', save_plots = show_details, show_plot = show_details)

    sPL.calc_PLQY(show = show_details, show_plots = show_details, save_plots = save_plots, show_lum = 'linear')

    sPL.abs_pf_spec(nsuns=1)

    if not show_details:
        A = sPL.A
        PLQY = sPL.PLQY
        print(f'A = {A:.1f}, PLQY = {PLQY:.1e}')

    sPL.save_asset()


# In[ ]:


#sPL.La.plot()


# In[ ]:


sys.exit()


# # Single data evaluation

# In[ ]:


if False:
    import importlib
    from importlib import reload
    reload(lqy)


# In[ ]:


# Re-initialize the Thot project and use different parameters

if False:
    # Initializes Thot project
    db = ThotProject( dev_root = r'PLQY_results' )
    root = db.find_container( dict(_id = db.root) )
    #Perovskite

    if 'sample_type' in root.metadata:
        which_sample = root.metadata[ 'sample_type' ]

    else:
        # default sample type
        # which_sample = 'Haizhou-FAPbI3'
        which_sample = 'FAPbI3'

        #DSC
        #which_sample = 'Yameng DSC'
        #which_sample = 'dye on TiO2'
        #which_sample = 'dye on Al2O3'
        #which_sample = 'Coumarin 153'
        #which_sample = 'MS5'
        #which_sample = 'XY1b'

    param = lqy.exp_param(which_sample=which_sample,
                          excitation_laser=None,
                          PL_left=None,
                          PL_right=None,
                          PL_peak=None,
                          corr_offs_left=40,
                          corr_offs_right=50,
                          PL_peak_auto=False,
                          eval_Pb=False)

    param2 = lqy.exp_param(which_sample=None,
                          excitation_laser=422,
                          PL_left=470,
                          PL_right=600,
                          PL_peak=None,
                          corr_offs_left=20,
                          corr_offs_right=30,
                          PL_peak_auto=True,
                          eval_Pb=False)

    samples = db.find_assets({'type' : 'calibrated PL spectrum'})
    names = list({sample.metadata['name'] for sample in samples})
    names.remove('no sample')
    if 'exclude' in root.metadata:
        for exc in root.metadata[ 'exclude' ]:
            names.remove(exc)
    if db.dev_mode():
        print( names )

    La = lqy.find({'metadata.name' : 'no sample', 'metadata.em_filter' : param.laser_marker}, samples, show_details = ( True and db.dev_mode() ))
    Pa = lqy.find({'metadata.name' : 'no sample', 'metadata.em_filter' : param.PL_marker}, samples, show_details = ( True and db.dev_mode() ))


# In[ ]:


if False:
    param.corr_offs_left = 20 #50
    param.corr_offs_right = 30 #60


# In[ ]:


#idx = 10
idx = 3
param.eval_Pb = False
skip_inb_adjust = False

show_details = ( True and db.dev_mode() )
save_plots = ( False or not db.dev_mode() )

sample_name = names[idx]

print(f'\n{idx:}____________________________')
print(sample_name)

group = thot.filter({'metadata.name' : sample_name}, samples)
Lb = lqy.find({'metadata.em_filter' : param.laser_marker, 'metadata.inboob' : 'outofbeam'}, group, show_details = show_details)
Lc = lqy.find({'metadata.em_filter' : param.laser_marker, 'metadata.inboob' : 'inbeam'}, group, show_details = show_details)
Pb = lqy.find({'metadata.em_filter' : param.PL_marker, 'metadata.inboob' : 'outofbeam'}, group, show_details = show_details)
Pc = lqy.find({'metadata.em_filter' : param.PL_marker, 'metadata.inboob' : 'inbeam'}, group, show_details = show_details)
fs = lqy.find({'metadata.em_filter' : param.PL_marker, 'metadata.fsip' : 'fs'}, group, show_details = show_details)

# Choose a different data
group = thot.filter({'metadata.name' : names[8]}, samples)
Lb = lqy.find({'metadata.em_filter' : param.laser_marker, 'metadata.inboob' : 'outofbeam'}, group, show_details = show_details)
Pb = lqy.find({'metadata.em_filter' : param.PL_marker, 'metadata.inboob' : 'outofbeam'}, group, show_details = show_details)
#fs = lqy.find({'metadata.em_filter' : param.PL_marker, 'metadata.fsip' : 'fs'}, group, show_details = show_details)

sPL = lqy.PLQY_dataset(db, La, Lb, Lc, Pa, Pb, Pc, fs, sample_name, param)
# sPL.fs.plot(yscale = 'linear', title = sPL.fs_asset.metadata['orig_fn'])

sPL.find_PL_peak()
print(f'PL peak: {sPL.PL_peak:.0f} nm')

if skip_inb_adjust:
    sPL.Pc_corrfac = 1
    sPL.adj_factor = 1
else:
    sPL.inb_adjust(adj_factor = None, show_adjust_factor = False, save_plots = save_plots, show_plots = show_details)
    sPL.calc_abs(what = 'inb', save_plots = show_details, show_plot = show_details)

if param.eval_Pb is True:
    sPL.oob_adjust(adj_factor = None, show_adjust_factor = True, save_plots = save_plots, show_plots = show_details)
    sPL.calc_abs(what = 'oob', save_plots = show_details, show_plot = show_details)

sPL.calc_PLQY(show = show_details, show_plots = show_details, save_plots = save_plots, show_lum = 'linear')

sPL.abs_pf_spec(nsuns=1)

if False:
    if not show_details:
        A = sPL.A
        PLQY = sPL.PLQY
        print(f'A = {A:.1f}, PLQY = {PLQY:.1e}')
    sPL.save_asset()
    


# # Determine laser light intensity

# In[ ]:


from math import pi
from FTE_analysis_libraries import General as gen
from FTE_analysis_libraries.General import f1240, k, T_RT, F, q, epsilon_0, F, h, c

A_laser = pi/4 * 693.0e-6 * 891.0e-6  #m2 for 657 nm laser
A_hole = pi/4 * (3e-3)**2 #m2
PE = h * c / 660e-9 
laser = sPL.La
laser_int = laser.calc_integrated_photonflux() * PE * A_hole
print(f'The laser intensity is {laser_int*1000:.2e} mW')


# In[ ]:


if False:
    for idx in range(len(names)):

        sample_name = names[idx]


        print(f'\n{idx:}____________________________')
        print(sample_name)

        show_details = False
        group = thot.filter({'metadata.name' : sample_name}, samples)
        Lb = lqy.find({'metadata.em_filter' : param.laser_marker, 'metadata.inboob' : 'outofbeam'}, group, show_details = show_details)
        Lc = lqy.find({'metadata.em_filter' : param.laser_marker, 'metadata.inboob' : 'inbeam'}, group, show_details = show_details)
        Pb = lqy.find({'metadata.em_filter' : param.PL_marker, 'metadata.inboob' : 'outofbeam'}, group, show_details = show_details)
        Pc = lqy.find({'metadata.em_filter' : param.PL_marker, 'metadata.inboob' : 'inbeam'}, group, show_details = show_details)
        fs = lqy.find({'metadata.em_filter' : param.PL_marker, 'metadata.fsip' : 'fs'}, group, show_details = show_details)

        if ( Lb is None ) or ( Lc is None ) or (fs is None) or ( Pc is None ) or ( (Pb is None) and (param.eval_Pb == True) ):
            warnings.warn("Attention: One or more of the necessary data is missing, PLQY can't be evaluated!")
            continue

        sPL = lqy.PLQY_dataset(db, La, Lb, Lc, Pa, Pb, Pc, fs, sample_name, param)
        laser = sPL.La
        laser_int = laser.calc_integrated_photonflux() * PE * A_hole
        print(f'The laser intensity is {laser_int*1000:.2e} mW')


# # Minimum PLQY to be measured

# In[ ]:


dat = sPL.Pa
m = dat.y.mean()
std = dat.y.std()
dat.plot(hline = [m, m-3*std, m+3*std])
print(f'Standard deviation: {std:.1e}')


# In[ ]:


# Take a PL with clearly visible PL peak (e.g. highest PLQY)
idx = 0
param.eval_Pb = False
skip_inb_adjust = False

show_details = ( True and db.dev_mode() )
save_plots = ( False or not db.dev_mode() )



sample_name = names[idx]


print(f'\n{idx:}____________________________')
print(sample_name)

group = thot.filter({'metadata.name' : sample_name}, samples)
Lb = lqy.find({'metadata.em_filter' : param.laser_marker, 'metadata.inboob' : 'outofbeam'}, group, show_details = show_details)
Lc = lqy.find({'metadata.em_filter' : param.laser_marker, 'metadata.inboob' : 'inbeam'}, group, show_details = show_details)
Pb = lqy.find({'metadata.em_filter' : param.PL_marker, 'metadata.inboob' : 'outofbeam'}, group, show_details = show_details)
Pc = lqy.find({'metadata.em_filter' : param.PL_marker, 'metadata.inboob' : 'inbeam'}, group, show_details = show_details)
fs = lqy.find({'metadata.em_filter' : param.PL_marker, 'metadata.fsip' : 'fs'}, group, show_details = show_details)

sPL = lqy.PLQY_dataset(db, La, Lb, Lc, Pa, Pb, Pc, fs, sample_name, param)
# sPL.fs.plot(yscale = 'linear', title = sPL.fs_asset.metadata['orig_fn'])

sPL.find_PL_peak()
print(f'PL peak: {sPL.PL_peak:.0f} nm')

if skip_inb_adjust:
    sPL.Pc_corrfac = 1
    sPL.adj_factor = 1
else:
    sPL.inb_adjust(adj_factor = None, show_adjust_factor = False, save_plots = save_plots, show_plots = show_details)
    sPL.calc_abs(what = 'inb', save_plots = show_details, show_plot = show_details)

# Min signal that can be measured
sPL.Pc.y *= 3*std/sPL.Pc.max_within(left = None, right = None)
sPL.Pb.y *= 0

if param.eval_Pb is True:
    sPL.oob_adjust(adj_factor = None, show_adjust_factor = True, save_plots = save_plots, show_plots = show_details)
    sPL.calc_abs(what = 'oob', save_plots = show_details, show_plot = show_details)

sPL.calc_PLQY(show = show_details, show_plots = show_details, save_plots = save_plots, show_lum = 'linear')

sPL.abs_pf_spec(nsuns=1)

# A = sPL.A
# PLQY = sPL.PLQY
# print(f'A = {A:.1f}, PLQY = {PLQY:.1e}')

#sPL.save_asset()


# ### Test calculate PL spectrum without reabsorption

# In[ ]:


# Re-initialize the Thot project and use different parameters

if True:
    # Initializes Thot project
    db = ThotProject( dev_root = r'PLQY_results' )
    root = db.find_container( dict(_id = db.root) )
    #Perovskite

    if 'sample_type' in root.metadata:
        which_sample = root.metadata[ 'sample_type' ]

    else:
        # default sample type
        which_sample = 'Haizhou-FAPbI3'
        #which_sample = 'FAPbI3'

        #DSC
        #which_sample = 'Yameng DSC'
        #which_sample = 'dye on TiO2'
        #which_sample = 'dye on Al2O3'
        #which_sample = 'Coumarin 153'
        #which_sample = 'MS5'
        #which_sample = 'XY1b'

    param = lqy.exp_param(which_sample=which_sample,
                          excitation_laser=None,
                          PL_left=None,
                          PL_right=None,
                          PL_peak=None,
                          corr_offs_left=40,
                          corr_offs_right=50,
                          PL_peak_auto=False,
                          eval_Pb=False)

    param.corr_offs_left = 60
    param.corr_offs_right = 70

    param2 = lqy.exp_param(which_sample=None,
                          excitation_laser=422,
                          PL_left=470,
                          PL_right=600,
                          PL_peak=None,
                          corr_offs_left=20,
                          corr_offs_right=30,
                          PL_peak_auto=True,
                          eval_Pb=False)

    samples = db.find_assets({'type' : 'calibrated PL spectrum'})
    names = list({sample.metadata['name'] for sample in samples})
    names.remove('no sample')
    if 'exclude' in root.metadata:
        for exc in root.metadata[ 'exclude' ]:
            names.remove(exc)
    if db.dev_mode():
        print( names )

    La = lqy.find({'metadata.name' : 'no sample', 'metadata.em_filter' : param.laser_marker}, samples, show_details = ( True and db.dev_mode() ))
    Pa = lqy.find({'metadata.name' : 'no sample', 'metadata.em_filter' : param.PL_marker}, samples, show_details = ( True and db.dev_mode() ))


# In[ ]:


idx = 2
param.eval_Pb = False
skip_inb_adjust = False

show_details = ( True and db.dev_mode() )
save_plots = ( False or not db.dev_mode() )

sample_name = names[idx]

print(f'\n{idx:}____________________________')
print(sample_name)

group = thot.filter({'metadata.name' : sample_name}, samples)
Lb = lqy.find({'metadata.em_filter' : param.laser_marker, 'metadata.inboob' : 'outofbeam'}, group, show_details = show_details)
Lc = lqy.find({'metadata.em_filter' : param.laser_marker, 'metadata.inboob' : 'inbeam'}, group, show_details = show_details)
Pb = lqy.find({'metadata.em_filter' : param.PL_marker, 'metadata.inboob' : 'outofbeam'}, group, show_details = show_details)
Pc = lqy.find({'metadata.em_filter' : param.PL_marker, 'metadata.inboob' : 'inbeam'}, group, show_details = show_details)
fs = lqy.find({'metadata.em_filter' : param.PL_marker, 'metadata.fsip' : 'fs'}, group, show_details = show_details)

# Choose a different data
#group = thot.filter({'metadata.name' : names[0]}, samples)
#fs = lqy.find({'metadata.em_filter' : param.PL_marker, 'metadata.fsip' : 'fs'}, group, show_details = show_details)

sPL = lqy.PLQY_dataset(db, La, Lb, Lc, Pa, Pb, Pc, fs, sample_name, param)
# sPL.fs.plot(yscale = 'linear', title = sPL.fs_asset.metadata['orig_fn'])

sPL.find_PL_peak()
print(f'PL peak: {sPL.PL_peak:.0f} nm')

if skip_inb_adjust:
    sPL.Pc_corrfac = 1
    sPL.adj_factor = 1
else:
    sPL.inb_adjust(adj_factor = None, show_adjust_factor = False, save_plots = save_plots, show_plots = show_details)
    sPL.calc_abs(what = 'inb', save_plots = show_details, show_plot = show_details)

if param.eval_Pb is True:
    sPL.oob_adjust(adj_factor = None, show_adjust_factor = True, save_plots = save_plots, show_plots = show_details)
    sPL.calc_abs(what = 'oob', save_plots = show_details, show_plot = show_details)

sPL.calc_PLQY(show = show_details, show_plots = show_details, save_plots = save_plots, show_lum = 'linear')

sPL.abs_pf_spec(nsuns=1)

if False:
    if not show_details:
        A = sPL.A
        PLQY = sPL.PLQY
        print(f'A = {A:.1f}, PLQY = {PLQY:.1e}')
    sPL.save_asset()
    


# In[ ]:


sPL.Pc_orig.plot()


# In[ ]:


import numpy as np
from FTE_analysis_libraries import Spectrum as spc

fs = sPL.Pc
y_fs = fs.y
ib = sPL.Pc_orig
y_ib = ib.y
x = fs.x
m = spc.PEL_spectra([ib, fs])
m.label(['ib', 'fs'])
m.plot()

zero_mask = np.where( y_fs != 0 )
A = 1-y_ib[zero_mask]/y_fs[zero_mask]
s = spc.abs_spectrum(x[zero_mask], A)
s.qy = 'A'
s.plot(title = 'Absorptance spectrum', hline = 0, bottom = -0.2, top = 1, figsize = (8,5), return_fig = False, show_plot = True)


# In[ ]:


m_new = m.copy()


# In[ ]:


#T = 1-1.39*A
T = 1-1.1*A
new = fs.copy()
#new = ib.copy()
new.y /= T
m_new.add(new)
m_new.normalize()
m_new.plot(yscale='linear', bottom=0)
#m_new.plot(yscale='log')
#m_new.plot(yscale='log', bottom=1e14, left=740, right=900)


# In[ ]:


sp = new.nm_to_eV()
sp.plot()
bb = sp.BBT_fit(Efit_start = 1.58, Efit_stop = 1.70, Tguess = 300)
#bb = sp.BBT_fit(Efit_start = 1.9, Efit_stop = 2.0, Tguess = 660)
sa = spc.spectra([sp, bb])
sa.label(['EL spectrum', f'BB fit: $T = {bb.T:.0f}$ K'])
m_max = max(sp.y)
sa.plot(title = 'High energy tail fit with BB spectrum', yscale = 'log', bottom = m_max / 500, top = 1.2 * m_max, left = 1.3, right = 1.75, figsize = (7,5))


# In[ ]:





# In[ ]:




