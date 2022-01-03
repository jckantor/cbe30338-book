#!/usr/bin/env python
# coding: utf-8

# # PID Control
# 
# ## References
# 
# Karl J. Astrom and Richard Murray (2016). _Feedback Systems: An Introduction for Scientists and Engineers, 2nd Edition_.  [Web version available]( http://www.cds.caltech.edu/~murray/amwiki/index.php/Second_Edition).

# ## PID Simulation

# In[2]:


get_ipython().system('pip install slycot')
get_ipython().system('pip install control')


# In[3]:


get_ipython().run_line_magic('matplotlib', 'inline')

import numpy as np
import matplotlib.pyplot as plt
import control.matlab as control

# control constants
Kc = 0.85
tauI = 10000

# control transfer function
Gc = Kc*control.tf([tauI,1],[tauI,0])

# model transfer functions
Gp = control.tf([0.31],[16,1])*control.tf([1],[135,1])


# In[5]:


t = np.linspace(0,1000)
y,t = control.step(Gp,t)
plt.plot(t,50*y + 22)


# In[7]:


# control constants
Kc = 2
tauI = 60

# control transfer function
Gc = Kc*control.tf([tauI,1],[tauI,0])

t = np.linspace(0,1000)

H = Gp*Gc/(1+Gp*Gc)
y,t = control.step(H,t)
plt.plot(t,y)


# ## PID Implementation
# 
# ### Reference Conditions
# 
# One of the implementation issues for PID control of the Temperature Control Lab is choice of reference conditions. One reason is that the linearization on which PID analysis is based is only valid in some 'neighborhood' of a nominal operating condition. But perhaps a more typical situation in most practical 

# In[8]:


get_ipython().run_line_magic('matplotlib', 'inline')

import sys
sys.path.append('..')
from TCLab import TCLab, clock, pid

# ambient and reference values
Tamb = 20
Tref = 50
uref = (Tref - Tamb)/0.85

# control parameters
b = 1              # setpoint weighting
kp = 0.8          # proportional control gain
ki = kp/60

# sampling period
tf = 1200           # experiment length (sec.)
h = 1               # sample time (sec.)

# setpoint function
def Tset(t):
    if t <= 900:
        return 50
    else:
        return 35


bi = ki*h

r = Tset(0) - Tref
y = Tamb - Tref

P = kp*(b*r - y)
I = 0

uref,P,I,r


# In[9]:


# device initialization
with TCLab() as a:
    a.initplot(tf)
    for t in clock(tf,h):
        r = Tset(t) - Tref
        y = a.T1 - Tref
    
        P = kp*(b*r - y)
        v = P + I
    
        u = max(0,min(200,v + uref))
        I += bi*(r-y)
    
        a.Q1 = u
        a.updateplot()
        


# In[ ]:




