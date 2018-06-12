import pandas as pd
import json

# open bestand om in te schrijven
file = open("descriptions.txt","w")

# get information from all the other tables
dfTableInfos = pd.read_json("http://opendata.cbs.nl/ODataApi/OData/81975NED/TableInfos")

dfDataProperties = pd.DataFrame(pd.read_json("http://opendata.cbs.nl/ODataApi/OData/81975NED/DataProperties")["value"].tolist())

# Hiermee krijg je een tabel met alleen "Title" en "Description"
DataPropertiesDescriptions = dfDataProperties[["Title","Description"]]

for i in range(len(DataPropertiesDescriptions)):
    if DataPropertiesDescriptions["Description"][i] != "":
        file.write(DataPropertiesDescriptions["Title"][i] + ": ")
        file.write(DataPropertiesDescriptions["Description"][i])
        file.write("\n \n ---------- \n \n")


dfCategoryGroups =  pd.DataFrame(pd.read_json("http://opendata.cbs.nl/ODataApi/OData/81975NED/CategoryGroups")["value"].tolist())

# Hiermee krijg je een tabel met alleen "Title" en "Description"
DataCategoryGroupsDescriptions = dfCategoryGroups[["Title","Description"]]

for i in range(len(DataCategoryGroupsDescriptions)):
    if DataCategoryGroupsDescriptions["Description"][i] != "":
        file.write(DataCategoryGroupsDescriptions["Title"][i] + ": ")
        file.write(DataCategoryGroupsDescriptions["Description"][i])
        file.write("\n \n ---------- \n \n")


dfAfzet = pd.DataFrame(pd.read_json("http://opendata.cbs.nl/ODataApi/OData/81975NED/Afzet")["value"].tolist())

# Hiermee krijg je een tabel met alleen "Title" en "Description"
AfzetDescriptions = dfAfzet[["Title","Description"]]

for i in range(len(AfzetDescriptions)):
    if AfzetDescriptions["Description"][i] != "":
        file.write(dfAfzet["Key"][i] + " - ")
        file.write(AfzetDescriptions["Title"][i] + ": ")
        file.write(AfzetDescriptions["Description"][i])
        file.write("\n \n ---------- \n \n")


dfBedrijfstakkenBranchesSBI2008 = pd.DataFrame(pd.read_json("http://opendata.cbs.nl/ODataApi/OData/81975NED/BedrijfstakkenBranchesSBI2008")["value"].tolist())

# Hiermee krijg je een tabel met alleen "Title" en "Description"
BedrijfstakkenBranchesSBI2008Descriptions = dfBedrijfstakkenBranchesSBI2008[["Title","Description"]]

for i in range(len(BedrijfstakkenBranchesSBI2008Descriptions)):
    if BedrijfstakkenBranchesSBI2008Descriptions["Description"][i] != "":
        file.write(dfBedrijfstakkenBranchesSBI2008["Key"][i] + " - ")
        file.write(BedrijfstakkenBranchesSBI2008Descriptions["Title"][i] + ": ")
        file.write(BedrijfstakkenBranchesSBI2008Descriptions["Description"][i])
        file.write("\n \n ---------- \n \n")


dfPerioden = pd.DataFrame(pd.read_json("http://opendata.cbs.nl/ODataApi/OData/81975NED/Perioden")["value"].tolist())

# Hiermee krijg je een tabel met alleen "Title" en "Description"
PeriodenDescriptions = dfPerioden[["Title","Description"]]

for i in range(len(PeriodenDescriptions)):
    if PeriodenDescriptions["Description"][i] != "":
        file.write(PeriodenDescriptions["Title"][i] + ": ")
        file.write(PeriodenDescriptions["Description"][i])
        file.write("\n \n ---------- \n \n")

file.close()