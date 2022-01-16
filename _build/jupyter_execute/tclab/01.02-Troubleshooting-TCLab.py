#!/usr/bin/env python
# coding: utf-8

# # Troubleshooting TCLab

# ## Testing
# 
# The next cells test for some commonly encountered issues with installation and operation of the Temperature Control Laboratory. This approach uses the library [`ipytest`](https://github.com/chmp/ipytest) which adapts the well known `pytest` unit testing environment for use within Jupyter notebooks. If you have not encountered unit testing before, it is a widely used technique to check for correct operation of individual units of code.
# 
# Run these cells. If the any of unit tests fail, comments within the unit test code may help determine the reason for the failure.

# ### Installing ipytest

# In[1]:


try:
    import ipytest
except:
    get_ipython().system('pip install ipytest')
    import ipytest
    
ipytest.autoconfig()


# ### Software testing
# 
# The following tetsts check for installation and operation the tclab library.

# In[2]:


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

# ### Laptop doesn't connect to the Arduino
# 
# If your laptop consistently fails to locate or connect to the Arduino device, check the following:
# 
# 1. Be sure you are have installed Python and tclab on your laptop, and that you are not attempting to run tclab on a remote server such as Google Colab. tclab requires direct access to the USB port on your laptop.
# 
# 1. Check cable connections. The USB cable from the Arduino should be connected to your laptop. The USB cable for the heater shield should be connected to a USB power supply. Reversing these connections will not harm anything but the system will not function.
# 
# 1. Verify that the laptop has made connection with the Arduino. This can be checked with the device manager on Windows. On Mac OS, open a terminal window and execute `ls /dev/cu*` on the command line. This will return a list of devices. If only `cu.Bluetooth-Incoming-Port` is present then Mac OS is not connecting to the Arduino. Try connecting and reconnecting the USB data cable. If that fails, try rebooting.
# 
# 1. Some USB cables are for charging only and not intended for data communications. Verify the cable you are using is a USB data cable.
# 
# 1. Download and install the Arduino IDE. From the tools menu, select "Arduino Leonardo" for the board, and select the incoming port. Though rare, we have experienced failures of the Arduino devices. Replace the Arduino and try again.
# 
# 1. The Arduino must have the tclab-sketch firmware to communicate with tclab. Download and install the latest tclab-sketch firmware.

# ### Heaters don't appear to work
# 
# If you observe no change in temperature after the heaters on turned on:
# 
# 1. Check that your heater power supply is plugged into power and into the top heater shield, not the Arduino.
# 
# 1. If you're using a power strip, verify the power strip is turned on.
# 
# 1. The LED indicator should be at 100% if the heaters are on.
# 
# 1. Check that lab.P1 and/or lab.P2 are set at non-zero values between 0 and 255. Values of about 100 are good for testing.
# 
# 1. We have experienced occasional failed USB power supplies. Try a different USB power supply.
