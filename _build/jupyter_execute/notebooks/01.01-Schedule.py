#!/usr/bin/env python
# coding: utf-8

# # Schedule and Course Organization

# ## Getting Started
# 
# **CBE 30338/32338 Chemical Process Control** will be conducted as a fully on-line course for the 2021 Spring semeter. For this to be effective, each student, instuctor, and teaching assistant will need access to the required technology and keep their systems and software in good working order for the duration of the semester.
# 
# **Please let the instructors know immediately if you don't have access to a laptop, or you don't have adequate internet connectivity. The University has resources available to assist with these situations.**
# 
# Please use the period before the start of the semester to prepare your systems and technology. Pay attention to the following the following details:
# 
# * We will be making extensive use of Zoom for office hours, on-classes, and laboratory sessions. Please verify that you can access Zoom by joining the test meeting **with video** at [https://zoom.us/test](https://zoom.us/test). 
# 
# * Please confirm that you have a working installation of the latest Anaconda distribution of Python. If in doubt, reinstall a fresh download available from [Anaconda.com](https://www.anaconda.com/).
# 
# * A major component of the course is hands-on use of real hardware to implement working control systems. For this purpose wyou will need to purchase an individual copy of the **Temperature Control Labortory** available through [Amazon](https://www.amazon.com/TCLab-Temperature-Control-Lab/dp/B07GMFWMRY), the Notre Dame Bookstore, and [apmonitor.com](https://apmonitor.com/pdc/index.php/Main/PurchaseLabKit). Please allow time for ordering, shipping, and for you to install and test the device using your laptop.
# 
# * The Temperature Control Lab requires a USB type A port. If your laptop is a newer model with only USB-C ports then you will need to purchase a USB-C to USB-A adaptor ([such as this device for an Apple Mac](https://www.amazon.com/Apple-USB-C-to-USB-Adapter/dp/B00VU2OID2/)) or USB-C docking station ([such as this](https://www.amazon.com/LENTION-Multi-Port-Compatible-2020-2016-Chromebook/dp/B07FNH5Y84/) from LENTION).

# ## Introduction to the Course and Process Control

# ### Week 1
# 
# Class meetings begin on week 1. Each of the sessions scheduled below will be done as a Zoom meeting. To protect privacy, the specific Zoom meeting links are available through the course management system. Attendance will be monitored for each session with required attendance.
# 
# | Date | Time (EDT) | Activity | Topic | Reading | Req'd? |
# | :--  | :--  | :------  | :--- | :--- | :---: |
# | 2/4(Th) | 11:10am-12:25pm | [Class Meeting](https://notredame.zoom.us/j/98411704304?pwd=Yk1GYjlkRjZnR3UxV0Q2V0RRRXJiUT09) | Introductions <br> Course Resources <br> Syllabus  <br> Introduction to TCLab <br> What is Process Control? | [Syllabus](https://docs.google.com/document/d/1nyId3IqaRej6zYwJ-HlFvR8lfqszkLH7OWzamw-vI-E/edit?usp=sharing) <br> [FBS 1.2-1.4](https://fbswiki.org/wiki/index.php/Feedback_Systems:_An_Introduction_for_Scientists_and_Engineers) <br> [cbe30338-2021 Section 1.1](https://jckantor.github.io/cbe30338-2021/) | &check;
# | 2/5(F) | 11:40am-12:30pm <br> 1:00-1:50pm | Lab Session 1 <br> Lab Session 2 | **No meeting for week 1** | | 

# ## Modeling and Parameter Estimation

# ### Week 2
# 
# | Date | Time (EDT) | Activity | Topic | Reading | Req'd? | Assignment Due |
# | :--  | :--  | :------  | :--- | :--- | :---: | :--- |
# | 2/8(M) | 1:30-3pm | Office hours | | |
# | 2/9(T) | 11:10am-12:25pm | [Class Meeting](https://notredame.zoom.us/j/98411704304?pwd=Yk1GYjlkRjZnR3UxV0Q2V0RRRXJiUT09) | System Modeling <br> Pharmacokinetics | [FBS 3.1, 3.2](https://fbswiki.org/wiki/index.php/System_Modeling) <br> [cbe30338-2021 Section 2.1](https://jckantor.github.io/cbe30338-2021/) | &check; | HW Assignment 1
# | 2/11(Th) | 11:10am-12:25pm | [Class Meeting](https://notredame.zoom.us/j/98411704304?pwd=Yk1GYjlkRjZnR3UxV0Q2V0RRRXJiUT09) | First Order Systems <br> Degrees of Freedom | [cbe30338-2021 Section 2.2](https://jckantor.github.io/cbe30338-2021/) | &check;
# | 2/12(F) | 11:40am-12:30pm <br> 1:00-1:50pm | Lab Session 1 <br> Lab Session 2 | TCLab Operation <br> First Order Model ID | [cbe30338-2021 Section 1.3](https://jckantor.github.io/cbe30338-2021/) <br> [cbe30338-2021 Section 1.4](https://jckantor.github.io/cbe30338-2021/)| &check;

# ### Week 3
# 
# | Date | Time (EDT) | Activity | Topic | Reading | Req'd? | Assignment Due |
# | :--  | :--  | :------  | :--- | :---| :---: | :--- |
# | 2/15(M) | 1:30-3pm | Office hours | | 
# | 2/16(T) | 11:10am-12:25pm | [Class Meeting](https://notredame.zoom.us/j/98411704304?pwd=Yk1GYjlkRjZnR3UxV0Q2V0RRRXJiUT09) | First-Order Model TCLab | [cbe30338-2021 Section 2.3](https://jckantor.github.io/cbe30338-2021/) | &check; | HW Assignment 2 |
# | 2/18(Th) | 11:10am-12:25pm | [Class Meeting](https://notredame.zoom.us/j/98411704304?pwd=Yk1GYjlkRjZnR3UxV0Q2V0RRRXJiUT09) | Identifying Linear Dynamics | [cbe30338-2021 Section 2.4](https://jckantor.github.io/cbe30338-2021/) | &check;
# | 2/19(F) | 11:40am-12:30pm <br> 1:00-1:50pm | Lab Session 1 <br> Lab Session 2 | Dynamic Model Identification | | &check; | Lab Assignment 1

# ## Feedback Control

# ### Week 4
# 
# | Date | Time (EDT) | Activity | Topic | Reading | Req'd? | Assignment Due |
# | :--  | :--  | :------  | :--- | :--- | :---: | :--- |
# | 2/22(M) | 1:30-3pm | Office hours | | 
# | 2/23(T) | 11:10am-12:25pm | [Class Meeting](https://notredame.zoom.us/j/98411704304?pwd=Yk1GYjlkRjZnR3UxV0Q2V0RRRXJiUT09) | Case Study: PCR Thermal Cycling <br> Setpoints | [cbe30338-2021 Section 3.1 & 3.2](https://jckantor.github.io/cbe30338-2021/) | &check; | HW Assignment 3 |
# | 2/25(Th) | 11:10am-12:25pm | [Class Meeting](https://notredame.zoom.us/j/98411704304?pwd=Yk1GYjlkRjZnR3UxV0Q2V0RRRXJiUT09) | Relay, Proportional, and PI Control | [cbe30338-2021 Section 3.3](https://jckantor.github.io/cbe30338-2021/)  | &check; | Quiz 1: Modeling & Identification
# | 2/26(F) | 11:40am-12:30pm <br> 1:00-1:50pm | Lab Session 1 <br> Lab Session 2 | Single Variable Relay Control <br> PI Control | [cbe30338-2021 Section 3.6](https://jckantor.github.io/cbe30338-2021/) | &check; | Lab Assignment 2

# ### Week 5
# 
# | Date | Time (EDT) | Activity | Topic | Reading | Req'd? | Assignment Due |
# | :--  | :--  | :------  | :--- | :--- | :---: | :--- |
# | 3/1(M) | 1:30-3pm | Office hours | | |
# | 3/2(T) | 11:10am-12:25pm | **University Mini-break** |  | | | |
# | 3/4(Th) | 11:10am-12:25pm | [Class Meeting](https://notredame.zoom.us/j/98411704304?pwd=Yk1GYjlkRjZnR3UxV0Q2V0RRRXJiUT09) | PI Implementation & Co-routines | [cbe30338-2021 Section 3.4](https://jckantor.github.io/cbe30338-2021/)  | &check;
# | 3/5(F) | | **Junior Parents Weekend** | | | | Lab Assignment 3

# ### Week 6
# 
# | Date | Time (EDT) | Activity | Topic | Reading | Req'd? | Assignment Due |
# | :--  | :--  | :------  | :--- | :--- | :---: | :--- |
# | 3/8(M) | 1:30-3pm | Office hours | | 
# | 3/9(T) | 11:10am-12:25pm | [Class Meeting](https://notredame.zoom.us/j/98411704304?pwd=Yk1GYjlkRjZnR3UxV0Q2V0RRRXJiUT09) | Practical PI Control  | [cbe30338-2021 Section 3.5](https://jckantor.github.io/cbe30338-2021/) <br> Astrom and Murray, Chapter 11 | &check; | No assignment (JPW)
# | 3/11(Th) | 11:10am-12:25pm | [Class Meeting](https://notredame.zoom.us/j/98411704304?pwd=Yk1GYjlkRjZnR3UxV0Q2V0RRRXJiUT09) | Advanced PI and PID Control | | &check;
# | 3/12(F) | 11:40am-12:30pm <br> 1:00-1:50pm | Lab Session 1 <br> Lab Session 2 | Advanced PID Control | | &check;

# ## Process Analytics

# ### Week 7
# 
# | Date | Time (EDT) | Activity | Topic | Reading | Req'd? | Assignment Due |
# | :--  | :--  | :------  | :---  | :--- | :---: | :--- |
# | 3/15(M) | 1:30-3pm | Drop-in office hours | | |
# | 3/16(T) | 11:10am-12:25pm | [Class Meeting](https://notredame.zoom.us/j/98411704304?pwd=Yk1GYjlkRjZnR3UxV0Q2V0RRRXJiUT09) | Guest: Katie Gates ND'10 <br> What is Process Analytics? | Data Historian <br> Anamoly Detection | &check; | |
# | 3/18(Th) | 11:10am-12:25pm | [Class Meeting](https://notredame.zoom.us/j/98411704304?pwd=Yk1GYjlkRjZnR3UxV0Q2V0RRRXJiUT09) | | | &check; | Quiz 2: Feedback Control
# | 3/19(F) | 11:40am-12:30pm <br> 1:00-1:50pm | Lab Session 1 <br> Lab Session 2 | Using the Data Historian | | &check; | Lab Assignment 4

# ### Week 8
# 
# | Date | Time (EDT) | Activity | Topic | Reading | Req'd? | Assignment Due |
# | :--  | :--  | :------  | :--- | :--- | :---: | :--- |
# | 3/22(M) | 1:30-3pm | Drop-in office hours | | |
# | 3/23(T) | 11:10am-12:25pm | [Class Meeting](https://notredame.zoom.us/j/98411704304?pwd=Yk1GYjlkRjZnR3UxV0Q2V0RRRXJiUT09) | Anamoly Detection | | &check; | |
# | 3/25(Th) | 11:10am-12:25pm | [Class Meeting](https://notredame.zoom.us/j/98411704304?pwd=Yk1GYjlkRjZnR3UxV0Q2V0RRRXJiUT09) | Machine Learning | | &check;
# | 3/26(F) | 11:40am-12:30pm <br> 1:00-1:50pm | Lab Session 1 <br> Lab Session 2 | Machine Learning | | &check; | Lab Assignment 5

# ## Optimization

# ### Week 9
# 
# | Date | Time (EDT) | Activity | Topic | Reading | Req'd? | Assignment Due |
# | :--  | :--  | :------  | :--- | :---  | :---: | :--- |
# | 3/29(M) | 1:30-3pm | Drop-in office hours | | |
# | 3/30(T) | 11:10am-12:25pm | [Class Meeting](https://notredame.zoom.us/j/98411704304?pwd=Yk1GYjlkRjZnR3UxV0Q2V0RRRXJiUT09) | Introduction to Semester Project <br> | | &check; | |
# | 4/1(Th) | 11:10am-12:25pm | [Class Meeting](https://notredame.zoom.us/j/98411704304?pwd=Yk1GYjlkRjZnR3UxV0Q2V0RRRXJiUT09) | Linear Production Problem <br> CVXPY| Section 5.1 | &check; | Quiz 3: Process Analytics
# | 4/2(F) | | **Good Friday** |

# ### Week 10
# 
# | Date | Time (EDT) | Activity | Topic | Reading | Req'd? | Assignment Due |
# | :--  | :--  | :------  | :--- | :--- | :---: | :--- |
# | 4/5(M) | 1:30-3pm | Drop-in office hours | | |
# | 4/6(T) | 11:10am-12:25pm | [Class Meeting](https://notredame.zoom.us/j/98411704304?pwd=Yk1GYjlkRjZnR3UxV0Q2V0RRRXJiUT09) | Linear Blending | Section 5.2 | &check; | |
# | 4/8(Th) | 11:10am-12:25pm | [Class Meeting](https://notredame.zoom.us/j/98411704304?pwd=Yk1GYjlkRjZnR3UxV0Q2V0RRRXJiUT09) | Blending | Section 5.3 | &check; | Lab Assignment 6 
# | 4/9(F) | 11:40am-12:30pm <br> 1:00-1:50pm | Lab Session 1 <br> Lab Session 2 | Static Operability Analysis | Section 6.1 | &check;

# ## Predictive Control

# ### Week 11
# 
# | Date | Time (EDT) | Activity | Topic | Reading | Req'd? | Assignment Due |
# | :--  | :--  | :------  | :--- | :--- | :---: | :--- |
# | 4/12(M) | 1:30-3pm | Drop-in office hours | | |
# | 4/13(T) | 11:10am-12:25pm | [Class Meeting](https://notredame.zoom.us/j/98411704304?pwd=Yk1GYjlkRjZnR3UxV0Q2V0RRRXJiUT09) | | | &check; |  HW Assignment 4 <br> Project Proposal |
# | 4/15(Th) | 11:10am-12:25pm | [Class Meeting](https://notredame.zoom.us/j/98411704304?pwd=Yk1GYjlkRjZnR3UxV0Q2V0RRRXJiUT09) | | | &check; |
# | 4/16(F) | 11:40am-12:30pm <br> 1:00-1:50pm | Lab Session 1 <br> Lab Session 2 | State Estimation | | &check; | Lab Assignment 7 

# ### Week 12
# 
# | Date | Time (EDT) | Activity | Topic | Reading | Req'd? | Assignment Due |
# | :--  | :--  | :------  | :--- | :--- | :---: | :--- |
# | 4/19(M) | 1:30-3pm | Drop-in office hours | | |
# | 4/20(T) | 11:10am-12:25pm | [Class Meeting](https://notredame.zoom.us/j/98411704304?pwd=Yk1GYjlkRjZnR3UxV0Q2V0RRRXJiUT09) | | | &check; | HW Assignment 4 |
# | 4/22(Th) | 11:10am-12:25pm | [Class Meeting](https://notredame.zoom.us/j/98411704304?pwd=Yk1GYjlkRjZnR3UxV0Q2V0RRRXJiUT09) | | | &check; |
# | 4/23(F) | 11:40am-12:30pm <br> 1:00-1:50pm | Lab Session 1 <br> Lab Session 2 | Model Predictive Control | | &check; | Lab Assignment 8

# ## Final Project

# ### Week 13
# 
# | Date | Time (EDT) | Activity | Topic | Reading | Req'd? | Assignment Due |
# | :--  | :--  | :------  | :--- | :--- | :---: | :--- |
# | 4/26(M) | 1:30-3pm | Drop-in office hours | | |
# | -- | --- | Office hours by appointment |
# | 4/27(T) | 11:10am-12:25pm | [Class Meeting](https://notredame.zoom.us/j/98411704304?pwd=Yk1GYjlkRjZnR3UxV0Q2V0RRRXJiUT09) | | | &check; |  |
# | 4/29(Th) | 11:10am-12:25pm | [Class Meeting](https://notredame.zoom.us/j/98411704304?pwd=Yk1GYjlkRjZnR3UxV0Q2V0RRRXJiUT09) | | | &check; | 
# | 4/30(F) | 11:40am-12:30pm <br> 1:00-1:50pm | Lab Session 1 <br> Lab Session 2 | | | &check; | Lab Assignment 9

# ### Week 14
# 
# | Date | Time (EDT) | Activity | Topic | Reading | Req'd? | Assignment Due |
# | :--  | :--  | :------  | :--- | :--- | :---: | :--- |
# | 5/3(M) | 1:30-3pm | Drop-in office hours | | |
# | -- | --- | Office hours by appointment |
# | 5/4(T) | 11:10am-12:25pm | [Class Meeting](https://notredame.zoom.us/j/98411704304?pwd=Yk1GYjlkRjZnR3UxV0Q2V0RRRXJiUT09) | | | &check; | Progress Report
# | 5/6(Th) | 11:10am-12:25pm | [Class Meeting](https://notredame.zoom.us/j/98411704304?pwd=Yk1GYjlkRjZnR3UxV0Q2V0RRRXJiUT09) | | | &check; | Quiz 4: Predictive Control
# | 5/7(F) | | no lab - Final Project | | |

# ### Finals Week
# 
# | Date | Time (EDT) | Activity | Topic | Reading | Req'd? | Assignment Due |
# | :--  | :--  | :------  | :--- | :--- | :---: | :--- |
# | 5/11(M) | 1:30-3pm | Office hours | | |
# | -- | --- | Office hours by appointment |
# | 5/11(T) | 11:10am-12:25pm | [Class Meeting](https://notredame.zoom.us/j/98411704304?pwd=Yk1GYjlkRjZnR3UxV0Q2V0RRRXJiUT09) | | | &check;
# | 5/14(F) | 10:30am - 12:30pm | Project Presentations | | | &check;

# In[ ]:




