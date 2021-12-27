#!/usr/bin/env python
# coding: utf-8

# # Homework Assignment 4
# 
# Homework assigment 4 is intended to develop your skills in creating linear programming models. The lecture notes (notebook 5.2) will provide with a starting point for the following exercises. The problem data has been changed to provide a more meaningful example for sensitivity analysis.
# 
# 
# You have been placed in charge of a metals reuse operation. A collection of raw materials are available with key parameters given in the following table.
# 
# | material | % carbon (C) | % copper (Cu) | % manganese (Mn) | amount (kg) | cost (\$/kg) | type |
# | :---: | :---: | :---: | :---: | :---: | :---: | :---
# | A | 2.5 | 0.0 | 1.3 | 4000 | 1.20 | iron alloy
# | B | 3.0 | 0.0 | 0.8 | 3000 | 1.50 | iron alloy
# | C | 0.0 | 0.3 | 0.0 | 6000 | 0.90 | iron alloy
# | D | 0.0 | 90.0 | 0.0 | 5000 | 1.30 | copper alloy
# | E | 0.0 | 96.0 | 4.0 | 2000 | 1.45 | copper alloy
# | F | 0.0 | 0.4 | 1.2 | 3000 | 1.20 | aluminum alloy
# | G | 0.0 | 0.6 | 0.0 | 2500 | 1.00 | aluminum alloy
# 
# A customer has requested 5000 kg of mix satisfying these  specifications:
# 
# | Component | min % | max % |
# | :---: | :---: | :---: |
# | C | 2.0 | 3.0 |
# | Cu | 0.4 | 0.6 |
# | Mn | 1.2 | 1.65 |
# 
# For convenience, the raw material data has been organized as a nested dictionaries.

# In[1]:


data = {
    "A": {"C": 2.5, "Cu": 0.0, "Mn": 1.3, "amount": 4000, "cost": 1.20},
    "B": {"C": 3.0, "Cu": 0.0, "Mn": 0.8, "amount": 3000, "cost": 1.50},
    "C": {"C": 0.0, "Cu": 0.3, "Mn": 0.0, "amount": 6000, "cost": 0.90},
    "D": {"C": 0.0, "Cu": 90.0, "Mn": 0.0, "amount": 5000, "cost": 1.30},
    "E": {"C": 0.0, "Cu": 96.0, "Mn": 4.0, "amount": 2000, "cost": 1.45},
    "F": {"C": 0.0, "Cu": 0.4, "Mn": 1.2, "amount": 3000, "cost": 1.20},
    "G": {"C": 0.0, "Cu": 0.6, "Mn": 0.0, "amount": 2500, "cost": 1.00},
}


# ## Exercise 1. Getting Started
# 
# 
# 

# Considering just the constraint on carbon content, adapt the `brew_blend` function from notebook 5.2 to find a minimum cost blend raw materials that yield 5000 kg of product with a carbon content between 2.0 and 3.0%. For this first exercise you can ignore the bounds on the available amount of each raw material.
# 
# * change the name of the function to `metal_blend`.
# * `metal_blend` should accept arguments including
#     * `data`, 
#     * the required mass of final product, and
#     *  the acceptable range of carbon content specified as a pair of numbers of  `[lower_bound, upper_bound]`.
# * `metal_blend` should return the minimum cost, and the amounts of each raw material to include in the blend.
# 
# Demonstrate use of `metal_blend` to compute the required blend. From the results of the calculation to report
# 
# * the cost of the blend
# * the total mass of the blend
# * the mass of each raw material used in the blend
# * the composition of the blend with regard to the species carbon, copper and managanese.
# 
# You may find it convenient to write a function for this purpose that can be used in the following exercise.
# 
# 

# ### Solution

# In[1]:





# ## Exercise 2. Incorporating Constraints
# 
# We'll continue this problem by incorporating all of the constraints. The constraiints include:
# 
# * Lower and upper bounds on the copper and manganese composition
# * Limits on the amount of available raw material
# 
# The easiest way to proceed is to copy and paste `metal_blend` into a cell below, then add constraints one at a time until all have been incorporated.
# 
# What is the minimum price you would need to charge in $/kg to produce 5,000 kg of requested product?

# In[1]:





# ## Exercise 3. Sensitivity Analysis
# 
# One of the important reasons to create optimization models is to understand the value of the raw materials that are available to you, and how to adjust operations to accomodate changing requirements. The is commonly referred to as **sensitivity analysis**.
# 
# Using the functions you've created in above exercises, answer the following questions:
# 
# 1. The customer is very pleased with your initial pricing for 5,000 kg of the desired product, and now wishes to increase the order to 6,000 kg. Does your unit cost ($/kg) go up? If so, explain why your unit cost has gone up.
# 
# 2. Is there an upper limit on how much product your can provide to this customer? (Use trial and error. To the nearest 100 kg, find the maximum amount of product you can ship to the customer.) What is the unit cost now?
# 
# 3. After some negotiation, you and your customer settle on an order of 6,500 kg. Now you wish to negotiate with your suppliers for more raw material. How much money to you save for 1 additional kg of raw material "A"? Based on this, what price would you be willing to pay your supplier for additional "A"?
# 
# 

# In[1]:





# In[ ]:




