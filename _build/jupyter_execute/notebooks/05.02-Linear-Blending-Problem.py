#!/usr/bin/env python
# coding: utf-8

# # Linear Blending Problems
# 
# This notebook introduces simple material blending problems, and outlines a multi-step procedure for creating and solving models for these problems using Pyomo.

# ## Learning Goals
# 
# * Linear Blending problems
#     * Frequently encountered in material blending 
#     * Models generally consist of linear mixing rules and mass/material balances
#     * Decision variables are indexed by a set of raw materials
# 
# 
# * Further practice with key elements of modeling for optimization
#     * cvxpy.Variable(): Create instance of an optimization **decision variable**
#     * cvxpy.Minimize()/cvxpy.Maximize(): Create instance of an **optimization objective**
#     * cvxpy.Problem(): Create instance of an optimization problem with objective and **constraints**.
#  
#  
# * Modeling and solving linear blending problems in CVXPY
#     * Step 1. Coding problem data. Nested dictionaries or Pandas dataframes.
#     * Step 2. Create index set. Use .keys() with nested dictionaries, or .index with Pandas dataframes.
#     * Step 3. Create a dictionary of decision variables. Add any pertinent qualifiers or constraints for individual variables such as lower and upper bounds, non-negativity, variable names.
#     * Step 4. Create an expression defining the problem objective.
#     * Step 5. Create a one or more lists of problem constraints.
#     * Step 6. Create the problem object from the objectives and constraints.
#     * Step 7. Solve and display the solution.

# ## Problem Statement (Jenchura, 2017)
# 
# A brewery receives an order for 100 gallons that is at least 4% ABV (alchohol by volume) beer. The brewery has on hand beer A that is 4.5% ABV and costs \\$0.32 per gallon to make, and beer B that is 3.7% ABV and costs \\$0.25 per gallon. Water (W) can also be used as a blending agent at a cost of \\$0.05 per gallon. Find the minimum cost blend of A, B, and W that meets the customer requirements.

# ## Analysis
# 
# Before going futher, carefully read the problem description with the following questions in mind.
# 
# * What are the decision variables?
# * What is the objective?
# * What are the constraints?
# 
# 
# ### Decision variables
# 
# The decision variables for this problem are the amounts of blending stocks "A", "B", and "W" to included in the final batch.  We can define a set of blending stocks $S$, and non-negative decision variables $x_s$ that are indexed by the components in $S$ that denote the amount of $s$ included in the final batch.
# 
# ### Objective
# 
# If we designate the price of blending stock $s \in S$ as $P_s$, the cost is 
# 
# $$
# \begin{align}
# \mbox{cost} & = \sum_{s\in C} x_s P_s
# \end{align}
# $$
# 
# The objective is to minimize cost.
# 
# ### Constraints
# 
# #### Order Volume
# 
# Let $V = 100$ represent the desired volume of product and assume ideal mixing. Then
# 
# $$\begin{align}
# V &  = \sum_{s\in S} x_s
# \end{align}$$
# 
# #### Alcohol by Volume
# 
# Let $C_s$ denote the volume fraction of alcohol in blending stock $s$. Assuming ideal mixing, the total volume of of alchohol in the final product be
# 
# $$C_{total} = \sum_{s\in S} x_s C_s$$
# 
# If $\bar{C}$ denotes the required average concentration, then 
# 
# $$\frac{C_{total}}{V} \geq \bar{C} \qquad \implies \qquad \frac{\sum_{s\in S} x_s C_s}{\sum_{s\in S} x_s} \geq \bar{C}$$
# 
# Which is not linear in the decision variables. If at all possible, linear constraints are much preferred because (1) they enable the use of LP solvers, and (2) then tend to avoid problems that can arise with division by zero and other issues.
# 
# $$\sum_{s\in S} (C_s - \bar{C}) x_s \geq 0$$
# 
# There are other ways to write composition constraints, but this one is preferred because it isolates the product quality parameter, $\bar{C}$, in a single constraint.  This constraint has "one job to do".

# ## Solving optimization problems with Pyomo

# ### Step 1. Coding Problem Data as a Pandas DataFrame
# 
# The first step is to represent the problem data in a generic manner that could be extended to include additional blending components.  Here we use a Pandas dataframe of raw materials, each row representing a unique blending agent, and columns containing attributes of the blending components. This is consistent with "Tidy Data" principles.

# In[62]:


data = pd.DataFrame([
    ['A', 0.045, 0.32],
    ['B', 0.037, 0.25],
    ['W', 0.000, 0.05]], 
    columns = ['blending stock', 'Concentration', 'Price']
)

data.set_index('blending stock', inplace=True)
display(data)


# ### Step 2. Creating a model instance

# In[63]:


import numpy as np
import pyomo.environ as pyo
import pandas as pd

bm = pyo.ConcreteModel('Blending Model')


# ### Step 3. Identifying index sets
# 
# The objectives and constraints encountered in optimization problems often include sums over a set of objects. In the case, we will need to create sums over the set of blending stocks. We will use these index sets to create decision variables and to express the sums that appear in the objective and constraints

# In[65]:


data.index


# In[67]:


bm.S = pyo.Set(initialize=data.index)

for s in bm.S:
    print(s)


# ### Step 4. Create decision variables
# 
# Most real-world applications of optimization technologies involve many decision variables and constraints. It would be impractical to create unique identifiers for literally thousands of variables. For this reason, the `pyo.Var()` and other objects can create indexed sets of variables and constraints. Here is how it is done for the blending problem.

# In[68]:


bm.x = pyo.Var(bm.S, domain=pyo.NonNegativeReals)


# ### Step 4. Objective Function
# 
# If we let subscript $d$ denote a blending d from the set of blending components $C$, and denote the volume of $c$ used in the blend as $x_c$, the cost of the blend is
# 
# $$
# \begin{align}
# \mbox{cost} & = \sum_{s\in S} x_s P_s
# \end{align}
# $$
# 
# where $P_s$ is the price per unit volume of $s$. Using the Python data dictionary defined above, the price $P_s$ is given by `data[s, 'Price']`

# In[73]:


@bm.Objective(sense=pyo.minimize)
def cost(bm):
    return sum(bm.x[s] * data.loc[s, "Price"] for s in bm.S)

bm.cost.pprint()


# ### Step 5. Constraints

# #### Volume Constraint
# 
# The customer requirement is produce a total volume $V$. Assuming ideal solutions, the constraint is given by
# 
# $$\begin{align}
# V &  = \sum_{s\in s} x_s
# \end{align}$$
# 
# where $x_s$ denotes the volume of blending stock $s$ used in the blend.

# In[83]:


V = 100

@bm.Constraint()
def volume(bm):
    return sum(bm.x[s] for s in bm.S) == V

bm.volume.pprint()


# #### Composition Constraint

# In[84]:


C_lb = 0.04

@bm.Constraint()
def composition(bm):
    return sum(bm.x[s]*(data.loc[s, "Concentration"] - C_lb) for s in bm.S) >= 0

bm.composition.pprint()


# ### Step 6. Solve

# In[85]:


bm.pprint()


# In[88]:


solver = pyo.SolverFactory('glpk')
solver.solve(bm, tee=True).write()


# ### Step 7. Display solution
# 
# Following solution, the values of any Pyomo variable, expression, objective, or constraint can be accessed using the associated `value` property.

# In[89]:


bm.pprint()


# In[90]:


print(bm.cost())


# In[97]:


print(f"Minimum cost to produce {V} gallons at greater than ABV={C_lb}: ${bm.cost():5.2f}")


# In[94]:


for s in bm.S:
    print(f"{s}: {bm.x[s]():6.2f} gallons")


# ## Parametric Studies
# 
# An important use of optimization models is to investigate how operations depend on critical parameters. For example, for this blending problem we may be interested in questions like:
# 
# * How does the operating cost change with product alcohol content?
# * What is the cost of producing one more gallon of product?
# * What if the supply of a raw material is constrained?
# * What if we produce two products rather than one?
# * How much would be pay for raw materials with different specifications

# ### Consolidating
# 
# To enable parametric studies, our first step is to consolidate the model into a function that accepts problem data and reports an optimal solution.

# In[15]:





# Demonstration

# In[16]:


# problem data
data = {
    'A': {'abv': 0.045, 'cost': 0.32},
    'B': {'abv': 0.037, 'cost': 0.25},
    'W': {'abv': 0.000, 'cost': 0.05},
}

# product requirement
volume = 100
abv = 0.04

# optimal solution
min_cost, optimal_blend = brew_blend(volume, abv, data)

# display solutoin
print(f"Minimum cost to produce {volume} gallons at ABV={abv} = ${min_cost:5.2f}")
for c in sorted(optimal_blend.keys()):
    print(f"{c}: {optimal_blend[c]:5.2f}")


# The Pandas library has a function to convert dictionaries of data to DataFrames. This is a convenient way to display and visualize the data resulting from a complex optimization problem.

# In[17]:


import pandas as pd

print(optimal_blend)
df = pd.DataFrame.from_dict(optimal_blend, orient="index")
df.plot(kind="bar")


# ### Optimal blend as a function of product specification

# In[18]:


get_ipython().run_line_magic('matplotlib', 'inline')

import numpy as np
import matplotlib.pyplot as plt

data = {
    'A': {'abv': 0.045, 'cost': 0.32},
    'B': {'abv': 0.037, 'cost': 0.25},
    'W': {'abv': 0.000, 'cost': 0.05},
}

# gather results for a range of abv values
abv = np.linspace(0, 0.05)
results = [brew_blend(volume, a, data) for a in abv]

fig, ax = plt.subplots(2, 1, sharex=True)
ax[0].plot(abv, [cost for cost, values in results])
ax[0].set_ylabel("$")
ax[0].grid(True)

for c in sorted(data.keys()):
    ax[1].plot(abv, [values[c] for cost, values in results], label=c)
ax[1].set_xlabel('Blended ABV')
ax[1].set_ylabel('gallons')
ax[1].legend()
ax[1].grid(True)


# <hr>
# 
# **Study Question:** Suppose an additional raw material "C" becomes available with an abv of 4.2% at a cost of 28 cents per gallon. How does that change the optimal blend?
# 
# **Study Question:** Having decided to use "C" for the blended product, you later learn only 50 gallons of "C" are available. Modify the solution procedure to allow for limits on the amount of raw maaterial, and investigate the implications for the optimal blend of having only 50 gallons of "C" available, and assuming the amounts of the other components "A", "B", and "W" remain unlimited.
# 
# **Study Question:** An opportunity has developed to sell a second product with an abv of 3.8%. The first product is now labeled "X" with abv 4.0% and sells for \\$1.25 per gallon, and the second product is designated "Y" and sells for \\$1.10 per gallon. You've also learned that all of your raw materials are limited to 50 gallons. What should your production plan be to maximize profits?
# 
# <hr>

# In[39]:


import numpy as np
import cvxpy as cp

def brew_blend(volume, abv, data):
    
    # create set of components
    components = set(data.keys())
    
    # create variables
    x = {c: cp.Variable(nonneg=True, name=c) for c in components}
    
    # create objective function
    total_cost = sum(x[c]*data[c]['cost'] for c in components)
    
    # create list of constraints
    constraints = [
        volume == sum(x[c] for c in components),
        0 == sum(x[c]*(data[c]['abv'] - abv) for c in components)
    ]
    
    # add volume constraints
    for c in components:
        constraints.append(x[c] <= data[c]['volume'])    
    
    # create and solve problem
    problem = cp.Problem(cp.Minimize(total_cost), constraints)
    problem.solve()
    
    # return results
    min_cost = problem.value
    optimal_blend = {c: x[c].value for c in components}
    return min_cost, optimal_blend


import numpy as np
import matplotlib.pyplot as plt

data = {
    'A': {'abv': 0.045, 'cost': 0.32, 'volume': 50},
    'B': {'abv': 0.037, 'cost': 0.25, 'volume': 50},
    'C': {'abv': 0.042, 'cost': 0.28, 'volume': 50},           # <= add raw material data
    'W': {'abv': 0.000, 'cost': 0.05, 'volume': 50},
}

# gather results for a range of abv values
abv = np.linspace(0.03, 0.05, 200)                         # <= narrow range of plott
results = [brew_blend(volume, a, data) for a in abv]

fig, ax = plt.subplots(2, 1, sharex=True)
ax[0].plot(abv, [cost for cost, values in results])
ax[0].set_ylabel("$")
ax[0].grid(True)

for c in sorted(data.keys()):
    ax[1].plot(abv, [values[c] for cost, values in results], label=c)
ax[1].set_xlabel('Blended ABV')
ax[1].set_ylabel('gallons')
ax[1].legend()
ax[1].grid(True)


# In[52]:


import numpy as np
import cvxpy as cp

def brew_blend(volume, abv, data):
    
    # create set of components
    components = set(data.keys())
    products = set(product_specs.keys())
    
    # create variables
    x = {(c, p): cp.Variable(nonneg=True, name=f"{c},{p}") for c in components for p in products}
    y = {p: cp.Variable(nonneg=True, name=p) for p in products}
    
    
    # create objective function
    total_cost = sum(x[c,p]*data[c]['cost'] for c in components for p in products)
    revenue = sum(y[p*product_specs[])
    
    print(total_cost)
    
    # create list of constraints
    constraints = [
        volume == sum(x[c] for c in components),
        0 == sum(x[c]*(data[c]['abv'] - abv) for c in components)
    ]
    
    # add volume constraints
    for c in components:
        constraints.append(x[c] <= data[c]['volume'])    
    
    # create and solve problem
    problem = cp.Problem(cp.Minimize(total_cost), constraints)
    problem.solve()
    
    # return results
    min_cost = problem.value
    optimal_blend = {c: x[c].value for c in components}
    return min_cost, optimal_blend


import numpy as np
import matplotlib.pyplot as plt

product_specs = {
    'X': {'abv': 0.040, 'price': 1.25},
    'Y': {'abv': 0.038, 'price': 1.10}
}

data = {
    'A': {'abv': 0.045, 'cost': 0.32, 'volume': 50},
    'B': {'abv': 0.037, 'cost': 0.25, 'volume': 50},
    'C': {'abv': 0.042, 'cost': 0.28, 'volume': 50},           # <= add raw material data
    'W': {'abv': 0.000, 'cost': 0.05, 'volume': 50},
}

# gather results for a range of abv values
abv = np.linspace(0.03, 0.05, 200)                         # <= narrow range of plott
results = [brew_blend(volume, a, data) for a in abv]

fig, ax = plt.subplots(2, 1, sharex=True)
ax[0].plot(abv, [cost for cost, values in results])
ax[0].set_ylabel("$")
ax[0].grid(True)

for c in sorted(data.keys()):
    ax[1].plot(abv, [values[c] for cost, values in results], label=c)
ax[1].set_xlabel('Blended ABV')
ax[1].set_ylabel('gallons')
ax[1].legend()
ax[1].grid(True)


# In[ ]:




