import pandas as pd
import json

# Maakt DF genaamd FeaturesDF aan met alleen de branchID en Titel
dfBedrijfstakkenBranchesSBI2008 = pd.DataFrame(pd.read_json("http://opendata.cbs.nl/ODataApi/OData/81975NED/BedrijfstakkenBranchesSBI2008")["value"].tolist())
FeaturesDF = dfBedrijfstakkenBranchesSBI2008.drop("CategoryGroupID", 1)
FeaturesDF = FeaturesDF.drop("Description", 1)


# Voeg kolommen toe van features (door niet-bestaande index te selecteren)
# default is nu 0 (crisis beinvloed niet)
FeaturesDF['Kredietcrisis'] = 0

# Alle branches die crisis ondergaan zijn
# (dus waar Kredietcrisis = 1)
KredietLijst = ['32811', '308400', '320000', '339200', '328100', '328105', '320705',
                '320700', '346700', '346600', '315800', '315200', '317100', '320005',
                '323700', '307700', '307800', '308800', '308700', '307610', '307600',
                '309000', '309100']


LijstVanFeatures = [KredietLijst]

# Lijst van de namen van de features op volgorde
LijstVanFN = ['Kredietcrisis']

i = 0
for FeatureLijst in LijstVanFeatures:
    for ID in FeatureLijst:
        FeaturesDF.loc[FeaturesDF['Key'] == ID, LijstVanFN] = 1
    i += 1

print(FeaturesDF)
FeaturesDF.to_csv('FeaturesDF')