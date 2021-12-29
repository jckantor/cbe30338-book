#!/usr/bin/env python
# coding: utf-8

# # Examples of Process Control

# ![](./figures/FeedbackControlDiagram.png)

# ## Biomedical: Automated Insulin Therapy
# 
# Over the last decade, due to the research work by chemical and biomedical engineers, automated insulin therapies are now commercially available from several manufacturers. The following links and illusration show the major components of these systems. 
# 
# * What sensors are required?
# * What actuators are required?
# * What is the control objective?
# * How do you assure safety?
# 
# [Medtronic MiniMed 770G System](https://www.medtronicdiabetes.com/products/minimed-770g-insulin-pump-system?utm_source=tsa_google_ppc&utm_campaign=Insulin+Pumps+2.0&utm_medium=text&gclid=Cj0KCQiA0-6ABhDMARIsAFVdQv87xTl1TF0Yx9YWM-LRV4x-FjZvWFaZhSA_33o--SDWvbY7h4O-UyEaAvzaEALw_wcB&gclsrc=aw.ds)
# 
# ![](https://www.medtronicdiabetes.com/res/img/770g/770g-img1a.jpg)

# ### Discussion Questions
# 
# Consider the automated insulin control system in the following image.  Indentify
# 
# * Sensors
# * Actuators
# * Process
# * Computations (where are they done?)
# * What are disturbance variables?
# * Can you directly measure what you actually need to control?
# * What are the manipulated variables? 
# * Are there other manipulations you might wish to do?
# * What is the setpoint?
# * What diagnostic outputs would you wish to monitor?

# ## Refineries: Fluidized Catalytic Cracking Unit (FCCU)
# 
# The FCCU is a critical process in most refineries. This is the unit responsible for 'cracking' the long chain hydrocarbons found to create more valuable molecules that can be blended into gasoline. Operation of the FCCU involves a complex coordination of a large scale reactors, regenerators, distillation operating with the potential for catastrophic accidents. When you here of explosions at refineries, often it is the outcome of some event involving operation of the FCCU.
# 
# The following video was created by the U.S. Chemical Safety Board (USCSB) to demonstrate causes of an explosion in 2015 at an ExxonMobil refinery in Torrance, CA.  Watch the first 2-3 minutes for an excellent animation of FCCU operation. While you are watching the animation, ask yourself how this unit can be controlled to establish desired flowrates, prevent hazards, maximize the economic value of the products, and acheive product quality requirements. 
# 
# (If found this interesting,  you might also check out an animation of a [2005 incident at the BP Texas City Refinery](https://youtu.be/goSEyGNfiPM?t=43))

# In[4]:


from IPython.display import HTML

HTML('<iframe width="560" height="315" src="https://www.youtube.com/embed/JplAKJrgyew" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>')


# ## Manufacturing: Tesla Shanghai Gigafactory
# 
# Telsa has recently been outfitting factories with very large scale automated casting ('megacasting') to signficantly reduce the complexity of its manufacturiing processes.
# 
# As you watch the following video, try to identify the many levels of control required to realize this automated manufacturing system. For example, what sensors and actuators are required for each robot to do their tasks?  How is quality control maintained? How are operations coordinated among the assembly stations in the manufacturing line?

# In[4]:


from IPython.display import HTML
s = '<blockquote class="twitter-tweet"><p lang="en" dir="ltr">' +     'Giga Shanghai is becoming a production powerhouse. Watch ' +     'mega castings for Model Y coming out of 6k-ton Giga presses. ' +     'The whole process is fully automated, including quality check. ' +     'Pretty mind blowing to say the least. ' +     '<a href="https://t.co/PBMUpDjnD8">pic.twitter.com/PBMUpDjnD8</a>' +     '</p>&mdash; Ray4Tesla⚡️🚘☀️🔋 (@ray4tesla) ' +     '<a href="https://twitter.com/ray4tesla/status/1356639381549846529?ref_src=twsrc%5Etfw">February 2, 2021</a>' +     '</blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>'
HTML(s)


# 
