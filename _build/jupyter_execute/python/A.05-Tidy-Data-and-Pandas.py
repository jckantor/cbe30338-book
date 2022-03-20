#!/usr/bin/env python
# coding: utf-8

# # Tidy Data and Pandas
# 
# [**Pandas**](https://pandas.pydata.org/) is the most popular and widely used Python library for data wrangling and analysis. Developed just over 10 years ago in the financial services industry, pandas is now included in all major distributions of Python and has become a mainstay for doing data analysis in Python. 
# 
# **Tidy Data** is a small set a of core principles to streamline analysis and coding by organizing data into tables with a simple and standardized structure. Tidy Data is highly intuitive and well suited to Pandas.   Keeping data organized following "Tidy Data" principles means less time wrangling data, short and clear Python code for analysis, and more time to capture good data and gain insight..
# 
# The purpose of this notebook is to get you started using Pandas with Tidy Data. Pandas is a full featured library capable of handling complex applications. In the spirit of the 80/20 rule (i.e., [Pareto principle]()), the goal here is to introduce just enough of the pandas library to handle routine data analysis tasks.
# 
# Some useful references:
# 
# * [Pandas Cheat Sheet](https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf)
# * [Tidy Data](https://vita.had.co.nz/papers/tidy-data.pdf) paper by Hadley Wickham.
# * [Tidy Data](https://r4ds.had.co.nz/tidy-data.html?q=Tidy%20Data#non-tidy-data), Chapter 12 from R for Data Science.
# * [13 Most Important Pandas Functions for Data Science](https://www.analyticsvidhya.com/blog/2021/05/pandas-functions-13-most-important/)
# * [Create Stunning Visualizations With Pandas Dataframes in One Line of Code](https://towardsdatascience.com/advanced-pandas-plots-e2347a33d576) Blog post describing more complex visualizations and libraries based on pandas dataframes.

# ## Tidy Data
# 
# >The KonMari Method™ is not a quick fix for a messy room or a once-in-a-while approach to tidying. 
# It’s a chance to reset your entire life – but only if you commit to following its principles. -- Marie Kondo
# 
# Data acquired in process applications generally consists of repeated observation of a set of process variables. The values are usually numbers, such as temperature or pressure, but can also be strings, integers, or categorical data indicating the status of equipment or alarms.
# 
# We assume data from repeated observations is arranged in tabular form in data files. Each distinct experiment, treatment, or unit of data is located in a separate file.
# 
# * Every column of a data file holds all data for a unique variable.
# * Every row of a data file is an observation.
# * Every cell contains a single value.
# 
# ![](https://r4ds.had.co.nz/images/tidy-1.png)
# Figure Source: Figure 12.1 from R for Data Science (Hadley Wickham & Garrett Grolemund)
# 
# These assumptions are the ["Tidy Data"](https://vita.had.co.nz/papers/tidy-data.pdf) principles popularized by Hadley Wickham, and closely related to concepts underlying relational databases. 
# Tiny Data assigns meaning to the structure of the data ffile, which significantly streamlines subsequenct coding and analysis. [Hart, et al., provide excellent contrasting examples of tidy and messy data](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1005097).
# 
# These notes assume data is stored in data files organized using "Tiny Data" principles. If your data isn't organized like this, the procedures described by [Wickham](https://vita.had.co.nz/papers/tidy-data.pdf) may help reorgnize your data for more efficient analysis.

# ## Reading Tidy Data
# 
# The first We proceed assuming data is organized by Tidy Data principles, each data set corresponding to an experiment or other clearly defined collection of observations.

# ### From .csv files
# 
# For files stored in `.csv` format, a pandas **DataFrame** object is created with the [`read_csv(data_file)`](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html). `data_file` is a string containing a url or the name of a local file. `read_csv()` function has many optional arguments, but for simple cases the path to the data file is often enough to do the job.

# In[1]:


import pandas as pd

data_file = "https://raw.githubusercontent.com/jckantor/cbe30338-book/main/notebooks/data/tclab-data-example.csv"
df = pd.read_csv(data_file)
display(df)


# ### From Google Sheets
# 
# Google sheets are a convenient to collect and share data. There is a complete API and libraries to enable full, authenticated, read/write access to Google Sheets.
# 
# But if the data is not confidential and can be temporarilty published to the web for public access, then it takes just a few steps and one line of Python to read the data as pandas DataFrame.
# 
# The first step is publish the sheet to the web. In Google Sheets, select "File > Share > Publish to the Web".
# 
# ![](figures/pandas-google-sheets-1.png)
# 
# In the dialog box, choose the "Link" tab. Locate the drop-down menus, then select the sheet to be published and "Comma-seperated values (.csv)" format. Click "Publish".
# 
# ![](figures/pandas-google-sheets-2.png)
# 
# After confirming the choice to publish, a link url will appear.  This url can be treat as a link to a .csv file. Use `.read_csv()` to create a pandas dataframe.
# 
# ![](figures/pandas-google-sheets-3.png)
# 
# Copy the url into the following cell to complete the operation.

# In[2]:


sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSNUCEFMaGZ-y18p-AnDoImEeenMLbRxXBABwFNeP8I3xiUejolPJx-kr4aUywD0szRel81Kftr8J0R/pub?gid=865146464&single=true&output=csv"
hx = pd.read_csv(sheet_url)
hx


# ### From Python
# 
# Pandas dataframes can be created directly in Python. Here we demonstrate use of a Python dictionary to create a dataframe with data for variables computed as numpy arrays.

# In[3]:


import numpy as np

t = np.linspace(0, 10, 201)
s = np.sin(t)
c = np.cos(t)

df_np = pd.DataFrame({"time": t, "sin": s, "cos": c})
df_np


# ## Accessing Data
# 
# The core object in pandas is the **DataFrame**. For "Tidy Data", a DataFrame will be collection of columns, each column containing observations of a single, unique variable. Each row is one observation of all variables. 

# The **index** assigns a unique label to each row/observation.

# In[4]:


df.index


# The names of the **columns** are given by `.columns`.

# In[5]:


df.columns


# Each column forms a ``Series`` comprised of all observations of a variable. There are several common ways to access the data series for a variable. These produce the same result. 
# 
# * `df["T1"]` 
# * `df.T1`
# * `df.loc[:, "T1"]`
# 
# Which you choose depends on situation and context.

# In[6]:


df["T1"]


# The `.loc[row, column]` is used to extract slices of the dataframe. A single value is accessed by row index and column label.

# In[7]:


df.loc[3, "T1"]


# To extract values for multiple variables from a single observation.

# In[8]:


df.loc[3, ["T1", "T2"]]


# To extract a range of observations of one or more variables.

# In[9]:


df.loc[3:5, ["T1", "T2"]]


# Observations can be selected by conditions.

# In[10]:


df[(df.Time >= 100) & (df.Time <= 110)]


# ## Visualizing Data
# 
# Pandas provides convenient tools for displaying data in tabular and graphical formats.

# ### Tabular Display
# 
# The quickest way to display a dataframe as a table is with `display()`. Additional styling and formating options are available through a dataframe's `.style` property.

# In[11]:


display(df)


# For development it is often enough to view just the first few rows or last few rows of a dataframe. The dataframe methods `.head()` and `.tail()` provide this service.

# In[12]:


df.head(5)


# In[13]:


df.tail(5)


# ### Plotting
# 
# An extensive variety of plots can be constructed using a dataframe's `.plot()` method. Many of the usual Matploblib plotting commands can be accessed through options passed to `.plot()`. For many routine applications, a single call of a dataframe's `.plot()` method can replace many lines of Python code using Matplotlib.
# 
# For example, to plot all observations for a single variable.

# In[14]:


df.T1.plot()


# The `.plot()` method will often be used to plot one or more variables on the vertical 'y' axis as a function of another variable on the horizontal 'x' axes. Additional options specify line styles, grid, labels, titles, and much more. 

# In[15]:


df.plot("Time", ["T1", "T2"], style={"T1":'rx', "T2":'g'}, lw=2, ms=3, 
        ylabel="deg C", title="TC Lab", grid=True)


# In[16]:


df.plot(x = "Time", y=["T1", "T2"], subplots=True, figsize=(10, 2), grid=True, layout=(1, 2))


# In[17]:


df[(df.Time > 570) & (df.Time < 680)].plot(x="Time", y="T1", figsize=(12, 5), style={"T1":"s:"}, grid=True)


# ### Scatter Plots

# In[18]:


df.plot.scatter(x = "T1", y = "T2")


# ### Statistical Plots

# In[19]:


df[["T1", "T2"]].hist(bins=30, figsize=(10, 3))


# ## Case Study: Analysis of a Double Pipe Heat Exchanger
# 
# A stalwart of undergraduate chemical engineering laboratories is study of a double-pipe heat exchanger in counter-current flow. In this case, a student group collected multiple measurements of flow and temperature data from a heat exchanger with sensors configured as shown in the following diagram. (Note: The diagram shows co-current flow. The data was collected with the valves configured for counter-current flow of the hot stream.)
# 
# ![](https://www.gunt.de/images/datasheet/1495/WL-315C-Comparison-of-various-heat-exchangers-gunt-1495-zeichnung_einzelheit_2.jpg)
# Source: [Gunt WL315C Product Description](https://www.gunt.de/en/products/comparison-of-various-heat-exchangers/060.315C0/wl315c/glct-1:pa-148:pr-1495)

# ### Tidy Data
# 
# The student group designed a series of experiments measuring the performance of the heat exchanger to high (H), medium (M), and low (L) flowrates for both the hot and cold streams --- a total of nine flowrate combinations. For each combination they reported data for three repeated observations. [A portion of their data is available on Google Sheets](https://docs.google.com/spreadsheets/d/1wuJq3B4z0tmTIsRpm5zZUP-PBBxT6OpuJKeBlQcQ4Z0/edit?usp=sharing). From this data they intend to compute the overall heat transfer coefficient $UA$, and attempt to fit a regression model for the heat transfer coefficients as a function of the flowrates.
# 
# A screenshot of the data collected by the students is given below.
# 
# ![](figures/pandas-google-sheets-4.png)
# 
# :::{admonition} Study Question
# 
# Before reading further, can you find three ways this data set is not consistent with Tidy Data?
# 
# :::{toggle}
# 
# * Empty rows are included for formatting that do not contain observations.
# * Missing observations for trial 9.
# * The use of vertical merging to indicate values by position rather than by actual content.
# * The "Flow Rate (H/C)" includes two values in each cell.
# * Information in the first column is meta-data, not a useful value to include in the observations.
# 
# :::
# :::

# ### Reading Data
# 
# The raw data was copied to a new sheet in the same Google Sheets file, edited to conform with Tidy Data, and a link created using the procedures outlined above for reading data from Google Sheets. The data is read in the following cell.

# In[20]:


hx = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vSNUCEFMaGZ-y18p-AnDoImEeenMLbRxXBABwFNeP8I3xiUejolPJx-kr4aUywD0szRel81Kftr8J0R/pub?gid=865146464&single=true&output=csv")
hx.head()


# ### Energy Balances
# 
# The first step in this analysis is to verify the energy balance. 
# 
# $$
# \begin{align*}
# Q_h & = \dot{q}_h \rho C_p (T_{h,in} - T_{h,out}) \\
# Q_c & = \dot{q}_c \rho C_p (T_{c,out} - T_{c, in})
# \end{align*}
# $$
# 
# The next cell creates two new calculated variables in the dataframe for $Q_h$ and $Q_c$, and uses the pandas plotting facility to visualize the results. This calculation takes advantage of the "one variable per column" rule of Tidy Data which enables calculations for all observations to be done in a single line of code.

# In[21]:


# heat capacity of water 
rho = 1.00                # kg / liter
Cp = 4.18                 # kJ/ kg / deg C

# heat balances
hx["Qh"] = rho * Cp * hx["Hot Flow (L/hr)"] * (hx["H Inlet"] - hx["H Outlet"]) / 3600
hx["Qc"] = rho * Cp * hx["Cold Flow (L/hr)"] * (hx["C Outlet"] - hx["C Inlet"]) / 3600
hx["Loss (%)"] = 100 * (1 - hx["Qc"]/hx["Qh"])

# plot
display(hx[["Qh", "Qc", "Loss (%)"]].style.format(precision=2))
hx.plot(y = ["Qh", "Qc"], ylim = (0, 15), grid=True, xlabel="Observation", ylabel="kW")


# ### Overall Heat Transfer Coefficient $UA$
# 
# The performance of a counter-current heat exchanger is given the relationship
# 
# $$Q = U A \Delta T_{lm} $$
# 
# where $\Delta T_{lm}$ is the log-mean temperature given by
# 
# $$
# \begin{align*}
# \Delta T_0 & = T_{h, out} - T_{c, in} \\
# \Delta T_1 & = T_{h, in} - T_{c, out} \\
# \\
# \Delta T_{lm} & = \frac{\Delta T_1 - \Delta T_0}{\ln\frac{\Delta T_1}{\Delta T_0}}
# \end{align*}
# $$

# In[22]:


dT0 = hx["H Outlet"] - hx["C Inlet"]
dT1 = hx["H Inlet"] - hx["C Outlet"]
hx["LMTD"] = (dT1 - dT0) / np.log(dT1/dT0)

Q = (hx.Qh + hx.Qc)/2
hx["UA"] =  Q/hx.LMTD

hx.plot(y="UA", xlabel="Observation", ylabel="kW/deg C", grid=True)


# ### How does $UA$ depend on flowrates?
# 
# The data clearly demonstrate that the heat transfer coefficient in the double pipe heat exchanger depends on flowrates of both the cold and hot liquid streams. We can see this by inspecting the data.

# In[23]:


hx[["Flow Rate H", "Flow Rate C", "Hot Flow (L/hr)", "Cold Flow (L/hr)", "UA"]]


# The replicated measurements provide an opportunity to compute averages. Here we use the pandas `.groupby()` function to group observations and compute means. The data will be used to plot results, so we'll save the results of these calculations as a new dataframe for reuse.

# In[24]:


sx = hx.groupby(["Flow Rate H", "Flow Rate C"]).mean()[["Hot Flow (L/hr)", "Cold Flow (L/hr)", "UA"]]
sx


# In[25]:


import matplotlib.pyplot as plt

fig, ax = plt.subplots(1, 1)
sx.sort_values("Cold Flow (L/hr)").groupby("Flow Rate H").plot(x = "Cold Flow (L/hr)", y = "UA", 
                                                               style={"UA": 'ro-'}, ax=ax)


# In[26]:


fig, ax = plt.subplots(1, 1)
sx.sort_values("Hot Flow (L/hr)").groupby("Flow Rate C").plot(x = "Hot Flow (L/hr)", y = "UA", 
                                                               style={"UA": 'ro-'}, ax=ax)


# ### Fitting a Model for $UA$
# 
# For a series of transport mechanisms, the overall heat transfer coefficient 
# 
# $$\frac{1}{UA} = \frac{1}{U_hA} + \frac{1}{U_{tubeA}} + \frac{1}{U_cA}$$
# 
# $U_{tube}A$ is a constant for this experiment. $U_h$A and $U_c$A varying with flowrate and proporitonal to dimensionless Nusselt number.  The hot and cold liquid flows in the double pipe heat exchanger are well within the range for fully developed turbulent flow. Under these conditions for flows inside closed tubes, the Dittus-Boelter equation provides an explicit expression for Nusselt number
# 
# $$Nu = C \cdot Re ^{4/5} Pr ^ n$$
# 
# where $C$ is a constant, $Re$ is the Reynold's number that is proportional to flowrate, and $Pr$ is the Prandtl number determined by fluid properties.
# 
# Experimentally, consider a set of values for $UA$ determined by varying $\dot{m}_h$ and $\dot{m}_c$ over range of values. Because Reynold's number is proportional to flowrate, we can propose a model
# 
# $$\frac{1}{UA} = R =  R_{t} + r_h \dot{q}_h^{-0.8} + r_c \dot{q}_h^{-0.8}$$
# 
# This suggests a linear regression for $R = \frac{1}{UA}$ in terms of $X_h = \dot{q}_h^{-0.8}$ and $X_c  = \dot{q}_c^{-0.8}$.
# 

# In[27]:


hx["R"] = 1.0/hx["UA"]
hx["Xh"] = hx["Hot Flow (L/hr)"]**(-0.8)
hx["Xc"] = hx["Cold Flow (L/hr)"]**(-0.8)


# In[28]:


import statsmodels.formula.api as sm

result = sm.ols(formula="R ~ Xh + Xc", data = hx).fit()
print(result.params)
print(result.summary())


# In[29]:


hx["Rh"] = 115.3 * hx["Xh"]
hx["Rc"] = 186.3 * hx["Xc"]
hx["Rt"] = 0.142

hx["R_pred"] = hx["Rt"] + hx["Rh"] + hx["Rc"]
hx[["R", "R_pred", "Rt", "Rh", "Rc"]]


# ### Comparison of Model to Experimental Data

# In[30]:


hx["UA_pred"] = 1/hx["R_pred"]
hx.plot(y = ["UA", "UA_pred"], grid=True, title="Heat Transfer Coefficient")


# ## Concluding Remarks
# 
# Learning Pandas and data analysis is like learning to ride a bicycle. Once you have the enough knowledge to get going, the next steps are about practice and learning by doing. 
# 
# This notobook provides basic knowledge to the use of pandas for data analysis for engineering applications. With Tidy Data principles, data analysis can be streamlined and intuitive. The next steps are to put these tools work on your data analaysis tasks, and explore other elements of the pandas library that can be useful in your work.

# In[ ]:




