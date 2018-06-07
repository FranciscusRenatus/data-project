import pandas as pd
import json
import matplotlib.pyplot as plt

# initialiseer dataframe.
dftypedDataSet = pd.read_json("http://opendata.cbs.nl/ODataApi/OData/81975NED/TypedDataSet?$top=1")

top = 9668
skip = 1
url = "http://opendata.cbs.nl/ODataApi/OData/81975NED/TypedDataSet"
while skip < 96681:
    big = dftypedDataSet.append(pd.read_json("http://opendata.cbs.nl/ODataApi/OData/81975NED/TypedDataSet?$top=" + str(top) + "&$skip=" + str(skip)))
    skip = skip + 9668
    dftypedDataSet = big

# lijst maken van values in df.
DatasetTypedList = dftypedDataSet["value"].tolist()
DF = pd.DataFrame(DatasetTypedList)
DF

# maak een nieuwe df die geen gemmidelde jaarmetingen bevat
jaarlozenummers = []
for i,datum in enumerate(DF["Perioden"].tolist()):
    if datum.find("MM") != -1:
        jaarlozenummers.append(i)

maanddf = DF.iloc[jaarlozenummers]
# maanddf

# get information from all the other tables
dfTableInfos = pd.read_json("http://opendata.cbs.nl/ODataApi/OData/81975NED/TableInfos")
dfTableInfos["value"]

dfDataProperties = pd.read_json("http://opendata.cbs.nl/ODataApi/OData/81975NED/DataProperties")
dfDataProperties["value"][0]

dfCategoryGroups = pd.read_json("http://opendata.cbs.nl/ODataApi/OData/81975NED/CategoryGroups")
dfCategoryGroups["value"]

dfAfzet = pd.read_json("http://opendata.cbs.nl/ODataApi/OData/81975NED/Afzet")
dfAfzet["value"][0]

dfBedrijfstakkenBranchesSBI2008 = pd.read_json("http://opendata.cbs.nl/ODataApi/OData/81975NED/BedrijfstakkenBranchesSBI2008")
dfBedrijfstakkenBranchesSBI2008["value"][0]

dfPerioden = pd.read_json("http://opendata.cbs.nl/ODataApi/OData/81975NED/Perioden")
dfPerioden["value"][0]

# able to make more than 20 graphs at one time
plt.rcParams.update({'figure.max_open_warning': 0})

for bedrijfkey in maanddf.BedrijfstakkenBranchesSBI2008.unique():

    # find the title for this branch
    for item in dfBedrijfstakkenBranchesSBI2008["value"]:
        if item["Key"] == bedrijfkey:
            titel = item["Title"]
    
    # alle data van deze bedrijfstak
    bedrijfstak = maanddf.loc[maanddf["BedrijfstakkenBranchesSBI2008"] == bedrijfkey]
    
    # convert dates to numbers
    X = [int(datum[:4]) + int(datum[-2:])/12 for datum in bedrijfstak["Perioden"].tolist()]

    # what the graph is plotted out against
    Y = bedrijfstak["ProducentenprijsindexPPI_1"].tolist()
    
    # zip the information to keep the right coordinates together
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
    plt.title(titel + ", " + bedrijfkey)
    ax1.plot(Xs,Ys)