#!/usr/bin/env python
# coding: utf-8

# # Observer Synthesis using Linear Matrix Inequalities
# 
# Note: This is an advanced topic

# ## References
# 
# 1. Charkabarty, Ankush. ["Guest Lecture: Exploiting Linear Matrix Inequalities In
# Control Systems Design"](https://engineering.utsa.edu/ataha/wp-content/uploads/sites/38/2017/10/EE5243_Module10.pdf). (2015). Retrieved 29 March 2021.
# 
# 2. Boyd, Stephen, et al. [Linear matrix inequalities in system and control theory.](https://web.stanford.edu/~boyd/lmibook/index.html) Society for industrial and applied mathematics, 1994.
# 
# 3. Caverly, Ryan James, and James Richard Forbes. ["Lmi properties and applications in systems, stability, and control theory."](https://arxiv.org/abs/1903.08599) arXiv preprint arXiv:1903.08599 (2019). 
# 

# ## Model Parameters

# ## Lyapunov Design
# 
# Assuming no modeling error and ignoring disturbance inputs, the observer dynamics are described by
# 
# $$\frac{de}{dt} = (A - LC)e$$
# 
# where $e = \hat{x}-x$ is the difference between the estimated and process states. Given a symmetric positive definite matrix $P$, define the **Lyapunov** frunction $V(e)$ as $V(e) = e^TPe$. 
# 
# $$
# \begin{align}
# \frac{dV}{dt} & = \dot{e}^TP e + e^TP\dot{e} \\
# & = e^T(A - LC)^T Pe + e^T P (A - LC) e \\ 
# & = e^T(A^TP + PA - C^TL^TP - P L C)e\\
# \end{align}
# $$
# 
# A sufficient condition for the global asympototic stability of observer is the left-hand side of this equation be negative for all $e \ne 0$. This will be true if and only if $A^TP + PA - C^TL^TP - P L C$ is negative definite, i.e;,
# 
# $$e^T(A^TP + PA - C^TL^TP - P L C)e < 0 \qquad\forall e \ne 0$$
# 
# To provide some margin for robustness relative to model error, we will specify
# 
# $$
# \begin{align}
# \frac{dV}{dt} \leq -\gamma V
# \end{align}
# $$
# 
# for some $\gamma > 0$. When recast as a linear matrix inequality, we obtain
# 
# $$A^TP + PA - C^TL^TP - P L C  \prec -\gamma P$$
# 
# where the notation $Q \prec 0$ implies $Q$ is negative definite.
# 
# As stated, given parameters $A$, $C$ and $\gamma$, the task is to find a symmetric positive definite $P \succ 0$ and a matrix of observer gains $L$ which satistify the condition above. As stated, this is a bilinear relationship due to the terms $PL$ and $C^TL^T$ appearing in the expression. A standard 'trick' is to introduce a new decision variable $Y = PL$ to yield the linear matrix inequality
# 
# $$A^TP + PA - C^TY^T - Y C + \gamma P \prec 0$$
# 
# After finding a satisfactory solution $P \succ 0$ and $Y$, the desired observer gains are given by
# 
# $$L = P^{-1} Y$$
# 
# The next challenge is to perform the necessary calculations. 
# 
# The first challenge is that the above relationship is homogeneous. In other words, for any scale factor $\alpha > 0$, if $P$ and $Y$ satisfy the relationship then so do $\alpha P$ and $\alpha Y$ resulting in the same solution for $L$. Without loss of generality, we can specify a specific solution by adding the constraints
# 
# $$P \succ I$$

# ## CVXPY
# 
#     !pip install cvxpy

# In[2]:


# parameter estimates.
alpha = 0.00016       # watts / (units P * percent U1)
P1 = 200              # P units
P2 = 100              # P units
CpH = 4.46            # heat capacity of the heater (J/deg C)
CpS = 0.819           # heat capacity of the sensor (J/deg C)
Ua = 0.050            # heat transfer coefficient from heater to environment
Ub = 0.021            # heat transfer coefficient from heater to sensor
Uc = 0.0335           # heat transfer coefficient between heaters
Tamb = 21             # ambient room temperature

# state space model
A = np.array([[-(Ua + Ub + Uc)/CpH, Ub/CpH, Uc/CpH, 0], 
              [Ub/CpS, -Ub/CpS, 0, 0],
              [Uc/CpH, 0, -(Ua + Ub + Uc)/CpH, Ub/CpH],
              [0, 0, Ub/CpS, -Ub/CpS]])

Bu = np.array([[alpha*P1/CpH, 0], [0, 0], [0, alpha*P2/CpH], [0, 0]])

Bd = np.array([[Ua/CpH], [0], [Ua/CpH], [0]])

C = np.array([[0, 1, 0, 0], [0, 0, 0, 1]])

n = A.shape[0]
p = C.shape[0]


# In[3]:


import numpy as np
import cvxpy as cp

P = cp.Variable((n, n), PSD=True)
Y = cp.Variable((n, p))

gamma = 1/10
constraints = [P >> np.eye(n)]
constraints += [A.T@P + P@A - C.T@Y.T - Y@C + gamma*P << 0]

prob = cp.Problem(cp.Minimize(0), constraints)
prob.solve()
L = np.linalg.inv(P.value)@Y.value
print(L)


# ## $\cal{H}_2$ Optimal State Estimation
# 
# Let's now consider performance metrics for the observer. In particular, we assume our system is of the form
# 
# $$
# \begin{align}
# \frac{dx}{dt} & = A x + B_d d \\
# y & = C_y x \\
# z & = C_z x
# \end{align}
# $$
# 
# where $d$ are unmeasured disturbances, $y$ are process measurements, and $z$ are process variables we are attempting to estimate. Constructing an estimator
# 
# $$
# \begin{align}
# \frac{d\hat{x}}{dt} & = A\hat{x} - L(\hat{y} - y) + B_d\hat{d}\\
# \hat{y} & = C_y\hat{x}
# \end{align}
# $$
# 
# and defining the state error in the usual way as $e_x = \hat{x} - x$ yields error dynamics given by
# 
# $$
# \begin{align}
# \frac{de}{dt} & = (A - LC_y) e + B_d(\hat{d} - d) \\
# e_z & = C_z e
# \end{align}
# $$
# 
# where $e_z = C_z e$ denotes the estimator error of interest. The design objective is to find values for $L$ that minimize the impact of changes in disturbance $\hat{d} - d$ on $e_z$.
# 
# $$
# \begin{align}
# \begin{bmatrix} PA + A^TP - YC_y - C_y^TY^T & PB_d \\ B_d^T P & -I\end{bmatrix} & \prec 0 \\
# \begin{bmatrix} P & C_z^T \\ C_z & Z\end{bmatrix} & \succ 0 \\
# Tr(Z) & < \nu
# \end{align}
# $$

# In[268]:


import numpy as np
import cvxpy as cp

P = cp.Variable((n, n), PSD=True)
Z = cp.Variable((p, p), PSD=True)
Y = cp.Variable((n, p))
nu = cp.Variable()

Cz = np.array([[1, 0, 0, 0], [0, 0, 1, 0]])

constraints = [cp.bmat([[A.T@P + P@A - Y@C - C.T@Y.T + np.eye(n), P@Bd], 
                       [Bd.T@P, -np.ones((1,1))]]) << 0]
constraints += [cp.bmat([[P, Cz.T], [Cz, Z]]) >> 0]
constraints += [cp.trace(Z) <= nu]
constraints += [nu >= 0]

prob = cp.Problem(cp.Minimize(nu), constraints)
prob.solve()
print(nu.value)
L = np.linalg.inv(P.value) @ Y.value
print(L)


# In[1]:


import numpy as np
import cvxpy as cp

P = cp.Variable((5, 5), PSD=True)
Z = cp.Variable((1, 1), PSD=True)
Y = cp.Variable((5, 2))
nu = cp.Variable()


A_aug = np.vstack([np.hstack([A, Bd]), np.zeros([1, 5])])
Bu_aug = np.vstack([Bu, [[0, 0]]])
Bd_aug = np.vstack([np.zeros([4, 1]), [[1]]])
C_aug = np.hstack([C, np.zeros([2, 1])])

Cz_aug = np.array([[0, 0, 0, 0, 1]])


P = cp.Variable((5, 5), PSD=True)
Y = cp.Variable((5, 2))

gamma = 1/20
constraints = [P >> np.eye(5)]
constraints += [A_aug.T@P + P@A_aug - C_aug.T@Y.T - Y@C_aug + gamma*P << 0]

prob = cp.Problem(cp.Minimize(0), constraints)
prob.solve()
L = np.linalg.inv(P.value)@Y.value
print(L)

constraints = [cp.bmat([[A_aug.T@P + P@A_aug - Y@C_aug - C_aug.T@Y.T + np.eye(5), P@Bd_aug], 
                       [Bd_aug.T@P, -np.ones((1,1))]]) << 0]
constraints += [cp.bmat([[P, Cz_aug.T], [Cz_aug, Z]]) >> 0]
constraints += [cp.trace(Z) <= nu]
constraints += [nu >= 0]

prob = cp.Problem(cp.Minimize(0), constraints)
prob.solve()
print(P.value)
print(nu.value)
L = np.linalg.inv(P.value) @ Y.value
print(L)


# ## $\cal{H}_{\infty}$ Optimal State Estimation

# In[159]:


import numpy as np
import cvxpy as cp

P = cp.Variable((n, n), PSD=True)
Y = cp.Variable((4, 2))

constraint = cp.bmat([[A.T@P + P@A - Y@C - C.T@Y.T + np.eye(n), P@Bd], 
                       [Bd.T@P, -2*np.ones((1,1))]]) << 0
prob = cp.Problem(cp.Minimize(0), [constraint])
prob.solve()
L = np.linalg.inv(P.value) @ Y.value
print(L)


# In[191]:


ev, _ = np.linalg.eig(A - L@C)
-1/ev


# In[194]:


(repr(L))


# In[ ]:




