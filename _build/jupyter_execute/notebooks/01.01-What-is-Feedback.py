#!/usr/bin/env python
# coding: utf-8

# # What is Feedback?
# 
# The main theme of this course is the use of feedback to create useful engineering systems. So what is feedback?

# ## Biomedical Example: Artificial Pancreas
# 
# [NIH: Artificial pancreas system better controls blood glucose levels than current technology](https://www.nih.gov/news-events/news-releases/artificial-pancreas-system-better-controls-blood-glucose-levels-current-technology)

# ### Insulin/Glucose/Glucagon Dynamics
# 
# The Insulin/Glucose/Glucagon system of the human body provides excellent examples of negative feedback. **Negative feedback provides a corrective action to return a system to a desired steady-state following a disturbance.** In biological contexts, steady-state is called homoestasis.
# 
# ![](https://bio.libretexts.org/@api/deki/files/15807/glucose_feedback.png?revision=1) <br>Image Credit: bio.libretexts.org

# Diabetes is a disease in which thte pancreas can not produce sufficient insuline (Type I) or has lost the ability to regulate glucose (Type II). High glucose levels lead to serious chronic disorders.
# 
# Over the last decade, due to the research work by chemical and biomedical engineers, automated insulin therapies are now commercially available from multiple manufacturers. The following links and illusration show the major components of these systems. 
# 
# [Medtronic MiniMed 770G System](https://www.medtronicdiabetes.com/products/minimed-770g-insulin-pump-system?utm_source=tsa_google_ppc&utm_campaign=Insulin+Pumps+2.0&utm_medium=text&gclid=Cj0KCQiA0-6ABhDMARIsAFVdQv87xTl1TF0Yx9YWM-LRV4x-FjZvWFaZhSA_33o--SDWvbY7h4O-UyEaAvzaEALw_wcB&gclsrc=aw.ds)
# 
# ![](https://www.medtronicdiabetes.com/res/img/770g/770g-img1a.jpg)

# ![](figures/Medtronic.png)

# Discussion Questions
# 
# * What sensors are required to implement control?
# * What actuators are required?
# * What is the control objective?
# * How do you assure device safety?
# * What computations are necessary?
# * What data should be recorded?
# * What alarms or diagnostic information would you wish to provide to the user?

# ## Other examples:

# ### Biological Systems: Iron and Oxygen Sensing
# 
# ![](https://els-jbs-prod-cdn.jbs.elsevierhealth.com/cms/attachment/0ea1b4a8-5f44-4b64-a40d-11c8ebd6cdee/gr1.jpg) <br> Image Credit: https://doi.org/10.1016/j.kint.2019.01.003

# ### Aerospace Systems: SpaceX Falcon 9
# 
# Video: [Space Landing](https://youtu.be/WLidfyD4eUM?t=7)

# ![](https://zlsadesign.com/infographic/vehicle/spacex-falcon9-control.png) <br> Image Credit: John Ross, [ZLSA Design](https://zlsadesign.com/)

# ### Pharmaceutical Manufacturing: Fermentation 
# 
# ![](https://support.industry.siemens.com/cs/images/109478439/fermentation_process.png) <br> Image Credit: [Siemens](https://support.industry.siemens.com/cs/document/109478439/simatic-pcs-7-in-the-pharmaceutical-industry-%E2%80%9Cfermentation%E2%80%9D-(demo-project)?dti=0&lc=en-WW)

# ### Refineries: Fluidized Catalytic Cracking Unit (FCCU)
# 
# The FCCU is a critical process in most refineries. This is the unit responsible for 'cracking' the long chain hydrocarbons found to create more valuable molecules that can be blended into gasoline. Operation of the FCCU involves a complex coordination of a large scale reactors, regenerators, distillation operating with the potential for catastrophic accidents. When you here of explosions at refineries, often it is the outcome of some event involving operation of the FCCU.
# 
# The following video was created by the U.S. Chemical Safety Board (USCSB) to demonstrate causes of an explosion in 2015 at an ExxonMobil refinery in Torrance, CA.  Watch the first 2-3 minutes for an excellent animation of FCCU operation. While you are watching the animation, ask yourself how this unit can be controlled to establish desired flowrates, prevent hazards, maximize the economic value of the products, and acheive product quality requirements. 
# 
# (If found this interesting,  you might also check out an animation of a [2005 incident at the BP Texas City Refinery](https://youtu.be/goSEyGNfiPM?t=43))

# In[2]:


from IPython.display import HTML

HTML('<iframe width="560" height="315" src="https://www.youtube.com/embed/JplAKJrgyew" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>')


# ### Many, Many Others
# 
# * **Automotive:** Autonomous Driving
#     
# * **Sports:** Baseball/Softball ... hitting a ball, catching a fly ball, throw and catch from the outfield.

# In[ ]:





# 1. **Positive Feedback** Positive feedback reinforces change. A desirable behavior for management, training, social situations, bank accounts.
# 
# 1. **Negative Feedback** Negative feedback suppresses change. Generally what we want for automatic control of processes and devices, in nature and biology.
# 
# 1. There are two fundamental and potentially conflicting goals of feedback control:
# 
#     * **Setpoint Tracking:** Cause a system variable of interest to achieve and track an externally specified value.
# 
#     * **Disturbance Rejection:** Maintain a system variable at a desired value regardless of external influences on the system.
# 
# 1. Setpoints generally come from other control systems. Complex systems usually involve **control heirarchies** to manage complexity and reduce the impact of uncertainty. ![](https://i1.wp.com/www.hisour.com/wp-content/uploads/2018/11/Hierarchical-control-system.jpg) <br> Image Credit: HiSour
# 
# 1. Disturbances are the uncertainties which control systems are designed to mitigate. Uncertainties are not always subject to classical mathematics.
#     * **Measured Disturbances:** Disturbances which can be measured or estimated in advance of their effect on a process system.
#     * **Unmeasured Disturbancs:** Disturbances which are not measured.
#     
#     * **Resolvable Uncertainty:** Uncertainties that can be quantitatively characterized using probabilistic or other methods. Often "long tails". The "known unknowns".
#     
#     * **Radical Uncertainty:** Cannot be described by probabilistic models. The "unknown unknowns". Outcomes of political events, modes of software failure, changes in customer requirements. This is the human condition.
# 
# 1. Consequences of feedback.
# 
#     * The dynamics of systems under active control are often difficult to understand. Cause and effect may not be what you expect.
#     * Feedback control reduces the need for highly accurate or detailed models. Systems become as accurate as their sensors.  
#     * The role of feedback is often not understood in social and economic settings.
# 
# 1. Control is a large interdisciplineary field of ever-growing technical importance. This course will introduce many of the topics in the "Map of Control Theory" by Brian Douglas. ![](figures/Control_Map_ver5.png) <br> Image Credit: Brian Douglas {cite}`douglas2017fundamentals`
# 

# In[ ]:




