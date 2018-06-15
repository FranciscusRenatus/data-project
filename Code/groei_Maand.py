
# coding: utf-8

# In[8]:


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


# In[18]:


mainDF = pd.read_csv("maanddf.csv")


# In[19]:



perioden2 = mainDF["Perioden"].unique()
branches = mainDF["BedrijfstakkenBranchesSBI2008"].unique()
dict2 = {}
dict2['Maanden'] = perioden2

for b in branches:
    tempOnt = mainDF.loc[mainDF["BedrijfstakkenBranchesSBI2008"] == b ]
    tempOnt = tempOnt.loc[tempOnt["Afzet"] == "A6"]
    tempOnt = tempOnt["OntwikkelingTOV1MaandEerder_3"]
    tempOnt = pd.to_numeric(tempOnt).tolist()
    dict2[str(b)] = tempOnt


# In[20]:


df = pd.DataFrame(data=dict2)
df['Maanden'] = df['Maanden'].astype(str)
df = df.set_index('Maanden')
df.columns.name = 'B'
df = df.fillna(0)

maanden = list(df.index)
b = list(df.columns)

df = pd.DataFrame(df.stack(), columns=['Ont']).reset_index()


# In[26]:


# this is the colormap from the original NYTimes plot
colors = list(reversed(["#75968f", "#a5bab7", "#c9d9d3", "#e2e2e2", "#dfccce", "#ddb7b1", "#cc7878", "#933b41", "#550b1d"]))
mapper = LinearColorMapper(palette=colors, low=df.Ont.min(), high=df.Ont.max())

source = ColumnDataSource(df)

TOOLS = "hover,save,pan,box_zoom,reset,wheel_zoom"

p = figure(title="ontwikkeling per maand ({0} - {1})".format(datums[0], datums[-1]),
           x_range=maanden, y_range=list(reversed(b)),
           x_axis_location="above", plot_width=900, plot_height=400,
           tools=TOOLS, toolbar_location='below')

p.grid.grid_line_color = None
p.axis.axis_line_color = None
p.axis.major_tick_line_color = None
p.axis.major_label_text_font_size = "5pt"
p.axis.major_label_standoff = 0
p.xaxis.major_label_orientation = pi / 3

p.rect(x='Maanden', y='B', width=1, height=1,
       source=source,
       fill_color={'field': 'Ont', 'transform': mapper},
       line_color=None)

color_bar = ColorBar(color_mapper=mapper, major_label_text_font_size="5pt",
                     ticker=BasicTicker(desired_num_ticks=len(colors)),
                     formatter=PrintfTickFormatter(format="%d%%"),
                     label_standoff=6, border_line_color=None, location=(0, 0))
p.add_layout(color_bar, 'right')

p.select_one(HoverTool).tooltips = [
     ('date', '@Maanden'),
     ('rate', '@Ont%'),
]

show(p)      # show the plot


# In[25]:


type(mainDF["Perioden"].unique()[0])

