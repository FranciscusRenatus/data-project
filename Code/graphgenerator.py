import pandas as pd
import json
import matplotlib.pyplot as plt

maanddf = pd.read_csv("../data/maanddf.csv")

dit = {}
# able to make more than 20 graphs at one time
plt.rcParams.update({'figure.max_open_warning': 0})
for bedrijfkey in maanddf.BedrijfstakkenBranchesSBI2008.unique():
    # alle data van deze bedrijfstak
    bedrijfstak = maanddf.loc[maanddf["BedrijfstakkenBranchesSBI2008"] == bedrijfkey]
    for afzet in ["A4","A5","A6"]:
        tijdlijn = bedrijfstak.loc[bedrijfstak["Afzet"] == afzet]
        for i in range(len(tijdlijn)):
            item = tijdlijn.iloc[i]
            if item["Perioden"] in dit:
                dit[item["Perioden"]] = item["ProducentenprijsindexPPI_1"]
            
        # convert dates to numbers
        [for datum in [int(datum[:4]) + int(datum[-2:])/12 for datum in bedrijfstak["Perioden"].tolist()]]

        # what the graph is plotted out against
        Y = bedrijfstak["ProducentenprijsindexPPI_1"].tolist()
    
figure = plt.figure()
ax1 = figure.add_subplot(111)
plt.title(str(titel) + ", " + str(bedrijfkey))
ax1.plot(Xs,Ys)

# dfBedrijfstakkenBranchesSBI2008 = pd.DataFrame(pd.read_json("http://opendata.cbs.nl/ODataApi/OData/81975NED/BedrijfstakkenBranchesSBI2008")["value"])

# for bedrijfkey in maanddf.BedrijfstakkenBranchesSBI2008.unique():
#     bedrijfstak = maanddf.loc[maanddf["BedrijfstakkenBranchesSBI2008"] == bedrijfkey]

#     for item in dfBedrijfstakkenBranchesSBI2008["value"]:
#         if int(item["Key"]) == int(bedrijfkey):
#             titel = "".join(ch for ch in item["Title"] if ch != ".")
#             break
    
#     figure = plt.figure()
#     i = 0
    # for afzet in ["A4","A5","A6"]:
    #     i += 1
    #     tijdlijn = bedrijfstak.loc[bedrijfstak["Afzet"] == afzet]
#         X = []
#         Y = []
#         for i in range(len(tijdlijn)):
#             item = tijdlijn.iloc[i]
#             datum = int(item["Perioden"][:4]) + int(item["Perioden"][-2:])/12
#             X.append(datum)
#             Y.append(item["ProducentenprijsindexPPI_1"])
    #     ax1 = figure.add_subplot(110+i)
    #     ax1.plot(X,Y)
    # size = figure.get_size_inches()
    # figure.set_size_inches(size[0]*2,size[1]*2)
    # figure.savefig("figures/" + titel, dpi = 1000, bbox_inches='tight')