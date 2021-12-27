#!/usr/bin/env python
# coding: utf-8

# # Model Identification

# ## Experimental Inputs

# In[34]:


get_ipython().run_line_magic('matplotlib', 'notebook')

import numpy as np
import matplotlib.pyplot as plt

tperiod = 120
tsample = 1

tp  = [0,  0,  0, 600, 600, 1200, 1200]
u1p = [0,  0, 60,  60,   0,    0,    0]
u2p = [0,  0,  0,   0,  60,    60,   0]

def u1(t):
    return np.interp(t, tp, u1p, left=0, right=0)

def u2(t):
    return np.interp(t, tp, u2p, left=0, right=0)

t = np.linspace(0, 1200, 1200)
plt.plot(t, u1(t), t, u2(t))


# ## Perform Experiment

# In[42]:


from tclab import TCLab, clock, Historian, Plotter


tperiod = 1800
tsample = 1
    
with TCLab() as lab:
    sources = [
        ('T1', lambda: lab.T1),
        ('T2', lambda: lab.T2),
        ('P1', lambda: lab.P1),
        ('U1', lambda: lab.U1),
        ('P2', lambda: lab.P2),
        ('U2', lambda: lab.U2),
    ]
    h = Historian(sources)
    p = Plotter(h, tperiod)
    lab.P1 = 255
    lab.P2 = 255
    for t in clock(tperiod, tsample):
        lab.U1 = u1(t)
        lab.U2 = u2(t)
        p.update(t)

h.to_csv('data.csv')


# ## Fit Model to Data

# In[43]:


# read data file

import pandas as pd

data = pd.read_csv('data.csv').set_index('Time')[1:]
t = data.index
T1 = data['T1'].values
T2 = data['T2'].values
P1 = data['P1'].values
P2 = data['P2'].values
U1 = data['U1'].values
U2 = data['U2'].values

# known parameter values
T_ambient = (T1[0] + T2[0])/2.0
T_ambient

P1 = 0.013*P1.mean()
P2 = 0.013*P2.mean()


# In[44]:


# data plotting function

def plot_data(t, T1, T1_pred, T2, T2_pred, U1, U2):
    
    fig = plt.figure(figsize=(8,5))
    grid = plt.GridSpec(4, 1)
    ax = [fig.add_subplot(grid[:2]), fig.add_subplot(grid[2]), fig.add_subplot(grid[3])]

    ax[0].plot(t, T1, t, T1_pred, t, T2, t, T2_pred)
    ax[0].set_ylabel("deg C")
    ax[0].legend(["T1", "T1_pred", "T2", "T2_pred"])
    
    ax[1].plot(t, T1_pred - T1, t, T2_pred - T2)
    ax[1].set_ylabel("deg C")
    ax[1].legend(["T_pred - "])
    
    ax[2].plot(t, U1, t, U2)
    ax[2].set_ylabel("%")
    ax[2].legend(["U1", "U2"])
    
    for a in ax: a.grid(True)
    ax[-1].set_xlabel("time / seconds")
    plt.tight_layout()
    
plot_data(t, T1, T1, T2, T2, U1, U2)


# In[58]:


from ipywidgets import interact
from scipy.integrate import odeint
from scipy.optimize import minimize

def compare(Ua, Ub, Uc, Cp_H, Cp_S):
    model_complete([Ua, Ub, Uc, Cp_H, Cp_S], True)

def model_complete(param, plot=False):
    
    Ua, Ub, Uc, Cp_H, Cp_S = param

    def deriv(T, t):
        T_H1, T_S1, T_H2, T_S2 = T
        dT_H1 = -(Ua + Ub + Uc)*T_H1/Cp_H + Ub*T_H2/Cp_H + Uc*T_S1/Cp_H + P1*u1(t)/Cp_H/100
        dT_S1 = Uc*T_H1/Cp_S - Uc*T_S1/Cp_S
        dT_H2 = -(Ua + Ub + Uc)*T_H2/Cp_H + Ub*T_H1/Cp_H + Uc*T_S2/Cp_H + P2*u2(t)/Cp_H/100
        dT_S2 = Uc*T_H2/Cp_S - Uc*T_S2/Cp_S
        return [dT_H1, dT_S1, dT_H2, dT_S2]
    
    T = odeint(deriv, [0,0,0,0], t)
    
    T1_pred = T[:,1] + T_ambient
    T2_pred = T[:,3] + T_ambient
    
    print(param)
    if plot:
        plot_data(t, T1, T1_pred, T2, T2_pred, U1, U2)
        
    return np.linalg.norm(T[:,1] - T1 + T_ambient) + np.linalg.norm(T[:,3] - T2 + T_ambient)

# parameter values and units
Ua = 0.036             # watts/deg C
Ub = 0.01            # watts/deg C
Uc = 0.08
Cp_H = 4.9                # joules/deg C
Cp_S = 1.26


w = interact(compare, 
             Ua=(0, 2*Ua, 0.001), 
             Ub=(0, 2*Ub, 0.001), 
             Uc=(0, 2*Uc, 0.001), 
             Cp_H=(0, 2*Cp_H, 0.01), 
             Cp_S = (0, 2*Cp_S, .01))


# In[ ]:




