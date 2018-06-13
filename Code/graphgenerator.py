import pandas as pd
import json
import matplotlib.pyplot as plt
import os
import nationalaverage as avg

def main():
    # able to make more than 20 graphs at a time without a warning
    plt.rcParams.update({'figure.max_open_warning': 0})
    a = 4
    n = 0

    for file in os.listdir("../Data/DataFrames/DataFrames_Afzet_Branches"):
        path = os.path.join("../Data/DataFrames/DataFrames_Afzet_Branches", file)
        df = pd.read_csv(path)
        graph = []

        for i in range(len(df)):
            item = df.iloc[i]
            graph.append((item["Perioden"],item["ProducentenprijsindexPPI_1"]))
            
        X = [avg.month(x) for x,y in sorted(graph)]
        Y = [y for x,y in sorted(graph)]
        plt.figure(n)
        plt.plot(X,Y, label = avg.titel("A"+str(a)))

        a += 1
        # if this is the end of this figure
        if a > 6:
            a = 4
            n += 1
            plt.title(avg.titel(file[:6]) + ", " + file[:6])
            plt.xlim(1980, 2019)
            plt.ylim(0, 160)
            plt.legend()

            # make the title
            space = False
            titel = ""
            for ch in avg.titel(file[:6]):
                if space and ch != ".":
                    titel += ch
                if ch == " ":
                    space = True
            plt.savefig("updatedfigures/" + titel)

if __name__ == "__main__":
    main()