#!/usr/bin/env python
# coding: utf-8

# # Gasoline Blending
# 
# ** THIS WILL BE REVISED IN CLASS 3/22 (spill over to 3/24) **
# 
# The task is to determine the most profitable blend of gasoline products from given set of refinery streams.
# 
# ![](https://www.researchgate.net/profile/Jeffrey-Kelly-2/publication/260356707/figure/fig4/AS:267835926642706@1440868469487/Typical-gasoline-blending-system-Color-figure-can-be-viewed-in-the-online-issue-which_W640.jpg)
# 

# In[22]:


import sys
if "google.colab" in sys.modules:
    get_ipython().system('wget "https://raw.githubusercontent.com/ndcbe/CBE60499/main/notebooks/helper.py"')
    import helper
    helper.install_idaes()
    helper.install_ipopt()
    helper.install_glpk()
    helper.install_cbc()


# In[2]:


import pandas as pd
import pyomo.environ as pyo


# ## Gasoline Product Specifications
# 
# The gasoline products include regular and premium gasoline. In addition to the current price, the specifications include
# 
# * **octane** the minimum road octane number.  Road octane is the computed as the average of the Research Octane Number (RON) and Motor Octane Number (MON).
# * **Reid Vapor Pressure** Upper and lower limits are specified for the Reid vapor pressure. The Reid vapor pressure is the absolute pressure exerted by the liquid at 100°F.
# * **benzene** the maximum volume percentage of benzene allowed in the final product. Benzene helps to increase octane rating, but is also a treacherous environmental contaminant.
# 

# In[3]:


products = pd.DataFrame({
    'Regular'        : {'price': 2.75, 'octane': 87, 'RVPmin': 0.0, 'RVPmax': 15.0, 'benzene': 1.1},
    'Premium'        : {'price': 2.85, 'octane': 91, 'RVPmin': 0.0, 'RVPmax': 15.0, 'benzene': 1.1},
}).T

display(products)


# ## Stream Specifications
# 
# A typical refinery produces many intermediate streams that can be incorporated in a blended gasoline product. Here we provide data on seven streams that include:
# 
# * **Butane** n-butane is a C4 product stream produced from the light components of the crude being processed by the refinery. Butane is a highly volatile of gasoline.
# * **LSR** Light straight run naptha is a 90°F to 190°F cut from the crude distillation column primarily consisting of straight chain C5-C6 hydrocarbons.
# * **Isomerate** is the result of isomerizing LSR to produce branched molecules that results in higher octane number.
# * **Reformate** is result of catalytic reforming heavy straight run napthenes to produce a high octane blending component, as well by-product hydrogen used elsewhere in the refinery for hydro-treating.
# * **Reformate LB** is a is a low benzene variant of reformate.
# * **FCC Naphta** is the product of a fluidized catalytic cracking unit designed to produce gasoline blending components from long chain hydrocarbons present in the crude oil being processed by the refinery.
# * **Alkylate** The alkylation unit reacts iso-butane with low-molecular weight alkenes to produce a high octane blending component for gasoline.
# 
# The stream specifications include research octane and motor octane numbers for each blending component, the Reid vapor pressure, the benzene content, cost, and availability (in gallons per day). The road octane number is computed as the average of the RON and MON.

# In[39]:


streams = pd.DataFrame({
    'Butane'       : {'RON': 93.0, 'MON': 92.0, 'RVP': 54.0, 'benzene': 0.00, 'cost': 0.85, 'avail': 30000},
    'LSR'          : {'RON': 78.0, 'MON': 76.0, 'RVP': 11.2, 'benzene': 0.73, 'cost': 2.05, 'avail': 35001},
    'Isomerate'    : {'RON': 83.0, 'MON': 81.1, 'RVP': 13.5, 'benzene': 0.00, 'cost': 2.20, 'avail': 0},
    'Reformate'    : {'RON':100.0, 'MON': 88.2, 'RVP':  3.2, 'benzene': 1.85, 'cost': 2.80, 'avail': 60000},
    'Reformate LB' : {'RON': 93.7, 'MON': 84.0, 'RVP':  2.8, 'benzene': 0.12, 'cost': 2.75, 'avail': 0},
    'FCC Naphtha'  : {'RON': 92.1, 'MON': 77.1, 'RVP':  1.4, 'benzene': 1.06, 'cost': 2.60, 'avail': 70000},
    'Alkylate'     : {'RON': 97.3, 'MON': 95.9, 'RVP':  4.6, 'benzene': 0.00, 'cost': 2.75, 'avail': 40000},
}).T

