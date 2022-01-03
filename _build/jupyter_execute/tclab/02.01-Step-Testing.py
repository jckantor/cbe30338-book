#!/usr/bin/env python
# coding: utf-8

# <!--NOTEBOOK_HEADER-->
# *This notebook contains course material from [CBE32338](https://jckantor.github.io/CBE32338)
# by Jeffrey Kantor (jeff at nd.edu); the content is available [on Github](https://github.com/jckantor/CBE2338.git).
# The text is released under the [CC-BY-NC-ND-4.0 license](https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode),
# and code is released under the [MIT license](https://opensource.org/licenses/MIT).*

# <!--NAVIGATION-->
# < [Model Identification](http://nbviewer.jupyter.org/github/jckantor/CBE32338/blob/master/notebooks/02.00-Model-Identification.ipynb) | [Contents](toc.ipynb) | [Fitting Step Test Data to Empirical Models](http://nbviewer.jupyter.org/github/jckantor/CBE32338/blob/master/notebooks/02.02-Fitting-Step-Test-Data-to-Empirical-Models.ipynb) ><p><a href="https://colab.research.google.com/github/jckantor/CBE32338/blob/master/notebooks/02.01-Step-Testing.ipynb"><img align="left" src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open in Colab" title="Open in Google Colaboratory"></a><p><a href="https://raw.githubusercontent.com/jckantor/CBE32338/master/notebooks/02.01-Step-Testing.ipynb"><img align="left" src="https://img.shields.io/badge/Github-Download-blue.svg" alt="Download" title="Download Notebook"></a>

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


# <!--NAVIGATION-->
# < [Model Identification](http://nbviewer.jupyter.org/github/jckantor/CBE32338/blob/master/notebooks/02.00-Model-Identification.ipynb) | [Contents](toc.ipynb) | [Fitting Step Test Data to Empirical Models](http://nbviewer.jupyter.org/github/jckantor/CBE32338/blob/master/notebooks/02.02-Fitting-Step-Test-Data-to-Empirical-Models.ipynb) ><p><a href="https://colab.research.google.com/github/jckantor/CBE32338/blob/master/notebooks/02.01-Step-Testing.ipynb"><img align="left" src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open in Colab" title="Open in Google Colaboratory"></a><p><a href="https://raw.githubusercontent.com/jckantor/CBE32338/master/notebooks/02.01-Step-Testing.ipynb"><img align="left" src="https://img.shields.io/badge/Github-Download-blue.svg" alt="Download" title="Download Notebook"></a>
