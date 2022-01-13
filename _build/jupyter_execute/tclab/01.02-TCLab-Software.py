#!/usr/bin/env python
# coding: utf-8

# # TCLab Software Setup
# 
# The accompanying diagram shows how to access the temperature contol laboratory using the TCLab library.
# 
# ![](figures/TClab.jpg)
# 
# **_Jupyter notebooks and Python scripts:_**
# The highest level consists of the you code you write to implement control algorithms. This can be done in Jupyter/Python notebooks, directly from Python using a development environment such as Spyder or PyCharm. This repository contains several examples, lessons, and student projects.
# 
# **_TCLab:_**
# [TCLab](https://github.com/jckantor/TCLab) consists of a Python library entitled `tclab` that provides high-level access to sensors, heaters, a pseudo-realtime clock. The package includes `TCLab()` class that creates an object to access to the device, an iterator `clock` for synchronizing with a real time clock, `Historian()` class to create objects for data logging, and a `Plotter()` class to visualize data in realtime.
# 
# **_TCLab-sketch:_**
# The [TCLab-sketch](https://github.com/jckantor/TCLab-sketch) github repository provides firmware to ensure intrisically safe operation of the Arduino board and shield. The sketch is downloaded to the Arduino using the [Arduino IDE](https://www.arduino.cc/en/Main/Software). Loading firmware to the Arduino is a one-time operation. 
# 
# **_Arduino:_**
# The hardware platform for the Temperature Control Laboratory. The Python tools and libraries have been tested with the Arduino Uno and Arduino Leonardo boards.

# The TCLab package is installed from a terminal window (MacOS) or command window (PC) with the command
# 
#     pip install tclab
# 
# Alternatively, the installation can be performed from within a Jupyter/Python notebook with the command
# 
#     !pip install tclab
# 
# There are occasional updates to the library. These can be installed by appending a ` --upgrade` to the above commands and demonstrated in the next cell.

# In[1]:


get_ipython().system('pip install tclab --upgrade')

