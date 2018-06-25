
# coding: utf-8

# In[2]:


import pandas as pd
import json
from sklearn import preprocessing

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


# In[3]:


# initialize dataframe
dftypedDataSet = pd.read_json("http://opendata.cbs.nl/ODataApi/OData/81975NED/TypedDataSet?$top=1")

# data ophalen
top = 9668
skip = 1
url = "http://opendata.cbs.nl/ODataApi/OData/81975NED/TypedDataSet"
while skip < 96681:
    big = dftypedDataSet.append(pd.read_json("http://opendata.cbs.nl/ODataApi/OData/81975NED/TypedDataSet?$top=" + str(top) + "&$skip=" + str(skip)))
    skip = skip + 9668
    dftypedDataSet = big

# lijst maken van values in df
DatasetTypedList = dftypedDataSet["value"].tolist()

# dataframe maken van lijst met beoogde values
newDF2 = pd.DataFrame(DatasetTypedList)


# jaren weghalen
jaarlozenummers = []
for i,datum in enumerate(newDF2["Perioden"].tolist()):
    if datum.find("JJ") != -1:
        jaarlozenummers.append(i)


# In[4]:


# scatDF maken.
CleanDF2 = newDF2.iloc[jaarlozenummers]
scatDF = CleanDF2.loc[CleanDF2["Wegingcoefficient_4"] > 0]


# In[6]:


#Data aanpassen, zie head van df.

#data veranderen
scatDF = scatDF.drop(["ID"], axis=1)
scatDF = scatDF.drop(["OntwikkelingTOV1JaarEerder_2"], axis=1)
scatDF = scatDF.drop(["OntwikkelingTOV1MaandEerder_3"], axis=1)
scatDF = scatDF.drop(["Wegingcoefficient_4"], axis=1)

#ontbreekt deels of 1 jaar is 0 procent.
scatDF = scatDF.loc[CleanDF2["BedrijfstakkenBranchesSBI2008"] != "310100"]
scatDF = scatDF.loc[CleanDF2["BedrijfstakkenBranchesSBI2008"] != "344400"]
scatDF = scatDF.loc[CleanDF2["BedrijfstakkenBranchesSBI2008"] != "312200"]
scatDF = scatDF.loc[CleanDF2["BedrijfstakkenBranchesSBI2008"] != "315200"]

# bevatten geen buitenlands afzet.
scatDF = scatDF.loc[CleanDF2["BedrijfstakkenBranchesSBI2008"] != "348000"]
scatDF = scatDF.loc[CleanDF2["BedrijfstakkenBranchesSBI2008"] != "348100"]

#index opnieuw instellen
scatDF["index"] = list(range(0,len(scatDF)))
scatDF = scatDF.set_index('index')
scatDF.index.name = None

scatDF = scatDF.fillna(0)


# In[7]:


#Jaren eruithalen
periodes = scatDF["Perioden"]
jaren = []

for p in periodes:
    jaren.append(p[0:4])


# In[8]:


#toevoegen jaren zodat we kunnen gaan sommeren per jaar.
scatDF["jaren"] = jaren
scatDF = scatDF.drop(["Perioden"], axis=1)
scatDF = scatDF.loc[scatDF["jaren"] != "2017"]


# In[9]:


#categorische data binnenland/buitenlands nummer geven.
dff = scatDF["Afzet"]
afzet = []

for a in dff:
    if a == "A6":
        afzet.append(0)
    elif a == "A4":
        afzet.append(1)
    elif a == "A5":
        afzet.append(2)
scatDF["AfzetN"] = afzet
scatDF = scatDF.drop(["Afzet"], axis=1)


# In[10]:


# Om alle overkoepelende industrieen samen te nemen.
scatDF['OB'] = 0

#1
delftstoffenwinning = ['305800', '306300', '320000']

#2
energievoorziening = ['346700']

#3
houtbouwindustrie = ['315800', '324600']

#4
metalektro =['34440', '330300', '800002', '336500', '332900',
            '332905', '332910', '334800', '328105', '328100',
            '339200']

#5
papiergrafisch = ['318600', '317100']

#6
raffinaderijenchemie = ['323700', '323200', '320700', '320705']

#7
texkleledindustrie = ['315200', '314000', '312500']

#8
voedinggenotsindustrie = ['312100', '310200', '310100', '309700',
                        '309400', '309100', '308800', '308500',
                        '308400', '308000', '307900', '307800', 
                        '311000', '310000', '309600', '309300', 
                        '309000', '308700', '308600', '308300', 
                        '308100', '307700', '312200', '311300',
                        '307600']

#9
waterafval = ['348100']

#overkoepelende lijst die overkoepelende industrie overkoepelt
koepelkoepellijst = ['305700', '346600', '315805', '328110', '341600', '317105', '320005',
                  '312500', '307610', '348000', '342400', '307500']


KoepelLijst = [delftstoffenwinning, energievoorziening, houtbouwindustrie, metalektro,
            papiergrafisch, raffinaderijenchemie, texkleledindustrie, voedinggenotsindustrie, koepelkoepellijst]

i = 1
for Lijst in KoepelLijst:
    for ID in Lijst:
        scatDF.loc[scatDF['BedrijfstakkenBranchesSBI2008'] == ID, 'OB'] = i
    i += 1
    
scatDF = scatDF.loc[scatDF['AfzetN'] != 0]

scatDF = scatDF.loc[scatDF['OB'] == 9]

# KoepelDF.to_csv('KoepelDF.csv')
#scatDF


# In[11]:


scatDF["AfzetN"] = scatDF["AfzetN"].astype(str)


# ### heatmapping Binnenlands

# In[23]:


# Namen van industrieen erbij halen
dfBedrijfstakkenBranchesSBI2008 = pd.read_json("http://opendata.cbs.nl/ODataApi/OData/81975NED/BedrijfstakkenBranchesSBI2008")
listBedrijfstakken = dfBedrijfstakkenBranchesSBI2008["value"].tolist()
pdBedrijfstakkenSBI = pd.DataFrame(listBedrijfstakken)
branchNamen = pdBedrijfstakkenSBI[["Key","Title"]]

d = pdBedrijfstakkenSBI.drop(["CategoryGroupID","Description"], axis=1)
#d.loc[d["Key"]==305700]


# In[24]:


# dictionary maken van key en industrie naam.
dd = {k: g["Title"].tolist() for k,g in d.groupby("Key")}


# In[28]:


ub = [305700,346600,315805,328110,341600,317105,320005,312500,307610,348000,342400,307500]
for i in ub:
    print(dd[str(i)])


# In[12]:


# dict bouwen voor de dataframe df
jaren = scatDF["jaren"].unique().tolist()
dictt1 = {}
dictt1["j"] = jaren

branches = scatDF["BedrijfstakkenBranchesSBI2008"].unique()

for b in branches:
    
    naam = dd[b]
    tempOnt = scatDF.loc[scatDF["BedrijfstakkenBranchesSBI2008"]== b]
    tempOnt = tempOnt.loc[tempOnt["AfzetN"]=="2"]
    tempOnt = tempOnt["ProducentenprijsindexPPI_1"]
    tempOnt = pd.to_numeric(tempOnt).tolist()
    
    dictt1[naam[0]] = tempOnt


# In[13]:


# bouwen van de dataframe
df = pd.DataFrame(data=dictt1)
df['j'] = df['j'].astype(str)
df = df.set_index('j')
df.columns.name = 'B'

jaren = list(df.index)
b = list(df.columns)

df = pd.DataFrame(df.stack(), columns=['ppi']).reset_index()


# In[224]:


colors = list(reversed(["#75968f", "#a5bab7", "#c9d9d3", "#e2e2e2", "#dfccce", "#ddb7b1", "#cc7878", "#933b41", "#550b1d"]))
mapper = LinearColorMapper(palette=colors, low=50, high=df.ppi.max())

source = ColumnDataSource(df)

TOOLS = "hover,save,pan,box_zoom,reset,wheel_zoom"

p = figure(title="Buitenlands PPI per jaar ({0} - {1})".format(jaren[0], jaren[-1]),
           x_range=jaren, y_range=list(reversed(b)),
           x_axis_location="above", plot_width=1250, plot_height=600,
           tools=TOOLS, toolbar_location='below')

p.grid.grid_line_color = None
p.axis.axis_line_color = None
p.axis.major_tick_line_color = None
p.axis.major_label_text_font_size = "5pt"
p.axis.major_label_standoff = 0
p.xaxis.major_label_orientation = pi / 3

p.rect(x='j', y='B', width=1, height=1,
       source=source,
       fill_color={'field': 'ppi', 'transform': mapper},
       line_color=None)

color_bar = ColorBar(color_mapper=mapper, major_label_text_font_size="5pt",
                     ticker=BasicTicker(desired_num_ticks=len(colors)),
                     formatter=PrintfTickFormatter(format="%d%%"),
                     label_standoff=6, border_line_color=None, location=(0, 0))
p.add_layout(color_bar, 'right')

p.select_one(HoverTool).tooltips = [
     ('Jaar', '@j'),
     ('PPI', '@ppi%'),
]

show(p)      # show the plot


# In[14]:


df.head()


# In[15]:


df["ppi"]


# In[12]:


from bokeh.plotting import figure, show, output_file

colormap = {'1': 'red', '2': 'blue'}
scatDF['color'] = scatDF['AfzetN'].map(lambda x: colormap[x])

output_file("afzet.html", title="test")

p = figure(title = "Afzet Binnenlands en Buitenlands")
p.xaxis.axis_label = 'tijd'
p.yaxis.axis_label = "pemPPI"

p.circle(scatDF["jaren"], scatDF["ProducentenprijsindexPPI_1"],
color=scatDF["color"], fill_alpha=0.2, size=3, )

show(p)

