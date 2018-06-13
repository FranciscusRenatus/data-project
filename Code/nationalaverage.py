import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

def month(string):
    return int(string[:4]) + int(string[-2:])/12

def average():
    X = {}
    N = {}
    filepaths = []

    for file in os.listdir("../Data/DataFrames/DataFrames_Afzet_Branches"):
        filepaths.append(os.path.join("../Data/DataFrames/DataFrames_Afzet_Branches", file))

    for path in filepaths:
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
    return X

def titel(key):
    if key in ["A4","A5","A6"]:
        df = pd.read_csv("../Data/Afzet")
    else:
        df = pd.read_csv("../Data/Bedrijfstakken")
    return df["Title"].iloc[[str(k) for k in df["Key"]].index(key)]

if __name__ == "__main__":
    AVG = average()
    X = [x for x,y in sorted(zip(AVG,AVG.values()))]
    Y = [y for x,y in sorted(zip(AVG,AVG.values()))]
    plt.plot(X,Y)
    plt.plot([X[0]]+[X[-1]],[Y[0]]+[Y[-1]])
    plt.savefig("figures/A6average")