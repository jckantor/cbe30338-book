#!/usr/bin/env python
# coding: utf-8

# # Lab Assignment: Relay and PI Control
# 
# This lab assignment introduces the use of relay, proportional (P), and proportional-integral (PI) control for the Temperature Control Laboratory. In this assignment you will 
# 
# 1. implement and test a relay control for the dual heater/sensor system
# 2. implement and test a proportional-integral (PI) control algorithm for a single heater/sensor

# ## Exercise 1. Relay (or On-Off) control
# 

# Create a notebook to implement a relay control for the Temperature Control Lab subject the following requirements:
# 
# * Simultaneous control of sensor temperatures T1 and T2.
# * Use a tolerance value $d$ of 0.5 deg C.
# * Set the minimum and maximum values of the heater to 0 and 100%, respectively. lab.P1 and lab.P2 should be left at their default values.
# * Show the results of an experiment in which the setpoints are adjusted as follows:
#     * SP1 is initially ambient temperature. SP1 increases to 35 deg at time t=20 and remains constant.
#     * SP2 is initially ambient temperature. SP2 increases linearly to 45 deg C beginning at t=120 with the transition complete at time t=220.
#     * Run the experiment until you reach a steady oscillation about the final operating point, and for no shorter than  600 sec.
#     
#     
# Questions:
# 
#    1. After the system has settled to a steady oscillation about the final operating point, what is the maximum deviation from the setpoints?
#    2. What is the approximate switching frequency of the manipulated variables?

# In[5]:


get_ipython().run_line_magic('matplotlib', 'inline')
from tclab import TCLab, clock, Historian, Plotter

# insert code below


# ## Exercise 2. Implementing a PI Controller

# Create a notebook to implement PI for the Temperature Control Lab.
# 
# * Using the simulation mode, create an implementaton of PI control and, by trail and error, find values for Kp and Ki, that provide a fast and accurate acquisitioni of the desired setpoint.
# 
# * Show the results of an experiment in which the setpoints are adjusted as follows:
#     * SP1 is initially ambient temperature. SP1 increases linearly to 45 deg C beginning at t=20 with the transition complete at time t=120.
#     * Run the experiment until you reach a steady oscillation about the final operating point, and for no shorter than  600 sec.
#     
#     
# Questions:
# 
#    1. After the system has settled to a steady oscillation about the final operating point, what is the maximum deviation from the setpoints?
# 

# In[ ]:




