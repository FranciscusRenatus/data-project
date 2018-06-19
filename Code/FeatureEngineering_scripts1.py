
# coding: utf-8

# ## info
# ### Script gericht op het benutten van de wegingscoeficient in dataset en verder analyseren van de data.
# #### Aantal aanmerkingen:
# ###### *Wegingscoefficienten worden pas vanaf 2005 gemeten
# ###### *Waarschijnlijk het beste resultaten met Overkoepelende industrieen in eigen data set te houden, te sparse anders ?
# ###### *Idee, maken van categorische data voor het indelen van branches in de bijhorende overkoepelende industrie.

# In[68]:


import pandas as pd
import json
from sklearn import preprocessing
import numpy as np
import matplotlib.pyplot as plt
import math
import sys


# In[69]:


mainDF = pd.read_csv("../Data/Dataframe/maanddf.csv")


# In[70]:


wegingDF = mainDF.loc[mainDF["Wegingcoefficient_4"] != 0]
wegingDF = wegingDF.drop(["Unnamed: 0"], axis=1)
wegingDF = wegingDF.drop(["ID"], axis=1)
wegingDF.loc[:,"index"] = list(range(0,len(wegingDF)))
wegingDF = wegingDF.set_index('index')
wegingDF.index.name = None

wegingDF.loc[:,"weging_tov_b"] = np.nan


# In[89]:


branches = wegingDF["BedrijfstakkenBranchesSBI2008"].unique()
ont_percent = {}
l = []
for b in branches:
    
    temp = wegingDF.loc[wegingDF["BedrijfstakkenBranchesSBI2008"] == b, :]
    wx = temp["Wegingcoefficient_4"].unique()
    afzetx = temp["Afzet"].unique()
    
    print(afzetx, b)
    
    if len(afzetx) == 3 and len(wx) == 3:       
        buiten = wx[2]/wx[0]
        binnen = wx[1]/wx[0]  
        l.append(buiten+binnen)
        l.append(binnen)
        l.append(buiten)
    elif len(afzetx) == 2 and len(wx) == 2:      
        buiten = wx[1]/wx[0]
        binnen = wx[1]/wx[0]
        l.append(buiten+binnen)
        l.append(binnen)
        l.append(buiten)
    elif len(afzetx) == 1 and len(wx) == 1:
        buiten = 1
        binnen = 1
        l.append(buiten)
        l.append(binnen)
        l.append(buiten)
    elif len(afzetx) == 2 and len(wx) == 1:
        buiten = 1
        binnen = 1
        l.append(buiten)
        l.append(binnen)
        l.append(buiten)
    ont_percent[b] = l
    l = []


# In[ ]:


wegingDF.loc[wegingDF["BedrijfstakkenBranchesSBI2008"] == b, :]


# #### wegingscoifficient van overkoepelende industrieen.

# In[75]:



ub = [305700,346600,315805,328110,341600,317105,320005,312500,307610,348000,342400,307500]
ont_percent_ob = {}
l2 = []
summing = 0

for b in ub:
    
    temp = wegingDF.loc[wegingDF["BedrijfstakkenBranchesSBI2008"] == b, :]
    wx = temp["Wegingcoefficient_4"].unique()
   
    summing+=wx[0]

for b in ub:
    
    temp = wegingDF.loc[wegingDF["BedrijfstakkenBranchesSBI2008"] == b, :]
    wx = temp["Wegingcoefficient_4"].unique()
    ont_percent_ob[b] = wx[0]/summing


# #### newDF contains feature "weging_tov_b" in percentages

# In[73]:


dictO ={}
listO = []
branches = wegingDF["BedrijfstakkenBranchesSBI2008"].unique()

for b in branches:
    
    temp = wegingDF.loc[wegingDF["BedrijfstakkenBranchesSBI2008"] == b]
    value = ont_percent[b]

    for v in temp.values: 
        if v[0] == "A6":
            listO.append(value[0])
        elif v[0] == "A4":
            listO.append(value[1])
        elif v[0] == "A5":
            listO.append(value[2])
        
    dictO[b] = listO
    listO = []

newDF = pd.DataFrame(columns = wegingDF.columns.tolist())
    
for key,value in dictO.items():
    
    temp = wegingDF.loc[wegingDF["BedrijfstakkenBranchesSBI2008"] == key]

    temp = temp.assign(weging_tov_b=pd.Series(np.array(value)).values)
        
    newDF = newDF.append(temp)


# #### afzetgroter feature: 1 = meer binnenlands afzet, 0 = meer buitenlands afzet.

# In[77]:


dictO ={}
listO = []
branches = wegingDF["BedrijfstakkenBranchesSBI2008"].unique()

for b in branches:
    
    temp = wegingDF.loc[wegingDF["BedrijfstakkenBranchesSBI2008"] == b]
    value = ont_percent[b]
    
    binnen = 0
    
    if value[1] > value[2]:
        binnen = 1

    for v in temp.values: 
        listO.append(binnen)
         
    dictO[b] = listO
    listO = []
    
newDF2 = pd.DataFrame(columns = newDF.columns.tolist())

for key,value in dictO.items():
    
    temp = newDF.loc[newDF["BedrijfstakkenBranchesSBI2008"] == key]

    temp = temp.assign(afzetGroter=pd.Series(np.array(value)).values)
        
    newDF2 = newDF2.append(temp)


# #### Sparse feature, alleen binnenlands afzet.

# In[97]:


dictO ={}
listO = []
branches = newDF2["BedrijfstakkenBranchesSBI2008"].unique()

for b in branches:
    
    temp = newDF2.loc[newDF2["BedrijfstakkenBranchesSBI2008"] == b]
    afzety = temp["Afzet"].unique()
    
    alleenBinnen = 0
    
    if len(afzety) < 3:
        alleenBinnen = 1

    for v in temp.values: 
        listO.append(alleenBinnen)
         
    dictO[b] = listO
    listO = []
    
newDF3 = pd.DataFrame(columns = newDF2.columns.tolist())

for key,value in dictO.items():
    
    temp = newDF2.loc[newDF2["BedrijfstakkenBranchesSBI2008"] == key]

    temp = temp.assign(alleenBinnenlands=pd.Series(np.array(value)).values)
        
    newDF3 = newDF3.append(temp)


# In[98]:


newDF3.loc[newDF3["BedrijfstakkenBranchesSBI2008"] == 344400]

