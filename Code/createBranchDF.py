import pandas as pd
import json

# bedrijfstakken naar .csv
dfBedrijfstakkenBranchesSBI2008 = pd.DataFrame(pd.read_json("http://opendata.cbs.nl/ODataApi/OData/81975NED/BedrijfstakkenBranchesSBI2008")["value"].tolist())
dfBedrijfstakkenBranchesSBI2008.to_csv("Bedrijfstakken")

# afzet naar .csv
dfAfzet = pd.DataFrame(pd.read_json("http://opendata.cbs.nl/ODataApi/OData/81975NED/Afzet")["value"].tolist())
dfAfzet.to_csv("Afzet")