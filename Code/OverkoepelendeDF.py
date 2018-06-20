import pandas as pd
import json

# Maakt DF genaamd FeaturesDF aan met alleen de branchID en Titel
dfBedrijfstakkenBranchesSBI2008 = pd.DataFrame(pd.read_json("http://opendata.cbs.nl/ODataApi/OData/81975NED/BedrijfstakkenBranchesSBI2008")["value"].tolist())
KoepelDF = dfBedrijfstakkenBranchesSBI2008.drop("CategoryGroupID", 1)
KoepelDF = KoepelDF.drop("Description", 1)

verwijderlijst = ['305700', '346600', '315805', '328110', '341600', '317105', '320005', '312500', '307610', '348000', '342400', '307500']

for ID in verwijderlijst:
    KoepelDF = KoepelDF.ix[KoepelDF['Key'] != ID]


KoepelDF['Hoofdbranch'] = 0

# meubelindustrie is overgeslagen omdat deze alleen de
# overkoepelende branch zelf bevat

#1
delftstoffenwinning = ['305800', '306300', '320000']

#2
energievoorziening = ['346700']

#3
houtbouwindustrie = ['315800', '324600']

#4
metalektro =['34440', '330300', '800002', '336500', '332900',
            '332905', '332910', '334800', '328105', '328100',
            '339200']

#5
papiergrafisch = ['318600', '317100']

#6
raffinaderijenchemie = ['323700', '323200', '320700', '320705']

#7
texkleledindustrie = ['315200', '314000', '312500']

#8
voedinggenotsindustrie = ['312100', '310200', '310100', '309700',
                        '309400', '309100', '308800', '308500',
                        '308400', '308000', '307900', '307800', 
                        '311000', '310000', '309600', '309300', 
                        '309000', '308700', '308600', '308300', 
                        '308100', '307700', '312200', '311300',
                        '307600']

#9
waterafval = ['348100']


KoepelLijst = [delftstoffenwinning, energievoorziening, houtbouwindustrie, metalektro,
            papiergrafisch, raffinaderijenchemie, texkleledindustrie, voedinggenotsindustrie]

i = 1
for Lijst in KoepelLijst:
    for ID in Lijst:
        KoepelDF.loc[KoepelDF['Key'] == ID, 'Hoofdbranch'] = i
    i += 1

print(KoepelDF)
KoepelDF.to_csv('KoepelDF.csv')