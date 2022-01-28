#!/usr/bin/env python
# coding: utf-8

# # Second-order model

# ## Dynamics of the Heater/Sensor System
# 
# The previous results are not yet fully satisfactory. We're still missing the initial 'lag' in response of the measured temperature. 
# 
# For this third model, we consider the possibility that the heater and sensor may not be at the same temperature. In other words, that the heater/sensor assembly is not at a uniform temperature. To account for this possibility, we introduce $T_{H,1}$ to denote the temperature of heater one and $T_{S,1}$ to denote the temperature of the corresponding sensor. We'll further assume that sensor mainly exchanges heat with the heater, and the dominant heat transfer to the surroundings is through the heat sink attached to the heater.
# 
# This motivates a model
# 
# \begin{align}
# C^H_p\frac{dT_{H,1}}{dt} & = U_a(T_{amb} - T_{H,1}) + U_b(T_{S,1} - T_{H,1}) + \alpha P_1u_1\\
# C^S_p\frac{dT_{S,1}}{dt} & = U_b(T_{H,1} - T_{S,1}) 
# \end{align}
# 
# where $C^H_p$ and $C^S_p$ are the gross heat capacities of the heater and sensor, respectively, and $U_b$ is a new heat transfer coefficient characterizing the exchange of heat between the heater and sensor.
# 
# \begin{align}
# \frac{dT_{H,1}}{dt} & = -\frac{U_a+U_b}{C^H_p}T_{H,1} + \frac{U_b}{C^H_p}T_{S,1} + \frac{\alpha P_1}{C^H_p}u_1 + \frac{U_a}{C^H_p}T_{amb}\\
# \frac{dT_{S,1}}{dt} & = \frac{U_b}{C^S_p}(T_{H,1} - T_{S,1}) 
# \end{align}
# 
# Where measured temperature, that is, the temperature recorded by the Arduino, $T_1$ is given by
# 
# $$T_1 = T_{S,1}$$

# In[6]:


get_ipython().run_line_magic('matplotlib', 'inline')
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import  pandas as pd

# known parameters
T_amb = 21             # deg C
alpha = 0.00016        # watts / (units P1 * percent U1)
P1 = 200               # P1 units
U1 = 50                # steady state value of u1 (percent)
u1 = 50



data_file = "data/Model_Data.csv"
data = pd.read_csv("https://jckantor.github.io/cbe30338-2021/" + data_file).set_index("Time")[1:]
t_expt = data.index
T1 = data['T1'].values


# adjustable parameters
CpH = 5                # joules/deg C
CpS = 1                # joules/deg C
Ua = 0.05              # watts/deg C
Ub = 0.05              # watts/deg C


def model_energy_second_order(param, plot=False):
    # unpack the adjustable parameters
    CpH, CpS, Ua, Ub = param

    # model solution
    def deriv(t, y):
        T1H, T1S = y
        dT1H = (-(Ua + Ub)*T1H + Ub*T1S + alpha*P1*u1(t) + Ua*T_amb)/CpH
        dT1S = Ub*(T1H - T1S)/CpS
        return [dT1H, dT1S]

    soln = solve_ivp(deriv, [min(t_expt), max(t_expt)], [T_amb, T_amb], t_eval=t_expt) 
    
    # create dataframe with predictions
    pred = pd.DataFrame(columns=["T1", "T2", "Q1", "Q2"], index=t_expt)
    pred["T1"] = soln.y[1]

    # plot solution
    if plot:
        ax = plot_data(expt, pred)
        
    return pred["T1"] - expt["T1"]
    
model_energy_second_order([CpH, CpS, Ua, Ub], plot=True)


# ### Best fit

# In[12]:


results = least_squares(model_energy_second_order,  [CpH, CpS, Ua, Ub])
CpH, CpS, Ua, Ub = results.x
print(f"CpH = {CpH},  CpS = {CpS},   Ua = {Ua},  Ub = {Ub}")
model_energy_second_order(results.x, True)


# ## Fourth-Order Multi-Input Multi-Output Model

# ### Model derivation
# 
# \begin{align}
# C^H_p\frac{dT_{H,1}}{dt} & = U_a(T_{amb} - T_{H,1}) + U_b(T_{S,1} - T_{H,1}) + U_c(T_{H,2}-T_{H,1})  + \alpha P_1u_1\\
# C^S_p\frac{dT_{S,1}}{dt} & = U_b(T_{H,1} - T_{S,1})  \\
# C^H_p\frac{dT_{H,2}}{dt} & = U_a(T_{amb} - T_{H,2}) + U_b(T_{S,2} - T_{H,2}) + U_c(T_{H,1}-T_{H,2}) + \alpha P_2 u_2\\
# C^S_p\frac{dT_{S,2}}{dt} & = U_b(T_{H,2} - T_{S,2}) 
# \end{align}
# 
# where
# 
# \begin{align}
# T_1 & = T_{S,1} \\
# T_2 & = T_{S,2}
# \end{align}

# ### Standard form
# 
# \begin{align}
# \frac{dT_{H,1}}{dt} & = -(\frac{U_a+U_b+U_c}{C^H_p})T_{H,1} + \frac{U_b}{C^H_p}T_{S,1} + \frac{U_c}{C^H_p}T_{H,2}  + \frac{\alpha P_1}{C^H_p}u_1 + \frac{U_a}{C^H_p}T_{amb}\\
# \frac{dT_{S,1}}{dt} & = \frac{U_b}{C^S_p}(T_{H,1} - T_{S,1})  \\
# \frac{dT_{H,2}}{dt} & = -(\frac{U_a+U_b+U_c}{C^H_p})T_{H,2} + \frac{U_b}{C^H_p}T_{S,2} + \frac{U_c}{C^H_p}T_{H,1}  + \frac{\alpha P_2}{C^H_p}u_2 + \frac{U_a}{C^H_p}T_{amb}\\
# \frac{dT_{S,2}}{dt} & = \frac{U_b}{C^S_p}(T_{H,2} - T_{S,2}) 
# \end{align}
# 
# where
# 
# \begin{align}
# T_1 & = T_{S,1} \\
# T_2 & = T_{S,2}
# \end{align}

# In[13]:


get_ipython().run_line_magic('matplotlib', 'inline')
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# adjustable parameters
CpH = 5                # joules/deg C
CpS = 1                # joules/deg C
Ua = 0.05              # watts/deg C
Ub = 0.05              # watts/deg C
Uc = 0.05              # watts/deg C

def model_energy_fourth_order(param, plot=False):
    # unpack the adjustable parameters
    CpH, CpS, Ua, Ub, Uc = param  

    # model solution
    def deriv(t, y):
        T1H, T1S, T2H, T2S= y
        dT1H = (-(Ua + Ub + Uc)*T1H + Ub*T1S + Uc*T2H + alpha*P1*u1(t) + Ua*T_amb)/CpH
        dT1S = Ub*(T1H - T1S)/CpS
        dT2H = (-(Ua + Ub + Uc)*T2H + Ub*T2S + Uc*T1H + alpha*P2*u2(t) + Ua*T_amb)/CpH
        dT2S = Ub*(T2H - T2S)/CpS
        return [dT1H, dT1S, dT2H, dT2S]

    soln = solve_ivp(deriv, [min(t_expt), max(t_expt)], [T_amb]*4, t_eval=t_expt) 
    
    # create dataframe with predictions
    pred = pd.DataFrame(columns=["T1", "T2", "Q1", "Q2"], index=t_expt)
    pred["T1"] = soln.y[1]
    pred["T2"] = soln.y[3]

    # plot solution
    if plot:
        ax = plot_data(expt, pred)
    
    err1 = np.array(pred["T1"] - expt["T1"])
    err2 = np.array(pred["T2"] - expt["T2"])
    
    return np.concatenate((err1, err2))
    
model_energy_fourth_order([CpH, CpS, Ua, Ub, Uc], plot=True)


# In[14]:


results = least_squares(model_energy_fourth_order,  [CpH, CpS, Ua, Ub, Uc])
CpH, CpS, Ua, Ub, Uc = results.x
print(f"CpH = {CpH},  CpS = {CpS},   Ua = {Ua},  Ub = {Ub},  Uc = {Uc}")
model_energy_fourth_order(results.x, True)


# ## Lab Assignment 2: Identification of a Multi-input, Multi-output Model for the Temperature Control Laboratory
# 
# Create one or more notebooks to show your results for the following exercises. The model you develop in this exercise will be used in the remainder of the semester for simulation and control design for your copy of the Temperature Control Laboratory.

# ### Exercise 1.
# 
# Write two python functions, one called u1(t) and the other u2(t), that create the following input signals that will be used to test the Temperature Control Lab.
# 
# * u1(t) and u2(t) are initially zero.
# * At time t=20, u1(t) jumps to 60% power, u2(t) remains at zero.
# * At time t=620, u2(t) jumps to 60% power, u1(t) remains at 60.
# * At time t=1020, u1(t) returns to 0, u2(t) remains at 60.
# * At time t=1420, u2(t) returns to zero. Experiment is over.
# 
# Develop these functions, and plot the results for t=-100 to t=1800 (yes, beyond the end of the experiment) showing correct performance.

# ### Exercise 2.
# 
# Use the functions created in Exercise 1 to obtain experimental data for your Temperature Control Lab. This will take some time (about 1/2 hour if everything works perfectly). Record T1, T2, Q1, Q2 using the Historian. Be careful to ...
# 
# * Set P1=200, P2=100 before the experiment begins
# * Let the device reach equilibrium with ambient temperture before starting. Allow at least 10 minutes. Don't shortcut this (as tempting as that may be) since you will only get data that provide headaches later. "Go slow to go fast."
# * You might use the box the kit came in to put a little "tent" over the device to protect from air currents.
# * Before starting, be sure the heat sinks are not touching, and that everything looks in good shape.
# * If your thermal paste looks like it is melting, stop the experiment immediately. Lower P1 and P2 by 25% and start over. Note this in your lab report.
# 
# Save this data to a .csv file. 

# ### Exercise 3.
# 
# To avoid overwriting or damaging the data you collected in Exercise 2, create a separate notebook for model fitting. Fit two models to your data:
# 
# * Fit the first-order plus delay model to the results for "T1" using data up to t=620 (i.e, the data before you turn on the second heater.).  What are the gain, time-constant, and time delay for your device?
# 
# * Fit the fourth-order model (alternatively, the state-space model if you're comfortable with that formulation), and report all heat capacities, heat transfer coefficients. Note that you're fitting a two-input, two-output model which is very challenging. So the fit may not look quite as good as those shown above when u2(t) was held constant.

# In[ ]:




