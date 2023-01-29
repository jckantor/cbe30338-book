#!/usr/bin/env python
# coding: utf-8

# # Step Testing
# 
# This notebook guides you through the steps necessary to perform a simple step test of a heater/sensor unit on the Temperature Contnrol Lab. 
# 
# Download this notebook to your laptop, then run these cells to capture step test data.

# In[1]:


import matplotlib.pyplot as plt
import pandas as pd

from tclab import TCLab, clock, Historian, Plotter


# ## Executing the Step Test
# 
# ### Verify an Initial Steady State
# 
# **Don't start a step test without first letting the device come to an initial steady state!**
# 
# A step test assumes the system is initially at steady state. In the case of the Temperature Control Lab, the initial steady with no power input would be room temperature. It generally takes 10 minutes or more to reach steady state. We'll do a measurement to confirm the initial temperature. Repeat this until you are sure you are at an initial steady state.

# In[3]:


lab = TCLab()
print(lab.T1, lab.T1)
lab.close()


# ### Conduct the Experiment

# In[16]:


# experimental parameters
P1 = 200
Q1 = 50
tfinal = 600

# perform experiment
with TCLab() as lab:
    lab.P1 = P1
    h = Historian(lab.sources)
    p = Plotter(h, tfinal)
    lab.Q1(Q1)
    for t in clock(tfinal):
        p.update(t)


# ### Verify the Experimental Data

# In[18]:


h.to_csv("data.csv")


# ### Verify the Data File

# In[26]:


import pandas as pd
df = pd.read_csv('data.csv').set_index('Time')
df.plot(grid=True)


# In[27]:


df.head()


# In[28]:


df.tail()


# In[ ]:




