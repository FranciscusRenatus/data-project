
# coding: utf-8

# In[2]:


import pandas as pd
import json


# # 1. Data exploration
# deep dive into the world of pandas

# ## 1.1 UntypedDataSet

# In[3]:


# initialiseer dataframe.
dfUntypedDataSet = pd.read_json("http://opendata.cbs.nl/ODataApi/OData/81975NED/UntypedDataSet?$top=1")


# In[4]:


# Loop tot alle data points in dataframe zitten met limiet van 10000 per keer.
top = 9668
skip = 1
while skip < 96681:
    big = dfUntypedDataSet.append(pd.read_json("http://opendata.cbs.nl/ODataApi/OData/81975NED/UntypedDataSet?$top=" + str(top) + "&$skip=" + str(skip)))
    skip = skip + 9668
    dfUntypedDataSet = big


# Nu hebben we de alle UntypedDataSet in een df, hiervan willen we alleen de values.

# In[5]:


# lijst maken van values in df.
DatasetUntypesList = dfUntypedDataSet["value"].tolist()


# In[6]:


# dataframe maken van lijst met beoogde values.
newDF = pd.DataFrame(DatasetUntypesList)


# In[7]:


newDF


# ## 1.2 Typed DataSet

# In[8]:


dftypedDataSet = pd.read_json("http://opendata.cbs.nl/ODataApi/OData/81975NED/TypedDataSet?$top=1")


# In[9]:


top = 9668
skip = 1
url = "http://opendata.cbs.nl/ODataApi/OData/81975NED/TypedDataSet"
while skip < 96681:
    big = dftypedDataSet.append(pd.read_json("http://opendata.cbs.nl/ODataApi/OData/81975NED/TypedDataSet?$top=" + str(top) + "&$skip=" + str(skip)))
    skip = skip + 9668
    dftypedDataSet = big


# In[10]:


# lijst maken van values in df.
DatasetTypedList = dftypedDataSet["value"].tolist()


# In[11]:


# dataframe maken van lijst met beoogde values.
newDF2 = pd.DataFrame(DatasetTypedList)


# In[12]:


newDF2


# In[13]:


import matplotlib.pyplot as plt


# In[51]:


jaarlozenummers = []
for i,datum in enumerate(newDF2["Perioden"].tolist()):
    if datum.find("MM") != -1:
        jaarlozenummers.append(i)

maanddf = newDF2.iloc[jaarlozenummers]
maanddf


# In[54]:


dfBedrijfstakkenBranchesSBI2008 = pd.read_json("http://opendata.cbs.nl/ODataApi/OData/81975NED/BedrijfstakkenBranchesSBI2008")
options = maanddf.BedrijfstakkenBranchesSBI2008.unique()
# able to make more than 20 graphs
plt.rcParams.update({'figure.max_open_warning': 0})
for bedrijfkey in options:
    # find the title for this branch
    for item in dfBedrijfstakkenBranchesSBI2008["value"]:
        if item["Key"] == bedrijfkey:
            titel = item["Title"]
    
    # alle data van deze bedrijfstak
    bedrijfstak = maanddf.loc[maanddf["BedrijfstakkenBranchesSBI2008"] == bedrijfkey]
    
    X = [int(datum[:4]) + int(datum[-2:])/12 for datum in bedrijfstak["Perioden"].tolist()]
    Y = bedrijfstak["ProducentenprijsindexPPI_1"].tolist()
    
    graph = [x for x in sorted(zip(X,Y))]
    # take the mean of the y coordinates of the coordinates whose date is the same
    newgraph = []
    for x,y in graph:
        graph.remove((x,y))
        n = 1
        if pd.notnull(y):
            for x2,y2 in graph:
                if x == x2 and pd.notnull(y2):
                    graph.remove((x2,y2))
                    n += 1
                    y += y2
        y = y/n
        newgraph.append((x,y))
#     print(newgraph)
    
    Xs = [x for x,y in sorted(newgraph)]
    Ys = [y for x,y in sorted(newgraph)]
    figure = plt.figure()
    ax1 = figure.add_subplot(111)
    plt.title(titel + " " + bedrijfkey)
    ax1.plot(Xs,Ys)
    


# ### 1.3TableInfos

# In[15]:


dfTableInfos = pd.read_json("http://opendata.cbs.nl/ODataApi/OData/81975NED/TableInfos")


# In[16]:


dfTableInfos["value"]


# ### 1.4 DataProperties

# In[17]:


dfDataProperties = pd.read_json("http://opendata.cbs.nl/ODataApi/OData/81975NED/DataProperties")
dfDataProperties["value"][0]


# ### 1.5 CategoryGroups

# In[18]:


dfCategoryGroups = pd.read_json("http://opendata.cbs.nl/ODataApi/OData/81975NED/CategoryGroups")
dfCategoryGroups["value"]


# ### 1.6 Afzet

# In[19]:


dfAfzet = pd.read_json("http://opendata.cbs.nl/ODataApi/OData/81975NED/Afzet")
dfAfzet["value"][0]


# ### 1.7 BedrijfstakkenBranchesSBI2008

# In[20]:


dfBedrijfstakkenBranchesSBI2008 = pd.read_json("http://opendata.cbs.nl/ODataApi/OData/81975NED/BedrijfstakkenBranchesSBI2008")
dfBedrijfstakkenBranchesSBI2008["value"][0]


# ### 1.8 Perioden

# In[21]:


dfPerioden = pd.read_json("http://opendata.cbs.nl/ODataApi/OData/81975NED/Perioden")
dfPerioden["value"][0]

