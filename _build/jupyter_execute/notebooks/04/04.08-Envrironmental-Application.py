#!/usr/bin/env python
# coding: utf-8

# # Application of Luenberger Observers to Environmental Modeling of Rivers
# 
# Rodriguez-Mata, Abraham Efraim, et al. "A Fractional High-Gain Nonlinear Observer Design—Application for Rivers Environmental Monitoring Model." Mathematical and Computational Applications 25.3 (2020): 44. [https://www.mdpi.com/2297-8747/25/3/44](https://www.mdpi.com/2297-8747/25/3/44)

# ## Model
# 
# The Streeter-Phelps model for oxygen in a river or stream is given by the pair of linear differential equations
# 
# \begin{align}
# \frac{dx_1}{dt} & = -\frac{k_1}{U} x_2 + \frac{k_2}{U}(D_s - x_1) \\
# \frac{dx_2}{dt} & = -\frac{k_1}{U} x_2
# \end{align}
# 
# where $x_1$ is dissolved oxygen (DO) and $x_2$ is biological oxygen demand (BOD).  Rate constant $k_1$ is the BOD removal rate, $k_2$ is the re-areation rate, and $D_s$ is the oxygen saturation level which, for this problem, is a disturbance variable. No manipulations to this system are possible.
# 
# For environmental monitoring, dissolved oxygen can be measured in the field with a low-cost sensor. BOD, however, cannot be measured in the field.
# 
# Our standard model for a state-space system is given by
# 
# \begin{align}
# \frac{dx}{dt} & = A x + B_d d + B_u u\\
# y & = C x
# \end{align}
# 
# where $x$ contains the states, $d$ contains the disturbances, and $u$ contains the manipulable inputs.

# Parameter values are $k_1 = 0.3\ \text{day}^{-1}$, $k_2 = 0.06\ \text{day}^{-1}$, and $U = 1$. A typical value of Ds = 16 mg/liter. For these values the state space model becomes
# 
# \begin{align}
# \frac{dx}{dt} & = A x + B_d d + B_u u\\
# y & = C x
# \end{align}
# 
# where 
# 
# \begin{align}
# A & = \begin{bmatrix} -0.06 & -0.3 \\0 & -0.3\end{bmatrix}
# \qquad
# B_d = \begin{bmatrix} 0.06 \\ 0 \end{bmatrix} \\
# C & = \begin{bmatrix} 1 & 0 \end{bmatrix}
# \end{align}
# 
# For the state estimator, aat each time step $t_k$ there are two calculations to perform:
# 
# * **Model Prediction:** Use the model to update the state to the next time step, i.e., $\hat{x}_{k-1} \rightarrow \hat{x}_{k}^{pred}$ with the equation
# 
# \begin{align}
# \hat{x}_k^{pred} & = \hat{x}_{k-1} + (t_k - t_{k-1}) ( A \hat{x}_{k-1} + B_u u_{k-1} + B_d \hat{d}_{k-1}) \\
# \hat{y}_k^{pred} & = C \hat{x}_k^{pred}
# \end{align}
# 
# * **Measurement Correction:** Use measurement $y_k$ to update $\hat{x}_{k}^{pred} \rightarrow \hat{x}_{k}$ with the equation
# 
# $$\hat{x}_{k} = \hat{x}_{k}^{pred} - (t_k - t_{k-1})L (\hat{y}_{k}^{pred} - y_k)$$ 
# 
# 
# 

# In[ ]:




therefore it is desired to implement a Luenberger observer to estimate BOD. 


Our standard model for a state-space system is given by

\begin{align}
\frac{dx}{dt} & = A x + + B_u u + B_d d \y & = C x
\end{align}


# ## State Space Model

# In[9]:


import numpy as np

k1 = 0.3
k2 = 0.06
U = 1
Ds = 16.0


A = np.array([[-k2/U, -k1/U], [0, -k1/U]])
Bd = np.array([[k2/U], [0]])
C = np.array([[1, 0]])


sources = [
    ("DO", lambda: x[0]),
    ("BOD", lambda: x[1]),
    ("DS", lambda: Ds )
]


# In[21]:


import numpy as np
import cvxpy as cp
n=2
p = 1

P = cp.Variable((n, n), PSD=True)
Y = cp.Variable((n, p))

gamma = .75
constraints = [P >> np.eye(n)]
constraints += [A.T@P + P@A - C.T@Y.T - Y@C + gamma*P << 0]

prob = cp.Problem(cp.Minimize(0), constraints)
prob.solve()
L = np.linalg.inv(P.value)@Y.value
print(L)


# In[22]:


np.linalg.eig(A-L@C)


# In[ ]:




