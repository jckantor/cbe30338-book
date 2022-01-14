#!/usr/bin/env python
# coding: utf-8

# # Lab 1: Thermostat Control

# The purpose of this first laboratory session is to verify that you can interface and interact with the TCLab hardware, and familiarize you with the TCLab library. The first exercise will be to code a rudimentary relay (also called 'on-off' or thermostat) controller for one of the two heaters.
# 
# For background on on-off control, consult
# 
# * [On-Off Control in Section 1.6 of *Feedback Control for Scientists and Engineers*](http://www.cds.caltech.edu/~murray/books/AM08/pdf/fbs-intro_07Aug2019.pdf#page=19)

# ## Procedures

# 1. Download a copy of this notebook to your laptop and complete the exercises shown below. Under each exercise heading, add as many text and code cells as needed to complete the exercise. The results should be embedded in the notebook. 'Save-as-you-go' to avoid losing your work.
# 
# 1. Submit your completed lab notebook via Canvas. All submissions must be pdf format.

# ## Step 1. Download and install TCLab.py
# 
# Execute the following cell to download and install the TCLab.py python library.

# In[1]:


get_ipython().system('pip install tclab --upgrade')


# ## Step 2.  Verify that your hardware and software are working correctly.
# 
# The following cell should cause the LED on the TCLab shield to light up to 50% maximum brightness. The output of this cell should indicate successful connection and disconnect.

# In[3]:


from tclab import TCLab

with TCLab() as lab:
    lab.LED(50)


# ## Step 3. Turn on the heaters for 120 seconds and log temperature response.
# 
# For this exercise, write a code cell that turns on heater 1 at 100% power, then log the temperature response once per second for 120 seconds. The output of the cell should report the time, power level, and temperature for each measurement. You will need the `clock` function from `tclab` for this exercise.

# In[4]:


# put your code here.


# ## Step 4. Code an on-off controller. 
# 
# Code an on-off controller for a setpoint of 30 degrees C using heater 1 as the manipulated variable, and temperature 1 as the measured variable. Operate the controller for at least 5 minutes (600 seconds) reporting time/power/temperature measurements every 2 seconds. 

# In[5]:


# put your code here.


# ## Step 5. Analysis
# 
# Examine the results of the previous exercise and answer the following questions.
# 
# 1. After the initial transients decay and the system is in continuous cycling mode, how much time elapses between power on and power off events?
# 
# 2. What is the approximate duty cycle (i.e, fraction of time the heater is in the 'on' state) once the initial start-up period has passed.
# 
# 3. What is the peak-to-peak magnitude of the temperature oscillation around the setpoint?  Why does this occur?
# 
# Type your answers in the markdown cell below.

# Write your answers in this markdown cell.
