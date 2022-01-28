#!/usr/bin/env python
# coding: utf-8

# # Assignment: Model Identification

# Fitting models to data is an engineering skill that links between the real world of engineering systems to the theory you've been learning in the classroom. For this laboratory session you will collect data from a step test experiments, then fit the data to models derived from first-principles energy balances. 

# ## Procedure

# 1. Download a copy of this notebook to your laptop and complete the the data collection exercises shown below. The results should be embedded in the notebook. Be sure to 'save-as-you-go' to avoid losing your work. 
# 
# 2. Use your step test data to fit two versions of a model for the temperature control lab:
# 
# * One-state model with one input.
# * Two-state model with one input
# 
# 5. Submit your completed lab notebook via Canvas.

# ## Exercise 1. Step Tests and Data Collection

# ### Step 1. Verify operation.
# 
# Execute the following cell to verify that you have a working connection to the temperature control lab hardware. This will test for installation of TCLab.py, connection to the Arduino device, and working firmware within the Arduino.

# In[ ]:


from tclab import TCLab, clock, Historian, Plotter

lab = TCLab()
print("TCLab Temperatures:", lab.T1, lab.T2)
lab.close()


# ### Step 2.  Check for steady state
# 
# As discussed in class, for step testing the device must be initially at steady state. Run the following code to verify the heaters are off and that the temperatures are at a steady ambient temperature.

# In[ ]:


# experimental parameters
tfinal = 30

# perform experiment
with TCLab() as lab:
    lab.U1 = 0
    lab.U2 = 0
    h = Historian(lab.sources)
    p = Plotter(h, tfinal)
    for t in clock(tfinal):
        p.update(t)


# ### Step 3. Step Test
# 
# The step test consists of turning one heater one at 50% power and recording temperature data for at least 800 seconds. Copy the code from Step 2 into the following cell. Then modify as needed to accomplish the step test with P1 at 200 and using 50% of maximum power.

# In[ ]:


# write your code here


# ### Step 4. Save data to a .csv file
# 
# Run the following cell to verify and save your data to a '.csv' file. Be sure you can find and locate the data on your laptop before ending your session. You will need access to this data for subsequent exercises.

# In[ ]:


import matplotlib.pyplot as plt

t, T1, T2, Q1, Q2 = h.fields

plt.plot(t, T1, t, T2, t, Q1, t, Q2)
plt.legend(['T1','T2','Q1','Q2'])
plt.xlabel('Time / seconds')
plt.grid()

h.to_csv('tclab-data.csv')


# ## Exercise 2. Fitting a First-Order Model

# As discussed in class, a simple energy balance model for T1 is given by
# 
# $$C_p \frac{dT_1}{dt} = U_a(T_{amb} - T_1) + \alpha P_1 U_1$$
# 
# where the parameter $\alpha$ has, through independent means, been determined as 0.00016 when U1 is given in percent of full power and power is measured in Watts. Following the notes from Section 2.4, use the results of this experiment to estimate values for $C_p$ and $U_a$. Write your answers in the following cell.  
# 
# You may cut and paste code from Section 2.4 for this task. You will need to modify the code to read your data file. Be sure to report
# 
# 1. Final estimates for $U_a$ and $C_p$
# 2. An estimate of the time constant computed from $U_a$ and $C_p$.
# 3. An estimate of the steady-state gain computed from $U_a$.

# In[ ]:





# ## Exercise 3. Fitting a Second-Order Model
# 
# A second order model is for the heater/sensor combination is given by
# 
# $$
# \begin{align}
# C^H_p\frac{dT_{H,1}}{dt} & = U_a(T_{amb} - T_{H,1}) + U_b(T_{S,1} - T_{H,1}) + P_1u_1\\
# C^S_p\frac{dT_{S,1}}{dt} & = U_b(T_{H,1} - T_{S,1}) 
# \end{align}
# $$
# 
# where $T_{H,1}$ is the heater temperature, $T_{S,1}$ is the sensor temperature, and $U_b$ is the heat transfer coefficient between the heater and sensor. 
# 
# Modify the code you developed for Exercise 2 to fit this second order model. The code shown in Section 2.5 of the notes may be helpful. 
# 
# 1. Report your best fit for $U_a$, $U_b$, $C^H_p$, and $C^S_p$. 
# 2. What are the time constants for the heater and sensor? Do you see any relationship between these time constants and what you found for the first-order model?
# 
# 

# In[ ]:




