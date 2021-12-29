#!/usr/bin/env python
# coding: utf-8

# # Linear Programming
# 
# Linear programming is the minimization (or maximization) of a linear objective subject to linear constraints. There are several widely adopted schemes for representing linear programming problems. Here we adopt a scheme corresponding where the linear objective is written in terms of decision variables $x_1, x_2, \ldots, x_N$ as
# 
# $$
# \begin{align}
# \min_{x_1, x_1, \ldots, x_N} c_1x_1 + c_2x_2 + \cdots + c_Nx_N
# \end{align}
# $$
# 
# subject to
# 
# $$
# \begin{align}
# x_i  \geq 0 & \qquad i=1,\ldots,N\quad\mbox{lower bounds on decision variables}\\
# \sum_{j=1}^N a^{ub}_{ij}x_j \leq b^{ub}_i & \qquad i=1,\ldots,M_{ub}\quad\mbox{upper bound constraints} \\
# \sum_{j=1}^N a^{eq}_{ij}x_j = b^{eq}_i & \qquad i=1,\ldots,M_{eq}\quad\mbox{equality constraints}\\
# \end{align}
# $$

# ## Matrix/Vector format
# 
# The notation can be simplified by adopting a matrix/vector formulation where
# 
# $$
# \begin{align}
# \min_{x\geq 0} c^T x
# \end{align}
# $$
# 
# subject to
# 
# $$
# \begin{align}
# A_{ub} x \leq b_{ub} \\
# A_{eq} x = b_{eq}
# \end{align}
# $$
# 
# where $c$, $A_{ub}, b_{ub}$, and $A_{eq}, b_{eq}$, are vectors and matrices of coefficients constructed from the linear expressions given above.

# ## Example 19.3: Refinery Blending Problem
# 
# The decision variables are
# 
# 
# | Variable | Description | Units |
# | ---------|-------------| ------|
# | $x_1$ | crude #1 | bbl/day |
# | $x_2$ | crude #2 | bbl/day |
# | $x_3$ | gasoline | bbl/day |
# | $x_4$ | kerosine | bbl/day |
# | $x_5$ | fuel oil | bbl/day |
# | $x_6$ | residual | bbl/day |
# 
# 
# The overall objective is to maximize profit
# 
# $$
# \begin{align}
# \mbox{profit} & = \mbox{income} - \mbox{raw_material_cost} - \mbox{processing_cost}
# \end{align}
# $$
# 
# where the financial components are given by
# 
# $$
# \begin{align}
# \mbox{income} & = 72x_3 + 48x_4 + 42x_5 + 20x_6 \\
# \mbox{raw_material_cost} & = 48x_1 + 30x_2 \\
# \mbox{processing_cost} & = 1 x_1 + 2x_2
# \end{align}
# $$
# 
# Combining these terms, the objective is to maximize
# 
# $$
# \begin{align}
# f & = c^T x = - 49 x_1 - 32 x_2 + 72 x_3 + 48x_4 + 42x_5 + 20x_6 
# \end{align}
# $$
# 
# The material balance equations are
# 
# $$
# \begin{align}
# \mbox{gasoline: } x_3 & = 0.80 x_1 + 0.44 x_2 \\
# \mbox{kerosine: } x_4 & = 0.05 x_1 + 0.10 x_2 \\
# \mbox{fuel oil: } x_5 & = 0.10 x_1 + 0.36 x_2 \\
# \mbox{residual: } x_6 & = 0.05 x_1 + 0.10 x_2
# \end{align}
# $$
# 
# Production limits
# 
# $$
# \begin{align}
# \mbox{gasoline: } x_3 & \leq 24,000 \\
# \mbox{kerosine: } x_4 & \leq 2,000 \\
# \mbox{fuel oil: } x_5 & \leq 6,000
# \end{align}
# $$
# 
# $$
# \begin{align}
# \underbrace{\left[\begin{array}{cccccc}
# 0.80 & 0.44 & -1 & 0 & 0 & 0 \\
# 0.05 & 0.10 & 0 & -1 & 0 & 0 \\
# 0.10 & 0.36 & 0 & 0 & -1 & 0 \\
# 0.05 & 0.10 & 0 & 0 & 0 & -1
# \end{array}\right]}_{A_{eq}}
# \left[\begin{array}{c}
# x_1 \\ x_2 \\ x_3 \\ x_4 \\ x_5 \\ x_6 
# \end{array}\right]
# & = 
# \underbrace{\left[\begin{array}{c}
# 0 \\ 0 \\ 0 \\ 0
# \end{array}\right]}_{b_{eq}}
# \end{align}
# $$

# In[10]:


from scipy.optimize import linprog

c = [49, 32, -72, -48, -42, -20]

A_ub = [[0, 0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 1, 0]]

b_ub = [24000, 2001, 6000]

A_eq = [[0.80, 0.44, -1,  0,  0,  0],
        [0.05, 0.10,  0, -1,  0,  0],
        [0.10, 0.36,  0,  0, -1,  0],
        [0.05, 0.10,  0,  0,  0, -1]]

b_eq = [0, 0, 0, 0]

results = linprog(c, A_ub, b_ub, A_eq, b_eq)
results
p0 = 573517.24
print('additional profit', -results.fun - p0)


# In[11]:


print(results.message)
if results.success:
    for k in range(len(results.x)):
        print('x[{0:2d}] = {1:7.1f} bbl/day'.format(k+1, results.x[k]))


# In[ ]:




