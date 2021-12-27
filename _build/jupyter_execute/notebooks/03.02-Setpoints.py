#!/usr/bin/env python
# coding: utf-8

# # Setpoints
# 
# Setpoints are functions of time that establish target values for key control variables. This notebook describes typical nomenclature used in describing setpoint functions, and shows how to creatd setpoint functions in Python.

# ## Setpoint profiles
# 
# Example descriptions from commercial vendors:
# 
# * [West Control Solutions: Understanding Setpoint Ramping and Ramp/Soak Temperature Control](https://www.west-cs.com/news/understanding-setpoint-ramping-and-rampsoak-temperature-control/)
# * [Eurotherm: Ramp and Soak Applications](https://www.eurotherm.com/us/temperature-control-applications-us/ramp-and-soak-applications/)
# * [Allen-Bradley: Introduction to the Allen Bradley Ramp/Soak Controller](https://control.com/technical-articles/Introduction-to-the-Allen-Bradley-Ramp-Soak-Controller-System/)
# * [Wikipedia: Thermal Profiling](https://en.wikipedia.org/wiki/Thermal_profiling)
# 
# Common descriptions for setpoint functions include so-called **step** changes, and **ramp** and **soak** periods.
# 
# * A **step** change is an discontinuous change in setpoint value occuring as specified point in time. An example is specifying a setpoint change from 45 deg C to 65 deg C at a specified point in time.
# * A **soak** (or **dwell**) is a specified period of time over which the setpoint is held a constant, specified value.
# * A **ramp** is a specified period of time over which the setpoint changes at a constant rate from a specified starting value to a specified final value.
# * The **ramp rate** is the rate of change in a setpoint ramp. These may have positive or negative values.

# In[13]:


get_ipython().run_line_magic('matplotlib', 'inline')
import numpy as np
import matplotlib.pyplot as plt

# specify a setpoint profile
profile = [
    (0, 25),
    (50, 35),
    (120, 35),
    (120, 40),
    (170, 50),
    (170, 50),
    (270, 50),
    (370, 40),
    (450, 40),
    (600, 25),
]

# convert to numpy array to provide simple access to columns
profile = np.array(profile)

# create an annotated plot
fig, ax = plt.subplots(1, 1, figsize=(10, 5))
ax.plot(profile[:, 0], profile[:, 1], lw=4)
ax.annotate("Step", xy=(120, 37.5), xytext=(180, 37.5), fontsize=20, 
            va="center", arrowprops=dict(facecolor='black', shrink=0.05))
ax.annotate("Ramp", xy=(320, 45), xytext=(380, 48), fontsize=20, 
            va="center", arrowprops=dict(facecolor='black', shrink=0.05))
ax.annotate("Soak/Dwell", xy=(210, 50), xytext=(210, 55), fontsize=20, 
            ha="center", arrowprops=dict(facecolor='black', shrink=0.05))
ax.set_ylim(25, 60)
ax.set_title("Sample Setpoint Profile")
ax.set_xlabel("Time")
ax.grid(True)


# <hr>
# 
# **Study Question:** Classify all of the segments in the sample setpoint profile.
# 
# **Study Question:** What is the ramp rate of the first ramp in the example above.
# 
# **Study Question:** Modify the data in the above example to remove the step. Replace it with a single raamp from the initial condition to the soak period that begins at t=170 at a temperature of 170C.
# 
# <hr>

# ## Creating setpoint functions
# 
# For feedback control we would like functions that return the value of a setpoint for any point in time. Functions are in the form $SP_1(t)$ and $SP_2(t)$, for example, are straightfoward to use inside in control applications. 
# 
# In the section we show how to write a function that accepts points defining a piecewise linear setpoint profile, then produce a function to compute the setpoint for any point in time.

# ### Specifying piecewise linear setpoint profiles
# 
# Describiing the setpoint as a series of a step/ramp/soak periods naturally leads a piecewise linear function. The start and end of each line segment are spceified by (time, value) pairs. Ordering these points into a list provides a straightforward specification of the setpoint, 
# 
# Here we show the points for a typical setpoint.

# In[21]:


get_ipython().run_line_magic('matplotlib', 'inline')
import numpy as np
import matplotlib.pyplot as plt

profile = [
    (0, 25),
    (50, 35),
    (120, 35),
    (120, 40),
    (170, 50),
    (170, 50),
    (270, 50),
    (370, 40),
    (450, 40),
    (600, 25),
]

t = [t for t, _ in profile]
y = [y for _, y in profile]

fig, ax = plt.subplots(1, 1)
ax.plot(t, y, '.', ms=10)


# ### A functon to create functions
# 
# Python functions are frequently written to accept data, perform calculations, and return values. What may be less familiar is that functions can also return function. This is just what we neeed - a function that accepts a series of (time, value) pairs describing a setpoint profile, then returns a function that can be used to find values of the setpoint at any point in time.

# In[22]:


def create_setpoint_function(profile):
    
    profile = np.array(profile)
    ti = profile[:, 0]
    yi = profile[:, 1]
    
    # define a function to interpolate time and values
    def setpoint_function(t):
        return np.interp(t, ti, yi)
    
    # return that function
    return setpoint_function


# ### Example of a setpoint function
# 
# The following example creates a setpoint function that produces setpoints corresponding the profile described in the introduction to this notebook.

# In[23]:


sp = create_setpoint_function(profile)

# print select values
t = 100
print(f"at time = {t:3d} setpoint = {sp(t)}")


# We can use the setpoint function to create plots.

# In[24]:


# compute setpoint values
t = np.linspace(0, 600, 600)
y = sp(t)

# create a plot
fix, ax = plt.subplots(1, 1, figsize=(10, 5))
ax.plot(t, y)
ax.set_xlabel("time / seconds")
ax.set_title("setpoint function")
ax.grid(True)


# ### Creating multiple setpoint functions 
# 
# The next cell demonstrates the use of `create_setpoint_function` to create multiple independent setpoint functions.

# In[25]:


T_amb = 21.0

sp_1 = create_setpoint_function([[0, T_amb], [20, T_amb], [60, 50], [100, 50], [140, T_amb]])
sp_2 = create_setpoint_function([[0, T_amb], [0, 45], [120, 35], [200, T_amb]])

# create plot axes
fig, ax = plt.subplots(2, 1)

# plot setpoint functions
t = np.linspace(-1, 250, 250)
ax[0].plot(t, sp_1(t))
ax[1].plot(t, sp_2(t))


# ## Case Study: PCR Thermal Cycler Protocols
# 
# The goal of this next section is to create a function that returns the value of a setpoint profile for a PCR thermal cycler. We'll break this into a series of steps:
# 
# * Specify a PCR protocol
# * Convert the PCR protocol in a sequence of ramp and soak periods
# * Create a function that returns the value of setpoint at any point in time
# * Create a function that returns a setpoint function.

# ### Typcial PCR thermal cycler protocols
# 
# Here's an example of a PCR thermal cycler protocol:
# 
# * Activation of polymerase: 95°C, 15 min
# * Thermal cycling: 30 cycles
#     * Denaturation: 94°C, 20 s
#     * Annealing: 60°C, 20 s
#     * Elongation: 72°C, 30 s
# * Extension: 72°C, 10 min
# * Storage: 4°C, as necessary
# 
# The details of these protocols vary depending on the nature of the test, the reagents used, and the type of detection that will be employed. In real-time PCR, the number of cycling steps will end once a positive result is obtained.

# ### Representing PCR protocols in Python
# 
# The PCR protocol is a series of (time, temperature) pairs. The code in the next cell represents a protocol as a sequence of (time, temperature) pairs in a Python list. The list is constructed by concatenating subprotocols denoting the activation, cycling and extension steps in a PCR protocol

# In[6]:


get_ipython().run_line_magic('matplotlib', 'inline')
import numpy as np
import matplotlib.pyplot as plt

# number of cycles
n_cycles = 5

# enter steps in the protocol as a list of (time, temperature) pairs
activation = [(900, 95)]
cycling = [(20, 94), (20, 60), (30, 72)]*n_cycles
extension = [(600, 72)]
finish = [[0, 30]]

# concatenate into a list of (time, temperature) intervals
protocol = np.concatenate([activation, cycling, extension, finish])
protocol


# ### Converting to ramp, soak specifications
# 
# Each step in a PCR protocol consists of an initial ramp to the specified temperature, followed by a soak for the specified time and temperature. We begin the coding by demonstrating how to interpret the protocol specification as a series of ramp and soak periods.

# In[7]:


# each soak period is preceeded by a ramp
for time, temp in protocol:
    print(f"Ramp to {temp}C")
    print(f"Soak at {temp}C for {time:3d} seconds." )


# The next step is to introduce a ramp rate and add variables to track the start time and temperature for each segment. We will assume all ramp rates have the same absolute value.

# In[8]:


# add varibles to track current time and temperature
# ramp period is determined by a "ramp_rate"
ramp_rate = 2.5
time_now = 0.0
temp_now = 21.0

for time, temp in protocol:
    print(f"Time = {time_now:6.1f}: Ramp to {temp}C")
    time_now += np.abs((temp - temp_now)/ramp_rate) 
    temp_now = temp
    print(f"Time - {time_now:6.1f}: Soak at {temp}C for {time} seconds")
    time_now += time


# ### Finding the start and finish of each segment
# 
# Finally, we create a two column numpy array representing the setpoint profile. The first row in the array is the starting time and temperature. Each subsequent row constains the ending time and temperature of a segment.

# In[9]:


# store the data in a list of time, temperature pairs marking the end of each period

ramp_rate = 0.5 # deg/sec
time_now = 0.0
temp_now = 21.0

# intialze a list with the starting time and temperature
SP_list = [[time_now, temp_now]]

# append the ending time and temperature to the list
for time, temp in protocol:
    # ramp
    time_now += np.abs((temp - temp_now)/ramp_rate) 
    temp_now = temp
    SP_list.append([time_now, temp_now])

    # soak
    time_now += time
    SP_list.append([time_now, temp_now])

# convert list to numpy array to access columns
SP_array = np.array(SP_list)
SP_array


# In[10]:


fig, ax = plt.subplots(1, 1, figsize=(12, 5))
ax.plot(SP_array[:,0], SP_array[:,1], '.')


# ### Finding the setpoint function by interpolating the start and end of each segment
# 
# To implement control algorithms we will need to find values of the setpoint function at arbitrary points in time, not just at the start and finish of ramp or soak periods. The standard numpy library includes a linear interpolation function [`numpy.interp`](https://numpy.org/doc/stable/reference/generated/numpy.interp.html) well suited to this purpose.

# In[11]:


# create function to interpolate

def SP(t):
    return np.interp(t, SP_array[:,0], SP_array[:, 1])

# plotting the setpoint function
t = np.linspace(-100, max(SP_array[:,0]), 2000)
fig, ax = plt.subplots(1, 1, figsize=(12,5))
ax.plot(t, SP(t))
ax.set_title("Setpoint function")


# ### Creating a setpoint function for PCR thermal cycler
# 
# The last step is to put all of these steps together to create a function that generates a setpoint function. This is an example of a very powerful coding technique of [nested functions](https://realpython.com/inner-functions-what-are-they-good-for/).

# In[12]:


# create the setpoint function from a specified PCR 
def PCR_setpoint(protocol):
    
    ramp_rate = 0.5 # deg/sec
    time_now = 0.0
    temp_now = 21.0

    # intialze a list with the starting time and temperature
    SP_list = [[time_now, temp_now]]

    # append the ending time and temperature to the list
    for time, temp in protocol:
        # ramp
        time_now += np.abs((temp - temp_now)/ramp_rate) 
        temp_now = temp
        SP_list.append([time_now, temp_now])

        # soak
        time_now += time
        SP_list.append([time_now, temp_now])

    # convert list to numpy array to access columns
    SP_array = np.array(SP_list)
    
    def SP(t):
        return np.interp(t, SP_array[:,0], SP_array[:, 1])

    return SP

# create a setpoint function
setpoint = PCR_setpoint(protocol)

# plotting the setpoint function
t = np.linspace(0, 3000, 3000)
fig, ax = plt.subplots(1, 1, figsize=(12,5))
ax.plot(t, setpoint(t))
ax.set_title("Setpoint function")


# <hr>
# 
# **Study Question:** Change the protocol to include 30 thermal cycles, then create the setpoint function with `PCR_setpoint()` and plot the results.
# 
# **Study Question:** To better reflect the unequal heating and cooling rates available in most PCR devices, modify `PCR_setpoint()` to provide differing ramp rates for positive going and negative going ramps. Demonstrate the result using a postive ramp_rate of 2.5 degC/sec and a negative ramp_rate of -0.5 degC/sec.
# 
# <hr>
