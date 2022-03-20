#!/usr/bin/env python
# coding: utf-8

# # Quiz Review for Chapters 5 and 6

# ## Material covered
# 
# * Optimization: 5.1, 5.2, 5.3, 5.5, 
# * Predictive Control: 6.1, 6.2, 6.3, 6.4

# ## Learning Goals
# 
# You should be able to:
# 
# 1. Describe elements of an optimization problem:
#     * Decision variables.
#         * What are decision variables?
#         * Types of decision variables: Real, Nonnegative, boolean, integer.
#         * Typical onstraints on decision variables: Upper and lower bounds.
#     * Constraints
#         * Inequalities
#         * Equalitis
#         * Algebraic
#         * Differential equations
#         * Feasible regions
#         * Active vs inactive constraints
#     * Objective function
#         * Types: Minimize, maximize
#         * Objective functions are scalar functions of the decision variables
#     * Types of optimization problems
#         * Linear, Nonlinear
#         * Integer
#     * Outcomes
#         * Feasible vs infeasible
#         * Unbounded
#         * Optimal solution 
#         
# 2. Formulating Optimization problems
#     * Blending problems
#         * Decision variables represent how much of something will be used or created
#         * There is usually a collection of underlying materials or resourcds that will be combined.
#         * The objective function typically represents overall cost, profit, or property.
#     * Procedure
#         * Identify the index sets.
#         * Create decision variables, one for each member of the index set
#         * Establish upper and lower bounds, if they exist, for the decision variables
#         * Define objective function
#         * Define constraints
#         * Create problem and solve
#         * Display solution in ways that are meaningful to the application
#     * Sensitivity Studies
#         
# 3. Predictive Control
#     * Open-Loop optimization
#         * Formulate and solve for the control trajectory
#         * The state-space model provide equality constraints
#     * Closed-loop predictive control
#         * Observer/Estimator required to provide current values of the state
#         * Solve an open-loop optimization to find control policy
#         * Apply new control policy
#         * Repeat the procedure when new measurement information is available
#         

# ## Exercises
# 
# 1. Study questions from Notebook 5.2.3
# 2. Review the sensitivity analysis for Homework 4
# 3. Review the medical application in this notebook https://jckantor.github.io/CBE30338/07.01-Simulation-and-Optimal-Control-in-Pharmacokinetics.html.  
#     * Be sure you can recode the same problem in CVXPY.
#     * As stated, this is an open-loop opimization problem. Be sure you would know how to formulate the problem for predictive control. What would be the objective function? The constraints? The bounds on the decision variables? 

# In[ ]:




