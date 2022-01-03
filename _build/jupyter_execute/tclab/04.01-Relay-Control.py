#!/usr/bin/env python
# coding: utf-8

# # Relay Control

# ## Simple Relay Control
# 
# The following code implements relay control for temperature T1 on the Temperature Control Lab.
# 
# \begin{align}
# Q(t) & = \begin{cases} 
#     Q^{max} &\text{if $T \leq T_{setpoint}$}\\
#     0       & \text{if $T \geq T_{setpoint}$}
#     \end{cases}
# \end{align}
# 
# This is simple to implement, in fact it is just one line of code in the following cell. Adjust `Tsetpoint` to a desired setpoint value, then run the cell.

# In[1]:


get_ipython().run_line_magic('matplotlib', 'inline')
from tclab import TCLab, clock, Historian

# control parameters
Qmax = 100
Tsetpoint = 40

# time horizon and time step
tfinal = 300
tstep = 1

# perform experiment
with TCLab() as a:
    h = Historian(a)
    h.initplot(tfinal)
    for t in clock(tfinal, tstep):
        T1 = a.T1                             # measure temperature
        Q1 = Qmax if a.T1 < Tsetpoint else 0  # compute manipulated variable
        a.Q1(Q1)                              # adjust power
        h.update(t)                           # log results


# ## Relay Control with Hysteresis
# 
# One of the issues with simple relay control is the potential for 'chattering', which are situations where the manipulated variable (in this case heater power) rapid on-and-off switching. This can be caused by systems that are highly response to control inputs or where the sensor measurements carry significant noise.
# 
# The typical home thermostat used for furnace control incorporates a simple but highly effective solution to the chattering period. The idea is to intentially overshoot the setpoint. Then, after the control switches state, there will be at least a short period of time where no further control action should be necessary. The control algorithm can be written
# 
# \begin{align}
# Q(t) & = \begin{cases} 
#     0       & \text{if $T \geq T_{Setpoint} - \frac{d}{2}$}\\
#     Q^{max} &\text{if $T \leq T_{Setpoint} + \frac{d}{2}$}\\
#     Q(t-\delta t) & \mbox{otherwise}
#     \end{cases}
# \end{align}
# 
# where $d$ is the *tolerance* or *hysteresis*. For home heating systems a typical value is in the range of 0.5 to 1 degree F. This image shows how hystersis was adjusted on a typical home thermostat in common usage in the late 20th century.
# 
# <a title="By Vincent de Groot - http://www.videgro.net (Own work) [GFDL (http://www.gnu.org/copyleft/fdl.html), CC-BY-SA-3.0 (http://creativecommons.org/licenses/by-sa/3.0/) or CC BY 2.5 (http://creativecommons.org/licenses/by/2.5)], via Wikimedia Commons" href="https://commons.wikimedia.org/wiki/File%3AHoneywell_thermostat_open.jpg"><img width="512" alt="Honeywell thermostat open" src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Honeywell_thermostat_open.jpg/512px-Honeywell_thermostat_open.jpg"/></a>
# 
# The furnance is turned on for temperatures below the range 
# 
# \begin{align}
# T_{Setpoint} - \frac{d}{2} \leq T \leq T_{Setpoint} + \frac{d}{2}
# \end{align}
# 
# and is turned for temperatures above the range. Within the range, however, the furnance may be on or off depending on what happened at the last decision point.
# 
# The following code implements relay control with hystersis. 

# In[2]:


get_ipython().run_line_magic('matplotlib', 'inline')
from tclab import TCLab, clock, Historian

# control parameters
Qmax = 100
Tsetpoint = 50
d = 0.5

# time horizon and time step
tfinal = 300
tstep = 1

# perform experiment
with TCLab() as a:
    h = Historian(a)
    h.initplot(tfinal)
    Q1 = a.Q1()
    for t in clock(tfinal, tstep):
        T1 = a.T1
        if T1 <= Tsetpoint - d/2:
            Q1 = Qmax
        if T1 >= Tsetpoint + d/2:
            Q1 = 0
        a.Q1(Q1)
        h.update()


# ## Multivariable On-Off Control

# In[3]:


get_ipython().run_line_magic('matplotlib', 'inline')
from tclab import TCLab, clock, Historian

Tsetpoint1 = 45
Tsetpoint2 = 35
Qmax = 100
tfinal = 480
d = 0.5

with TCLab() as a:
    h = Historian(a)
    h.initplot(tfinal)
    Q1 = a.Q1()
    Q2 = a.Q2()
    for t in clock(tfinal):
        T1 = a.T1
        if T1 <= Tsetpoint1 - d/2:
            Q1 = Qmax
        if T1 >= Tsetpoint1 + d/2:
            Q1 = 0
        a.Q1(Q1)

        T2 = a.T2
        if T2 <= Tsetpoint2 - d/2:
            Q2 = Qmax
        if T2 >= Tsetpoint2 + d/2:
            Q2 = 0
        a.Q2(Q2)
        h.update()


# ## Exercises
# 
# 1. Examining the closed-loop responses, it's obvious that the heater is oversized for the purpose of control at 40 deg C.  Try other values for $Q^{\max}$ to see if you can improve closed-loop performance.
# 
# 2. What is the effect of sample time on control performance? What happens if you make the controller sample time longer?
# 
# 3. In a new cell, create a modification of the script to include a change in setpoint from 40 deg C to 50 deg C at the 300 second mark. Run the experiment for at least 10 minutes to see the full effect.
# 
# 4. For a relay control with hystersis, try to sketch a graph of $Q$ as a function of $T$ assuming $T_{Setpoint} = 50$ and $h = 3$. Can you draw a unique function? Why not?

# In[ ]:




