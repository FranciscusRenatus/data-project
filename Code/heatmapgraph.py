import pandas as pd
import numpy as np
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

df = pd.read_csv("industryheatmap.csv").drop(columns="Unnamed: 0")
b = list(df["B1"].unique())

colors = ["#0000AA", "#0055DD", "#00BBFF", "#FFFFFF", "#00FF00","#00dd00","#008800"]
mapper = LinearColorMapper(palette=colors, low=min(df["corr"].tolist()), high=max(df["corr"].tolist()))

source = ColumnDataSource(df)

TOOLS = "hover,save,box_zoom,reset,wheel_zoom"

p = figure(title="heatmap correlatie",
           x_range=b, y_range=list(reversed(b)),
           x_axis_location="above", plot_width=1250, plot_height=600,
           tools=TOOLS, toolbar_location='below')

p.grid.grid_line_color = None
p.axis.axis_line_color = None
p.axis.major_tick_line_color = None
p.axis.major_label_text_font_size = "5pt"
p.axis.major_label_standoff = 0
p.xaxis.major_label_orientation = pi / 3

p.rect(x='B1', y='B2', width=1, height=1,
       source=source,
       fill_color={'field': 'corr', 'transform': mapper},
       line_color=None)

color_bar = ColorBar(color_mapper=mapper, major_label_text_font_size="5pt",
                     ticker=BasicTicker(desired_num_ticks=len(colors)),
                     formatter=PrintfTickFormatter(format="%f"),
                     label_standoff=6, border_line_color=None, location=(0, 0))
p.add_layout(color_bar, 'right')

p.select_one(HoverTool).tooltips = [
     ('B1', '@B1'),
     ('B2', '@B2'),
     ('corr', '@corr'),
]

show(p)