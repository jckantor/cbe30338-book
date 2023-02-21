#!/usr/bin/env python
# coding: utf-8

# # Case Study: PCR Thermal Cycler Protocols
# 
# The goal of this next section is to create a function that returns the value of a setpoint profile for a PCR thermal cycler. We'll break this into a series of steps:
# 
# * Specify a PCR protocol
# * Convert the PCR protocol in a sequence of ramp and soak periods
# * Create a function that returns the value of setpoint at any point in time
# * Create a function that returns a setpoint function.

# ## Typcial PCR thermal cycler protocols
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

# ## Representing PCR protocols in Python
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


# ## Converting to ramp, soak specifications
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


# ## Finding the start and finish of each segment
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


# ## Finding the setpoint function by interpolating the start and end of each segment
# 
# To implement control algorithms we will need to find values of the setpoint function at arbitrary points in time, not just at the start and finish of ramp or soak periods. The standard numpy library includes a linear interpolation function [`numpy.interp`](https://numpy.org/doc/stable/reference/generated/numpy.interp.html) well suited to this purpose.

# In[56]:


# create function to interpolate

def SP(t):
    return np.interp(t, SP_array[:,0], SP_array[:, 1])

# plotting the setpoint function
t = np.linspace(-100, max(SP_array[:,0]), 2000)
fig, ax = plt.subplots(1, 1, figsize=(12,5))
ax.plot(t, SP(t))
ax.set_title("Setpoint function")


# ## Creating a setpoint function for PCR thermal cycler
# 
# The last step is to put all of these steps together to create a function that generates a setpoint function. This is an example of a very powerful coding technique of [nested functions](https://realpython.com/inner-functions-what-are-they-good-for/).

# In[57]:


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