streams['octane'] = (streams['RON'] + streams['MON'])/2

display(streams)


# ## Questions we want to Answer
# 
# 1. What is the maximum profit possible using the current product specifications and available streams?
# 
# 2. What are the marginal values of each blending stream? That is, how much would you be willing to pay for each additional gallon of the blending streams?
# 
# 3. A marketing team says there is an opportunity to create a mid-grade gasoline product with a road octane number of 89 that would sell for $2.82/gallon, and with all other specifications the same. Would an additional profit be created? What at what price point does the mid-grade product enhance profits?
# 
# 4. New environmental regulations have reduced the allowable benzene levels from 1.1 vol% to 0.62 vol%, and the maximum Reid vapor pressure from 15.0 to 9.0. What is the impact on profits?

# ## Blending Model
# 
# This simplified blending model assumes the product attributes can be computed as linear volume weighted averages of the component properties. Let the decision variable $x_{s,p} \geq 0$ be the volume, in gallons, of blending component $s \in S$ used in the final product $p \in P$.
# 
# ### Objective
# 
# The objective is maximize profit, which is the difference between product revenue and stream costs. 
# 
# \begin{align}
# \mbox{profit} & = \max_{x_{s,p}}\left( \sum_{p\in P} \text{Price}_p \sum_{s\in S} x_{s,p}
# - \sum_{s\in S} \text{Cost}_s \sum_{p\in P} x_{s,p}\right) \\
# & = \max_{x_{s,p}}\left(\sum_{p\in P}\sum_{s\in S}x_{s,p}(\text{Price}_p - \text{Cost}_s)\right)
# \end{align}
# 
# ### Raw Materials
# 
# The first constraints in any blending problem are normally the limits on available raw materials. Letting $\text{
# 
# The blending constraint for octane can be written as 
# 
# \begin{align}
# \frac{\sum_{s \in S} x_{s,p} \mbox{Octane}_s}{\sum_{s \in S} x_{s,p}} & \geq \mbox{Octane}_p & \forall p \in P
# \end{align}
# 
# where $\mbox{Octane}_s$ refers to the octane rating of stream $s$, whereas $\mbox{Octane}_p$ refers to the octane rating of product $p$. Multiplying through by the denominator, and consolidating terms gives
# 
# \begin{align}
# \sum_{s \in S} x_{s,p}\left(\mbox{Octane}_s - \mbox{Octane}_p\right) & \geq  0 & \forall p \in P
# \end{align}
# 
# The same assumptions and development apply to the benzene constraint
# 
# \begin{align}
# \sum_{s \in S} x_{s,p}\left(\mbox{Benzene}_s - \mbox{Benzene}_p\right) & \leq  0 & \forall p \in P
# \end{align}
# 
# Reid vapor pressure, however, follows a somewhat different mixing rule.  For the Reid vapor pressure we have
# 
# \begin{align}
# \sum_{s \in S} x_{s,p}\left(\mbox{RVP}_s^{1.25} - \mbox{RVP}_{min,p}^{1.25}\right) & \geq  0 & \forall p \in P \\
# \sum_{s \in S} x_{s,p}\left(\mbox{RVP}_s^{1.25} - \mbox{RVP}_{max,p}^{1.25}\right) & \leq  0 & \forall p \in P
# \end{align}
# 
# This model is implemented in the following cell.

# In[44]:


import pyomo.environ as pyo

def gas_blending(products, streams):

    m = pyo.ConcreteModel("Gasoline Blending")
    
    m.PRODUCTS = pyo.Set(initialize=products.index)
    m.STREAMS = pyo.Set(initialize=streams.index)
    
    m.x = pyo.Var(m.STREAMS, m.PRODUCTS, domain=pyo.NonNegativeReals)
    
    @m.Objective(sense=pyo.maximize)
    def profit(m):
        return sum(sum(m.x[s, p]*(products.loc[p, 'price'] - streams.loc[s, 'cost']) for s in m.STREAMS) for p in m.PRODUCTS)
    
    @m.Constraint(m.STREAMS)
    def raw_material_available(m, s):
        return sum(m.x[s, p] for p in m.PRODUCTS) <= streams.loc[s, 'avail']
    
    @m.Constraint(m.PRODUCTS)
    def octane(m, p):
        return sum(m.x[s, p]*(streams.loc[s, 'octane'] - products.loc[p, 'octane']) for s in m.STREAMS) >= 0
    
    @m.Constraint(m.PRODUCTS)
    def benzene(m, p):
        return sum(m.x[s, p]*(streams.loc[s, 'benzene'] - products.loc[p, 'benzene']) for s in m.STREAMS) <= 0
   
    @m.Constraint(m.PRODUCTS)
    def min_reid_vapor_pressure(m, p):
        return sum(m.x[s, p]*(streams.loc[s, 'RVP']**1.25 - products.loc[p, 'RVPmin']**1.25) for s in m.STREAMS) >= 0
 
    @m.Constraint(m.PRODUCTS)
    def max_reid_vapor_pressure(m, p):
        return sum(m.x[s, p]*(streams.loc[s, 'RVP']**1.25 - products.loc[p, 'RVPmax']**1.25) for s in m.STREAMS) <= 0

    solver = pyo.SolverFactory('cbc')
    solver.solve(m)
    
    return m

m = gas_blending(products, streams)

    
soln = pd.DataFrame({s: {p: m.x[s,p]() for p in m.PRODUCTS} for s in m.STREAMS}).T
print("profit = ", m.profit())
display(soln)


# In[162]:


# create decision variables
S = streams.keys()
P = products.keys()
m.x = pyomo.Var(S,P, domain=pyomo.NonNegativeReals)
    
# objective
revenue = sum(sum(m.x[s,p]*products[p]['price'] for s in S) for p in P)
cost = sum(sum(m.x[s,p]*streams[s]['cost'] for s in S) for p in P)
m.profit = pyomo.Objective(expr = revenue - cost, sense=pyomo.maximize)

# constraints
m.cons = pyomo.ConstraintList()
for s in S:
    m.cons.add(sum(m.x[s,p] for p in P) <= streams[s]['avail'])
for p in P:
    m.cons.add(sum(m.x[s,p]*(feeds[s]['octane'] -    products[p]['octane'])       for s in S) >= 0)
    m.cons.add(sum(m.x[s,p]*(feeds[s]['RVP']**1.25 - products[p]['RVPmin']**1.25) for s in S) >= 0)
    m.cons.add(sum(m.x[s,p]*(feeds[s]['RVP']**1.25 - products[p]['RVPmax']**1.25) for s in S) <= 0)
    m.cons.add(sum(m.x[s,p]*(feeds[s]['benzene'] -   products[p]['benzene'])      for s in S) <= 0)

# solve
solver = pyomo.SolverFactory('glpk')
solver.solve(m)

# display results
vol = sum(m.x[s,p]() for s in S for p in P)
print("Total Volume =", round(vol, 1), "gallons.")
print("Total Profit =", round(m.profit(), 1), "dollars.")
print("Profit =", round(100*m.profit()/vol,1), "cents per gallon.")


# ## Display Results

# ### Results for each Stream

# In[152]:


stream_results = pd.DataFrame()
for s in S:
    for p in P:
        stream_results.loc[s,p] = round(m.x[s,p](), 1)
    stream_results.loc[s,'Total'] = round(sum(m.x[s,p]() for p in P), 1)
    stream_results.loc[s,'Available'] = streams[s]['avail']
    
stream_results['Unused (Slack)'] = stream_results['Available'] - stream_results['Total']
print(stream_results)


