#!/usr/bin/env python
# coding: utf-8

# # **PLQY_all**
# 
# _by Felix Eickemeyer_
# 
# Evaluation of all absolute PLQY data.

# In[ ]:


import os
from os import getcwd, listdir
import pandas as pd
import thot
from thot import ThotProject
from importlib import reload

from FTE_analysis_libraries import General as gen
from FTE_analysis_libraries import PLQY as lqy
from FTE_analysis_libraries import Spectrum as spc


# In[ ]:


# Initializes Thot project
db = ThotProject( dev_root = r'PLQY_results' )


# In[ ]:


samples = db.find_assets({'type': 'absolute PL spectrum'})
for idx, sample in enumerate(samples):
    A = sample.metadata["A"]
    PLQY = sample.metadata["PLQY"]    
    print(f'{idx:2}: {sample.name.split("_absolute")[0]:22}, A = {A:.1e}, PLQY = {PLQY:.1e}')    


# In[ ]:


#Select samples and change order
do_this_step = False

if do_this_step or ( not db.dev_mode() ):
    samples = db.find_assets({'type' : 'absolute PL spectrum'})
    #Shuai
    #order = [i for i in range(6, 20)]
    #Lin
    order = [0, 1, 5, 2, 3, 4] # without and with TPA
    
    samples_new = [samples[order[idx]] for idx in range(len(order))]
    for idx, sample in enumerate(samples_new):
        print(f'{idx:2}: {sample.name}')
    do_this_step = False
else:
    samples_new = samples


# In[ ]:


samples = samples_new
def load_spectrum(asset):
    return spc.PEL_spectrum.load(os.path.dirname(asset.file), FN = os.path.basename(asset.file), take_quants_and_units_from_file = True)
sa = []
for idx, sample in enumerate(samples):
    sample.file = sample.file
    #sample.file = sample.file+'.csv' #only for Shuai samples, delete later
    sa.append(load_spectrum(sample))
    print(f'{idx:2}: {sample.name}')


# In[ ]:


allPL = spc.PEL_spectra(sa)
allPL.names_to_label()

new_labels = []
sample_strlen = int(max([len(samples[idx].name.split('_absolute')[0]) for idx in range(len(samples))]))
for idx in range(len(samples)):
    allPL.sa[idx].plotstyle = dict(color = gen.colors[idx], linewidth = 5, linestyle = '-')
    sm = samples[idx].metadata
    A = sm['A']
    PLQY = sm['PLQY']
    s_name = samples[idx].name.split('_absolute')[0]
    new_labels.append(s_name)
    PF = allPL.sa[idx].photonflux(start = 700, stop = 900)
    print(f'{s_name.ljust(sample_strlen+1)}: A = {A:.1e}, PLQY = {PLQY:.1e}, PF = {PF:.1e} 1/(s m2)')

change_plotstyle = False
if change_plotstyle:
    allPL.sa[0].plotstyle = dict(color = gen.colors[0], linewidth = 5, linestyle = '-')
    allPL.sa[1].plotstyle = dict(color = gen.colors[0], linewidth = 5, linestyle = '-')
    allPL.sa[2].plotstyle = dict(color = gen.colors[1], linewidth = 5, linestyle = '-')
    allPL.sa[3].plotstyle = dict(color = gen.colors[1], linewidth = 5, linestyle = '-')
    allPL.sa[4].plotstyle = dict(color = gen.colors[2], linewidth = 5, linestyle = '-')
    allPL.sa[5].plotstyle = dict(color = gen.colors[3], linewidth = 5, linestyle = '-')
    #allPL.sa[6].plotstyle = dict(color = gen.colors[1], linewidth = 5, linestyle = '-')
    #allPL.sa[7].plotstyle = dict(color = gen.colors[1], linewidth = 5, linestyle = '-')
    #allPL.sa[8].plotstyle = dict(color = gen.colors[2], linewidth = 5, linestyle = '-')
    #allPL.sa[9].plotstyle = dict(color = gen.colors[2], linewidth = 5, linestyle = '-')
    #allPL.sa[10].plotstyle = dict(color = gen.colors[2], linewidth = 5, linestyle = '-')
    #allPL.sa[11].plotstyle = dict(color = gen.colors[2], linewidth = 5, linestyle = '-')
    #allPL.sa[12].plotstyle = dict(color = gen.colors[3], linewidth = 5, linestyle = '-')
    #allPL.sa[13].plotstyle = dict(color = gen.colors[3], linewidth = 5, linestyle = '-')
    #allPL.sa[14].plotstyle = dict(color = gen.colors[3], linewidth = 5, linestyle = '-')
    change_plotstyle = False
    
change_plotstyle = True
if change_plotstyle:
    for idx, sp in enumerate(allPL.sa):
        if idx < 3:
            sp.plotstyle = dict(color = gen.colors[0], linewidth = 5, linestyle = '-')
        elif idx < 12:
            sp.plotstyle = dict(color = gen.colors[1], linewidth = 5, linestyle = '-')
        elif idx < 18:
            sp.plotstyle = dict(color = gen.colors[2], linewidth = 5, linestyle = '-')            
        else:
            sp.plotstyle = dict(color = gen.colors[3], linewidth = 5, linestyle = '-')            
    change_plotstyle = False


