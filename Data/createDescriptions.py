import pandas as pd
import json


# # initialiseer dataframe.
# dftypedDataSet = pd.read_json("http://opendata.cbs.nl/ODataApi/OData/81975NED/TypedDataSet?$top=1")

# top = 9668
# skip = 1
# url = "http://opendata.cbs.nl/ODataApi/OData/81975NED/TypedDataSet"
# while skip < 96681:
#     big = dftypedDataSet.append(pd.read_json("http://opendata.cbs.nl/ODataApi/OData/81975NED/TypedDataSet?$top=" + str(top) + "&$skip=" + str(skip)))
#     skip = skip + 9668
#     dftypedDataSet = big

# # lijst maken van values in df.
# DatasetTypedList = dftypedDataSet["value"].tolist()
# DF = pd.DataFrame(DatasetTypedList)
# DF.to_csv("dataframe.csv")

# # maak een nieuwe df die geen gemmidelde jaarmetingen bevat
# jaarlozenummers = []
# for i,datum in enumerate(DF["Perioden"].tolist()):
#     if datum.find("MM") != -1:
#         jaarlozenummers.append(i)

# maanddf = DF.iloc[jaarlozenummers]
# # print(maanddf)
# maanddf.to_csv("maanddf.csv")

# # # get information from all the other tables
# dfTableInfos = pd.read_json("http://opendata.cbs.nl/ODataApi/OData/81975NED/TableInfos")
# # dfTableInfos["value"]


# dfDataProperties = pd.DataFrame(pd.read_json("http://opendata.cbs.nl/ODataApi/OData/81975NED/DataProperties")["value"].tolist())

# # Hiermee krijg je een tabel met alleen "Title" en "Description"
# DataPropertiesDescriptions = dfDataProperties[["Title","Description"]]

# for i in range(len(DataPropertiesDescriptions)):
#     if DataPropertiesDescriptions["Description"][i] != "":
#         print(DataPropertiesDescriptions["Title"][i] + ":")
#         print(DataPropertiesDescriptions["Description"][i])
#         print(" ---------- \n")

# print(dfDataProperties)


# dfCategoryGroups =  pd.DataFrame(pd.read_json("http://opendata.cbs.nl/ODataApi/OData/81975NED/CategoryGroups")["value"].tolist())

# # Hiermee krijg je een tabel met alleen "Title" en "Description"
# DataCategoryGroupsDescriptions = dfCategoryGroups[["Title","Description"]]

# for i in range(len(DataCategoryGroupsDescriptions)):
#     if DataCategoryGroupsDescriptions["Description"][i] != "":
#         print(DataCategoryGroupsDescriptions["Title"][i] + ":")
#         print(DataCategoryGroupsDescriptions["Description"][i])
#         print("\n ---------- \n")

# print(dfCategoryGroups)


# dfAfzet = pd.DataFrame(pd.read_json("http://opendata.cbs.nl/ODataApi/OData/81975NED/Afzet")["value"].tolist())

# # Hiermee krijg je een tabel met alleen "Title" en "Description"
# AfzetDescriptions = dfAfzet[["Title","Description"]]

# for i in range(len(AfzetDescriptions)):
#     if AfzetDescriptions["Description"][i] != "":
#         print(AfzetDescriptions["Title"][i] + ":")
#         print(AfzetDescriptions["Description"][i])
#         print("\n ---------- \n")

# print(dfAfzet)


# dfBedrijfstakkenBranchesSBI2008 = pd.DataFrame(pd.read_json("http://opendata.cbs.nl/ODataApi/OData/81975NED/BedrijfstakkenBranchesSBI2008")["value"].tolist())

# # Hiermee krijg je een tabel met alleen "Title" en "Description"
# BedrijfstakkenBranchesSBI2008Descriptions = dfBedrijfstakkenBranchesSBI2008[["Title","Description"]]

# for i in range(len(BedrijfstakkenBranchesSBI2008Descriptions)):
#     if BedrijfstakkenBranchesSBI2008Descriptions["Description"][i] != "":
#         print(BedrijfstakkenBranchesSBI2008Descriptions["Title"][i] + ":")
#         print(BedrijfstakkenBranchesSBI2008Descriptions["Description"][i])
#         print("\n ---------- \n")

# print(dfBedrijfstakkenBranchesSBI2008)


# dfPerioden = pd.DataFrame(pd.read_json("http://opendata.cbs.nl/ODataApi/OData/81975NED/Perioden")["value"].tolist())

# # Hiermee krijg je een tabel met alleen "Title" en "Description"
# PeriodenDescriptions = dfPerioden[["Title","Description"]]

# for i in range(len(PeriodenDescriptions)):
#     if PeriodenDescriptions["Description"][i] != "":
#         print(PeriodenDescriptions["Title"][i] + ":")
#         print(PeriodenDescriptions["Description"][i])
#         print("\n ---------- \n")

# print(dfPerioden)