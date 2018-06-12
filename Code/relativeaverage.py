import nationalaverage as avg
import pandas as pd
import matplotlib.pyplot as plt
import os

AVG = avg.average()

for file in os.listdir("../Data/DataFrames_Afzet_Branches"):
    path = os.path.join("../Data/DataFrames_Afzet_Branches", file)
    df = pd.read_csv(path)
    graph = []

    for prijs,datum in zip(df["ProducentenprijsindexPPI_1"],df["Perioden"].tolist()):
        graph.append((datum,prijs))
    
    figure = plt.figure()
    ax1 = figure.add_subplot(111)
    ax1.plot([x[0] for x in graph],[y[1] for y in graph])
    size = figure.get_size_inches()
    figure.set_size_inches(size[0]*2,size[1]*2)
    figure.savefig("avgfigures/" + file, dpi = 1000, bbox_inches='tight')