#allPL.label(['s1', 's2', 's3', 's4', 's6'])
allPL.label(new_labels)
all_graph = allPL.plot(bottom = 0, plotstyle = 'individual', figsize = (8, 6), return_fig = True, show_plot = False)
FN_lin = 'all_absolute_PL_spectra_linear.png'
lqy.add_graph(db, FN_lin, all_graph)
all_graph_log = allPL.plot(yscale = 'log', bottom = 1e15, divisor = 1e3, plotstyle = 'individual', figsize = (8, 6), return_fig = True, show_plot = False)
FN_log = 'all_absolute_PL_spectra_semilog.png'
lqy.add_graph(db, FN_log, all_graph_log)


# In[ ]:


names = []
A_arr = []
PLQY_arr = []
peak_arr = []
Eg_arr = []
Vsq_arr = []
dV_arr = []
QFLS_arr = []
adj_fac_arr = []
fs_absint_fac_arr = []
for sample in samples:
    #print(sample.name.split('_absolute')[0])
    sm = sample.metadata
    #print(sm)
    names.append(sample.name.split('_absolute')[0])
    A_arr.append(sm['A'])
    PLQY_arr.append(sm['PLQY'])
    peak_arr.append(sm['Peak'])
    Eg_arr.append(sm['Eg'])
    Vsq_arr.append(sm['Vsq'])
    dV_arr.append(sm['dV'])
    QFLS_arr.append(sm['QFLS'])
    adj_fac_arr.append(sm['adj_fac'])
    fs_absint_fac_arr.append(sm['fs_absint_factor'])    


# In[ ]:


# Save PLQY data
do_this_step = True

if do_this_step:

    df = pd.DataFrame({'Sample' : names, 'A' : A_arr, 'PLQY' : PLQY_arr, 'PL_peak (nm)' : peak_arr, 'Eg (eV)' : Eg_arr, 'Vsq (V)' : Vsq_arr, 'delta V (V)': dV_arr, 'QFLS/q (V)' : QFLS_arr, 'fs-inb adjustment factor' : adj_fac_arr, 'fs-absolute intensity factor' : fs_absint_fac_arr})

    directory = os.path.dirname(samples[0].file) 
    FN = 'PLQY.csv'
    #if save_ok(join(directory, FN)):
    #    df.to_csv(join(directory, FN), header = True, index = False)
        
    csv_asset_prop = dict(name = 'csv_'+FN, type = 'csv', file = FN)
    csv_asset_filepath = db.add_asset(csv_asset_prop)
    df.to_csv(csv_asset_filepath, header = True, index = False)
    
    do_this_step = False


# In[ ]:


# Save PLQY data to formatted excel worksheet

if True:
    
    FN = 'PLQY.xlsx'
    xlsx_asset_prop = dict(name = 'xlsx_'+FN, type = 'xlsx', file = FN)
    xlsx_asset_filepath = db.add_asset(xlsx_asset_prop)

    writer = pd.ExcelWriter(xlsx_asset_filepath, engine='xlsxwriter')
    df_xlsx = df.copy()
    df_xlsx = df_xlsx.drop( labels = 'fs-inb adjustment factor', axis = 1)
    df_xlsx = df_xlsx.drop( labels = 'fs-absolute intensity factor', axis = 1)
    df_xlsx.to_excel(writer, index=False, header = True, sheet_name='PLQY report')

    workbook = writer.book
    worksheet = writer.sheets['PLQY report']
    
    # Add cell formats.
    
    fmt_text = workbook.add_format(
        {
        'bold': True,
        'text_wrap': True,
        'align': 'left'
        #'valign': 'center'
        #'fg_color': '#5DADE2',
        #'font_color': '#FFFFFF',
        #'border': 1
        })
    fmt_percent = workbook.add_format({'num_format': '0.0%',
                                       'align': 'center'
                                       #'bold': True
                                       #, 'bg_color': '#FFC7CE'
                                       })
    fmt_PLQY = workbook.add_format({'num_format': '0.00E+00',
                                    'align': 'center'})
    fmt_PLpeak = workbook.add_format({'num_format': '0',
                                      'align': 'center'})
    fmt_V = workbook.add_format({'num_format': '0.000',
                                 'align': 'center'})

    # Set the column width and format.
    worksheet.set_column(0, 0, sample_strlen+1, fmt_text)
    worksheet.set_column(1, 1, 10, fmt_percent)
    worksheet.set_column(2, 2, 10, fmt_PLQY)
    worksheet.set_column(3, 3, 13, fmt_PLpeak)
    worksheet.set_column(4, 7, 10, fmt_V)
    

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()


# In[ ]:


#Save all data in exchange folder
exch_dir = os.path.join(db.root, 'exchange')

try:
    os.makedirs(exch_dir, exist_ok = True)
except OSError as error:
    print("Directory '%s' can not be created" % exch_dir)
    
import shutil

# PLQY.csv
csv_src = csv_asset_filepath
csv_FN = os.path.basename(csv_asset_filepath)
csv_dst =  os.path.join(exch_dir, csv_FN)
shutil.copyfile(csv_src, csv_dst)

# PLQY.xlsx
xlsx_src = xlsx_asset_filepath
xlsx_FN = os.path.basename(xlsx_asset_filepath)
xlsx_dst =  os.path.join(exch_dir, xlsx_FN)
shutil.copyfile(xlsx_src, xlsx_dst)

# absolute PL spectra
for idx, sample in enumerate(samples):
    src = sample.file
    FN = os.path.basename(sample.file)
    dst =  os.path.join(exch_dir, FN)
    shutil.copyfile(src, dst)
    


# In[ ]:


# all graph linear and semilog
filepath = os.path.join(exch_dir, FN_lin)
all_graph.savefig(filepath)

filepath = os.path.join(exch_dir, FN_log)
all_graph_log.savefig(filepath)


# In[ ]:




