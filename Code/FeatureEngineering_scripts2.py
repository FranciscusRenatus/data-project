
# coding: utf-8

# ## info
# ### Script gericht op het benutten van de wegingscoeficient in dataset en verder analyseren van de data.
# #### Aantal aanmerkingen:
# ###### *Wegingscoefficienten worden pas vanaf 2005 gemeten
# ###### *Waarschijnlijk het beste resultaten met Overkoepelende industrieen in eigen data set te houden, te sparse anders ?
# ###### *Idee, maken van categorische data voor het indelen van branches in de bijhorende overkoepelende industrie.

# In[1]:


import pandas as pd
import json
from sklearn import preprocessing
import numpy as np
import matplotlib.pyplot as plt
import math
import sys


# In[2]:


mainDF = pd.read_csv("maanddf.csv")


# In[3]:


mainDF.fillna(0)


# In[4]:


wegingDF = mainDF.loc[mainDF["Wegingcoefficient_4"] != 0]
wegingDF = wegingDF.drop(["Unnamed: 0"], axis=1)
wegingDF = wegingDF.drop(["ID"], axis=1)
wegingDF.loc[:,"index"] = list(range(0,len(wegingDF)))
wegingDF = wegingDF.set_index('index')
wegingDF.index.name = None

wegingDF.loc[:,"weging_tov_b"] = np.nan


# In[5]:


branches = wegingDF["BedrijfstakkenBranchesSBI2008"].unique()
ont_percent = {}
l = []
for b in branches:
    
    temp = wegingDF.loc[wegingDF["BedrijfstakkenBranchesSBI2008"] == b, :]
    wx = temp["Wegingcoefficient_4"].unique()
    afzetx = temp["Afzet"].unique()
    
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


# #### wegingscoifficient van overkoepelende industrieen.

# In[6]:


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
    
ont_percent_ob


# #### hieronder wordt barchart voor ont percent ob gemaakt

# In[12]:


dfBedrijfstakkenBranchesSBI2008 = pd.read_json("http://opendata.cbs.nl/ODataApi/OData/81975NED/BedrijfstakkenBranchesSBI2008")
listBedrijfstakken = dfBedrijfstakkenBranchesSBI2008["value"].tolist()
pdBedrijfstakkenSBI = pd.DataFrame(listBedrijfstakken)
branchNamen = pdBedrijfstakkenSBI[["Key","Title"]]


# In[15]:


from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource, FactorRange
from bokeh.plotting import figure
import bokeh.palettes as pal
from bokeh.models import HoverTool


# In[18]:


vList = []
for key, val in ont_percent_ob.items():
    vList.append(round(float(val*100),2))

color = pal.viridis(12)
 
ub = ['305700','346600','315805','328110','341600','317105','320005','312500','307610','348000','342400','307500']
#names = ["Delfstoffenwinning", "Energievoorziening", "Hout- en bouwmaterialenindustrie", "Metalektro", "Meubelindustrie", "Papier- en grafische industrie", "Raffinaderijen en chemie", "Textielindustrie", "Voedings-, genotmiddelenindustrie", "Waterbedrijven en afvalbeheer", "Overige industrie", "Industrie"]
names = ["Delfstoffen", "Energie", "Bouw", "Metalektro", "Meubels", "Papier", "chemie", "Textiel", "Voeding", "Water", "Overige", "Industrie"]


# In[19]:


output_file("colormapped_bars.html")

source = ColumnDataSource(data=dict(branches=ub, values=vList, color=color, names=names))

hover = HoverTool(tooltips=[
    ("Industrie", "@names"),
    ("Aandeel", "@values")
])

p = figure(x_range=FactorRange(factors=ub), y_range=(0.00, 40.00), plot_height=250, title="Precentages weging tov totaal",
           toolbar_location=None, tools=[hover])

p.vbar(x='branches', top='values', width=0.9, color='color', source=source)

p.xgrid.grid_line_color = None
p.legend.orientation = "horizontal"
p.legend.location = "top_center"

show(p)


# #### newDF contains feature "weging_tov_b" in percentages

# In[7]:


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

# In[8]:


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

# In[9]:


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


# In[10]:


newDF3.head()


# #### Vanaf hier wordt er gepoogt regressie toe te passen

# In[11]:


newDF3 = newDF3.drop(['Wegingcoefficient_4', 'Perioden', 'BedrijfstakkenBranchesSBI2008'], axis=1)


# In[12]:


#newDF3 = newDF3.loc[newDF3["Afzet"]!="A6"]


# In[13]:


newDF3 = newDF3.fillna(0)


# In[14]:


newDF3["ont_maal_weging"] = newDF3["OntwikkelingTOV1MaandEerder_3"] * newDF3["weging_tov_b"]


# In[15]:


newDF3 = newDF3.drop(['Afzet'], axis=1)
newDF3["ppi"] = newDF3["ProducentenprijsindexPPI_1"]
newDF3 = newDF3.drop(['ProducentenprijsindexPPI_1'], axis=1)
newDF3.head()


# In[16]:


import numpy as np

import pandas as pd
from pandas import Series,DataFrame
from bokeh.layouts import gridplot, row, column

from bokeh.io import push_notebook, show, output_notebook
from bokeh.plotting import figure

from sklearn.datasets import load_boston


# In[17]:


# You can see what these names mean in the description that we printed at the start
print(newDF3.columns[:6])

figures = [figure() for _ in range(6)]
for index, fig in enumerate(figures):
    # Create a scatter-plot
    fig.scatter(newDF3[newDF3.columns[index]], newDF3["ppi"])
    
    ## Add some axis information
    fig.xaxis.axis_label = newDF3.columns[index]
    fig.yaxis.axis_label = "ppi"

    
show(gridplot(figures, ncols=2, plot_width=400, plot_height=250, toolbar_location=None))

