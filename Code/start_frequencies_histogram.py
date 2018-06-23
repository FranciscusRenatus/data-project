import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

filepaths = []

for file in os.listdir("../Data/DataFrames/DataFrames_Afzet_Branches"):
    filepaths.append(os.path.join("../Data/DataFrames/DataFrames_Afzet_Branches", file))

def month(string):
    return int(string[:4]) + int(string[-2:])/12

X = {}

for path in filepaths:
    try:
        df = pd.read_csv(path)
        df.iloc[0]
        datum = month(str(df["Perioden"][0]))
        if datum in X:
            X[datum] += 1
        else:
            X[datum] = 1
    except IndexError:
        pass
    continue
dates = X.keys()
Y = X.values()
print(X)

#fig = plt.hist(dates, bins = 3)
plt.bar(dates, Y, color='g')
#plt.plot([x for x,y in sorted(zip(X,X.values()))],[y for x,y in sorted(zip(X,X.values()))])
plt.savefig("../Docs/start_frequencies")
plt.show()