# ### Results for each Product

# In[153]:


product_results = pd.DataFrame()
for p in P:
    product_results.loc[p,'Volume'] = round(sum(m.x[s,p]() for s in S), 1)
    product_results.loc[p,'octane'] = round(sum(m.x[s,p]()*streams[s]['octane'] for s in S)
                                            /product_results.loc[p,'Volume'], 1)
    product_results.loc[p,'RVP'] = round((sum(m.x[s,p]()*streams[s]['RVP']**1.25 for s in S)
                                            /product_results.loc[p,'Volume'])**0.8, 1)
    product_results.loc[p,'benzene'] = round(sum(m.x[s,p]()*streams[s]['benzene'] for s in S)
                                            /product_results.loc[p,'Volume'], 1)
print(product_results)


# ## Exercise 1.
# 
# The marketing team says there is an opportunity to create a mid-grade gasoline product with a road octane number of 89 that would sell for $2.82/gallon, and with all other specifications the same. Could an additional profit be created?
# 
# Create a new cell (or cells) below to compute a solution to this exercise.

# In[181]:


products = {
    'Regular'        : {'price': 2.75, 'octane': 87, 'RVPmin': 0.0, 'RVPmax': 15.0, 'benzene': 1.1},
    'Midgrade'       : {'price': 2.82, 'octane': 89, 'RVPmin': 0.0, 'RVPmax': 15.0, 'benzene': 1.1},
    'Premium'        : {'price': 2.85, 'octane': 91, 'RVPmin': 0.0, 'RVPmax': 15.0, 'benzene': 1.1},
}

print(pd.DataFrame.from_dict(products).T)

streams = {
    'Butane'       : {'RON': 93.0, 'MON': 92.0, 'RVP': 54.0, 'benzene': 0.00, 'cost': 0.85, 'avail': 30000},
    'LSR'          : {'RON': 78.0, 'MON': 76.0, 'RVP': 11.2, 'benzene': 0.73, 'cost': 2.05, 'avail': 35000},
    'Isomerate'    : {'RON': 83.0, 'MON': 81.1, 'RVP': 13.5, 'benzene': 0.00, 'cost': 2.20, 'avail': 0},
    'Reformate'    : {'RON':100.0, 'MON': 88.2, 'RVP':  3.2, 'benzene': 1.85, 'cost': 2.80, 'avail': 60000},
    'Reformate LB' : {'RON': 93.7, 'MON': 84.0, 'RVP':  2.8, 'benzene': 0.12, 'cost': 2.75, 'avail': 0},
    'FCC Naphtha'  : {'RON': 92.1, 'MON': 77.1, 'RVP':  1.4, 'benzene': 1.06, 'cost': 2.60, 'avail': 70000},
    'Alkylate'     : {'RON': 97.3, 'MON': 95.9, 'RVP':  4.6, 'benzene': 0.00, 'cost': 2.75, 'avail': 40000},
}

# calculate road octane as (R+M)/2
for s in streams.keys():
    streams[s]['octane'] = (streams[s]['RON'] + streams[s]['MON'])/2
    
# display feed information
print(pd.DataFrame.from_dict(streams).T)

# create model
m = pyomo.ConcreteModel()

# create decision variables
S = streams.keys()
P = products.keys()
m.x = pyomo.Var(S,P, domain=pyomo.NonNegativeReals)
    
# objective
revenue = sum(sum(m.x[s,p]*products[p]['price'] for s in S) for p in P)
cost = sum(sum(m.x[s,p]*streams[s]['cost'] for s in S) for p in P)
m.profit = pyomo.Objective(expr = revenue - cost, sense=pyomo.maximize)

# constraints
m.cons = pyomo.ConstraintList()
for s in S:
    m.cons.add(sum(m.x[s,p] for p in P) <= streams[s]['avail'])
for p in P:
    m.cons.add(sum(m.x[s,p]*(feeds[s]['octane'] -    products[p]['octane'])       for s in S) >= 0)
    m.cons.add(sum(m.x[s,p]*(feeds[s]['RVP']**1.25 - products[p]['RVPmin']**1.25) for s in S) >= 0)
    m.cons.add(sum(m.x[s,p]*(feeds[s]['RVP']**1.25 - products[p]['RVPmax']**1.25) for s in S) <= 0)
    m.cons.add(sum(m.x[s,p]*(feeds[s]['benzene'] -   products[p]['benzene'])      for s in S) <= 0)

# solve
solver = pyomo.SolverFactory('glpk')
solver.solve(m)
print("Profit = $", round(m.profit(),2))

stream_results = pd.DataFrame()
for s in S:
    for p in P:
        stream_results.loc[s,p] = round(m.x[s,p](), 1)
    stream_results.loc[s,'Total'] = round(sum(m.x[s,p]() for p in P), 1)
    stream_results.loc[s,'Available'] = streams[s]['avail']
    
stream_results['Unused (Slack)'] = stream_results['Available'] - stream_results['Total']
print(stream_results)

product_results = pd.DataFrame()
for p in P:
    product_results.loc[p,'Volume'] = round(sum(m.x[s,p]() for s in S), 1)
    product_results.loc[p,'octane'] = round(sum(m.x[s,p]()*streams[s]['octane'] for s in S)
                                            /product_results.loc[p,'Volume'], 1)
    product_results.loc[p,'RVP'] = round((sum(m.x[s,p]()*streams[s]['RVP']**1.25 for s in S)
                                            /product_results.loc[p,'Volume'])**0.8, 1)
    product_results.loc[p,'benzene'] = round(sum(m.x[s,p]()*streams[s]['benzene'] for s in S)
                                            /product_results.loc[p,'Volume'], 1)
print(product_results)

vol = sum(m.x[s,p]() for s in S for p in P)
print("Total Profit =", round(m.profit(), 1), "dollars.")
print("Total Volume =", round(vol, 1), "gallons.")
print("Profit =", round(100*m.profit()/vol,1), "cents per gallon.")


# ## Exercise 2.
# 
# New environmental regulations have reduced the allowable benzene levels from 1.1 vol% to 0.62 vol%, and the maximum Reid vapor pressure from 15.0 to 9.0.
# 
# Compared to the base case (i.e., without the midgrade product), how does this change profitability? 

# In[180]:


products = {
    'Regular'        : {'price': 2.75, 'octane': 87, 'RVPmin': 0.0, 'RVPmax': 9.0, 'benzene': 0.62},
    'Premium'        : {'price': 2.85, 'octane': 91, 'RVPmin': 0.0, 'RVPmax': 9.0, 'benzene': 0.62},
}

print(pd.DataFrame.from_dict(products).T)

streams = {
    'Butane'       : {'RON': 93.0, 'MON': 92.0, 'RVP': 54.0, 'benzene': 0.00, 'cost': 0.85, 'avail': 30000},
    'LSR'          : {'RON': 78.0, 'MON': 76.0, 'RVP': 11.2, 'benzene': 0.73, 'cost': 2.05, 'avail': 35000},
    'Isomerate'    : {'RON': 83.0, 'MON': 81.1, 'RVP': 13.5, 'benzene': 0.00, 'cost': 2.20, 'avail': 0},
    'Reformate'    : {'RON':100.0, 'MON': 88.2, 'RVP':  3.2, 'benzene': 1.85, 'cost': 2.80, 'avail': 60000},
    'Reformate LB' : {'RON': 93.7, 'MON': 84.0, 'RVP':  2.8, 'benzene': 0.12, 'cost': 2.75, 'avail': 0},
    'FCC Naphtha'  : {'RON': 92.1, 'MON': 77.1, 'RVP':  1.4, 'benzene': 1.06, 'cost': 2.60, 'avail': 70000},
    'Alkylate'     : {'RON': 97.3, 'MON': 95.9, 'RVP':  4.6, 'benzene': 0.00, 'cost': 2.75, 'avail': 40000},
}

# calculate road octane as (R+M)/2
for s in streams.keys():
    streams[s]['octane'] = (streams[s]['RON'] + streams[s]['MON'])/2
    
# display feed information
print(pd.DataFrame.from_dict(streams).T)

# create model
m = pyomo.ConcreteModel()

# create decision variables
S = streams.keys()
P = products.keys()
m.x = pyomo.Var(S,P, domain=pyomo.NonNegativeReals)
    
# objective
revenue = sum(sum(m.x[s,p]*products[p]['price'] for s in S) for p in P)
cost = sum(sum(m.x[s,p]*streams[s]['cost'] for s in S) for p in P)
m.profit = pyomo.Objective(expr = revenue - cost, sense=pyomo.maximize)

# constraints
m.cons = pyomo.ConstraintList()
for s in S:
    m.cons.add(sum(m.x[s,p] for p in P) <= streams[s]['avail'])
for p in P:
    m.cons.add(sum(m.x[s,p]*(feeds[s]['octane'] -    products[p]['octane'])       for s in S) >= 0)
    m.cons.add(sum(m.x[s,p]*(feeds[s]['RVP']**1.25 - products[p]['RVPmin']**1.25) for s in S) >= 0)
    m.cons.add(sum(m.x[s,p]*(feeds[s]['RVP']**1.25 - products[p]['RVPmax']**1.25) for s in S) <= 0)
    m.cons.add(sum(m.x[s,p]*(feeds[s]['benzene'] -   products[p]['benzene'])      for s in S) <= 0)

# solve
solver = pyomo.SolverFactory('glpk')
solver.solve(m)
print("Profit = $", round(m.profit(),2))

stream_results = pd.DataFrame()
for s in S:
    for p in P:
        stream_results.loc[s,p] = round(m.x[s,p](), 1)
    stream_results.loc[s,'Total'] = round(sum(m.x[s,p]() for p in P), 1)
    stream_results.loc[s,'Available'] = streams[s]['avail']
    
stream_results['Unused (Slack)'] = stream_results['Available'] - stream_results['Total']
print(stream_results)

product_results = pd.DataFrame()
for p in P:
    product_results.loc[p,'Volume'] = round(sum(m.x[s,p]() for s in S), 1)
    product_results.loc[p,'octane'] = round(sum(m.x[s,p]()*streams[s]['octane'] for s in S)
                                            /product_results.loc[p,'Volume'], 1)
    product_results.loc[p,'RVP'] = round((sum(m.x[s,p]()*streams[s]['RVP']**1.25 for s in S)
                                            /product_results.loc[p,'Volume'])**0.8, 1)
    product_results.loc[p,'benzene'] = round(sum(m.x[s,p]()*streams[s]['benzene'] for s in S)
                                            /product_results.loc[p,'Volume'], 1)
print(product_results)

vol = sum(m.x[s,p]() for s in S for p in P)
print("Total Profit =", round(m.profit(), 1), "dollars.")
print("Total Volume =", round(vol, 1), "gallons.")
print("Profit =", round(100*m.profit()/vol,1), "cents per gallon.")


# ## Exercise 3.
# 
# Given the new product specifications in Exercise 2, let's consider using different refinery streams. In place of Reformate, the refinery could produce Reformate LB. (That is, one or the other of the two streams could be 60000 gallons per day, but not both).  Same for LSR and Reformate.  How should the refinery be operated to maximize profitability?

# In[184]:


products = {
    'Regular'        : {'price': 2.75, 'octane': 87, 'RVPmin': 0.0, 'RVPmax': 9.0, 'benzene': 0.62},
    'Premium'        : {'price': 2.85, 'octane': 91, 'RVPmin': 0.0, 'RVPmax': 9.0, 'benzene': 0.62},
}

print(pd.DataFrame.from_dict(products).T)

streams = {
    'Butane'       : {'RON': 93.0, 'MON': 92.0, 'RVP': 54.0, 'benzene': 0.00, 'cost': 0.85, 'avail': 30000},
    'LSR'          : {'RON': 78.0, 'MON': 76.0, 'RVP': 11.2, 'benzene': 0.73, 'cost': 2.05, 'avail': 35000},
    'Isomerate'    : {'RON': 83.0, 'MON': 81.1, 'RVP': 13.5, 'benzene': 0.00, 'cost': 2.20, 'avail': 0},
    'Reformate'    : {'RON':100.0, 'MON': 88.2, 'RVP':  3.2, 'benzene': 1.85, 'cost': 2.80, 'avail': 0},
    'Reformate LB' : {'RON': 93.7, 'MON': 84.0, 'RVP':  2.8, 'benzene': 0.12, 'cost': 2.75, 'avail': 60000},
    'FCC Naphtha'  : {'RON': 92.1, 'MON': 77.1, 'RVP':  1.4, 'benzene': 1.06, 'cost': 2.60, 'avail': 70000},
    'Alkylate'     : {'RON': 97.3, 'MON': 95.9, 'RVP':  4.6, 'benzene': 0.00, 'cost': 2.75, 'avail': 40000},
}

# calculate road octane as (R+M)/2
for s in streams.keys():
    streams[s]['octane'] = (streams[s]['RON'] + streams[s]['MON'])/2
    
# display feed information
print(pd.DataFrame.from_dict(streams).T)

# create model
m = pyomo.ConcreteModel()

# create decision variables
S = streams.keys()
P = products.keys()
m.x = pyomo.Var(S,P, domain=pyomo.NonNegativeReals)
    
# objective
revenue = sum(sum(m.x[s,p]*products[p]['price'] for s in S) for p in P)
cost = sum(sum(m.x[s,p]*streams[s]['cost'] for s in S) for p in P)
m.profit = pyomo.Objective(expr = revenue - cost, sense=pyomo.maximize)

# constraints
m.cons = pyomo.ConstraintList()
for s in S:
    m.cons.add(sum(m.x[s,p] for p in P) <= streams[s]['avail'])
for p in P:
    m.cons.add(sum(m.x[s,p]*(feeds[s]['octane'] -    products[p]['octane'])       for s in S) >= 0)
    m.cons.add(sum(m.x[s,p]*(feeds[s]['RVP']**1.25 - products[p]['RVPmin']**1.25) for s in S) >= 0)
    m.cons.add(sum(m.x[s,p]*(feeds[s]['RVP']**1.25 - products[p]['RVPmax']**1.25) for s in S) <= 0)
    m.cons.add(sum(m.x[s,p]*(feeds[s]['benzene'] -   products[p]['benzene'])      for s in S) <= 0)
    
# solve
solver = pyomo.SolverFactory('glpk')
solver.solve(m)
print("Profit = $", round(m.profit(),2))

stream_results = pd.DataFrame()
for s in S:
    for p in P:
        stream_results.loc[s,p] = round(m.x[s,p](), 1)
    stream_results.loc[s,'Total'] = round(sum(m.x[s,p]() for p in P), 1)
    stream_results.loc[s,'Available'] = streams[s]['avail']
    
stream_results['Unused (Slack)'] = stream_results['Available'] - stream_results['Total']
print(stream_results)

product_results = pd.DataFrame()
for p in P:
    product_results.loc[p,'Volume'] = round(sum(m.x[s,p]() for s in S), 1)
    product_results.loc[p,'octane'] = round(sum(m.x[s,p]()*streams[s]['octane'] for s in S)
                                            /product_results.loc[p,'Volume'], 1)
    product_results.loc[p,'RVP'] = round((sum(m.x[s,p]()*streams[s]['RVP']**1.25 for s in S)
                                            /product_results.loc[p,'Volume'])**0.8, 1)
    product_results.loc[p,'benzene'] = round(sum(m.x[s,p]()*streams[s]['benzene'] for s in S)
                                            /product_results.loc[p,'Volume'], 1)
print(product_results)

vol = sum(m.x[s,p]() for s in S for p in P)
print("Total Profit =", round(m.profit(), 1), "dollars.")
print("Total Volume =", round(vol, 1), "gallons.")
print("Profit =", round(100*m.profit()/vol,1), "cents per gallon.")


# In[ ]:




