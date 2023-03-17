#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os


# In[ ]:


working_dir = os.getcwd()
FP_raw_met = os.path.join(working_dir, "THOT_raw_metadata.py")
FP_calib = os.path.join(working_dir, "THOT_calibration.py")


# In[ ]:


print(FP_raw_met)
print(FP_calib)


# In[ ]:


get_ipython().run_line_magic('run', '-t "C:\\Users\\dreickem\\switchdrive\\Work\\Python\\PL\\Steady_state_PL\\PLQY\\THOT_raw_metadata.py"')


# In[ ]:


get_ipython().run_line_magic('run', '-t "C:\\Users\\dreickem\\switchdrive\\Work\\Python\\PL\\Steady_state_PL\\PLQY\\THOT_calibration.py"')


# In[ ]:




