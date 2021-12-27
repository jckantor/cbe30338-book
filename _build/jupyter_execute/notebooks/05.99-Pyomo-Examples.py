#!/usr/bin/env python
# coding: utf-8

# <!--NOTEBOOK_HEADER-->
# *This notebook contains course material from [CBE30338](https://jckantor.github.io/CBE30338)
# by Jeffrey Kantor (jeff at nd.edu); the content is available [on Github](https://github.com/jckantor/CBE30338.git).
# The text is released under the [CC-BY-NC-ND-4.0 license](https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode),
# and code is released under the [MIT license](https://opensource.org/licenses/MIT).*

# <!--NAVIGATION-->
# < [Gasoline Blending](http://nbviewer.jupyter.org/github/jckantor/CBE30338/blob/master/notebooks/06.08-Gasoline-Blending.ipynb) | [Contents](toc.ipynb) | [Simulation and Optimal Control](http://nbviewer.jupyter.org/github/jckantor/CBE30338/blob/master/notebooks/07.00-Simulation-and-Optimal-Control.ipynb) ><p><a href="https://colab.research.google.com/github/jckantor/CBE30338/blob/master/notebooks/06.99-Pyomo-Examples.ipynb"><img align="left" src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open in Colab" title="Open in Google Colaboratory"></a><p><a href="https://raw.githubusercontent.com/jckantor/CBE30338/master/notebooks/06.99-Pyomo-Examples.ipynb"><img align="left" src="https://img.shields.io/badge/Github-Download-blue.svg" alt="Download" title="Download Notebook"></a>

# # Pyomo Examples

# ## Pyomo Model
# 
# A Pyomo implementation of this blending model is shown in the next cell. The model is contained within a Python function so that it can be more easily reused for additional calculations, or eventually for use by the process operator.
# 
# Note that the pyomo library has been imported with the prefix `pyomo`. This is good programming practive to avoid namespace collisions with problem data.

# In[222]:


import pyomo.environ as pyomo

vol = 100
abv = 0.040

def brew_blend(vol, abv, data):
    
    C = data.keys()
    
    model = pyomo.ConcreteModel()
    
    model.x = pyomo.Var(C, domain=pyomo.NonNegativeReals)
    
    model.cost = pyomo.Objective(expr = sum(model.x[c]*data[c]['cost'] for c in C))
    
    model.vol = pyomo.Constraint(expr = vol == sum(model.x[c] for c in C))
    model.abv = pyomo.Constraint(expr = 0 == sum(model.x[c]*(data[c]['abv'] - abv) for c in C))

    solver = pyomo.SolverFactory('glpk')
    solver.solve(model)

    print('Optimal Blend')
    for c in data.keys():
        print('  ', c, ':', model.x[c](), 'gallons')
    print()
    print('Volume = ', model.vol(), 'gallons')
    print('Cost = $', model.cost())
    
brew_blend(vol, abv, data)


# In[ ]:





# ## Example: Nonlinear Optimization  of Series Reaction in a Continuous Stirred Tank Reactor

# In[1]:


from pyomo.environ import *

V = 40     # liters
kA = 0.5   # 1/min
kB = 0.1   # l/min
CAf = 2.0  # moles/liter

# create a model instance
model = ConcreteModel()

# create x and y variables in the model
model.q = Var()

# add a model objective
model.objective = Objective(expr = model.q*V*kA*CAf/(model.q + V*kB)/(model.q + V*kA), sense=maximize)

# compute a solution using ipopt for nonlinear optimization
results = SolverFactory('ipopt').solve(model)
model.pprint()


# print solutions
qmax = model.q()
CBmax = model.objective()
print('\nFlowrate at maximum CB = ', qmax, 'liters per minute.')
print('\nMaximum CB =', CBmax, 'moles per liter.')
print('\nProductivity = ', qmax*CBmax, 'moles per minute.')


# ## Example 19.3: Linear Programming Refinery

# In[2]:


import pandas as pd

PRODUCTS = ['Gasoline', 'Kerosine', 'Fuel Oil', 'Residual']
FEEDS = ['Crude 1', 'Crude 2']

products = pd.DataFrame(index=PRODUCTS)
products['Price'] = [72, 48, 42, 20]
products['Max Production'] = [24000, 2000, 6000, 100000]

crudes = pd.DataFrame(index=FEEDS)
crudes['Processing Cost'] = [1.00, 2.00]
crudes['Feed Costs'] = [48, 30]

yields = pd.DataFrame(index=PRODUCTS)
yields['Crude 1'] = [0.80, 0.05, 0.10, 0.05]
yields['Crude 2'] = [0.44, 0.10, 0.36, 0.10]

print('\n', products)
print('\n', crudes)
print('\n', yields)


# In[3]:


price = {}
price['Gasoline'] = 72
price['Kerosine'] = 48
price


# In[4]:


products.loc['Gasoline','Price']


# In[5]:


# model formulation
model = ConcreteModel()

# variables
model.x = Var(FEEDS,    domain=NonNegativeReals)
model.y = Var(PRODUCTS, domain=NonNegativeReals)

# objective
income = sum(products.ix[p, 'Price'] * model.y[p] for p in PRODUCTS)
raw_materials_cost = sum(crudes.ix[f,'Feed Costs'] * model.x[f] for f in FEEDS)


# In[6]:


processing_cost = sum(processing_costs[f] * model.x[f] for f in FEEDS)
profit = income - raw_materials_cost - processing_cost
model.objective = Objective(expr = profit, sense=maximize)

# constraints
model.constraints = ConstraintList()
for p in PRODUCTS:
    model.constraints.add(0 <= model.y[p] <= max_production[p])
for p in PRODUCTS:
    model.constraints.add(model.y[p] == sum(model.x[f] * product_yield[(f,p)] for f in FEEDS))

solver = SolverFactory('glpk')
solver.solve(model)
model.pprint()


# In[7]:


from pyomo.environ import *
import numpy as np

# problem data
FEEDS = ['Crude #1', 'Crude #2']
PRODUCTS = ['Gasoline', 'Kerosine', 'Fuel Oil', 'Residual']

# feed costs
feed_costs = {'Crude #1': 48,
              'Crude #2': 30}

# processing costs
processing_costs = {'Crude #1': 1.00,
                    'Crude #2': 2.00}

# yield data
product_yield = 
product_yield = {('Crude #1', 'Gasoline'): 0.80,
                 ('Crude #1', 'Kerosine'): 0.05,
                 ('Crude #1', 'Fuel Oil'): 0.10,
                 ('Crude #1', 'Residual'): 0.05,
                 ('Crude #2', 'Gasoline'): 0.44,
                 ('Crude #2', 'Kerosine'): 0.10,
                 ('Crude #2', 'Fuel Oil'): 0.36,
                 ('Crude #2', 'Residual'): 0.10}

# product sales prices
sales_price = {'Gasoline': 72,
               'Kerosine': 48,
               'Fuel Oil': 42,
               'Residual': 20}

# production limits
max_production = {'Gasoline': 24000,
                  'Kerosine': 2000,
                  'Fuel Oil': 6000,
                  'Residual': 100000}

# model formulation
model = ConcreteModel()

# variables
model.x = Var(FEEDS, domain=NonNegativeReals)
model.y = Var(PRODUCTS, domain=NonNegativeReals)

# objective
income = sum(sales_price[p] * model.y[p] for p in PRODUCTS)
raw_materials_cost = sum(feed_costs[f] * model.x[f] for f in FEEDS)
processing_cost = sum(processing_costs[f] * model.x[f] for f in FEEDS)

profit = income - raw_materials_cost - processing_cost
model.objective = Objective(expr = profit, sense=maximize)

# constraints
model.constraints = ConstraintList()
for p in PRODUCTS:
    model.constraints.add(0 <= model.y[p] <= max_production[p])
for p in PRODUCTS:
    model.constraints.add(model.y[p] == sum(model.x[f] * product_yield[(f,p)] for f in FEEDS))

solver = SolverFactory('glpk')
solver.solve(model)
model.pprint()


# In[6]:


profit()


# In[7]:


income()


# In[8]:


raw_materials_cost()


# In[9]:


processing_cost()


# ## Example: Making Change
# 
# One of the important modeling features of Pyomo is the ability to index variables and constraints. The

# In[8]:


from pyomo.environ import *

def make_change(amount, coins):
    model = ConcreteModel()
    model.x = Var(coins.keys(), domain=NonNegativeIntegers)
    model.total = Objective(expr = sum(model.x[c] for c in coins.keys()), sense=minimize)
    model.amount = Constraint(expr = sum(model.x[c]*coins[c] for c in coins.keys()) == amount)
    SolverFactory('glpk').solve(model)
    return {c: int(model.x[c]()) for c in coins.keys()} 
            
# problem data
coins = {
    'penny': 1,
    'nickel': 5,
    'dime': 10,
    'quarter': 25
}
            
make_change(1034, coins)


# ## Example: Linear Production Model with Constraints with Duals

# In[3]:


from pyomo.environ import *
model = ConcreteModel()

# for access to dual solution for constraints
model.dual = Suffix(direction=Suffix.IMPORT)

# declare decision variables
model.x = Var(domain=NonNegativeReals)
model.y = Var(domain=NonNegativeReals)

# declare objective
model.profit = Objective(expr = 40*model.x + 30*model.y, sense = maximize)

# declare constraints
model.demand = Constraint(expr = model.x <= 40)
model.laborA = Constraint(expr = model.x + model.y <= 80)
model.laborB = Constraint(expr = 2*model.x + model.y <= 100)

# solve
SolverFactory('glpk').solve(model).write()


# In[ ]:





# In[4]:


str = "   {0:7.2f} {1:7.2f} {2:7.2f} {3:7.2f}"

print("Constraint  value  lslack  uslack    dual")
for c in [model.demand, model.laborA, model.laborB]:
    print(c, str.format(c(), c.lslack(), c.uslack(), model.dual[c]))


# <!--NAVIGATION-->
# < [Gasoline Blending](http://nbviewer.jupyter.org/github/jckantor/CBE30338/blob/master/notebooks/06.08-Gasoline-Blending.ipynb) | [Contents](toc.ipynb) | [Simulation and Optimal Control](http://nbviewer.jupyter.org/github/jckantor/CBE30338/blob/master/notebooks/07.00-Simulation-and-Optimal-Control.ipynb) ><p><a href="https://colab.research.google.com/github/jckantor/CBE30338/blob/master/notebooks/06.99-Pyomo-Examples.ipynb"><img align="left" src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open in Colab" title="Open in Google Colaboratory"></a><p><a href="https://raw.githubusercontent.com/jckantor/CBE30338/master/notebooks/06.99-Pyomo-Examples.ipynb"><img align="left" src="https://img.shields.io/badge/Github-Download-blue.svg" alt="Download" title="Download Notebook"></a>
