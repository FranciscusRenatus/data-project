import pandas as pd
import json
import matplotlib.pyplot as plt

# able to make more than 20 graphs at one time
plt.rcParams.update({'figure.max_open_warning': 0})
for bedrijfkey in maanddf.BedrijfstakkenBranchesSBI2008.unique():
    # find the title for this branch
    for item in dfBedrijfstakkenBranchesSBI2008["value"]:
        if int(item["Key"]) == int(bedrijfkey):
            titel = item["Title"]
            break
    
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
    plt.title(str(titel) + ", " + str(bedrijfkey))
    ax1.plot(Xs,Ys)