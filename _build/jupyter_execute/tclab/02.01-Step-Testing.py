#!/usr/bin/env python
# coding: utf-8

# # Step Testing
# 
# ## Reference materials
# 
# * Alizadeh, Esmaeil. "A Guide to Non-Minimum Phase Systems." *Towards Data Science.* https://towardsdatascience.com/a-guide-to-non-minimum-phase-systems-1403350917a0. Accessed 6 Decewmber 2020.

# In[2]:


get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
import pandas as pd

from tclab import TCLab, clock, Historian, Plotter


# ## Executing the Step Test
# 
# ### Verify an Initial Steady State
# 
# A step test assumes the system is initially at steady state. In the case of the Temperature Control Lab, the initial steady with no power input would be room temperature. It generally takes 10 minutes or more to reach steady state. We'll do a measurement to confirm the initial temperature.

# In[3]:


lab = TCLab()
print(lab.T1, lab.T1)
lab.close()


# ### Conduct the Experiment

# In[4]:


# experimental parameters
Q1 = 50
tfinal = 800

# perform experiment
with TCLab() as lab:
    h = Historian(lab.sources)
    p = Plotter(h, tfinal)
    lab.Q1(0)
    for t in clock(tfinal):
        p.update(t)
        lab.Q1(Q1)


# ### Verify the Experimental Data

# In[3]:


t = h.t
T1 = h.T1
T2 = h.T2
Q1 = h.Q1
Q2 = h.Q2

plt.plot(t, T1, t, T2, t, Q1, t, Q2)
plt.legend(['T1','T2','Q1','Q2'])
plt.xlabel('time / seconds')
plt.grid()


# ### Convert to a DataFrame

# In[4]:


import pandas as pd

df = pd.DataFrame([t, T1, T2, Q1]).T
df.columns = ['Time', 'T1', 'T2', 'Q1']
df = df.set_index('Time')
df.plot(grid=True)


# ### Save DataFrame as a .csv file

# In[5]:


df.to_csv('Step_Test_Data.csv')


# ### Verify the Data File

# In[2]:


get_ipython().run_line_magic('matplotlib', 'inline')

pd.read_csv('Step_Test_Data.csv').set_index('Time').plot(grid=True)


# In[7]:


df.head()


# In[8]:


df.tail()

