#!/usr/bin/env python
# coding: utf-8

# # Elements of Process Control

# ## Feedback Control
# 
# ![](./figures/FeedbackControlDiagram2.png)

# ## Process Variables
# 
# * **DV: Disturbance Variables** are exogenous variables (that is, variables that are determined outside the scope of the system under study) that impose changes on the system under study.
# 
# * **MV: Manipulated Variables** are system variables that can be directly manipulated in order to acheive a desired response.
# 
# * **CV: Controlled Variables** are the system variables that are the targets of the control actions.
# 
# * **PV: Process Variables** are the system variables that can be measured. Ideally these would be the same as the controlled variables. Frequently, however, values of the controlled variable must be inferred from the variables that can be measured with the available instrumentation.
# 
# * **SP: Setpoint Variables** are desired values for the controlled variables.
# 
# * **Diagnostics** are outputs from the controller indicating the internal state of the process, or which alert the operator to abnormal conditions.

# ## Process Sensors
# 
# There are only two methods to determine if a process is operating properly. The most direct method is to directly measure the variables of interest. If you're trying to control the temperature of a process stream, then a direct measurement of temperature is likely the most effective 
# 
# Temperature
# 
# Pressure
# 
# Level
# 
# Flow

# In[ ]:




