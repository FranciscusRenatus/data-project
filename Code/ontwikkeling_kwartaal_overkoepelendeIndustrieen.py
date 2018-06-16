
# coding: utf-8

# In[1]:


import pandas as pd
import json
from sklearn import preprocessing
import numpy as np
import matplotlib.pyplot as plt
import math

from math import pi

from bokeh.io import show
from bokeh.models import (
    ColumnDataSource,
    HoverTool,
    LinearColorMapper,
    BasicTicker,
    PrintfTickFormatter,
    ColorBar,
)
from bokeh.plotting import figure


# In[6]:


mainDF = pd.read_csv("maanddf.csv")


# In[7]:


# Kwartaal periodes
periodes = mainDF["Perioden"].unique()
newPer = []
count = 0
kwartaal = 1
for p in periodes:
    if count == 0:
        newPer.append(p[0:4]+"k:"+ str(kwartaal))
        count += 1
    elif count == 2:
        kwartaal += 1
        count = 0
    elif count == 1:
        count += 1
    if kwartaal == 5:
        kwartaal = 1


# In[18]:


dict1 = {}
x = newPer
dict1["Kwartalen"] = x

branches = list([305700, 346600, 315200, 328110, 341600, 317105, 320005, 312505, 307610, 348000, 342400, 307500])


# In[19]:


# kwartalen
for b in branches:
    
    kwart = []
    count = 1
    temp = 0
    
    tempOnt = mainDF.loc[mainDF["BedrijfstakkenBranchesSBI2008"]== b]
    tempOnt = tempOnt.loc[tempOnt["Afzet"]=="A6"]
    tempOnt = tempOnt["OntwikkelingTOV1MaandEerder_3"]
    tempOnt = pd.to_numeric(tempOnt).tolist()
    
    for ont in tempOnt:
        temp += ont
        if count == 3:
            n = round((temp/count),2)
            kwart.append(n)
            temp = 0
            count = 1
        elif count == 2:
            count += 1
        elif count == 1:
            count += 1
    
    dict1[str(b)] = np.array(kwart)


# In[21]:


df = pd.DataFrame(data=dict1)
df = df.fillna(0)
df['Kwartalen'] = df['Kwartalen'].astype(str)
df = df.set_index('Kwartalen')
df.columns.name = 'B'

kwartalen = list(df.index)
b = list(df.columns)

df = pd.DataFrame(df.stack(), columns=['Ont']).reset_index()


# In[22]:


# this is the colormap from the original NYTimes plot
colors = list(reversed(["#75968f", "#a5bab7", "#c9d9d3", "#e2e2e2", "#dfccce", "#ddb7b1", "#cc7878", "#933b41", "#550b1d"]))
mapper = LinearColorMapper(palette=colors, low=df.Ont.min(), high=df.Ont.max())

source = ColumnDataSource(df)

TOOLS = "hover,save,pan,box_zoom,reset,wheel_zoom"

p = figure(title="Ontwikkeling per kwartaal ({0} - {1})".format(kwartalen[0], kwartalen[-1]),
           x_range=kwartalen, y_range=list(reversed(b)),
           x_axis_location="above", plot_width=1250, plot_height=600,
           tools=TOOLS, toolbar_location='below')

p.grid.grid_line_color = None
p.axis.axis_line_color = None
p.axis.major_tick_line_color = None
p.axis.major_label_text_font_size = "5pt"
p.axis.major_label_standoff = 0
p.xaxis.major_label_orientation = pi / 3

p.rect(x='Kwartalen', y='B', width=1, height=1,
       source=source,
       fill_color={'field': 'Ont', 'transform': mapper},
       line_color=None)

color_bar = ColorBar(color_mapper=mapper, major_label_text_font_size="5pt",
                     ticker=BasicTicker(desired_num_ticks=len(colors)),
                     formatter=PrintfTickFormatter(format="%d%%"),
                     label_standoff=6, border_line_color=None, location=(0, 0))
p.add_layout(color_bar, 'right')

p.select_one(HoverTool).tooltips = [
     ('Kwartalen', '@Kwartalen'),
     ('Ont', '@Ont%'),
]

show(p)      # show the plot

