#!/usr/bin/env python
# coding: utf-8

# # The Temperature Control Laboratory
# 
# The [Temperature Control Laboratory](http://apmonitor.com/pdc/index.php/Main/ArduinoTemperatureControl) provides a hands-on learning environment for traditional courses in process control. The Arduino-based device consists of a two-input, two-output system of heaters and sensors. [TCLab](https://github.com/jckantor/TCLab) is a Python library providing the software tools to create and test control algorithms ranging from simple step testing to sophisticated multivarible predictive control.

# ## Hardware
# 
# This notebook provides a basic introduction to the device and the TCLab library.
# 
# <img src='figures/B.00-arduino_lab_kit.png' style="float: right;padding-left:30px;"></img>
# The Temperature Control Laboratory hardware consists of five components:
# 
# 1. Arduino microcontroller board (Arduino Uno, Arduino Leonardo, or equivalents).
# 
# 2. The Temperature Control Laboratory plug-in board (also known as a shield).
# 
# 3. Five watt USB power supply.
# 
# 4. 5.5mm to USB power supply cable.
# 
# 5. USB 2.0 data cable. (w/mini-USB connector for Arduino Uno, or micro-USB cable for Arduino Leonardo.)
# 
# Before going further, be sure to complete the steps outlined under *Hardware setup* as described in TCLab [README](https://github.com/jckantor/TCLab/blob/master/README.rst). Mac OS users may need to install a serial driver available [here](https://github.com/adrianmihalko/ch340g-ch34g-ch34x-mac-os-x-driver). Normally the TCLab shield will already be mounted on the Arduino board, and the firmware driver will have been loaded on to the Arduino.
