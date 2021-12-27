#!/usr/bin/env python
# coding: utf-8

# # One Compartment Pharmacokinetics

# ## Learning Goals
# 
# The notebook introduces a single, linear, first-order differential equation in the general form
# 
# $$\frac{dx}{dt} = a x + b u$$
# 
# as mathematical model to describe the dynamic response of a system to a changing input. 
# 
# In any particular application, the **state variable** $x$ corresponds to a process variable such as temperature, pressure, concentration, or position. The **input variable** $u(t)$ corresponds to a changing input such as heater power, flowrate, or valve position. This notebook uses this equation to describe a one-compartment model for a pharmacokinetics in the which the state is the concentration of an antimicrobrial, and the input is a rate of intraveneous administration.
# 
# This notebook demonstrates features of this model that can be used in a wide range of process applications:
# 
# * Simulate response from a known initial condition.
# * Simulate response to a changinig input.
# 

# ## Pharamacokinetics
# 
# Pharmacokinetics is a branch of pharmacology that studies the fate of chemical species in living organisms. The diverse range of applications includes the administration of drugs and anesthesia in humans. This notebook introduces a one compartment model for pharmacokinetics and shows how it can be used to determine strategies for the intravenous administration of an antimicrobial.

# ### One-Compartment Model
# 
# For the purposes of drug administration, for a one-compartment model of the human body is assumed to consist of a single compartment of a constant volume $V$ containing all the plasma of the body. The plasma is assumed to be sufficiently well mixed that any drug is uniformly distributed with concentration $C(t)$. The drug enters the plasma by direct injection into the plasma at rate $u(t)$. The drug leaves the body as a component of the plasma where $Q$ is the constant plasma clearance rate.
# 
# ![](./figures/PK-one-compartment.png)
# 
# A generic mass balance for a single species is given by
# 
# $$\fbox{Rate of Accumulation} = \fbox{Inflow} - \fbox{Outflow} + \fbox{Production by reaction} - \fbox{Consumption by reaction}$$
# 
# Assuming the drug is neither produced or consumed by reaction in the body, this generic mass balance can be translated to differential equation
# 
# $$\begin{align*}
# \underbrace{\fbox{Rate of Accumulation}}_{V \frac{dC}{dt}} & = \underbrace{\fbox{Inflow}}_{u(t)} - \underbrace{\fbox{Outflow}}_{Q C} + \underbrace{\fbox{Production by reaction}}_0 - \underbrace{\fbox{Consumption by reaction}}_0
# \end{align*}$$
# 
# or, summarizing,
# 
# $$V \frac{dC}{dt} = u(t) - Q C(t)$$
# 
# This model is characterized by two parameters, the plasma volume $V$ and the clearance rate $Q$.

# ### Antimicrobials
# 
# Let's consider the administration of an antimicrobial to a patient. Concentration $C(t)$ refers to the concentration of the antibiotic in blood plasma in units of [mg/L or $\mu$g/mL]. There are two concentration levels of interest in the medical use of an antimicrobrial:
# 
# **Minimum Inhibitory Concentration (MIC)** The minimum concentration of the antibiotic that prevents visible growth of a particular microorganism after overnight incubation. This is generally not enough to kill the microorganism, only enough to prevent further growth.
# 
# **Minimum Bactricidal Concentration (MBC)** The lowest concentration of the antimicrobrial that prevents the growth of the microorganism after subculture to antimicrobrial-free media. MBC is generally the concentration needed "kill" the microorganism.
# 
# Extended exposure to an antimicrobrial at levels below MBC leads to [antimicrobrial resistance](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4378521/).

# ### What questions can we ask and answer with this model?
# 
# There are multiple reasons to create mathematical models. In research and development, for example, a mathematical model forms a testable hypothesis of one's understanding of a system. The model guides the design of experiments to either validate or falsify the assumptions incorporated in the model.  
# 
# In the present context of control systems, a model is used to answer operating questions. In pharmacokinetics, for example, the operational questions might include:
# 
# * What values for the parameters $V$ and $Q$ provide accurate predictions of system response?
# * How long will it take to clear the antimicrobial from the body?
# * What rate of antimicrobial addition is required to achieve the minimum bactricidal concentration?
# * If doses are administered periodically, how large should each dose be, and how frequently should the doses be administered?
# 
# Questions like these can be answered through simulation, regression to experimental data, and mathematical analysis. We'll explore several of these techniques below.
# 
# * Simulation
#     * Known initial condition
#     * Time dependent input
# * Steady state analysis
# * Alternative model formulations
#     * State space model
#     * Gain and Time Constant

# ## Simulation

# ### Simulation from a Known Initial Condition

# #### Problem Statement 
# 
# Assume the minimum inhibitory concentration (MIC) of a particular organism to a particular antimicrobial is 5 mg/liter, and the minimum bactricidal concentration (MBC) is 8 mg/liter. Further assume the plasma volume $V$ is 4 liters with a clearance rate $Q$ of 0.5 liters/hour. 
# 
# An initial intravenous antimicrobial dose of 64 mg in 4 liters of plasm results in a plasma concentration $C_{initial}$ of 16 mg/liter.  How long will the concentration stay above MBC?  Above MIC?

# #### Step 1. Import libraries
# 
# For this first simulation we compute the response of the one compartment model due starting with an initial condition $C_{initial}$, and assuming input $u(t) = 0$. We will use the [`solve_ivp`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html) function for solving differential equations from the `scipy.integrate` library.
# 
# The first steps to a solution are:
# 
# 1. Initialize the plotting system.
# 2. Import the `numpy` library for basic mathematical functions.
# 3. Import the `matplotlib.pyplot` library for plotting.
# 4. Import the any needed mathematical functions or libraries.

# In[1]:


get_ipython().run_line_magic('matplotlib', 'inline')
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp


# #### Step 2. Enter Parameter Values

# In[2]:


V = 4           # liters
Q = 0.5         # liters/hour
MIC = 5         # mg/liter
MBC = 8         # mg/liter

C_initial = 16  # mg/liter


# #### Step 3. Write the differential equation in standard form
# 
# The most commonly solvers for systems of differential equations require a function evaluating the right hand sides of the differential equations when written in a standard form
# 
# $$\frac{dC}{dt} = \frac{1}{V}u(t) - \frac{Q}{V}C$$
# 
# Here we write two functions. One function returns values of the input $u(t)$ for a specified point in time, the second returns values of the right hand side as a function of time and state.

# In[3]:


def u(t):
    return 0

def deriv(t, C):
    return u(t)/V - (Q/V)*C


# #### Step 4. Solution and Visualization

# In[11]:


# specify time span and evaluation points
t_span = [0, 24]
t_eval = np.linspace(0, 24, 50)

# initial conditions
IC = [C_initial]

# add events
def cross_mbc(t, y):
    return y[0] - MBC
cross_mbc.direction = -1.0

def cross_mic(t, y):
    return MIC-y[0]
cross_mic.terminal = True

# compute solution
soln = solve_ivp(deriv, t_span, IC, t_eval=t_eval, events=[cross_mbc, cross_mic])

# display solution
print(soln)


# The decision on how to display or visualize a solution is problem dependent. Here we create a simple function to visualize the solution and relevant problem specifications. 

# In[12]:


def plotConcentration(soln):
    fig, ax = plt.subplots(1, 1)
    ax.plot(soln.t, soln.y[0])
    ax.set_xlim(0, max(soln.t))
    ax.plot(ax.get_xlim(), [MIC, MIC], 'g--', ax.get_xlim(), [MBC, MBC], 'r--')
    ax.legend(['Antibiotic Concentration','MIC','MBC'])
    ax.set_xlabel('Time [hrs]')
    ax.set_ylabel('Concentration [mg/liter]')
    ax.set_title('One Compartment Model with Known Initial Condition');
    
plotConcentration(soln)

# save solution to a file for reuse in documents and reports
plt.savefig('./figures/Pharmaockinetics1.png')


# #### Step 5. Analysis of the Results
# 
# Let's compare our results to a typical experimental result. 
# 
# | | |
# | :-: | :-: |
# |![](./figures/Pharmaockinetics1.png)|![](figures/nihms-475924-f0001.jpg)|
# 
# We see that that the assumption of a fixed initial condition is questionable. Can we fix this?
# 
# [Levison, Matthew E., and Julie H. Levison. “Pharmacokinetics and Pharmacodynamics of Antibacterial Agents.” Infectious disease clinics of North America 23.4 (2009): 791–vii. PMC. Web. 8 May 2017.](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3675903/)

# ### Example 2: Improving Simulation using Time-Dependent Input
# 
# For the next simulation we will assume the dosing takes place over a short period of time $\delta t$. To obtain a total dose $U_{dose}$ in a time period $\delta t$, the mass flow rate rate must be
# 
# $$u(t) = 
# \begin{cases}
# U/ \delta t \qquad \mbox{for } 0 \leq t \leq \delta t \\
# 0 \qquad \mbox{for } t \geq \delta t
# \end{cases}
# $$
# 
# Before doing a simulation, we will write a Python function for $u(t)$. 

# In[6]:


# parameter values
dt = 1.5         # length hours
Udose = 64       # mg

# function defintion
def u(t):
    if t <= 0:
        return 0
    elif t <= dt:
        return Udose/dt
    else:
        return 0


# This code cell demonstrates the use of a list comprehension to apply a function to each value in a list.

# In[7]:


# visualization
t = np.linspace(0, 24, 1000)              # create a list of time steps
y = np.array([u(tau) for tau in t])       # list comprehension

fig, ax = plt.subplots(1, 1)
ax.plot(t, y)
ax.set_xlabel('Time [hrs]')
ax.set_ylabel('Administration Rate [mg/hr]')
ax.set_title('Dosing function u(t) for of total dose {0} mg'.format(Udose))


# Simulation

# In[8]:


# specify time span and evaluation points
t_span = [0, 24]
t_eval = np.linspace(0, 24, 50)

# initial conditions
C_initial = 0
IC = [C_initial]

# compute solution
soln = solve_ivp(deriv, t_span, IC, t_eval=t_eval)

# display solution
plotConcentration(soln)
plt.savefig('./figures/Pharmaockinetics2.png')


# #### Analysis of the Results
# 
# Let's compare our results to a typical experimental result. 
# 
# | | |
# | :-: | :-: |
# |![](./figures/Pharmaockinetics2.png)|![](./figures/nihms-475924-f0001.jpg)|
# 
# While it isn't perfect, this is a closer facsimile of actual physiological response.
# 
# [Levison, Matthew E., and Julie H. Levison. “Pharmacokinetics and Pharmacodynamics of Antibacterial Agents.” Infectious disease clinics of North America 23.4 (2009): 791–vii. PMC. Web. 8 May 2017.](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3675903/)

# ### Example 2: Periodic Dosng
# 
# The minimum inhibitory concentration (MIC) of a particular organism to a particular antibiotic is 5 mg/liter, the minimum bactricidal concentration (MBC) is 8 mg/liter. Assume the plasma volume $V$ is 4 liters with a clearance rate $Q$ of 0.5 liters/hour. 
# 
# Design an antibiotic therapy to keep the plasma concentration above the MIC level for a period of 96 hours. 

# #### Solution
# 
# We consider the case of repetitive dosing where a new dose is administered every $t_{dose}$ hours. A simple Python "trick" for this calculation is the `%` operator which returns the remainder following division. This is a useful tool worth remembering whenever you need to functions that repeat in time.

# In[9]:


# parameter values
dt = 2           # length of administration for a single dose
tdose = 8        # time between doses
Udose = 42       # mg

# function defintion
def u(t):
    if t <= 0:
        return 0
    elif t % tdose <= dt:
        return Udose/dt
    else:
        return 0


# In[10]:


# visualization
t = np.linspace(0, 96, 1000)              # create a list of time steps
y = np.array([u(tau) for tau in t])       # list comprehension

fig, ax = plt.subplots(1, 1)
ax.plot(t, y)
ax.set_xlabel('Time [hrs]')
ax.set_ylabel('Administration Rate [mg/hr]')
ax.set_title('Dosing function u(t) for of total dose {0} mg'.format(Udose))


# The dosing function $u(t)$ is now applied to the simulation of drug concentration in the blood plasma. A fourth argument is added to `odeint(deriv, Cinitial, t, tcrit=t)` indicating that special care must be used for every time step. This is needed in order to get a high fidelity simulation that accounts for the rapidly varying values of $u(t)$.

# In[11]:


# specify time span and evaluation points
t_span = [0, 96]
t_eval = np.linspace(0, 96, 1000)

# initial conditions
C_initial = 0
IC = [C_initial]

# compute solution
soln = solve_ivp(deriv, t_span, IC, t_eval=t_eval)

# display solution
plotConcentration(soln)
plt.savefig('./figures/Pharmaockinetics3.png')

print(soln.t_events)


# This looks like a unevem. The problem here is that the solver may be using time steps that are larger than the dosing interval, and missing important changes in the input. The fix is to specify the `max_step` option for the solver. As a rule of thumb, your simulations should always specify a `max_step` shorter than the minimum feature in the input sequence. In this case, we will specify a `max_step` of 0.1 hr which is short enough to not miss a change in the input.

# In[13]:


# specify time span and evaluation points
t_span = [0, 96]
t_eval = np.linspace(0, 96, 1000)

# initial conditions
C_initial = 0
IC = [C_initial]

# compute solution
soln = solve_ivp(deriv, t_span, IC, t_eval=t_eval, max_step=0.1)

# display solution
plotConcentration(soln)
plt.savefig('./figures/Pharmaockinetics4.png')

print(soln.t_events)


# ## Assignment 2

# ### Exercise 1
# 
# The purpose of the dosing regime is to maintain the plasma concentration above the MBC level for at least 96 hours. Assuming that each dose is 64 mg, modify the simulation and find a value of $t_{dose}$ that satisfies the MBC objective for a 96 hour period.  Show a plot concentration versus time, and include Python code to compute the total amount of antibiotic administered for the whole treatment.

# In[ ]:





# ### Exercise 2
# 
# Consider a continous antibiotic injection at a constant rate designed to maintain the plasma concentration at minimum bactricidal level. Your solution should proceed in three steps:
# 
# 1. First, by hand, set up and solve the steady state equation to find the desired constant dosage rate. 
# 2. Modify the Python function for $u(t)$ to simulate the desired flowrate.
# 3. Verify your result by repeating the above simulation using your function for $u(t)$. 

# In[ ]:




