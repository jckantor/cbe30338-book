#!/usr/bin/env python
# coding: utf-8

# # Practical Proportional (P) and Proportional-Integral (PI) Control

# ## Learning Goals
# 
# * Explain terms in the equations for proportional control and proportional-integral control/
# * Derive velocity from form of PI control.
# * Define terminology
#     * negative feedback
#     * bias (aka offset or null) term
#     * proportional gain and integral gain
# * Explain difference between setpoint tracking and disturbance rejection.
# * Explain roles of the proportional and integral terms contribute.
# * Explain the purpose of each of the following enhancements of 'textbook' PI control:
#     * Anti-reset windup
#          * Control algorithm modifications
#          * Event loop modifications
#     * Bumpless Transfer

# ## Negative Feedback
# 
# **Negative feedback** is the core principle underpinining process control.  Negative feedback suppresses deviations from the setpoint assuming the proportional gain is positive and the process exhibits a positive-going response from a positive change in the manipulated variable. If the process variable grows above the setpoint then the manipulated variable is decreased. If the process variable falls below the setpoint then the manipulated variable is increased.
# 
# If the system exhibits a negative-going response to a postive change in the manipiulated variable, then the sign of the proportional gain must also be negative to assure negative feedback control.
# 
# ![](http://4.bp.blogspot.com/-ZKMZhvwDJ2o/UM3-y4BDIqI/AAAAAAAAAbM/PIsa1XpziNg/s1600/fbl+glucose.gif)
# 
# **Positive feedback** is encountered in social, economic, and biological systems where there is a desire to amplify a desirable outcome. Positive feedback can induce good behaviors, result in 'virtuous' cycles of innovation and development, or wealth creation. But in most hard engineering situations, the immediate objective is to cause a variable to track a setpoint for which negative feedback is enabling technology
# 
# <hr>
# 
# **Study Question:** Describe the two types of negative feedback taking place in the glucose/insulin/glucagon system diagrammed above. 
# 
# **Study Question:** Why are two feedback loops necessary in this biological system? Can you think of an analogy for temperature control of the Temperature Control Lab?
# 
# **Study Question:** For the glucose feedback loops diagrammed above, describe at least one physiological source disturbance for each.
# 
# **Study Question:** Describe a situation where you have witnessed positive feedback in an audio or visual system.
# 
# <hr>

# ## Proportional Control

# ### Description
# 
# **Proportional control** adjusts the manipulated variable in proportion to the error between the setpoint and measured process variable.
# 
# $$\begin{align}
# MV_k & = \bar{MV} - K_P(PV_k - SP_k)
# \end{align}$$
# 
# The constant of proportionality, $K_p$, is called the **proportional control gain**. The **error signal** is the difference between the the measured process variable and setpoint,
# 
# $$\begin{align}
# e_k & = PV_k - SP_k
# \end{align}$$
# 
# for which the proportional control becomes
# 
# $$\begin{align}
# MV_k & = \bar{MV} - K_P e_k
# \end{align}$$
# 
# The negative sign results in **negative feedback control**. 
# 
# The constant term $\bar{MV}$ is called the **bias**, **offset**, or **null** value of the manipulated variable. It is an initial estimate of the value of the manipulated variable required to maintain the desired setpoint. The estimate can be determined in several ways:
# 
# * manual adjustment of the manipulated variable followed by a transition to automatic control,
# * solving a process model for the desired steady state,
# * feedforward control,
# * a user provided estimate,
# * set to zero.
# 
# In subsequent notebooks we will see how $\bar{MV}$ is used when building advanced control implementations.

# ### Implementation
# 
# Using the Python `yield` statement, n instance of a proportional controller is created by specifying the gain $K_P$, upper and lower bounds on the manipulated variable, and the offset value $\bar{MV}$.

# In[64]:


def PI(Kp, Ki, t_step, MV_bar=0):
    MV = MV_bar
    e_prev = 0
    while True:
        SP, PV = yield MV
        e = PV - SP
        MV = MV - Kp*(e - e_prev) - t_step*Ki*e
        MV = max(0, min(100, MV))
        e_prev = e


# In[65]:


from tclab import TCLab, clock, Historian, Plotter, setup

TCLab = setup(connected=False, speedup=10)

def SP(t):
    return 40 if t >= 20 else 25

def DV(t):
    return 100 if t >= 200 else 0

t_final = 600
t_step = 2

controller = PI(3, 0.2, t_step)

with TCLab() as lab:

    sources = [["T1", lambda: lab.T1],
               ["SP1", lambda: SP(t)],
               ["E1", lambda: lab.T1 - SP(t)],
               ["Q1", lab.Q1]]
    
    h = Historian(sources)
    p = Plotter(h, t_final, layout=[["T1", "SP1"], ["E1"], ["Q1"]])
    
    lab.P1 = 200
    lab.P2 = 255
    lab.Q1(next(controller))

    # event loop
    for t in clock(t_final, t_step):
        T1 = lab.T1
        U1 = controller.send((SP(t), T1))
        lab.Q1(U1)
        lab.Q2(DV(t))
        p.update(t)


# In[ ]:


lab.


# ### Testing with Disturbance Inputs

# Let's see how proportional control works when applied to the Temperature Control Laboratory. For this simulation we set $\bar{MV} = 0$ and $K_p = 3.0$.

# In[23]:


from tclab import TCLab, clock, Historian, Plotter, setup
TCLab = setup(connected=False, speedup=60)

def SP(t):
    return 40 if t >= 20 else 0

def DV(t):
    return 100 if t>= 220 else 0

controller = P(3.0)

t_final = 600
t_step = 2

with TCLab() as lab:
    sources = [("T1", lambda: lab.T1),
               ("Q1", lab.Q1),
               ("DV", lab.Q2),
               ("SP1", lambda: SP(t))]
    h = Historian(sources)
    layout = [["T1", "SP1"], ["Q1"], ["DV"]]
    p = Plotter(h, t_final, layout=layout)
    
    # initialize manipulated variable
    lab.P1 = 200
    lab.P2 = 200
    lab.Q1(next(controller))

    # event loop
    for t in clock(t_final, t_step):
        T1 = lab.T1
        U1 = controller.send((SP(t), T1))
        lab.Q1(U1)
        lab.Q2(DV(t))
        p.update(t)    


# For systems without significant time delay and with properly chosen parameters, proportional control can achieve a fast response to changes in setpoint. Note, however, the steady state may be different than the desired setpoint, sometimes unacceptably different. This steady-state error a short-coming of purely proportional control.

# <hr>
# 
# **Study Question:** Did the proportional control acheive the setpoint? Did proportional control reject the disturbance? How serious is the problem?
# 
# <hr>

# ### Steady-State Offset
# 
# Proportional-only control provides no assurance the the process variable will eventually acquire the setpoint. To see this, consider the proportional control law
# 
# $$MV_k = \bar{MV} - K_P e_k$$
# 
# in the limit $k\rightarrow\infty$. 
# 
# $$e_{\infty} = \frac{\bar{MV} - MV_{\infty}}{K_P}$$
# 
# The error $e_\infty$ expresses the steady-state difference between a process variable and it setpoint. With proportional control, the only options to reduce steady-state offset are 
# 
# 1. Increase $K_P$. This leads to increasing oscillations and relay-like behavior of the manipulated variable.
# 2. Find a perfect initial estimate for $\bar{MV}$. If we could do this, we wouldn't need feedback control.
# 
# A persistent steady-state offset is most significant shortcoming of proportional-only control.

# <hr>
# 
# **Study Question:** Test the simulation for values of $K_p$ that are twice as large, and half as large as demonstrated above. What do you notice about the steady-state error between the desired setpoint and the measured process variable?
# 
# <hr>

# ## History Time-Out
# 
# 
# Boulton and Watt Steam Engine
# 
# ![](https://upload.wikimedia.org/wikipedia/commons/thumb/f/f2/SteamEngine_Boulton%26Watt_1784.png/1280px-SteamEngine_Boulton%26Watt_1784.png)
# 
# [Governor](https://youtu.be/B01LgS8S5C8?t=42)
# 
# PID Control
# 
# ![](https://owaysonline.com/wp-content/uploads/Block-Diagram-of-Ships-Auto-Pilot.png)
# 
# Pneumatic Control
# 
# ![](https://forumautomation.com/uploads/default/original/2X/8/80d57597e66ff4a5dae1243f91e0bf8c9e1d0dcb.png)
# 
# ![](https://upload.wikimedia.org/wikipedia/commons/thumb/1/16/Pneumatische_regelaar.jpg/640px-Pneumatische_regelaar.jpg)
# 
# ![](https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/Smart_current_loop_positioner.png/1024px-Smart_current_loop_positioner.png?1645118511583)
# 
# ![](https://www.amazon.com/pid-controller/s?k=pid+controller)
# 
# 

# ## Proportional-Integral (PI) Control

# ### Position form
# 
# Given a process variable $PV$ and setpoint $SP$, proportional-integral control is defined by the relation
# 
# \begin{align}
# MV(t) & = \bar{MV} - K_P\left(PV(t) - SP(t)\right) - K_I\int_{-\infty}^t (PV(t') - SP(t'))\,dt'
# \end{align}
# 
# or 
# 
# \begin{align}
# MV(t) & = \bar{MV} - K_P e(t) - K_I\int_{-\infty}^t e(t') \,dt'
# \end{align}
# 
# where
# 
# $$e(t) = PV(t) - SP(t)$$
# 
# where **$K_P$ is the proportional gain** and **$K_I$ is the integral gain**. When implemented in discrete time with time steps of length $h$, the basic rule for proportional-integral control becomes
# 
# \begin{align}
# MV_k & = \bar{MV} - K_P(PV_k - SP_k) - h K_I\sum_{j=0}^{j=k}(PV_j - SP_j)
# \end{align}
# 
# or 
# 
# \begin{align}
# MV_k & = \bar{MV} - K_P e_k - h K_I\sum_{j=0}^{j=k}e_j
# \end{align}
# 
# where
# 
# \begin{align}
# e_k & = PV_k - SP_k
# \end{align}
# 
# This is the so-called **position form** of PI control. The position form specifies the value (or "position") of the manipulated variable stricly in terms of the current and past values of the **error** signal $e_k$. Note the sign convention: A positive error occurs when the process variable is greater than the setpoint. The position form of PI control is rarely used in practice.

# ### Velocity form
# 
# A more common implementation of PI control is done by computing how much the manipulated variable changes at each time step, and incrementing the manipulated variable by that amount. Consecutive values of $MV$ are given by 
# 
# \begin{align}
# MV_{k-1} & = \bar{MV} - K_p e_{k-1} - h K_i \sum_{j=0}^{k-1} e_{j} \\
# MV_{k} & = \bar{MV} - K_p e_{k} - h K_i \sum_{j=0}^{k} e_{j}
# \end{align}
# 
# Taking differences gives a formula for updating the value of $MV$ in response to process measurements or changes in setpoint.
# 
# \begin{align}
# MV_{k} & = MV_{k-1} - K_p(e_{k} - e_{k-1}) - h K_i e_{k}
# \end{align}
# 
# with $MV_0 = \bar{MV}$. Let's see how this works.

# In[60]:


def PI(Kp, Ki, MV_bar=0):
    MV = MV_bar
    e_prev = 0
    while True:
        SP, PV = yield MV
        e = PV - SP
        MV = MV - Kp*(e - e_prev) - t_step*Ki*e
        e_prev = e
        


# In[30]:


from tclab import TCLab, clock, Historian, Plotter, setup
TCLab = setup(connected=False, speedup=60)

def SP(t):
    return 60 if t >= 20 else 0

def DV(t):
    return 100 if t>= 220 else 0

controller = PI(3, 0.2)

t_final = 450
t_step = 2

with TCLab() as lab:
    sources = [("T1", lambda: lab.T1),
               ("Q1", lab.Q1),
               ("DV", lab.Q2),
               ("SP1", lambda: SP(t))]
    h = Historian(sources)
    layout = [["T1", "SP1"], ["Q1"], ["DV"]]
    p = Plotter(h, t_final, layout=layout)
    
    # initialize manipulated variable
    lab.P1 = 200
    lab.P2 = 200
    lab.Q1(next(controller))

    # event loop
    for t in clock(t_final, t_step):
        T1 = lab.T1
        U1 = controller.send((SP(t), T1))
        lab.Q1(U1)
        lab.Q2(DV(t))
        p.update(t)    


# As we can see from this example, an important practical property of proportonal-integral control is **steady-state tracking of the setpoint.** In other words, for a steaady setpoint $\bar{SP}$, at steady-state 
# 
# \begin{align}
# \lim_{k \rightarrow \infty} PV_k = \bar{SP}
# \end{align}
# 
# To see why this is true, start with the velocity form of the proportional-integral controller
# 
# \begin{align}
# MV_{k} & = MV_{k-1} - K_p(e_{k} - e_{k-1}) - h K_i e_{k}
# \end{align}
# 
# At steady-state $MV_{k} = MV_{k-1}$ and $e_{k} = e_{k-1}$ leaving 
# 
# $$h K_i e_{k} = 0 \implies e_{k} = 0 \implies PV_{k} = \bar{SP}$$
# 
# Steady-state tracking is normally important in chemical process applications. For this reason, PI control is, by far, the most commonly encountered control used in the process industries.

# <hr>
# 
# **Study Question:** Repeat the simulation experiments using the Ziegler-Nichols and the Astrom and Murray tuning rules for PI control. Compare the magnitude of the recommended control constants. Compare the resulting performance in response to regard to both setpoint tracking and disturbance rejection. Compare:
# 
# * Maximum overshoot
# * Damping
# * Time to acheive steady-state
# 
# <hr>

# In[ ]:




