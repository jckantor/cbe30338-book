#!/usr/bin/env python
# coding: utf-8

# # Lab Assignment: Coding a Relay Controller

# The purpose of this first laboratory session is to verify that you can interface and interact with the TCLab hardware, and familiarize you with the TCLab library. The first exercise will be to code a rudimentary relay (also called 'on-off' or thermostat) controller for one of the two heaters.
# 
# Before you begin, you should be familiar with the following reading meterials:
# 
# * [On-Off Control in Section 1.6 of *Feedback Control for Scientists and Engineers*](http://www.cds.caltech.edu/~murray/books/AM08/pdf/fbs-intro_07Aug2019.pdf#page=19)

# ## Procedures

# 1. Select a lab partner. The lab sessions are often more productive when bringing the experiences of two students together to work on a task. The interaction between lab partners also enchances the learning opportunity.
# 
# 
# 2. Check out a TCLab kit. The kit consists of
#     * plastic container
#     * Arduino device with the TCLab shield installed
#     * 5 watt USB power supply
#     * USB power cable
#     * USB data cable
#     * equipment log sheet
# 
# 
# 3. Before going further, sign and date the equipment log sheet. 
# 
# 
# 4. Note that you may need to check out a power strip to share with other groups using the same lab bench.
# 
# 
# 5. Download a copy of this notebook to your laptop, and complete the exercises shown below. Under each exercise heading, add as many text and code cells as needed to complete the exercise. The results should be embedded in the notebook. Be sure to 'save-as-you-go' to avoid losing your work.
# 
# 
# 6. Add any relevant notes to the equipment log and return the kit to equipment at the front of the lab. **Return any malfunctioning kit to the instructor for repair.**
# 
# 
# 7. Submit your completed lab notebook via Sakai.  The notebook should contain the name of both lab partners. Both partners should submit a copy of the notebook.

# ## Step 1. Download and install TCLab.py
# 
# Execute the following cell to download and install the TCLab.py python library.

# In[1]:


get_ipython().system('pip install tclab --upgrade')


# ## Step 2.  Verify that your hardware and software are working correctly.
# 
# The following cell should cause the LED on the TCLab shield to light up to 100% maximum brightness.

# In[2]:


from tclab import TCLab

with TCLab() as lab:
    lab.LED(0)


# ## Step 3. Turn on the heaters for 120 seconds and log temperature response.
# 
# For this exercise, write a code cell that turns on heater 1 at 100% power, then log the temperature response once per second for 120 seconds. The output of the cell should report the time, power level, and temperature for each measurement. You may wish to consult [TCLab Python Package](https://nbviewer.jupyter.org/github/jckantor/CBE30338/blob/master/notebooks/B.01-The-TCLab-Python-Package.ipynb/) notebook for relevant code examples. You will need the `clock` function from `tclab` for this exercise.

# In[2]:


# put your code here.


# ## Step 4. Code an on-off controller. 
# 
# Code an on-off controller for a setpoint of 40 degrees C using heater 1 as the manipulated variable, and temperature 1 as the measured variable. Operate the controller for at least 5 minutes (600 seconds), reporting time/power/temperature measurements every 2 seconds. 

# In[3]:


# put your code here.


# ## Step 5. Analysis
# 
# Examine the results of the previous exercise and answer the following questions.
# 
# 1. Approximately how much time elapses between power on and power off events?
# 
# 2. What is the approximate duty cycle (i.e, fraction of time the heater is in the 'on' state) once the initial start-up period has passed.
# 
# 3. What is the size of the oscillation around the setpoint?  Why does this occur?

# Write your answers in this markdown cell.
