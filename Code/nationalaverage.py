import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

filepaths = []

for file in os.listdir("../Data/DataFrames_Afzet_Branches"):
    filepaths.append(os.path.join("../Data/DataFrames_Afzet_Branches", file))

def month(string):
    return int(string[:4]) + int(string[-2:])/12

X = {}
N = {}

for path in filepaths:
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
    
plt.plot([x for x,y in sorted(zip(X,X.values()))],[y for x,y in sorted(zip(X,X.values()))])
plt.savefig("figures/average")