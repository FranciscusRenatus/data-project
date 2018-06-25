import pandas as pd
import json
import matplotlib.pyplot as plt
import os
import nationalaverage as avg

def generate(starten,einden,files):
    # able to make more than 20 graphs at a time without a warning
    plt.rcParams.update({'figure.max_open_warning': 0})

    for n,file in enumerate(files):
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
            if eind < start:
                start,eind = eind,start

            plt.figure(n)
            plt.plot(X[:start],Y[:start], color = "blue")
            plt.plot(X[start-1:eind+1],Y[start-1:eind+1], color = "red")
            plt.plot(X[eind:],Y[eind:], color = "blue")
            plt.plot([start,start],[0,160])
            plt.title(avg.titel(file[:6]) + ", " + avg.titel(file[-2:]))
            plt.xlim(1980, 2019)
            plt.xlabel("jaar")
            plt.ylim(0, 160)
            plt.ylabel("producentenprijsindex")
            plt.savefig("../Docs/relativedipfigures/" + file + " " + "".join(ch if ch != "." else "," for ch in str(starten[n])))

# if __name__ == "__main__":
#     generate()