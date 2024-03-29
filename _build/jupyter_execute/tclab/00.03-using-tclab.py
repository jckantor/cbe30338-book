#!/usr/bin/env python
# coding: utf-8

# # Python Coding for TCLab
# 
# The following cells demonstrate the use of the TCLab hardware. Open a new Jupyter notebook on your laptop, connect the TCLab hardware to the USB port of your laptop, then create and run cells as you follow along in this notebook.

# ## Creating a TCLab instance
#     
# Once installed, the `tclab` package can be imported into Python and an instance created with the Python statements
# 
#     from tclab import TCLab
#     lab = TCLab()
#     # do something
#     lab.close()
# 
# TCLab() attempts to find a device connected to a serial port and return a connection. An error is generated if no device is found.  The connection must be closed when no longer in use.

# In[10]:


from tclab import TCLab

lab = TCLab()
# do something
lab.close()


# ## Using the LED
# 
# The following cell demonstrates the  process, and uses the tclab `LED()` function to flash the LED on the Temperature Control Lab for a period of 10 seconds at a 100% brightness level. 

# In[11]:


from tclab import TCLab

lab = TCLab()
lab.LED(50)
lab.close()


# ## Using TCLab and Python's `with` statement
# 
# The Python `with` statement provides a convenient means of setting up and closing a connection to the Temperature Control Laboratory. In particular, the with statement establishes a context where a tclab instance is created, assigned to a variable, and automatically closed upon completion. The `with` statement is the preferred way to connect the Temperature Control Laboratory for most uses.

# In[12]:


from tclab import TCLab

with TCLab() as lab:
    lab.LED(100)


# ## Reading Temperatures
# 
# Once a tclab instance is created and connected to a device the temperature sensors are acccessed with the attributes `.T1` and `.T2`.  Given an instance named `lab`, the temperatures are accessed as
# 
#     T1 = lab.T1
#     T2 = lab.T2
# 
# Note that `lab.T1` and `lab.T2` are read-only properties. Attempt to assign a value will return a Python error.

# In[13]:


from tclab import TCLab

with TCLab() as lab:
    T1 = lab.T1
    T2 = lab.T2
    print(f"Temperature 1: {T1:0.2f} C")
    print(f"Temperature 2: {T2:0.2f} C")


# ## Setting Heater Power

# ### Setting maximum power with `.P1` and `.P2`
# 
# Heater power is specified as a percentage of the maximum power available at each heater. The maximum power to each heater is determined by setting parameters `.P1` and `.P2` to number in the range 0 and 255. The default settings are
# 
#     lab.P1 = 200
#     lab.P2 = 100
#     
# Based on laboratory measurements, the power delivered to each heater is approximately 14.5 mW per unit increase in `.P1` and `.P2`. For heater 1 at the default setting of 200, the power is 
# 
# $$ 200 \times 14.5 \text{mW} \times \frac{\text{1 watt}}{\text{1000 mW}} = 2.9\text{ watts}$$
# 
# For heater 2 at the default setting of 100, the power is
# 
# $$ 100 \times 14.5 \text{mW} \times \frac{\text{1 watt}}{\text{1000 mW}} = 1.45\text{ watts}$$
# 
# Note that the power delivered to the heaters for constant `.P1` and `.P2` is temperature dependent, and there will be some variation among units.
# 
# The default values for `.P1` and `.P2` were chosen to avoid unnecessarily high temperatures, and to include an asymmetric response between the two heaters.

# In[14]:


from tclab import TCLab

with TCLab() as lab:
    P1 = lab.P1
    P2 = lab.P2
    print(f"The maximum power of heater 1 is set to {P1:.0f} corresponding to {P1*0.0145:.2f} watts.")
    print(f"The maximum power of heater 1 is set to {P2:.0f} corresponding to {P2*0.0145:.2f} watts.")


# ### Setting heater power with `.Q1()` and `.Q2()`
# 
# For legacy reasons, there are two ways to set the percentage of maximum power delivered to the heaters. The first way is to the functions`.Q1()` and `.Q2()` of a `TCLab` instance. For example, both heaters can be set to 100% power with the functions
# 
#     lab = TCLab()
#     lab.Q1(100)
#     lab.Q2(100)
# 
# The device firmware limits the heaters to a range of 0 to 100%. The current settiing may be accessed via
# 
#     Q1 = lab.Q1()
#     Q2 = lab.Q2()
#     
# The LED on the temperature control laboratory will turns bright when either heater is on. Closing the TCLab instance turns the heaters off.

# In[15]:


from tclab import TCLab
import time

with TCLab() as lab:
    print(f"Starting Temperature 1: {lab.T1:0.2f} C")
    print(f"Starting Temperature 2: {lab.T2:0.2f} C")

    lab.Q1(100)
    lab.Q2(100)
    
    print(f"Set Heater 1: {lab.Q1()} %")
    print(f"Set Heater 2: {lab.Q2()} %")
    
    t_heat = 30
    print(f"Heat for {t_heat} seconds")
    time.sleep(t_heat)

    print("Turn Heaters Off")
    lab.Q1(0)
    lab.Q2(0)

    print("Set Heater 1:", lab.Q1(), "%")
    print("Set Heater 2:", lab.Q2(), "%")
    
    print(f"Final Temperature 1: {lab.T1:0.2f} C")
    print(f"Final Temperature 2: {lab.T2:0.2f} C")


# ### Setting heater power with `.U1` and `.U2`
# 
# Alternatively, the percentage of maximum power delivered to the heaters can be set by assigning value to the `.U1` and `.U2` attributes of a `TCLab` instances. Getting the value of `.U1` and `.U2` retrieves the current settings.

# In[16]:


lab = TCLab()

print('Setting power levels on heaters 1 and 2')
lab.U1 = 50
lab.U2 = 25

print('Current power level on Heater 1 is: ', lab.U1, '%')
print('Current power level on Heater 1 is: ', lab.U2, '%')

lab.close()


# ## Synchronizing with Real Time using `clock`
# 
# The `tclab` module includes `clock` for synchronizing calculations with real time.  `clock(t_period, t_step)` generates a sequence of evenly spaced time step over a period`t_period` seconds that are `t_step` seconds apart. If `t_step` is omitted then the default time step is set to 1 second.

# In[17]:


from tclab import clock

t_period = 6
t_step = 2
for t in clock(t_period, t_step):
    print(t, "sec.")


# There are some considerations to keep in mind when using `clock`. Most important, by its nature Python is not a real-time environment. `clock` makes a best effort to stay in sync with evenly spaced ticks of the real time clock. If, for some reason, the loop falls behind the real time clock, then the generator will skip over the event to get back in sync with the real time clock. Thus the total number of iterations may be less than expected. This behavior is demonstrated in the following cell.

# In[18]:


from tclab import TCLab, clock

import time

t_period = 12
t_step = 2
for t in clock(t_period, t_step):
    print(t, "sec.")
    
    # insert a long time out between 3 and 5 seconds into the event loop
    if (t > 3) and (t < 5):
        time.sleep(2.2)


# ### Using `clock` with TCLab
# 
# The following cell demonstrates use of `clock` to perform a short experiment. 

# In[19]:


from tclab import TCLab, clock

# length of the experiment in seconds
t_period = 20

with TCLab() as lab:
    # turn heaters on to 100%
    lab.Q1(100)
    lab.Q2(100)
    print(f"Set Heater 1 to {lab.Q1():.1f} %")
    print(f"Set Heater 2 to {lab.Q2():.1f} %")

    # print temperatures each second for tperiod seconds
    for t in clock(t_period):
        print(f"{t:5.1f} sec:  T1 = {lab.T1:4.1f} C   T2 = {lab.T2:4.1f} C")   


# ## The TCLab `Historian`

# The `Historian` class provides means for logging process data to a database. 
# 
# Given a list `sources` of data sources and methods to access the data, `Historian(sources)` creates an historian that logs data to database on each call to `.update()`. Given an instance `lab` of a TCLab object, `lab.sources` is a default list of data sources and methods for logging temperatures `lab.T1` and `lab.T2` and power settings `lab.U1` and `lab.U2`.
# 
#     lab = TCLab()
#     h = Historian(lab.sources)
#     
# The historian automatically initializes a database to log the process data. The database is updated by issuing a command
# 
#     h.update(t)
#     
# where `t` is variable containing the current time. 
# 
# To demonstrate, the following cell logs 10 seconds of data with time varying power level applied to heater 1. When the experiment is over, `h.to_csv` saves the data to a file that be imported in python or a spreadsheet application.

# In[20]:


from tclab import TCLab, clock, Historian

with TCLab() as lab:
    h = Historian(lab.sources)
    for t in clock(10):
        lab.Q1(100 if t <= 5 else 0)
        h.update(t)
        
h.to_csv('data.csv')


# Once saved, data can be read and plotted using the [Pandas Data Analysis Library](https://pandas.pydata.org/) as demonstrated in this cell.

# In[21]:


get_ipython().run_line_magic('matplotlib', 'inline')

import pandas as pd
data = pd.read_csv('data.csv')
data.index = data['Time']
print(data)
data[['Q1', 'Q2']].plot(grid=True)


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

# In[22]:


get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt

from tclab import TCLab, clock, Historian, Plotter

with TCLab() as lab:
    h = Historian(lab.sources)
    p = Plotter(h, 10)
    for t in clock(10):
        lab.Q1(100 if t <= 5 else 0)
        p.update(t)
        
h.to_csv('data.csv')


# ## Using TCLab Offline
# 
# The `tclab` library includes a simulation capability. This is useful for circumstances when it isn't possible to access the hardware.  The followinig cell demonstrated the use of `setup` to use the library in simulation mode. The argument `connected` is set to `True` if the hardware is connected, otherwise `False`. Simulation mode allows the use of the `speedup` parameter to run experiments at some multiple of real time. 

# In[23]:


get_ipython().run_line_magic('matplotlib', 'inline')
from tclab import clock, setup, Historian, Plotter

t_period = 120
TCLab = setup(connected=False, speedup=20)
        
with TCLab() as lab:
    h = Historian(lab.sources)
    p = Plotter(h, t_period)
    for t in clock(t_period):
        lab.Q1(100 if t % 20 <= 5 else 0)
        p.update(t)


# In[ ]:




