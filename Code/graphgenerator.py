import pandas as pd
import json
import matplotlib.pyplot as plt

DF = pd.read_csv("dataframe.csv")

# able to make more than 20 graphs at one time
# plt.rcParams.update({'figure.max_open_warning': 0})
# for bedrijfkey in maanddf.BedrijfstakkenBranchesSBI2008.unique():
#     # find the title for this branch
    # for item in dfBedrijfstakkenBranchesSBI2008["value"]:
    #     if int(item["Key"]) == int(bedrijfkey):
    #         titel = item["Title"]
    #         break
    
#     # alle data van deze bedrijfstak
#     bedrijfstak = maanddf.loc[maanddf["BedrijfstakkenBranchesSBI2008"] == bedrijfkey]
    
    # # convert dates to numbers
    # X = [int(datum[:4]) + int(datum[-2:])/12 for datum in bedrijfstak["Perioden"].tolist()]

    # # what the graph is plotted out against
    # Y = bedrijfstak["ProducentenprijsindexPPI_1"].tolist()
    
    # # zip the information to keep the right coordinates together
    # graph = [x for x in sorted(zip(X,Y))]

#     # take the mean of the y coordinates of the coordinates whose date is the same
#     newgraph = []
#     for x,y in graph:
#         graph.remove((x,y))
#         n = 1
#         if pd.notnull(y):
#             for x2,y2 in graph:
#                 if x == x2 and pd.notnull(y2):
#                     graph.remove((x2,y2))
#                     n += 1
#                     y += y2
#         y = y/n
#         newgraph.append((x,y))
# #     print(newgraph)
    
#     Xs = [x for x,y in sorted(newgraph)]
#     Ys = [y for x,y in sorted(newgraph)]
#     figure = plt.figure()
#     ax1 = figure.add_subplot(111)
#     plt.title(str(titel) + ", " + str(bedrijfkey))
#     ax1.plot(Xs,Ys)

maanddf = pd.read_csv("../data/maanddf.csv")
dfBedrijfstakkenBranchesSBI2008 = pd.DataFrame(pd.read_json("http://opendata.cbs.nl/ODataApi/OData/81975NED/BedrijfstakkenBranchesSBI2008")["value"])

for bedrijfkey in maanddf.BedrijfstakkenBranchesSBI2008.unique():
    bedrijfstak = maanddf.loc[maanddf["BedrijfstakkenBranchesSBI2008"] == bedrijfkey]

    for item in dfBedrijfstakkenBranchesSBI2008["value"]:
        if int(item["Key"]) == int(bedrijfkey):
            titel = "".join(ch for ch in item["Title"] if ch != ".")
            break
    
    figure = plt.figure()
    i = 0
    for afzet in ["A4","A5","A6"]:
        i += 1
        tijdlijn = bedrijfstak.loc[bedrijfstak["Afzet"] == afzet]
        X = []
        Y = []
        for i in range(len(tijdlijn)):
            item = tijdlijn.iloc[i]
            datum = int(item["Perioden"][:4]) + int(item["Perioden"][-2:])/12
            X.append(datum)
            Y.append(item["ProducentenprijsindexPPI_1"])
        ax1 = figure.add_subplot(110+i)
        ax1.plot(X,Y)
    size = figure.get_size_inches()
    figure.set_size_inches(size[0]*2,size[1]*2)
    figure.savefig("figures/" + titel, dpi = 1000, bbox_inches='tight')