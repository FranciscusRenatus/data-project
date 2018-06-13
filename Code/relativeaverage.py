import nationalaverage as avg
import pandas as pd
import matplotlib.pyplot as plt
import os

AVG = avg.average()
bedrijfstakken = pd.read_csv("../Data/bedrijfstakken")
afzet = pd.read_csv("../Data/Afzet")

for file in os.listdir("../Data/DataFrames/DataFrames_Afzet_Branches"):
    path = os.path.join("../Data/DataFrames/DataFrames_Afzet_Branches", file)
    df = pd.read_csv(path)
    graph = []

    for prijs,datum in zip(df["ProducentenprijsindexPPI_1"],df["Perioden"].tolist()):
        datum = avg.month(datum)
        prijsverschil = prijs - AVG[datum]
        graph.append((datum,prijsverschil))
    
    for i, key in enumerate(bedrijfstakken["Key"]):
        if str(key) == str(file[:6]):
            title = bedrijfstakken["Title"].tolist()[i]
    for i, key in enumerate(afzet["Key"]):
        if str(key) == str(file[-2:]):
            title = title + ", " + afzet["Title"].tolist()[i]

    figure = plt.figure()
    ax1 = figure.add_subplot(111)
    ax1.set_xlim(1980,2018)
    ax1.set_ylim(-50,100)
    ax1.plot([x[0] for x in graph],[y[1] for y in graph])
    ax1.set_title(title)
    figure.savefig("avgfigures/" + file, dpi = 200, bbox_inches='tight')