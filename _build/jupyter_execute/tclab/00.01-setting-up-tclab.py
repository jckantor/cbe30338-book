#!/usr/bin/env python
# coding: utf-8

# # Setting up TCLab

# ## Hardware Setup
# 
# ![](figures/TCLab_labelled.jpg)
# 
# 1. Insert the temperature control shield into the Arduino module. This will fit together in only one way. Squeeze the modules together until the shield is fully seated.
# 
# 1. Connect the Arduino to your laptop with the USB data cable. You will need to USB-C to USB-A adapter if your laptop is equipped with USB-C only.
# 
# 1. Plug the DC power adapter into a wall socket and connect the power cable to to the temperature control shield. **Note: The temperature control shield requires its own power supply. Be sure the power supply it is plugged into the shield, not the Arduino.**
# 
# TCLab requires the one-time installation of custom firmware on an Arduino device. The firmware is normally preinstalled when you receive the device. But if necessary, the firmware and instructions for installation are available from the [TCLab-Sketch repository](https://github.com/jckantor/TCLab-sketch).
# 

# ## Software Setup

# ### Requirements
# 
# The tclab library must run locally on your laptop to access the USB port. A Python development system, such as [Anaconda](https://www.anaconda.com/products/individual) needs to be installed on your laptop prior to installing tclab. **tclab cannot access the USB port when run Google Colab.**

# ### How the software is organized
# 
# Software for the Temperature Control Lab is organized as shown in the accompanying diagram. Note that the Python scripts must run on your laptop, not a remote server, in order to access the local USB port.
# 
# ![](figures/TCLab_overview.png)
# 
# **_Jupyter notebooks and Python scripts:_**
# The top level consists of the you code you write to implement control algorithms. This may be done in Jupyter/Python notebooks or directly in Python using an interactive development environment (IDE). This repository contains many examples of code written in Jupyter/Python notebooks.
# 
# **_TCLab.py:_**
# [TCLab.py](https://github.com/jckantor/TCLab) is contained in a Python library entitled `tclab`. The library includes
# 
# * `TCLab()` class that creates an object to access to the device,
# * `clock` for synchronizing with a real time clock
# * `Historian()` class to create objects for data logging.
# * `Plotter()` class to visualize data in real time.
# 
# **_TCLab-sketch:_**
# The [TCLab-sketch](https://github.com/jckantor/TCLab-sketch) repository provides firmware to ensure intrisically safe operation of the Arduino board and shield. The sketch is downloaded to the Arduino using the [Arduino IDE](https://www.arduino.cc/en/Main/Software). Loading firmware to the Arduino is a one-time operation. 
# 
# **_Arduino:_**
# The hardware platform for the Temperature Control Laboratory. The Python tools and libraries have been tested with the Arduino Leonardo boards.

# ### Installing the tclab library
# 
# The tclab library is installed from a terminal window (MacOS) or command window (PC) with the command
# 
#     pip install tclab
# 
# Alternatively, the installation can be performed from within a Jupyter/Python notebook with the command

# In[3]:


get_ipython().system('pip install tclab')


# There are occasional updates to the library. These can be installed by appending a ` --upgrade` to the above commands and demonstrated in the next cell.

# In[4]:


get_ipython().system('pip install tclab --upgrade')


# ### Google Colab
# 
# The tclab library will install and can be run in off-line mode on Google Colab and can be run in off-line mode. **Note, however, the USB port is not accessible from Google Colab, so the attached Arduino and shield can not be run from Google Colab.**

# In[ ]:




