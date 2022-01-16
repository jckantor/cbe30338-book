#!/usr/bin/env python
# coding: utf-8

# # Setting Up TCLab

# ## Hardware Setup
# 
# ![](figures/TCLab_labelled.jpg)
# 
# 1. Insert the temperature control shield into the Arduino module. This will fit together in only one way. Squeeze the modules together until the shield is fully seated.
# 
# 1. Connect the Arduino to your laptop with the USB data cable. You will need to USB-C to USB-A adapter if your laptop is equipped with USB-C only.
# 
# 1. Plug the DC power adapter into a wall socket and connect the power cable to to the temperature control shield. **Note: The temperature control shield requires its own power supply. There are two places where the power connector will fit. It's important to be sure it is plugged into the shield, not the Arduino.**
# 
# TCLab requires the one-time installation of custom firmware on an Arduino device. The firmware is normally preinstalled when you receive the device. But if necessary, the firmware and instructions for installation are available from the [TCLab-Sketch repository](https://github.com/jckantor/TCLab-sketch).
# 

# ## Software Setup

# ### Requirements
# 
# The tclab library must run locally on your laptop to access the USB port. A Python development system, such as [Anaconda](https://www.anaconda.com/products/individual) needs to be installed on your laptop prior to installing tclab.

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

# In[6]:


get_ipython().system('pip install tclab')


# There are occasional updates to the library. These can be installed by appending a ` --upgrade` to the above commands and demonstrated in the next cell.

# In[7]:


get_ipython().system('pip install tclab --upgrade')


# ## Testing
# 
# The next cells test for some commonly encountered issues with installation and operation of the Temperature Control Laboratory. This approach uses the library [`ipytest`](https://github.com/chmp/ipytest) which adapts the well known `pytest` unit testing environment for use within Jupyter notebooks. If you have not encountered unit testing before, it is a widely used technique to check for correct operation of individual units of code.
# 
# Run these cells. If the any of unit tests fail, comments within the unit test code may help determine the reason for the failure.

# ### Installing ipytest

# In[66]:


try:
    import ipytest
except:
    get_ipython().system('pip install ipytest')
    import ipytest
    
ipytest.autoconfig()


# ### Software testing
# 
# The following tetsts check for installation and operation the tclab library.

# In[67]:


get_ipython().run_cell_magic('ipytest', '--verbosity=1', '\n# Verify tclab has been installed and is accessible by the Python kernal.\n    \ndef test_tclab_install():\n    from tclab import TCLab, clock, Historian, Plotter\n    \n# Verify that TCLab can be run offline (i.e., without access to hardware).\n\ndef test_tclab_offline():\n    from tclab import setup\n    TCLab = setup(connected=False, speedup=20)\n    with TCLab() as lab:\n        pass')


# ### Hardware testing
# 
# The following tests check for connectivity and operation of the Temperature Control Lab hardware.

# In[68]:


get_ipython().run_cell_magic('ipytest', '--verbosity=1', '\n# TCLab cannot access the Arduino if it is run remotely on Google Colab. This is a common\n# error since notebooks are so easy to open in Google Colab. The following test fails if\n# the test is run on Google Colab.\n\ndef test_not_google_colab():\n    import sys\n    assert not "google.colab" in sys.modules\n\n# Verify that a connection an be opened to the Arduino.\n\ndef test_tclab_connect():\n    from tclab import TCLab, clock, Historian, Plotter\n    lab = TCLab()\n    lab.close()\n    \n# Verify tclab-sketch firmware version number is 2.0.1 or greater\n\ndef test_tclab_firmware_version():\n    import packaging\n    from tclab import TCLab\n    with TCLab() as lab:\n        vers = re.search(r\'\\s*([\\d.]+)\', lab.version).group(1)\n    assert packaging.version.parse(vers) >= packaging.version.parse("2.0.1")')


# ### Visual test

# If all of the above tests pass, then the following code fragment should turn on the LED at 50% level for 10 seconds.

# In[46]:


from tclab import TCLab

lab = TCLab()
lab.LED(50)
lab.close()


# ## Troubleshooting
# 
# 1. If your laptop consistently fails to locate or connect to the Arduino device, check the following:
# 
#     * Be sure you are have installed Python and tclab on your laptop, and that you are not attempting to run tclab on a remote server such as Google Colab. tclab requires direct access to the USB port on your laptop.
#     * Check cable connections. The USB cable from the Arduino should be connected to your laptop. The USB cable for the heater shield should be connected to a USB power supply. Reversing these connections will not harm anything but the system will not function.
#     * Verify that the laptop has made connection with the Arduino. This can be checked with the device manager on Windows. On Mac OS, open a terminal window and execute `ls /dev/cu*` on the command line. This will return a list of devices. If only `cu.Bluetooth-Incoming-Port` is present then Mac OS is not connecting to the Arduino. Try connecting and reconnecting the USB data cable. If that fails, try rebooting.
#     * Some USB cables are for charging only and not intended for data communications. Verify the cable you are using is a USB data cable.
#     * Download and install the Arduino IDE. From the tools menu, select "Arduino Leonardo" for the board, and select the incoming port. Though rare, we have experienced failures of the Arduino devices. Replace the Arduino and try again.
#     * The Arduino must have the tclab-sketch firmware to communicate with tclab. Download and install the latest tclab-sketch firmware.
# 
# 2. If you observe no change in temperature after the heaters on turned on:
# 
#     * Check that your heater power supply is plugged into power and into the top heater shield, not the Arduino.
#     * If you're using a power strip, verify the power strip is turned on.
#     * The LED indicator should be at 100% if the heaters are on.
#     * Check that lab.P1 and/or lab.P2 are set at non-zero values between 0 and 255. Values of about 100 are good for testing.
#     * We have experienced occasional failed USB power supplies. Try a different USB power supply.
# 

# In[ ]:




