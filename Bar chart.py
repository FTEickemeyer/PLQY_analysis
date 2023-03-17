#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import thot
from thot import ThotProject
from FTE_analysis_libraries import PLQY as lqy


# In[ ]:


# Initializes Thot project
db = ThotProject(dev_root=r'PLQY_results')


# In[ ]:


PLQY = db.find_assets({'type': 'xlsx'})
fp = PLQY[0].file


# In[ ]:


#fp = r'C:\Users\dreickem\switchdrive\Work\Python\PL\Steady_state_PL\PLQY\PLQY_results\exchange\PLQY.xlsx'


# In[ ]:


df = pd.read_excel(fp)
df.head(n=len(df))


# In[ ]:


# modify 'Sample' string if necessary
if False:
    for sample in df['Sample']:
        if len(sample.split('-')[-1].split('_')[0]) == 3:
            print(sample)
    #print(df['Sample'].str.split('_'))


# In[ ]:


# Change Sample name so that it is exactly the same for all equivalent samples
#df['Sample'] = df['Sample'].str[:-2]
df['Sample'] = df['Sample'].str.split('_').str.get(0)
#df['Sample'] = df['Sample'].str.split('-').str.get(0)
#df['Sample'] = np.asarray(df['Sample'].str.split('-').values)
df.head(n=len(df))


# In[ ]:


# modify 'Sample' string if necessary
if False:
    for idx, sample in enumerate(df['Sample']):
        if len(sample.split('_')[-1]) == 3:
            print(sample)
            print(sample[:-4])
            df.at[idx, 'Sample'] = sample[:-4]
    df.head(n=len(df))


# In[ ]:


# Now we can group it by the same name
df_gr = df.groupby('Sample')
# Calculate the standard deviation
df_std = df_gr.std()
df_std.reset_index(inplace=True)
# ... and the mean value
df_mean = df_gr.mean()
df_mean.reset_index(inplace=True)
# Display the grouped data
df_mean.head(n=len(df_mean))


# In[ ]:


if True:
    new_order = [0, 3, 4, 1, 2]
    mean = df_mean.reindex(new_order)
else:
    mean = df_mean
mean = mean.reset_index()
mean.pop('index')
mean = mean.set_index('Sample').iloc[::-1]

std = df_std.reindex(new_order)
std = std.reset_index()
std.pop('index')
std = std.set_index('Sample').iloc[::-1]

figs = []

for column in mean.columns:
    fig, ax = plt.subplots()
    if column == 'PLQY':
        logx = True
        xlim = None
    else:
        logx = False
        min_x = np.min(mean[column] - std[column])
        max_x = np.max(mean[column] + std[column])
        xlim = (min_x - 0.02*(max_x-min_x), max_x + 0.02*(max_x-min_x))
    if True:
        barplot = mean[column].plot.barh(xerr=std[column], ax=ax, logx=logx, ylabel='', xlabel=column, capsize=4, xlim=xlim, rot=0)
    else:
        barplot = mean[column].plot.barh(ax=ax, logx=logx, ylabel='', xlabel=column, capsize=4, xlim=xlim, rot=0)
        ax.bar_label(ax.containers[0], fmt='%.1e')
    plt.tight_layout()
    figs.append(fig)
    plt.show()


# In[ ]:


# Save mean and std

def save_mean_std(FN, df):
    csv_asset_prop = dict(name='csv_'+FN, type='csv', file=FN)
    csv_asset_filepath = db.add_asset(csv_asset_prop)
    df.to_csv(csv_asset_filepath, header=True, index=True)
    exch_dir = os.path.join(db.root, 'exchange')
    filepath = os.path.join(exch_dir, FN)
    df.to_csv(filepath, header=True, index=True)

save_mean_std('PLQY_mean.csv', mean)
save_mean_std('PLQY_std.csv', std)


# In[ ]:


for column, fig in zip(mean.columns, figs):
    FN_barplot = 'barplot_'+column.replace('/q', '')+'.png'
    print(FN_barplot)
    lqy.add_graph(db, FN_barplot, fig)
    exch_dir = os.path.join(db.root, 'exchange')
    filepath = os.path.join(exch_dir, FN_barplot)
    fig.savefig(filepath)


# In[ ]:




