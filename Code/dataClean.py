import pandas as pd
import json
from sklearn import preprocessing
import os


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
CleanDF2 = CleanDF2.drop("Wegingcoefficient_4",1)


# branchnamen en id's in dictionary stoppen
dfBedrijfstakkenBranchesSBI2008 = pd.read_json("http://opendata.cbs.nl/ODataApi/OData/81975NED/BedrijfstakkenBranchesSBI2008")
pdBedrijfstakkenSBI = pd.DataFrame(dfBedrijfstakkenBranchesSBI2008["value"].tolist())
branchNamen = pdBedrijfstakkenSBI[["Key","Title"]]

# lege entries verwijderen en alle data opsplitsen per branch en afzet
path=r'../Data/DataFrames/DataFrames_Afzet_Branches/'


for i in branchNamen["Key"]:
    for k in ["A4","A5","A6"]:
        BranchTemp = CleanDF2.loc[CleanDF2["BedrijfstakkenBranchesSBI2008"] == i]
        BranchCleanAfzet = BranchTemp.loc[BranchTemp["Afzet"] == k]
        BranchCleanAfzet = BranchCleanAfzet.drop("Afzet", 1)
        BranchCleanAfzet = BranchCleanAfzet.drop("BedrijfstakkenBranchesSBI2008", 1)
        BranchCleanAfzet = BranchCleanAfzet.drop("ID", 1)
        BranchCleanAfzet = BranchCleanAfzet.drop("OntwikkelingTOV1JaarEerder_2", 1)
        BranchCleanAfzet = BranchCleanAfzet.drop("OntwikkelingTOV1MaandEerder_3", 1)
        BranchCleanAfzet = BranchCleanAfzet.interpolate()
        BranchCleanAfzet = BranchCleanAfzet.loc[BranchCleanAfzet["ProducentenprijsindexPPI_1"].notnull()]
        BranchCleanAfzet.to_csv(os.path.join(path,(i + " - " + k)))
        