#!/usr/bin/env python
# coding: utf-8

# # Linear Production Model in Pyomo
# 
# [Pyomo](http://www.pyomo.org/) is a state-of-the-art language for solving optimization problems embedded within Python. Using Pyomo, a user can describe optimization model by specifying decision **variables**, **constraints**, and an optimization **objective**. Pyomo includes a rich set of features to enable modeling of complex systems, specifying a solver, and displaying the solution.

# ## Installation

# ### Anaconda
# 
# These instructions assume you have previously installed a suitable Python development environment, in particular the [Anaconda package for Python 3.x](https://www.anaconda.com/download).
# 
# The following commands will install Pyomo and extra files plus the glpk (MILP) and ipopt (nonlinear) solvers.  These commands should be executed one at a time from the terminal window on MacOS, or the Anaconda command prompt on Windows 10.
# 
#     conda install -c conda-forge pyomo
#     conda install -c conda-forge pyomo.extras
#     conda install -c conda-forge glpk
#     conda install -c conda-forge ipopt
#     
# Optionally, you may also wish to install the COIN-OR cbc solvers.
# 
#     conda install -c conda-forge coincbc
# 
# This installation provides a capable open-source optimization suite with multiple solvers well suited a wide range of process applications. The solvers are
# 
# * [glpk](https://en.wikibooks.org/wiki/GLPK). "GNU Linear Programming Kit" is a software package written in highly portable C for the solution of mixed integer linear programming and related problems.
# * [ipopt](https://en.wikipedia.org/wiki/IPOPT). "Interior Point Optimizer" for large scale nonlinear optimization of continuous systems. 
# * [cbc](https://projects.coin-or.org/Cbc). "COIN-OR Branch and Cut" is a mixed integer linear programming solver written in C++. It generally solves the same problems as glpk, but can run multiple threads, and is often faster and more robust.
# 
# This suite can be further augmented by installing additional solvers from open-source and commercial sources.
# 
# NOTE: If command window procedure fails on your laptop, you might try running these commands in a Jupyter notebook. In that case, each command needs to be prefixed with the shell escape `!`, and followed by the `-y` option to handle the y/n 
# interaction. For example, the basic pyomo install command would read
# 
#     !conda install -c conda-forge pyomo -y
# 
# To provide timely feedback, each install command should be executed in a separate cell.

# ### Google Colab

# In[1]:


get_ipython().run_cell_magic('capture', '', '!pip install -q pyomo\n!apt-get install -y -qq glpk-utils')


# ## Algebraic Modeling Languages
# 
# One of the difficult aspects of applying optimization methods to large scale applications is creating and maintaining the underlying model. An application may include tens, hundreds, even thousdands of variables and constraints, and may incorporate data extracted in real time from sensor networks and corporate data bases. The resulting models can be very complex, and essentially impossible to create and maintain without use of software tools.
# 
# Algebraic Modeling Languages (AMLs) were developed to assist with the creation and maintainence of optimization models. [GAMS](https://en.wikipedia.org/wiki/General_Algebraic_Modeling_System) (General Algebraic Modeling System, https://www.gams.com/), first proposed in 1976, was among the first and still widely used. Other notable examples include [AIMMS](https://en.wikipedia.org/wiki/AIMMS), [AMPL](https://en.wikipedia.org/wiki/AMPL), and [FICO XPRESS](https://en.wikipedia.org/wiki/FICO_Xpress).
# 
# In recent years, modeling for optimization has become more tightly integrated with scripting languages commonly used in science and engineering. Open-source examples include [YALMIP](https://yalmip.github.io/) and [CVX](http://web.cvxr.com/cvx/doc/) which are tightly integrated with Matlab, [JuMP](https://jump.readthedocs.io/en/latest/) which works with Julia, and a variety of systems integrated with Python.
# 
# Of the Python options, the open-source [Pyomo](http://www.pyomo.org/) is perhaps the most ambitious and certainly the most aligned with the needs of process systems engineering. 

# ## Key Concepts in Pyomo
# 
# A typical Pyomo application involves the creation of at least two Pyomo objects from the following classes:
# 
# * **ConcreteModel()**  A python object representing the optimization problem to be solved.
# * **SolverFactory()** A python object representing the mathematical progamming software to be used for calculating a solution.
# 
# There are a number of of open-source and commercial solvers that can be used with Pyomo. This simple structure allows one to test and find solvers suited to a particular application.  
# 
# A model, in turn, is composed of additional objects used to specify a problem. A minimal set of classes is needed to create useful models. These classes are:
# 
# * **Var()** Objects representing variables determined in the course of solving a particular problem.
# * **Objective()** An object denoting the problem objective function that is to be either minimized or maximized.
# * **Contraint()** Objects representing problem constraints.
# 
# The following cell presents a typical example.

# ## Example: Linear Production Model with Constraints
# 
# The mathematical formulation of a simple linear production model is given by
# 
# \begin{align}
# \max_{x,y \geq 0} &\ 40\ x + 30\ y  & \mbox{objective}\\
# \mbox{subject to:}\qquad \\
# x & \leq 40  & \mbox{demand constraint} \\
# x + y & \leq 80  & \mbox{labor A constraint} \\
# 2x + y & \leq 100 & \mbox{labor B constraint}
# \end{align}
# 
# where $x$ and $y$ are the rates of production (in units per week) for two products.

# ### Step 1. Import Pyomo.
# 
# The first step in any Pyomo project is to import relevant components of the Pyomo library. This can be done with the following python statement.
# 
#     from pyomo.environ import *
#     

# ### Step 2. Create the model object.
# 
# Pyomo provides two distinct methods to create models. Here we use `ConcreteModel()` to create a model instance which is appropriate when all of the data needed to complete the model is avaiable at the current time.
# 
#     model = ConcreteModel()
#     
# The Python variable `model` stores the model instance. This could be any valid Python variable name.
#     

# ### Step 3. Add the Decision Variables, Objective, and Constraints to the model object.
# 
# The first major component of a Pyomo model are decision variables which are added as fields to `model`. In the case we name the fields `model.x` and `model.y` corresponding to $x$ and $y$ in the process model. The Python class `Var()` is used to specify these as real numbers that must be greater than or equal to zero.
# 
#     model.x = Var(domain=NonNegativeReals)
#     model.y = Var(domain=NonNegativeReals)
#     
# As we will see in other examples, the `domain` can specify other types of decision variables including reals, integers, and booleans.
# 
# The objective is specified as an algebraic expression involving the decision variables. Here we store the objective in `model.profit`, and use the optional keyword `sense` to specify a maximization problem.
# 
#     model.profit = Objective(expr = 40*model.x + 30*model.y, sense=maximize)
# 
# Constraints are added as fields to the model, each constraint created using the `Constraint()` class. The constraints are specified using the `expr` keywork in the form of linear algebraic expressions of the decision variables.
# 
#     model.demand = Constraint(expr = model.x <= 40)
#     model.laborA = Constraint(expr = model.x + model.y <= 80)
#     model.laborB = Constraint(expr = 2*model.x + model.y <= 100)

# ### Step 4.  Create a solver object and solve.
# 
# The Pyomo libary includes a `SolverFactory()` class used to specify a solver. In this case, because the problem is a linear programming problem, we use the `glpk` solver. 
# 
#     results = SolverFactory('glpk').solve(model)
#     results.write()
#     if results.solver.status == 'ok':
#         model.pprint()
#     
# The `solve()` method attempts to solve the model using the specified solver, and returns `results` which can be inspected to see if, in fact, a solution was found. If a solution is found, then `model` will have a pretty-print method `pprint()` that creates a summary of the problem solution.

# ### Step 5. Display the solution.
# 
# Most applications will require access to specific components of the model. If a solution is found, the model will include methods with the same name as the fields created above, and which can be used to access solution values.
# 
#     print('Profit = ', model.profit())
# 
#     print('\nDecision Variables')
#     print('x = ', model.x())
#     print('y = ', model.y())
# 
#     print('\nConstraints')
#     print('Demand  = ', model.demand())
#     print('Labor A = ', model.laborA())
#     print('Labor B = ', model.laborB())

# In[ ]:


from pyomo.environ import *

# create a model
model = ConcreteModel()

# declare decision variables
model.x = Var(domain=NonNegativeReals)
model.y = Var(domain=NonNegativeReals)

# declare objective
model.profit = Objective(expr = 40*model.x + 30*model.y, sense=maximize)

# declare constraints
model.demand = Constraint(expr = model.x <= 40)
model.laborA = Constraint(expr = model.x + model.y <= 80)
model.laborB = Constraint(expr = 2*model.x + model.y <= 100)

# solve
results = SolverFactory('glpk').solve(model)
results.write()
if results.solver.status:
    model.pprint()

# display solution
print('\nProfit = ', model.profit())

print('\nDecision Variables')
print('x = ', model.x())
print('y = ', model.y())

print('\nConstraints')
print('Demand  = ', model.demand())
print('Labor A = ', model.laborA())
print('Labor B = ', model.laborB())


# ## Python Lists, Sets, Dictionaries, and Iterators
# 
# Pyomo is integrated with the Python language, and inherits significant functionality by leveraging the basic data structures of Python. To make the best use of Pyomo, it is important to understand the basics of Python lists, sets, and dictionaries.

# ### Data in Matrix/Vector Format
# 
# The example above used scalar modeling components, `model.x = Var()` and `model.y = Var()`, and each constraint was added as a separate line in the model.  This is fine for small problems with a just a few unknowns, but becomes impractical for larger problems.
# 
# Here we repeat the example above, this time using `numpy` arrays to enter the data. An indexed variable `model.x` represents the unknowns, and the constraints are indexed as well. The indices are represented by the Python `range()` statement.

# In[ ]:


from pyomo.environ import *
import numpy as np

# enter data as numpy arrays
A = np.array([[1, 0], [1, 1],[2,1]])
b = np.array([40, 80,100])
c = np.array([40,30])

# set of row indices
I = range(len(A))

# set of column indices
J = range(len(A.T))

# create a model instance
model = ConcreteModel()

# create x and y variables in the model
model.x = Var(J)

# add model constraints
model.constraints = ConstraintList()
for i in I:
    model.constraints.add(sum(A[i,j]*model.x[j] for j in J) <= b[i])

# add a model objective
model.objective = Objective(expr = sum(c[j]*model.x[j] for j in J), sense=maximize)

# create a solver
solver = SolverFactory('glpk')

# solve
solver.solve(model)

# print solutions
for j in J:
    print("x[", j, "] =", model.x[j].value)

model.constraints.display()


# In[ ]:




