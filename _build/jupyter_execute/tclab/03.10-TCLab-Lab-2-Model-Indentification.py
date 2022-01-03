#!/usr/bin/env python
# coding: utf-8

# # TCLab Lab 2: Model Identification

# For this laboratory session you will collect data from a step test experiment, then fit the data to models derived from first-principles energy balances. Fitting models to data is an engineering skill that links between the real world of engineering systems to the theory you've been learning in the classroom.

# ## Procedures

# 1. Please work in groups of two.
# 
# 2. Check out a TCLab kit. The kit consists of
#     * plastic container
#     * Arduino device with the TCLab shield installed
#     * 5 watt USB power supply
#     * USB power cable
#     * USB data cable
#     * equipment log sheet
#     
#    Before going further, sign and date the equipment log sheet. 
# 
# 3. Download a copy of this notebook to your laptop, and complete the exercises shown below. Under each exercise heading, add as many text and code cells as needed to complete the exercise. The results should be embedded in the notebook. Be sure to 'save-as-you-go' to avoid losing your work.
# 
# 4. Add any relevant notes to the equipment log and return the kit to equipment at the front of the lab. **Return any malfunctioning kit to the instructor for repair.**
# 
# 5. Submit your completed lab notebook via Sakai.  The notebook should contain the name of both lab partners. Both partners should submit a copy of the notebook.

# ## Exercise 1. Verify operation of the temperature control lab.
# 
# Execute the following cell to verify that you have a working connection to the temperature control lab hardware. This will test for installation of TCLab.py, connection to the Arduino device, and working firmware within the Arduino.

# In[ ]:


from tclab import TCLab, clock, Historian, Plotter

lab = TCLab()
print("TCLab Temperatures:", lab.T1, lab.T2)
lab.close()


# ## Exercise 2.  Check for steady state
# 
# As discussed in class, for good model fitting it is essential for the TCLab hardware to be at steady state before proceeding with the step test. Run the following code to verify that the heaters are off and that the temperatures are at a steady ambient temperature.

# In[ ]:


# experimental parameters
tfinal = 30

# perform experiment
with TCLab() as lab:
    h = Historian(lab.sources)
    p = Plotter(h, tfinal)
    for t in clock(tfinal):
        p.update(t)


# ## Exercise 3. Step test.
# 
# The step test consists of turning on one heater at 50% power and recording temperature data for at least 800 seconds. Copy and paste the code from Exercise 2 into the following cell, then modify as needed to accomplish the step test. 

# In[ ]:


# write your code here


# ## Exercise 4. Verify and save data to a .csv file
# 
# Run the following cell to verify and save your data to a '.csv' file. Be sure you can find and locate the data on your laptop before leaving the lab. You will need access to this data for subsequent exercises.

# In[ ]:


get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt

t, T1, T2, Q1, Q2 = h.fields

plt.plot(t, T1, t, T2, t, Q1, t, Q2)
plt.legend(['T1','T2','Q1','Q2'])
plt.xlabel('Time / seconds')
plt.grid()

h.to_csv('tclab-data.csv')


# ## Exercise 5. Analysis
# 
# 1.) Approximating the the step test results for T1 as a first order transfer function, estimate the time constant and gain. Write your answer in the following cell.

# In[ ]:





# 2.) As we discussed in class, a simple energy balance model for T1 is given by
# 
# $$C_p \frac{dT_1}{dt} = U_a(T_{amb} - T_1) + P Q_1$$
# 
# where the parameter $P$ has, through independent means, been determined as 0.04 watts per percent increase in $Q_1$. Use the results of this experiment to estimate values for $C_p$ and $U_a$. Write your answers in the following cell.

# 
