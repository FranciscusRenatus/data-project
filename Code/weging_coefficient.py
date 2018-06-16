
# coding: utf-8

# In[1]:


import pandas as pd
import json
from sklearn import preprocessing
import numpy as np
import matplotlib.pyplot as plt
import math


# In[2]:


mainDF = pd.read_csv("../Data/DataFrames/maanddf.csv")
#mainDF.head()


# In[25]:


m = mainDF.loc[mainDF["Wegingcoefficient_4"] > 0]


# In[26]:


dfBedrijfstakkenBranchesSBI2008 = pd.read_json("http://opendata.cbs.nl/ODataApi/OData/81975NED/BedrijfstakkenBranchesSBI2008")


# In[27]:


listBedrijfstakken = dfBedrijfstakkenBranchesSBI2008["value"].tolist()
pdBedrijfstakkenSBI = pd.DataFrame(listBedrijfstakken)

branchNamen = pdBedrijfstakkenSBI[["Key","Title"]]


# In[35]:


z = m["BedrijfstakkenBranchesSBI2008"].unique().tolist()
for i in z:
    x = m.loc[m["BedrijfstakkenBranchesSBI2008"] == i]
    x1 = x["Wegingcoefficient_4"].unique()
    print(branchNamen.loc[branchNamen["Key"]==str(i)])
    print(x1)
    


# In[34]:


m.loc[m["BedrijfstakkenBranchesSBI2008"] == 305700]["Wegingcoefficient_4"].unique()

