#!/usr/bin/env python
# coding: utf-8

# # Getting Started with Pandas
# 
# [Pandas](https://pandas.pydata.org/) is the most popular and widely used Python library for data wrangling and analysis. Originally eveloped in the financial services industry, pandas is now included in all major distributions of Python and has become a mainstay for doing data analysis in Python. 
# 
# The purpose of this notebook is to get you started using pandas. Pandas is a big library capable of handling complex applications. But in the spirit of the 80/20 rule (i.e., [Pareto principle]()), our goal here is to introduce a small part of the pandas library that can handle requirements.
# 
# This streamlined approach employees principles of "Tidy Data", a consistent, simple, and straightforward approach to organizing tabular data. Keeping data organized following "Tidy Data" principles means much less time "wrangling" data, short and clear Python code for analysis, and more time devoted to creating good data.

# ## Tidy Data
# 
# Data acquired in process applications is normally accumulated by repeated observation of process variables. The values are typically numbers, such as temperature or pressure, but can also be strings, integers, or categorical data, such as whether a solenoid valve is an "on" or "off", or the status of a process alarm.
# 
# We will make the following assumptions about our data sets.
# 
# * Data from repeated observations is arranged in tabular form in data files. Each distinct experiment, treatment, or unit of data is located in a separate file.
# * Every column of a data file holds all data for a unique variable.
# * Every row of a data file is an observation.
# * Every cell contains a single value.
# 
# These straightforward guidelines are closely tied to concepts underlying relational databases and have become known as the ["Tidy Data"](https://vita.had.co.nz/papers/tidy-data.pdf) principles popularized by Hadley Wickham. Adopting these principles when creating and saving data streamlines later analysis. [Hart, et al., provide excellent contrasting examples of tidy and messy data](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1005097).
# 
# For these notes we will assume our data is stored in data files organized using "Tiny Data" principles. If your data doesn't satisfy these assumptions, follow the procedures described by [Wickham](https://vita.had.co.nz/papers/tidy-data.pdf) to reorgnize your data for efficient analysis.

# ## Reading Data Files
# 
# We proceed assuming data stored in data files, each data file corresponding to an experiment or other clearly defined collection of observations. 

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
# Google sheets are a convenient to collect and share data. There is a complete API and libraries to enable full read/write access to Google Sheets. But if the data is not confidential and can be temporarilty published to the web for public access, then it takes just a few steps and one line of Python to read the data as pandas DataFrame.
# 
# The first step is publish the sheet to the web. In Google Sheets, select "File > Share > Publish to the Web".
# 
# ![](figures/pandas-google-sheets-1.png)
# 
# In the dialog box, choose the "Link" tab. The choose the sheet to be published and "Comma-seperated values (.csv)" from the drop down menus. Click "Publish".
# 
# ![](figures/pandas-google-sheets-2.png)
# 
# After confirming the choice to publish, copy the link url.  This url can be read by `.read_csv()` to create a pandas dataframe.
# 
# ![](figures/pandas-google-sheets-3.png)
# 
# Copy the url into the following cell to complete the operation.

# In[2]:


sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSNUCEFMaGZ-y18p-AnDoImEeenMLbRxXBABwFNeP8I3xiUejolPJx-kr4aUywD0szRel81Kftr8J0R/pub?gid=896527992&single=true&output=csv"
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


# ## Accessing Data from DataFrames
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


# ## Working with Variables
# 
# Pandas provide are an effective data structure for calculations with data.
# 
# To illustrate, here we have temperature and flow data for a double pipe heat exchanger 

# In[20]:


print(hx.columns)


# In[22]:


# heat capacity of water 
Cp = 4.18 # kJ/ L / C

hx["Qh"] = Cp * hx["Hot Flow (L/hr)"] * (hx["H Inlet"] - hx["H Outlet"]) / 3600
hx["Qc"] = Cp * hx["Cold Flow (L/hr)"] * (hx["C Outlet"] - hx["C Inlet"]) / 3600

hx.plot(y = ["Qh", "Qc"], ylim = (0, 15), grid=True, title="Heat Balances")


# In[25]:


import numpy as np

dT1 = hx["H Inlet"] - hx["C Outlet"]
dT0 = hx["H Outlet"] - hx["C Inlet"]

hx["LMTD"] = (dT1 - dT0) / np.log(dT1/dT0)
hx["LMTD"]


# In[45]:


hx["UA"] =  0.5*(hx.Qh + hx.Qc)/hx.LMTD
hx["R"] = 1.0/hx["UA"]
hx["Ac"] = hx["Hot Flow (L/hr)"]**(-0.8)
hx["Ah"] = hx["Cold Flow (L/hr)"]**(-0.8)


# In[46]:


import statsmodels.formula.api as sm

result = sm.ols(formula="R ~ Ac + Ah", data = hx).fit()
print(result.params)
print(result.summary())


# In[47]:


hx["UA_pred"] = 1/(0.14 + 115.3*hx["Ac"] + 186.3*hx["Ah"])
hx.plot(y = ["UA", "UA_pred"], grid=True)


# In[ ]:




