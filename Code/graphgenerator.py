import pandas as pd
import json
import matplotlib.pyplot as plt
import os
import nationalaverage as avg

def generate(starten,einden):
    # able to make more than 20 graphs at a time without a warning
    plt.rcParams.update({'figure.max_open_warning': 0})

    for n,file in enumerate(os.listdir("../Data/DataFrames/DataFrames_Afzet_Branches")):
        path = os.path.join("../Data/DataFrames/DataFrames_Afzet_Branches", file)
        df = pd.read_csv(path)
        graph = []

        if not df.empty:
            for i in range(len(df)):
                item = df.iloc[i]
                graph.append((item["Perioden"],item["ProducentenprijsindexPPI_1"]))
                
            X = [avg.month(x) for x,y in sorted(graph)]
            Y = [y for x,y in sorted(graph)]
            start = X.index(starten[n])
            eind = X.index(einden[n])

            plt.figure(n)
            plt.plot(X[:start+1],Y[:start+1], color = "blue")
            plt.plot(X[start:eind],Y[start:eind], color = "red")
            plt.plot(X[eind-1:],Y[eind-1:], color = "blue")
            plt.title(avg.titel(file[:6]) + ", " + avg.titel(file[-2:]))
            plt.xlim(1980, 2019)
            plt.xlabel("jaar")
            plt.ylim(0, 160)
            plt.ylabel("producentenprijsindex")
            plt.savefig("../Docs/Dip_Figures/" + file)

# if __name__ == "__main__":
#     generate()