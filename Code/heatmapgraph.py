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
from colour import Color

df = pd.read_csv("industryheatmap.csv").drop(columns="Unnamed: 0")
b = list(df["B1"].unique())

blue = Color("blue")
white = Color("white")
green = Color("green")
colors = [c.hex_l for c in blue.range_to(white,25)] + [c.hex_l for c in white.range_to(green,25)]
mapper = LinearColorMapper(palette=colors, low=min(df["corr"].tolist()), high=max(df["corr"].tolist()))

source = ColumnDataSource(df)
#.loc[df["B1"] == "B Delfstoffenwinning"]

TOOLS = "hover,save,box_zoom,reset,wheel_zoom"

p = figure(title="heatmap correlatie",
           x_range=b, y_range=list(reversed(b)),
           x_axis_location="above", plot_width=1000, plot_height=1000,
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