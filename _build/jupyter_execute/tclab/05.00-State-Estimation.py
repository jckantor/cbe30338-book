#!/usr/bin/env python
# coding: utf-8

# <!--NOTEBOOK_HEADER-->
# *This notebook contains course material from [CBE32338](https://jckantor.github.io/CBE32338)
# by Jeffrey Kantor (jeff at nd.edu); the content is available [on Github](https://github.com/jckantor/CBE2338.git).
# The text is released under the [CC-BY-NC-ND-4.0 license](https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode),
# and code is released under the [MIT license](https://opensource.org/licenses/MIT).*

# <!--NAVIGATION-->
# < [Model Identification: Fitting models to data](http://nbviewer.jupyter.org/github/jckantor/CBE32338/blob/master/notebooks/02.11-TCLab-Lab-2-Fitting.ipynb) | [Contents](toc.ipynb) | [Open and Closed Loop Estimation](http://nbviewer.jupyter.org/github/jckantor/CBE32338/blob/master/notebooks/03.01-Open-and-Closed-Loop-Estimation.ipynb) ><p><a href="https://colab.research.google.com/github/jckantor/CBE32338/blob/master/notebooks/03.00-State-Estimation.ipynb"><img align="left" src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open in Colab" title="Open in Google Colaboratory"></a><p><a href="https://raw.githubusercontent.com/jckantor/CBE32338/master/notebooks/03.00-State-Estimation.ipynb"><img align="left" src="https://img.shields.io/badge/Github-Download-blue.svg" alt="Download" title="Download Notebook"></a>

# # State Estimation
# 
# 
# ## Reference materials
# 
# * Wang, Shuo. "Kalman Filter in a Nutshell." *Towards Data Science*, https://towardsdatascience.com/kalman-filter-in-a-nutshell-e66154a06862. Accessed 6 December 2020.

# <!--NAVIGATION-->
# < [Model Identification: Fitting models to data](http://nbviewer.jupyter.org/github/jckantor/CBE32338/blob/master/notebooks/02.11-TCLab-Lab-2-Fitting.ipynb) | [Contents](toc.ipynb) | [Open and Closed Loop Estimation](http://nbviewer.jupyter.org/github/jckantor/CBE32338/blob/master/notebooks/03.01-Open-and-Closed-Loop-Estimation.ipynb) ><p><a href="https://colab.research.google.com/github/jckantor/CBE32338/blob/master/notebooks/03.00-State-Estimation.ipynb"><img align="left" src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open in Colab" title="Open in Google Colaboratory"></a><p><a href="https://raw.githubusercontent.com/jckantor/CBE32338/master/notebooks/03.00-State-Estimation.ipynb"><img align="left" src="https://img.shields.io/badge/Github-Download-blue.svg" alt="Download" title="Download Notebook"></a>
