
# coding: utf-8

# In[1]:


import pandas as pd
import json
from sklearn import preprocessing
import numpy as np
import matplotlib.pyplot as plt
import math

from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource, FactorRange
from bokeh.plotting import figure
import bokeh.palettes as pal


# In[ ]:


# Here data opzetten
#xaxis = X
#yaxis = y
#color = pal.viridis(12)
#legenda = names


# In[ ]:


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

