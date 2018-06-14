import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

bedrijfstakken = pd.read_csv("../Data/bedrijfstakken")
afzet = pd.read_csv("../Data/Afzet")

def average():
    X = {}
    N = {}
    filepaths = []

    for file in os.listdir("../Data/DataFrames/DataFrames_Afzet_Branches"):
        filepaths.append(os.path.join("../Data/DataFrames/DataFrames_Afzet_Branches", file))

    for path in filepaths:

        graph = []

        if path[-2:] == "A6":

            df = pd.read_csv(path)

            for i,prijs in enumerate(df["ProducentenprijsindexPPI_1"].tolist()):
                datum = month(df["Perioden"][i])
                if datum in X:
                    X[datum] += prijs
                else:
                    X[datum] = prijs
                if datum in N:
                    N[datum] += 1
                else:
                    N[datum] = 1

            for datum in X:
                X[datum] = X[datum]/N[datum]
                graph.append((datum,X[datum]))

            for i, key in enumerate(bedrijfstakken["Key"]):
                if str(key) == str(path[:6]):
                    title = bedrijfstakken["Title"].tolist()[i]

            for i, key in enumerate(afzet["Key"]):
                if str(key) == str(path[-2:]):
                    title = title + ", " + afzet["Title"].tolist()[i]
                    

            figure = plt.figure()
            ax1 = figure.add_subplot(111)
            ax1.set_xlim(1980,2018)
            ax1.set_ylim(-50,100)
            ax1.plot([x[0] for x in graph],[y[1] for y in graph])
            ax1.set_title(title)
            figure.savefig("afzetVerschil/" + file, dpi = 200, bbox_inches='tight')
