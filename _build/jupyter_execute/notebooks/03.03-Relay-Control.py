#!/usr/bin/env python
# coding: utf-8

# # Relay Control

# ## Relay Control for the Temperature Control Lab
# 
# Relay control is perhaps the simplest form of feedback control that comes to mind for controlling common heaters. This is the on/off control familiar from home thermostats, air conditioners, and other devices where the manipulated variable is in either an "on" state or an "off" state.
# 
# The following code implements relay control for temperature T1 on the Temperature Control Lab. At each time step $t_k$, the value of 
# 
# $$
# \begin{align}
# U_{k} & = \begin{cases} 
#     U^{max} &\text{if $T_k \leq T^{SP}_k$}\\
#     U^{min} & \text{if $T_k \geq T^{SP}_k$}
#     \end{cases}
# \end{align}
# $$
# 
# where $ 0\% \leq U_{k} \leq 100\%$ refers to percentage of the maximum heater power, $T_k$ is the measured temperature at time $t_k$, and $T^{SP}_k$ is the temperature setpoint at time $t_k$. Typically $U^{min}$ and $U^{max}$ will be set to 0% and 100%, respectively, but other choices are possible.
# 
# Relay control can be implemented as a single line of code in the standard clock-driven loop of the Temperature Control Lab.

# In[1]:


get_ipython().run_line_magic('matplotlib', 'inline')
from tclab import TCLab, clock, Historian, Plotter, setup

TCLab = setup(connected=False, speedup=20)

# control parameters
U_min = 0
U_max = 100
T_SP = 40

# time horizon and time step
t_final = 250
t_step = 1

# perform experiment
with TCLab() as lab:
    lab.P1 = 200
    h = Historian(lab.sources)
    p = Plotter(h, t_final)
    for t in clock(t_final, t_step):
        T1 = lab.T1                             # measure temperature
        U1 = U_max if lab.T1 < T_SP else U_min  # compute manipulated variable
        lab.Q1(U1)                              # adjust power
        p.update(t)                             # log results


# ## Relay Control with Deadzone (Hysteresis) or Deadtime
# 
# One of the issues with simple relay control is the potential for 'chattering' where the manipulated variable (in this case heater power) exhibits periods of rapid on-and-off switching. This can be caused by systems that are highly response to control inputs, or where sensor measurements carry significant noise.
# 
# There are several simple and highly effective solutions to the problem of chattering.
# 
# * **Deadzone** (also called hysteresis). The manipulated variable is switched on or off only after the process variable has moved past the setpoint by a specified amount $d$.
# * **Deadtime** Following an on-or-off transition in the manipulated variable, no further transition is allowed for a specified period of time called the deadtime.
# 
# 
# The control algorithm for relay control with a deadzone extending $d$ above and below the setpoint, a closed form is given by
# 
# $$
# \begin{align}
# U_{k} & = \begin{cases} 
#     U^{max} &\text{if $T_k \leq T^{SP}_k$} - d\\
#     U^{min} & \text{if $T_k \geq T^{SP}_k$} + d\\
#     U_{k-1} & \text{ otherwise}
#     \end{cases}
# \end{align}
# $$
# 
# where $d$ is the *tolerance* or *hysteresis*. 
# 
# For home heating systems a typical value is in the range of 0.5 to 1 degree F. This image shows how hystersis was adjusted on a typical home thermostat in common usage in the late 20th century.
# 
# <a title="By Vincent de Groot - http://www.videgro.net (Own work) [GFDL (http://www.gnu.org/copyleft/fdl.html), CC-BY-SA-3.0 (http://creativecommons.org/licenses/by-sa/3.0/) or CC BY 2.5 (http://creativecommons.org/licenses/by/2.5)], via Wikimedia Commons" href="https://commons.wikimedia.org/wiki/File%3AHoneywell_thermostat_open.jpg"><img width="512" alt="Honeywell thermostat open" src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Honeywell_thermostat_open.jpg/512px-Honeywell_thermostat_open.jpg"/></a>
# 
# The furnance is turned on for temperatures below the range 
# 
# $$
# \begin{align}
# T^{SP} - d \leq T \leq T^{SP} + d
# \end{align}
# $$
# 
# and is turned for temperatures above the range. Within the range, however, the furnance may be on or off depending on what happened at the last decision point.
# 
# The following code implements relay control with hystersis. 

# In[2]:


get_ipython().run_line_magic('matplotlib', 'inline')
from tclab import TCLab, clock, Historian, Plotter, setup

TCLab = setup(connected=False, speedup=20)

# control parameters
U_min = 0
U_max = 100
T_SP = 40
d = 0.5

# time horizon and time step
t_final = 250
t_step = 1

# perform experiment
with TCLab() as lab:
    lab.P1 = 200
    h = Historian(lab.sources)
    p = Plotter(h, t_final)
    U1 = U_min
    for t in clock(t_final, t_step):
        T1 = lab.T1
        if T1 <= T_SP - d:
            U1 = U_max
        elif T1 >= T_SP + d:
            U1 = U_min
        lab.Q1(U1)
        p.update(t)      


# <hr>
# 
# **Study Question:** Examining the closed-loop responses, it's obvious that the heater is oversized for the purpose of control at 40 deg C.  Try other values for $Q^{\max}$ to see if you can improve closed-loop performance.
# 
# **Study Question:** What is the effect of sample time on control performance? What happens if you make the controller sample time longer?
# 
# **Study Question:** In a new cell, create a modification of the script to include a change in setpoint from 40 deg C to 50 deg C at the 300 second mark. Run the experiment for at least 10 minutes to see the full effect.
# 
# **Study Question:** For a relay control with deadzone (also called hysteresis), try to sketch a graph of the manipulated variable $Q$ as a function of the process variable $T$. Assume the setpoint is 50 and $d = 3$. Can you draw a unique function? Why not?
# 
# <hr>
