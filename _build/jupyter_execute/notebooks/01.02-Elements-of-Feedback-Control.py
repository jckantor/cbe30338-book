#!/usr/bin/env python
# coding: utf-8

# # Elements of Process Control

# ## Feedback Control
# 
# ![](./figures/FeedbackControlDiagram.png)

# ## System Variables
# 
# * **DV: Disturbance Variables**: External variables that impose changes on the system under study.
# 
# * **MV: Manipulated Variables**: Variables that can be manipulated in order to acheive a desired response.
# 
# * **CV: Controlled Variables**: System variables that are the targets of the control actions.
# 
# * **PV: Process Variables**: System variables that are measured for the purpose of control. Ideally these would be the same as the controlled variables. Frequently, however, values of the controlled variable must be inferred from variables that can be measured with the available instrumentation.
# 
# * **SP: Setpoint Variables**: Desired values for the controlled variables.
# 
# * **Diagnostics**: Control system outputs indicating the internal state or condition of the process or controller.

# ## Controllers
# 
# ![](figures/PID_controllers.jpg)

# ## Sensors
# 
# There are only two methods to determine if a process is operating properly. The most direct method is to directly measure the variables of interest. If you're trying to control the temperature of a process stream, then a direct measurement of temperature is likely the most effective 
# 
# 
# ### The "Big Four"
# 
# * Thermocouples
# 
# ![](figures/thermocouple.jpg)
# 
# * Platinum resistance
# * Thermisters
# * Infrared Imaging sensors
# 
# Pressure
# 
# ![](figures/pressure.jpg)
# 
# Level
# 
# Flow

# ### A "Cast of Thousands"
# 
# Position
# 
# Composition
# 
# Humidity
# 
# Accelerators
# 
# Magnetic field

# ## Actuators
# 
# ### Control Valves
# 
# Solenoid Valves (On/Off)
# 
# ![](figures/solenoid_valve.jpg)
# 
# Proportional Control Valves
# 
# ![](figures/control_valve.jpg)
# 
# ### Pumps
# 
# ![](figures/pump2.jpg)
# 
# ![](figures/pump.jpg)
# 
# Heaters
# 
# Positioners/Motors/Servos
# 
# 

# In[ ]:




