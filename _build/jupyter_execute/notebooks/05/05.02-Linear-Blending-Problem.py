#!/usr/bin/env python
# coding: utf-8

# # Linear Blending Problems
# 
# This notebook introduces material blending problems and outlines a multi-step procedure for developing and solving models using Pyomo.

# ## Learning Goals
# 
# 1. Linear Blending problems
# 
#     * Frequently encountered in material blending 
#     
#     * Models generally consist of linear mixing rules and mass/material balances
#     
#     * Decision variables are indexed by a set of raw materials
# 
# 
# 2. Further practice with key elements of modeling for optimization
# 
#     * `pyo.ConcreteModel()` to create a new instancce of an optimization model
#     
#     * `pyo.Set()` to create an index used to index decision variables
#     
#     * `pyo.Var()` to create an optimization **decision variable**
#     
#     * `model.Comstraint()` to decorate (tag) the output of a function as an optimization constraint
#     
#     * `model.Objective()` to decorate (tag) the output of a function as an optimization objective
# 
# 
# 3. Modeling and solving linear blending problems in CVXPY
# 
#     * Step 1. Coding problem data. Nested dictionaries or Pandas dataframes.
#     
#     * Step 2. Create index set. Use .keys() with nested dictionaries, or .index with Pandas dataframes.
#     
#     * Step 3. Create a dictionary of decision variables. Add any pertinent qualifiers or constraints for individual variables such as lower and upper bounds, non-negativity, variable names.
#     
#     * Step 4. Create an expression defining the problem objective.
#     
#     * Step 5. Create a one or more lists of problem constraints.
#     
#     * Step 6. Create the problem object from the objectives and constraints.
#     
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

# ### Consolidating the model into a single function to create and solve for optimal blend
# 
# To enable parametric studies, our first step is to consolidate the model into a function that accepts problem data and reports an optimal solution.

# In[16]:


import numpy as np
import pyomo.environ as pyo
import pandas as pd


def blend_beer(data, V=100, C_lb=0.04):
    
    # create model
    bm = pyo.ConcreteModel('Blending Model')

    # create index set for decision variables
    bm.S = pyo.Set(initialize=data.index)

    # create decision variables
    bm.x = pyo.Var(bm.S, domain=pyo.NonNegativeReals)

    # specify objective
    @bm.Objective(sense=pyo.minimize)
    def cost(bm):
        return sum(bm.x[s] * data.loc[s, "Price"] for s in bm.S)

    # volume constraint
    @bm.Constraint()
    def volume(bm):
        return sum(bm.x[s] for s in bm.S) == V

    # composition constraint
    @bm.Constraint()
    def composition(bm):
        return sum(bm.x[s]*(data.loc[s, "Concentration"] - C_lb) for s in bm.S) >= 0

    # solve model
    solver = pyo.SolverFactory('glpk')
    solver.solve(bm)
    
    # return model for post-processing and display
    return bm


# ### How to use the optimization model

# In[92]:


# specify blending stock data
data = pd.DataFrame([
    ['A', 0.045, 0.32],
    ['B', 0.037, 0.25], ['C', .042, .28],
    ['W', 0.000, 0.05]], 
    columns = ['blending stock', 'Concentration', 'Price']
)
data.set_index('blending stock', inplace=True)
display(data)

# set product requirements
volume = 100
abv = 0.04

# compute optimal solution using optimization model
bm = blend_beer(data, volume, abv)

# extract data from the model
optimal_blend = pd.DataFrame()
optimal_blend.index = [s for s in bm.S]
optimal_blend["amount"] = [bm.x[s]() for s in bm.S]
min_cost = bm.cost()

# display solutoin
print(f"Minimum cost to produce {volume} gallons at ABV={abv} = ${min_cost:5.2f}")
display(optimal_blend)
optimal_blend.plot(y="amount", kind="bar")


# ## Parametric Study
# 
# The following cell uses the optimal blending model to compute the minimum cost and blending stocks to produce 

# In[87]:


print(data)
volume = 100

# gather results for a range of abv values
abv = np.linspace(0, 0.045)

results = pd.DataFrame(columns=["abv", "cost", "A", "B", "W"])
for row, a in enumerate(abv):
    bm = blend_beer(data, volume, a)
    results.loc[row] = [a, bm.cost(), bm.x["A"](), bm.x["B"](), bm.x["W"]()]

results.plot(x="abv", y="cost", ylabel="$ per 100 gallons", grid=True)
results.plot(x="abv", y=["A", "B", "W"], ylabel="gallons", grid=True)


# ## Study Exercises

# ### Exercise 1
# 
# An additional raw blending stock "C" becomes available with an abv of 4.2% at a cost of 28 cents per gallon. How does that change the optimal blend for a product volume of 100 gallons and an abv of 4.0%?

# In[ ]:





# ### Exercise 2
# 
# Having decided to use "C" for the blended product, you later learn only 50 gallons of "C" are available. Modify the solution procedure to allow for limits on the amount of raw maaterial, and investigate the implications for the optimal blend of having only 50 gallons of "C" available, and assuming the amounts of the other components "A", "B", and "W" remain unlimited.

# In[ ]:





# ### Exercise 3
# 
# An opportunity has developed to sell a second product with an abv of 3.8%. The first product is now labeled "X" with abv 4.0% and sells for \\$1.25 per gallon, and the second product is designated "Y" and sells for \\$1.10 per gallon. You've also learned that all of your raw materials are limited to 50 gallons. What should your production plan be to maximize profits?
# 
# 

# In[ ]:




