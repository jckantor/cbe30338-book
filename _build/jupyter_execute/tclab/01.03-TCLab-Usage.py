#!/usr/bin/env python
# coding: utf-8

# # TCLab Usage

# ## Importing
#     
# Once installed, the `tclab` package can be imported into Python and an instance created with the Python statements
# 
#     from tclab import TCLab
#     lab = TCLab()
# 
# TCLab() attempts to find a device connected to a serial port and return a connection. An error is generated if no device is found.  The connection should be closed when no longer in use.
# 
# The following cell demonstrates this process, and uses the tclab `LED()` function to flash the LED on the Temperature Control Lab for a period of 10 seconds at a 100% brightness level. 

# In[4]:


from tclab import TCLab

lab = TCLab()
lab.LED(100)
lab.close()


# ## Using TCLab with Python's `with` statement
# 
# The Python `with` statement provides a convenient means of setting up and closing a connection to the Temperature Control Laboratory. In particular, the with statement establishes a context where a tclab instance is created, assigned to a variable, and automatically closed upon completion. The `with` statement is the preferred way to connect the Temperature Control Laboratory for most uses.

# In[5]:


from tclab import TCLab

with TCLab() as lab:
    lab.LED(100)


# ## Reading Temperatures
# 
# Once a tclab instance is created and connected to a device, the temperature sensors on the temperature control lab can be acccessed with the attributes `.T1` and `.T2`.  For example, given an instance `lab`, the temperatures are accessed as
# 
#     T1 = lab.T1
#     T2 = lab.T2
# 
# `lab.T1` and `lab.T2` are read-only properties. Any attempt to set them to a value will return a Python error.

# In[6]:


from tclab import TCLab

with TCLab() as a:
    print("Temperature 1: {0:0.2f} C".format(a.T1))
    print("Temperature 2: {0:0.2f} C".format(a.T2))


# ## Setting Heaters
# 
# For legacy reasons, there are two ways to set the power levels of the heaters. 
# 
# The first way is to the functions`.Q1()` and `.Q2()` of a `TCLab` instance. For example, both heaters can be set to 100% power with the functions
# 
#     lab = TCLab()
#     lab.Q1(100)
#     lab.Q2(100)
# 
# The device firmware limits the heaters to a range of 0 to 100%. The current value of attributes may be accessed via
# 
#     Q1 = lab.Q1()
#     Q2 = lab.Q2()
#     
# Important notes:
# 1. The led on the temperature control laboratory will turns from dim to bright when either heater is on.
# 2. Closing the TCLab instance turns the heaters off.
# 3. The power level of the two heaters may be different. Current versions of the firmware limit maximum power of first heater to 4 watts, and maxium power of the second heater to 2 watts.
# 4. In addition to the constraints imposed by the firmware, the power supply may not be capable of providing all of the power needed to operate both heaters at 100%
# 5. The values retrieved from these functions may be different than the values set due to the power limits enforced by the device firmware.

# In[18]:


from tclab import TCLab
import time

with TCLab() as a:
    print("\nStarting Temperature 1: {0:0.2f} C".format(a.T1),flush=True)
    print("Starting Temperature 2: {0:0.2f} C".format(a.T2),flush=True)

    a.Q1(100)
    a.Q2(100)
    print("\nSet Heater 1:", a.Q1(), "%",flush=True)
    print("Set Heater 2:", a.Q2(), "%",flush=True)
    
    t_heat = 30
    print("\nHeat for", t_heat, "seconds")
    time.sleep(t_heat)

    print("\nTurn Heaters Off")
    a.Q1(0)
    a.Q2(0)
    print("\nSet Heater 1:", a.Q1(), "%",flush=True)
    print("Set Heater 2:", a.Q2(), "%",flush=True)
    
    print("\nFinal Temperature 1: {0:0.2f} C".format(a.T1))
    print("Final Temperature 2: {0:0.2f} C".format(a.T2))


# Alternatively, the heaters can be set using the `.U1` and `.U2` attributes of a `TCLab` instance. 

# In[20]:


lab = TCLab()

print('Setting power levels on heaters 1 and 2')
lab.U1 = 50
lab.U2 = 25

print('Current power level on Heater 1 is: ', lab.U1, '%')
print('Current power level on Heater 1 is: ', lab.U2, '%')

lab.close()


# ## Synchronizing with Real Time using `clock`
# 
# The `tclab` module includes `clock` for synchronizing calculations with real time.  `clock(tperiod, tstep)` generates a sequence of iterations over a period of `tperiod` seconds evenly by `tstep` seconds. If `tstep` is omitted then the default period is set to 1 second.

# In[24]:


from tclab import clock

tperiod = 6
tstep = 2
for t in clock(tperiod,tstep):
    print(t, "sec.")


# There are some considerations to keep in mind when using `clock`. Most important, by its nature Python is not a real-time environment. `clock` makes a best effort to stay in sync with evenly spaced ticks of the real time clock. If, for some reason, the loop falls behind the real time clock, then the generator will skip over the event to get back in sync with the real time clock. Thus the total number of iterations may be less than expected. This behavior is demonstrated in the following cell.

# In[27]:


from tclab import TCLab, clock

import time

tfinal = 12
tstep = 2
for t in clock(tfinal, tstep):
    print(t, "sec.")
    
    # insert a long time out between 3 and 5 seconds into the event loop
    if (t > 3) and (t < 5):
        time.sleep(2.2)


# ### Using `clock` with TCLab

# In[29]:


from tclab import TCLab, clock

tperiod = 20

# connect to the temperature control lab
with TCLab() as a:
    # turn heaters on
    a.Q1(100)
    a.Q2(100)
    print("\nSet Heater 1 to {0:f} %".format(a.Q1()))
    print("Set Heater 2 to {0:f} %".format(a.Q2()))

    # report temperatures for the next tperiod seconds
    sfmt = "   {0:5.1f} sec:   T1 = {1:0.1f} C    T2 = {2:0.1f} C"
    for t in clock(tperiod):
        print(sfmt.format(t, a.T1, a.T2), flush=True)
        


# ## The TCLab `Historian`

# The `Historian` class provides means for data logging. Given an instance `lab` of a TCLab object, `lab.sources` is a list of all data sources and methods to access the data.
# 
#     lab = TCLab()
#     h = Historian(lab.sources)
#     
# The historian initializes a data log. The data log is updated by issuing a command
# 
#     h.update(t)
#     
# where `t` marks the current time. The following cell logs 10 seconds of data with a chaning power level to heater 1, then saves the data to a file.

# In[7]:


from tclab import TCLab, clock, Historian

with TCLab() as lab:
    h = Historian(lab.sources)
    for t in clock(10):
        lab.Q1(100 if t <= 5 else 0)
        h.update(t)
        
h.to_csv('data.csv')


# Once saved, data can be read and plotted using the [Pandas Data Analysis Library](https://pandas.pydata.org/) as demonstrated in this cell.

# In[59]:


get_ipython().run_line_magic('matplotlib', 'inline')

import pandas as pd
data = pd.read_csv('data.csv')
data.index = data['Time']
print(data)
data[['Q1','Q2']].plot(grid=True)


# ## The TCLab `Plotter`
# 
# The `Plotter` class adds a real time plotting of experimental data. A plotter is created from an instance of an historian as follows
# 
#     h = Historian(lab.sources)
#     p = Plotter(h)
#     
# Updating the plotter also updates the associated historian.
# 
#     p.update(t)
#     
# The following example shows how this works.

# In[9]:


get_ipython().run_line_magic('matplotlib', 'notebook')

from tclab import TCLab, clock, Historian, Plotter

with TCLab() as lab:
    h = Historian(lab.sources)
    p = Plotter(h, 10)
    for t in clock(10):
        lab.Q1(100 if t <= 5 else 0)
        p.update(t)
        
h.to_csv('data.csv')


# ## Using TCLab Offline

# In[3]:


get_ipython().run_line_magic('matplotlib', 'inline')
from tclab import clock, setup, Historian, Plotter

TCLab = setup(connected=False, speedup=20)

SP = 40
with TCLab() as a:
    h = Historian(a.sources)
    p = Plotter(h)
    for t in clock(120,2):
        PV = a.T1
        MV = 100 if SP > PV else 0
        a.U1 = MV
        p.update()


# ## Running Diagnostics

# In[7]:


import tclab

print("Version = ", tclab.__version__)
tclab.diagnose()

