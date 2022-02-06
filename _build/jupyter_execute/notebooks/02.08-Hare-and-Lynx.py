#!/usr/bin/env python
# coding: utf-8

# # Hare and Lynx Population Dynamics
# 

# ## Summary
# 
# This notebook provides an introduction to nonlinear dynamics using a well-known model for the preditor-prey interaction of Snowshoe Hare and Canadian Lynx. Topics include limit cycles, the existence of multiple steady states, and simple phase plane analysis using nullclines. This notebook can be displayed as a slide presentation.

# ## Introduction
# 
# [Snowshoe hare](https://en.wikipedia.org/wiki/Snowshoe_hare) (*Lepus americanus*) are the primary food for the [Canadian lynx](https://en.wikipedia.org/wiki/Canada_lynx) (*Lynx canadensis*) in the Northern boreal forests of North America. When hare are abundant, Lynx will eat hare about two every three days almost to the complete exclusion of other foods. As a consequence, the population dynamics of the two species are closely linked. 
# 
# | Canadian Lynx | Snowshoe Hare |
# | :---: | :---: |
# |![Canadian lynx by Keith Williams](https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Canadian_lynx_by_Keith_Williams.jpg/256px-Canadian_lynx_by_Keith_Williams.jpg)| ![Snowshoe Hare, Shirleys Bay](https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Snowshoe_Hare%2C_Shirleys_Bay.jpg/256px-Snowshoe_Hare%2C_Shirleys_Bay.jpg) |
# |kdee64 (Keith Williams) [CC BY 2.0](https://creativecommons.org/licenses/by/2.0), [via Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Canadian_lynx_by_Keith_Williams.jpg) | D. Gordon E. Robertson [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0), [via Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Snowshoe_Hare,_Shirleys_Bay.jpg)|
# 
# It has been known for over a century that the populations of the two species vary dramatically in cycles of 8 to 11 year duration. This chart, for example, shows pelt-trading data taken from the Hudson's Bay Company (from MacLulich, 1937.  See important notes on this data in [Stenseth, 1997](http://www.pnas.org/content/94/10/5147.full))
# 
# ![https://commons.wikimedia.org/wiki/File:Figure_45_06_01.jpg](https://upload.wikimedia.org/wikipedia/commons/1/16/Figure_45_06_01.jpg)
# 
# (CNX OpenStax [CC BY 4.0](https://creativecommons.org/licenses/by/4.0), [via Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Figure_45_06_01.jpg))
# 
# The actual cause of the cycling is still a matter of scientific inquiry. Hypotheses include the inherent instability of the preditor-prey dynamics, the dynamics of a more complex food web, and the role of climate (see [Zhang, 2007](http://www.int-res.com/articles/feature/c034p083.pdf)). The discussion in this notebook addresses the preditor-prey dynamics.

# ## Historical Data
# 
# A digitized version of the historical data is available from [D. R. Hundley at Whitman College](http://people.whitman.edu/~hundledr/courses/M250F03/M250.html). The following cell reads the data from the url, imports it into a pandas dataframe, and creates a plot. 

# In[5]:


import pandas as pd

url = 'http://people.whitman.edu/~hundledr/courses/M250F03/LynxHare.txt'
df = pd.read_csv(url, delim_whitespace=True, header=None)
df.columns = ["Year", "Hare", "Lynx"]
df.plot(x="Year", figsize=(10, 6), grid=True)


# ## Population Dynamics

# ### Model Equations
# 
# The model equatons describe the time rate of change of the population densities of hare ($H$) and lynx ($L$). Each is the difference between the birth and death rate. The death rate of hare is coupled to the population density of lynx. The birth rate of lynx is a simple multiple of the death rate of hare.
# 
# \begin{align*}
# \frac{dH}{dt} & = \underbrace{rH\left(1-\frac{H}{k}\right)}_{Hare Birth Rate}-\underbrace{\frac{aHL}{c+H}}_{Hare Death Rate}\\
# \frac{dL}{dt} & = \underbrace{a\frac{bHL}{c+H}}_{Lynx Birth Rate}-\underbrace{dL}_{Lynx Death Rate}
# \end{align*}

# ### Parameter Values
# 
# | Parameter | Symbol | Value |
# | - | :----: | :---: |
# | Lynx/Hare Predation Rate | $a$ | 3.2 |
# | Lynx/Hare Conversion | $b$ | 0.6 |
# | Lynx/Hare Michaelis Constant| $c$ | 50 |
# | Lynx Death Rate | $d$ | 0.56 |
# | Hare Carrying Capacity| $k$ | 125 |
# | Hare Reproduction Rate | $r$ | 1.6 |

# ## Simulation using the scipy.integrate.solve_ivp()

# ### Step 1. Initialization
# 
# The `SciPy` library includes functions for integrating differential equations. Of these, the function `odeint` provides an easy-to-use general purpose algorithm well suited to this type of problem.

# In[6]:


import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp


# ### Step 2. Establish Parameter Values
# 
# Set global default values for the parameters

# In[7]:


# default parameter values
a = 3.2
b = 0.6
c = 50
d = 0.56
k = 125
r = 1.6


# ### Step 3.  Write function for the RHS of the Differential Equations
# 
# `deriv` is a function that returns a two element list containting values for the derivatives of $H$ and $L$. The first argument is a two element list with values of $H$ and $L$, followed by the current time $t$.
# 
# \begin{align*}
# \frac{dH}{dt} & = r H \left(1-\frac{H}{k}\right) - \frac{a H L}{c + H} \\
# \frac{dL}{dt} & = b\frac{a H L}{c + H} - dL
# \end{align*}

# In[8]:


# differential equations
def deriv(t, y):
    H, L = y
    dH =  r*H*(1 - H/k) - a*H*L/(c + H)
    dL = b*a*H*L/(c + H) - d*L
    return [dH, dL]


# ### Step 4. Choose Time Grid, Initial Conditions, and Integrate

# In[25]:


# perform simulation
t = np.linspace(0, 70, 500)                               # time grid
IC = [20, 20]                                             # H, L initial conditions 
soln = solve_ivp(deriv, [min(t), max(t)], IC, t_eval=t)   # compute solution
df = pd.DataFrame({"Year": soln.t, 
                   "Hare": soln.y[0, :],
                   "Lynx": soln.y[1, :]})                 # create dataframe


# ### Step 5. Visualize and Analyze the Solution
# 
# For this choice of parameters and initial conditions, the Hare/Lynx population exhibits sustained oscillations.

# In[29]:


df.plot(x="Year", grid=True, title="Hare/Lynx Population Dynamics")


# #### Phase Plane

# In[30]:


df.plot(x="Hare", y="Lynx", grid=True)


# ## Nullclines
# 
# Nullclines are the points in the phase plane where the derivatives are equal to zero. 
# 
# The nullclines for hare are where 
# 
# $$\frac{d\bar{H}}{dt} = 0 \implies \begin{cases}
# \begin{align*}
# \bar{H} & = 0 \\
# \\
# \bar{L} & = \frac{r}{a}\left(c + \bar{H}\right)\left(1 - \frac{\bar{H}}{k}\right)
# \end{align*}
# \end{cases}$$

# The nullclines for Lynx are where 
# 
# $$\frac{dL}{dt} = 0 \implies \begin{cases}
# \begin{align*}
# \bar{L} & = 0 \\
# \\
# \bar{H} & = \frac{c d}{a b - d}
# \end{align*}
# \end{cases}$$

# For convenience, we create a function to plots the nullclines and steady states that occur where the nullclines intersect.

# In[61]:


def plot_nullclines():
    # nullcline dH/dt = 0
    Hp = np.linspace(0,k)
    Lp = (r/a)*(c + Hp)*(1 - Hp/k)
    plt.plot(Hp, Lp, 'b')
    plt.ylim(0, 130)
    plt.xlim(0, 150)
    
    # nullcline dL/dt = 0
    Hd = c*d/(a*b - d)
    plt.plot([Hd, Hd], plt.ylim(), 'r', lw=3)

    # additional nullclines
    plt.plot([0, 0], plt.ylim(), 'b', lw=3)
    plt.plot(plt.xlim(), [0, 0], 'r', lw=3)

    # steady states
    Hss = c*d/(a*b - d)
    Lss = r*(1 - Hss/k)*(c + Hss)/a
    plt.plot([0, k, Hss], [0, 0, Lss], 'r.', ms=20)

    plt.xlabel('Hare')
    plt.ylabel('Lynx')
    plt.legend(['dH/dt = 0','dL/dt = 0'])  
    
    plt.grid(True)


# Here's a plot of the nullclines for the default parameter values. The steady states correspond to 
# 
# * No Hare, and no Lynx.
# * Hare population at the carry capacity of the environment, and no Lynx
# * Coexistence of Hare and Lynx.

# In[62]:


plot_nullclines()


# Visualization of the nullclines give us some insight into how the Hare and Lynx populations depend on the model parameters. Here we look at how the nullclines depend on the Hare/Lynx predation rate $a$.

# In[51]:


from ipywidgets import interact

def sim(aslider=3.2):
    global a
    a = aslider
    plotNullclines()
    
interact(sim,aslider=(1.25, 4, 0.01))


# ## Interactive Simulation

# ### Visualization Function
# 
# The visualization function for this example accepts a list of time values, values of $H$ and $L$, and model parameters. The model parameters are needed to plot nullclines and steady states on the phase plane.

# In[80]:


# visualization
def hare_lynx_plot(t, H, L):
    # time axis
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))
    ax[0].plot(t, H, label="Hare")
    ax[0].plot(t, L, label="Lynx")
    ax[0].set_xlabel('Time [years]')
    ax[0].set_ylabel('Population Density')
    ax[0].set_ylim(0, 130)
    ax[0].grid(True)

    # phase plane
    ax[1].plot(H ,L)
    ax[1].set_xlim(0, 150)
    ax[1].set_ylim(0, 130)
    plot_nullclines()


# ### Simulation Function
# 
# An additional function is created to encapsulate the entire process of solving the model and displaying the solution. The function takes arguments specifing the initial values of $H$ and $L$, and a value of the parameter $a$.  These argument 

# In[81]:


# default parameter values
a = 3.2
b = 0.6
c = 50
d = 0.56
k = 125
r = 1.6

# perform simulation
t = np.linspace(0,70,500)

def lynx_hare(H=20, L=20, aslider=3.2):
    IC = [H, L]
    global a
    a = aslider
    soln = solve_ivp(deriv, [min(t), max(t)], IC, t_eval=t)
    hare_lynx_plot(soln.t, soln.y[0, :], soln.y[1, :])


# Use the `aslider` to adjust values of the Hare/Lynx interaction.  Can you indentify stable and unstable steady states?

# In[82]:


from ipywidgets import interact
interact(lynx_hare, H = (0,80,1), L =(0,80,1), aslider=(1.25,4.0,0.01));


# ## Stability of a Steady State

# ### 1. Unstable Focus 
# 
# Any displacement from an unstable focus leads to a trajectory that spirals away from the steady state. 

# In[83]:


lynx_hare(H=20, L=20, aslider=4)


# ### 2. Stable Focus 
# 
# Small displacements from a stable focus results in trajectories that spiral back towards the steady state.

# In[84]:


lynx_hare(H=20, L=20, aslider=1.9)


# ### 3. Stable and Unstable Nodes
# 
# Displacements from a steady state either move towards (stable) or away from (unstable) nodes without the spiral structure of a focus.

# In[85]:


lynx_hare(H=20, L=20, aslider=1.4)


# ## Summary
# 
# Hope you enjoyed this brief introduction to the modeling of a small food web. This is a fascinating field with many important and unanswered questions. Recent examples in the research literature are [here](http://journals.plos.org/plosone/article?id=10.1371/journal.pone.0108243) and [here](http://science.sciencemag.org/content/320/5876/658). 
# 
# What you should learn from this notebook:
# 
# * How to simulate small systems of nonlinear ODEs.
# * How to plot trajectories in a phase plane.
# * How to plot the nullclines of two differential equations with constant parameters.
# * Solve systems for multiple steady states.
# * Recognize limit cycles, steady-states, stable and unstable foci, stable and unstable nodes.

# ## Suggested Exercise
# 
# Explore the impact of the parameter $a$ on the nature of the solution. $a$ is proporational to the success of the Lynx hunting the Hare.  What happens when the value is low?  high?  Can you see the transitions from conditions when the Lynx done't survive, the emergence of a stable coexistence steady-state, and finally the emergence of a stable limit cycle?

# In[ ]:




