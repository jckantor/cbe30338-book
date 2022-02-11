#!/usr/bin/env python
# coding: utf-8

# # Lab Assignment 4: Relay Control
# 
# In this lab assignment you will implement relay control for the Temperature Control Laboratory.
# 
# 1. Implement and test a relay control for the heater/sensor system
# 2. Implement and test a relay control to track a complex setpoint.

# ## Exercise 1. Relay (or On-Off) control
# 

# Create a notebook to implements a relay control for the Temperature Control Lab subject the following requirements:
# 
# * Simultaneous control of sensor temperatures T1 and T2 to setpoints 35 and 40 degrees, respectively. The setpoints return to 25 deg C at  t = 300.
# * Use a tolerance value $d$ of 0.5 deg C.
# * Set the minimum and maximum values of the heater to 0 and 100%, respectively. lab.P1 and lab.P2 should be left at their default values.
# * Show the results of an experiment in which the setpoints are adjusted as 
# 
# Some started code is include below.

# In[1]:


from tclab import TCLab, clock, Historian, Plotter, setup

TCLab = setup(connected=False)

# modify these setpoints to change with time

def SP1(t):
    return 40

def SP2(t):
    return 35

# relay controller
def relay(SP, d=1, Umin=0, Umax=100):
    U = 0
    while True:
        t, T = yield U
        if T < SP(t) - d/2:
            U = Umax
        if T > SP(t) + d/2:
            U = Umin

# create a single control loop
controller1 = relay(SP1)
controller1.send(None)

t_final = 500
t_step = 1
with TCLab() as lab:
    h = Historian(lab.sources)
    p = Plotter(h, t_final)
    for t in clock(t_final, t_step):
        T1 = lab.T1
        U1 = controller1.send([t, T1])
        lab.Q1(U1)
        p.update()


# ## Procedures
# 
# 1. Begin by testing the above code on your laptop.
# 2. Create a new cell, copy the code to the new cell, and extend the code to control both T1 and T2 to the desired setpoints.
# 3. Create another new cell, modify the setpoint functions to include the switch to 25 degrees at t=300 for both temperatures. Test this cell on your real hardware.
# 4. Create one more new cell, and use class notes on setpoints to create a setpoint function using interpolation that reproduces the chart below. Scale time so the whole temperature program can be completed in 10 minutes. The goal is to hit 50 deg C at 3 miinutes, 27 deg C at 7 minutes, return to 32 deg C at 8 minutes, and hold until 10 minutes. The goal is follow the ramp as closely as possible.
# 
# Apply the setpoint to T1 while maintaining T2 at a constant 30 deg C.

# ![](https://d29hmqxeker05q.cloudfront.net/eyJidWNrZXQiOiJpbWFnZXMuY2tiay5jb20iLCJrZXkiOiJpbWFnZXMvY2hvYzI0NDE0YzA0czAwMXNzMDAxc3NzMDA0ZzAxLmpwZyIsImVkaXRzIjp7InJlc2l6ZSI6eyJ3aXRob3V0RW5sYXJnZW1lbnQiOnRydWUsIndpZHRoIjo2NTEsImhlaWdodCI6NTAwLCJmaXQiOiJpbnNpZGUifSwianBlZyI6eyJxdWFsaXR5Ijo5MCwicHJvZ3Jlc3NpdmUiOnRydWV9fX0=)

# In[ ]:




