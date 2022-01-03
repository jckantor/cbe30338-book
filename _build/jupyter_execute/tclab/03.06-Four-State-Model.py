#!/usr/bin/env python
# coding: utf-8

# # Four State Model

# ## Multivariable Heater/Sensor System
# 
# Model equations
# 
# \begin{align}
# C^H_p\frac{dT_{H,1}}{dt} & = U_a(T_{amb} - T_{H,1}) + U_b(T_{H,2}-T_{H,1}) + U_c(T_{S,1} - T_{H,1}) + P_1u_1\\
# C^S_p\frac{dT_{S,1}}{dt} & = U_c(T_{H,1} - T_{S,1})  \\
# C^H_p\frac{dT_{H,2}}{dt} & = U_a(T_{amb} - T_{H,2}) + U_b(T_{H,1}-T_{H,2}) + U_c(T_{S,2} - T_{H,2}) + P_2u_2\\
# C^S_p\frac{dT_{S,2}}{dt} & = U_c(T_{H,2} - T_{S,2}) 
# \end{align}
# 
# 
# 

# ## Deviation variables
# 
# \begin{align}
# \frac{dT_{H,1}'}{dt} & = -(\frac{U_a+U_b+U_c}{C^H_p})T_{H,1}' + \frac{U_b}{C^H_p}T_{H,2}' + \frac{U_c}{C^H_p}T_{S,1}' + \frac{P_1}{C^H_p}u_1\\
# \frac{dT_{S,1}'}{dt} & = \frac{U_c}{C^S_p}(T_{H,1}' - T_{S,1}')  \\
# \frac{dT_{H,2}'}{dt} & = -(\frac{U_a+U_b+U_c}{C^H_p})T_{H,2}' + \frac{U_b}{C^H_p}T_{H,1}' + \frac{U_c}{C^H_p}T_{S,2}' + \frac{P_2}{C^H_p}u_2\\
# \frac{dT_{S,2}'}{dt} & = \frac{U_c}{C^S_p}(T_{H,2}' - T_{S,2}') 
# \end{align}

# ## State space
# 
# \begin{align}
# \left[\begin{array}{c}\frac{dT_{H,1}'}{dt} \\ \frac{dT_{S,1}'}{dt} \\ \frac{dT_{H,2}'}{dt} \\ \frac{dT_{S,2}'}{dt}\end{array}\right]
# & = 
# \left[\begin{array}{cccc}
# -(\frac{U_a+U_b+U_c}{C^H_p}) & \frac{U_c}{C^H_p} & \frac{U_b}{C^H_p} & 0 \\
# \frac{U_c}{C^S_p} & -\frac{U_c}{C^S_p} & 0 & 0 \\
# \frac{U_b}{C^H_p} & 0 & -(\frac{U_a+U_b+U_c}{C^H_p}) & \frac{U_c}{C^H_p} \\
# 0 & 0 & \frac{U_c}{C^H_p} & -\frac{U_c}{C^H_p}
# \end{array}\right]
# \left[\begin{array}{c}T_{H,1}' \\ T_{S,1}' \\ T_{H,2}' \\ T_{S,2}'\end{array}\right]
# +
# \left[\begin{array}{cc}\frac{P_1}{C_p} & 0 \\ 0 & 0 \\ 0 & \frac{P_2}{C_p} \\ 0 & 0 \end{array}\right]
# \left[\begin{array}{c}u_1 \\ u_2\end{array}\right]
# \end{align}

# In[8]:


get_ipython().run_line_magic('matplotlib', 'inline')
import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from ipywidgets import interact

data = pd.read_csv('Step_Test_Data.csv').set_index('Time')[1:]
t = data.index
T1 = data['T1'].values
T2 = data['T2'].values

# known parameter values
P1 = 4
u1 = 0.5   # steady state value of u1 (fraction of total power)
P2 = 2
u2 = 0.0
T_ambient = 21.5

def compare(Ua, Ub, Uc, Cp_H, Cp_S):

    def deriv(T,t):
        T_H1, T_S1, T_H2, T_S2 = T
        dT_H1 = -(Ua + Ub + Uc)*T_H1/Cp_H + Ub*T_H2/Cp_H + Uc*T_S1/Cp_H + P1*u1/Cp_H
        dT_S1 = Uc*T_H1/Cp_S - Uc*T_S1/Cp_S
        dT_H2 = -(Ua + Ub + Uc)*T_H2/Cp_H + Ub*T_H1/Cp_H + Uc*T_S2/Cp_H + P2*u2/Cp_H
        dT_S2 = Uc*T_H2/Cp_S - Uc*T_S2/Cp_S
        return [dT_H1, dT_S1, dT_H2, dT_S2]
    T = odeint(deriv, [0,0,0,0], t)

    plt.figure(figsize=(12,6))
    plt.subplot(2,1,1)
    plt.plot(t, T[:,1] + T_ambient, t, T[:,3] + T_ambient, t, T1, t, T2)
    plt.xlabel('Time / seconds')
    plt.ylabel('Temperature / °C')
    plt.grid()
    plt.subplot(2,1,2)
    plt.plot(t, T[:,1]-T1+T_ambient)
    plt.plot(t, T[:,3]-T2+T_ambient)
    plt.grid

# parameter values and units
P1 = 4                 # watts
P2 = 2                 # watts
Ua = 0.044             # watts/deg C
Ub = 0.018             # watts/deg C
Cp = 7                 # joules/deg C

w = interact(compare, Ua=(0,0.06,0.001), Ub=(0,0.06,0.001), Uc=(0,0.06,0.001), Cp_H=(3,11,0.01), Cp_S = (0.1,2,.01))


# In[3]:


import numpy as np

Ua = 0.043
Ub = 0.022
Uc = 0.036
Cp_H = 6.38
Cp_S = 0.98

A = [[-(Ua+Ub+Uc)/Cp_H, Uc/Cp_H, Ub/Cp_H, 0],
     [Uc/Cp_S, -Uc/Cp_S, 0, 0],
     [Ub/Cp_H, 0, -(Ua+Ub+Uc)/Cp_H, Uc/Cp_H],
     [0, 0, Uc/Cp_H, -Uc/Cp_H]
    ]

evals, evecs = np.linalg.eig(A)

1/evals


# In[4]:


def compare(Ua, Ub, Uc, Cp_H, Cp_S):

    def deriv(T,t):
        T_H1, T_S1, T_H2, T_S2 = T
        dT_H1 = -(Ua + Ub + Uc)*T_H1/Cp_H + Ub*T_H2/Cp_H + Uc*T_S1/Cp_H + P1*u1/Cp_H
        dT_S1 = Uc*T_H1/Cp_S - Uc*T_S1/Cp_S
        dT_H2 = -(Ua + Ub + Uc)*T_H2/Cp_H + Ub*T_H1/Cp_H + Uc*T_S2/Cp_H + P2*u2/Cp_H
        dT_S2 = Uc*T_H2/Cp_S - Uc*T_S2/Cp_S
        return [dT_H1, dT_S1, dT_H2, dT_S2]
    T = odeint(deriv, [0,0,0,0], t)

    plt.figure(figsize=(12,6))
    plt.subplot(2,1,1)
    plt.plot(t, T[:,1] + T_ambient, t, T[:,3] + T_ambient)
    plt.plot(t, T[:,0] + T_ambient)
    plt.plot(t, T[:,2] + T_ambient)
    plt.xlabel('Time / seconds')
    plt.ylabel('Temperature / °C')
    plt.grid()
    plt.subplot(2,1,2)
    plt.plot(t, T[:,1]-T1+T_ambient)
    plt.plot(t, T[:,3]-T2+T_ambient)
    plt.grid
    print(Ua,Ub,Uc,Cp_H,Cp_S)


# In[ ]:




