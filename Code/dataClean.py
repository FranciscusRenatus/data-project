import pandas as pd
import json
from sklearn import preprocessing


# initialize dataframe
dftypedDataSet = pd.read_json("http://opendata.cbs.nl/ODataApi/OData/81975NED/TypedDataSet?$top=1")

# data ophalen
top = 9668
skip = 1
url = "http://opendata.cbs.nl/ODataApi/OData/81975NED/TypedDataSet"
while skip < 96681:
    big = dftypedDataSet.append(pd.read_json("http://opendata.cbs.nl/ODataApi/OData/81975NED/TypedDataSet?$top=" + str(top) + "&$skip=" + str(skip)))
    skip = skip + 9668
    dftypedDataSet = big

# lijst maken van values in df
DatasetTypedList = dftypedDataSet["value"].tolist()

# dataframe maken van lijst met beoogde values
newDF2 = pd.DataFrame(DatasetTypedList)


# jaren weghalen
jaarlozenummers = []
for i,datum in enumerate(newDF2["Perioden"].tolist()):
    if datum.find("MM") != -1:
        jaarlozenummers.append(i)

CleanDF2 = newDF2.iloc[jaarlozenummers]
CleanDF2 = CleanDF2.drop(columns=["Wegingcoefficient_4"])


# branchnamen en id's in dictionary stoppen
dfBedrijfstakkenBranchesSBI2008 = pd.read_json("http://opendata.cbs.nl/ODataApi/OData/81975NED/BedrijfstakkenBranchesSBI2008")
pdBedrijfstakkenSBI = pd.DataFrame(dfBedrijfstakkenBranchesSBI2008["value"].tolist())
branchNamen = pdBedrijfstakkenSBI[["Key","Title"]]

# lege entries verwijderen en alle data opsplitsen per branch en afzet
afzet = ["A4","A5","A6"]
for i in branchNamen["Key"]:
    BranchTemp = CleanDF2.loc[CleanDF2["BedrijfstakkenBranchesSBI2008"] == i]
    BranchTemp = BranchTemp.interpolate()
    BranchClean = BranchTemp.loc[(BranchTemp["OntwikkelingTOV1JaarEerder_2"].notnull()) | (BranchTemp["OntwikkelingTOV1MaandEerder_3"].notnull()) | (BranchTemp["ProducentenprijsindexPPI_1"].notnull())]
    for k in afzet:
        BranchCleanAfzet = BranchClean.loc[BranchClean["Afzet"] == k]
        BranchCleanAfzet = BranchCleanAfzet.drop("Afzet", 1)
        BranchCleanAfzet = BranchCleanAfzet.drop("BedrijfstakkenBranchesSBI2008", 1)
        BranchCleanAfzet = BranchCleanAfzet.drop("ID", 1)
        BranchCleanAfzet = BranchCleanAfzet.drop("OntwikkelingTOV1JaarEerder_2", 1)
        BranchCleanAfzet = BranchCleanAfzet.drop("OntwikkelingTOV1MaandEerder_3", 1)
        BranchCleanAfzet.to_csv(i + " - " + k)