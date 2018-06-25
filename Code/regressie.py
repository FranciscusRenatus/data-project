
# coding: utf-8

# In[1]:


import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import style 
import pandas as pd
import sklearn
import warnings
from sklearn import linear_model
from sklearn.cross_validation import train_test_split
import math
warnings.simplefilter(action = "ignore", category = FutureWarning)
get_ipython().magic('matplotlib inline')


# In[2]:


def slope_intercept(x_val,y_val):
    x=np.array(x_val)
    y=np.array(y_val)
    m=( ( (np.mean(x)*np.mean(y)) - np.mean(x*y)) /
      ((np.mean(x)*np.mean(x)) - np.mean(x*x)) )
    m=round(m,2)
    b=(np.mean(y)-np.mean(x)*m)
    b=round(b,2)
    
    return m,b


# In[3]:


def rmse(y1, y_hat):
    y_actual=np.array(y1)
    y_pred=np.array(y_hat)
    error=(y_actual-y_pred)**2
    error_mean=round(np.mean(error))
    err_sq=math.sqrt(error_mean)
    return err_sq


# In[125]:


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
newDFX = pd.DataFrame(DatasetTypedList)


# jaren weghalen
jaarlozenummers = []
for i,datum in enumerate(newDFX["Perioden"].tolist()):
    if datum.find("JJ") != -1:
        jaarlozenummers.append(i)


# In[126]:


df = newDFX.iloc[jaarlozenummers]
df = df.loc[df["ProducentenprijsindexPPI_1"].notnull()]
df.head()


# In[127]:


df1 = df.drop(["OntwikkelingTOV1JaarEerder_2", "OntwikkelingTOV1MaandEerder_3", "Wegingcoefficient_4", "ID"], axis=1)
df1.head()


# In[131]:


#df1 = df1.loc[df1["Afzet"]=="A6"]
#df1 = df1.loc[df1["BedrijfstakkenBranchesSBI2008"] == str(305700)]

# perioden numeriek maken
numeriekPeriodes = []
for i,datum in enumerate(df1["Perioden"].tolist()):
    ndatum = datum[:4]
    numeriekPeriodes.append(float(ndatum))
    
df1["tijd"] = numeriekPeriodes


# In[132]:


afz = ["A6", "A4", "A5"]


# In[133]:


for a in afz:
    if a == "A6":
        naam = "Totaal "
    elif a == "A4":
        naam = "Binnenlands "
    elif a == "A5":
        naam = "Buitenlands "
        
    dfX = df1.loc[ df1["Afzet"] == a ]
    
    x = dfX["tijd"].tolist()
    y = dfX["ProducentenprijsindexPPI_1"].astype(float).tolist()
    
    m,b = slope_intercept(x,y)
    reg_line = [(m*i)+b for i in x]
    
    plt.scatter(x, y, color = "red")
    plt.plot(x, reg_line)
    plt.title(naam + "totaal industiereen NL")
    plt.show()
    
    rsme = rmse(y,reg_line)
    
    print("RSME: " + str(rsme))
    print("Slope: " + str(m))
    print("b :" + str(b))


# ## Stuff

# In[134]:


dfBedrijfstakkenBranchesSBI2008 = pd.read_json("http://opendata.cbs.nl/ODataApi/OData/81975NED/BedrijfstakkenBranchesSBI2008")
listBedrijfstakken = dfBedrijfstakkenBranchesSBI2008["value"].tolist()
pdBedrijfstakkenSBI = pd.DataFrame(listBedrijfstakken)
branchNamen = pdBedrijfstakkenSBI[["Key","Title"]]

d = pdBedrijfstakkenSBI.drop(["CategoryGroupID","Description"], axis=1)
dd = {k: g["Title"].tolist() for k,g in d.groupby("Key")}


# In[135]:


obLijst =['305700', '346600', '315805', '328110', '341600', '317105', '320005',
                  '312500', '307610', '348000', '342400', '307500']


# In[138]:


for i,b in enumerate(obLijst):   
    naam = dd[b][0]
    df2 = df1.loc[df1["BedrijfstakkenBranchesSBI2008"] == b]
    
    dfBinnenlands = df2.loc[df2["Afzet"] == "A4"]
    dfBuitenlands = df2.loc[df2["Afzet"] == "A5"]
    dfTotaal = df2.loc[df2["Afzet"] == "A6"]
    
    xbi = dfBinnenlands["tijd"].tolist()
    ybi = dfBinnenlands["ProducentenprijsindexPPI_1"].astype(float).tolist()
    
    xbu = dfBuitenlands["tijd"].tolist()
    ybu = dfBuitenlands["ProducentenprijsindexPPI_1"].astype(float).tolist()
    
    xto = dfTotaal["tijd"].tolist()
    yto = dfTotaal["ProducentenprijsindexPPI_1"].astype(float).tolist()
    
    mbi,bbi = slope_intercept(xbi,ybi)
    reg_lineBi = [(mbi*i)+bbi for i in xbi]
    
    mbu,bbu = slope_intercept(xbu,ybu)
    reg_lineBu = [(mbu*i)+bbu for i in xbu]
    
    mto,bto = slope_intercept(xto,yto)
    reg_lineTo = [(mto*i)+bto for i in xto]
    
    plt.scatter(xbi, ybi, color = "red")
    plt.title(naam + " Binnenlands")
    plt.plot(xbi, reg_lineBi)
    plt.show()
    
    print("Slope: " + str(mbi))
    
    
    plt.scatter(xbu, ybu, color = "red")
    plt.title(naam + " Buitenlands")
    plt.plot(xbu, reg_lineBu)
    plt.show()
    
    print("Slope: " + str(mbu))
    
    
    plt.scatter(xto, yto, color = "red")
    plt.title(naam + " Totaal")
    plt.plot(xto, reg_lineTo)
    plt.show()
    
    print("Slope: " + str(mto))


# ## Multivariate regression

# In[68]:


df2 = newDFX.iloc[jaarlozenummers]
df2 = df2.loc[df2["Wegingcoefficient_4"] > 0]
df2 = df2.drop(["ID"], axis=1)
df2.loc[:,"index"] = list(range(0,len(df2)))
df2 = df2.set_index('index')
df2.index.name = None


# In[69]:


branches = df2["BedrijfstakkenBranchesSBI2008"].unique()
ont_percent = {}
l = []
for b in branches:
    
    temp = df2.loc[df2["BedrijfstakkenBranchesSBI2008"] == b, :]
    wx = temp["Wegingcoefficient_4"].unique()
    afzetx = temp["Afzet"].unique()
    
    if len(afzetx) == 3 and len(wx) == 3:       
        buiten = wx[2]/wx[0]
        binnen = wx[1]/wx[0]  
        l.append(buiten+binnen)
        l.append(binnen)
        l.append(buiten)
    elif len(afzetx) == 2 and len(wx) == 2:      
        buiten = wx[1]/wx[0]
        binnen = wx[1]/wx[0]
        l.append(buiten+binnen)
        l.append(binnen)
        l.append(buiten)
    elif len(afzetx) == 1 and len(wx) == 1:
        buiten = 1
        binnen = 1
        l.append(buiten)
        l.append(binnen)
        l.append(buiten)
    elif len(afzetx) == 2 and len(wx) == 1:
        buiten = 1
        binnen = 1
        l.append(buiten)
        l.append(binnen)
        l.append(buiten)
    ont_percent[b] = l
    l = []


# In[70]:


ub = [305700,346600,315805,328110,341600,317105,320005,312500,307610,348000,342400,307500]
ont_percent_ob = {}
l2 = []
summing = 0

for b in ub:
    temp = df2.loc[df2["BedrijfstakkenBranchesSBI2008"] == str(b), :]
    wx = temp["Wegingcoefficient_4"].unique()
   
    summing+=wx[0]

for b in ub:
    
    temp = df2.loc[df2["BedrijfstakkenBranchesSBI2008"] == str(b), :]
    wx = temp["Wegingcoefficient_4"].unique()
    ont_percent_ob[b] = wx[0]/summing


# In[71]:


dictO ={}
listO = []
branches = df2["BedrijfstakkenBranchesSBI2008"].unique()

for b in branches: 
    
    temp = df2.loc[df2["BedrijfstakkenBranchesSBI2008"] == b]
    value = ont_percent[b]

    for v in temp.values: 
        if v[0] == "A6":
            listO.append(value[0])
        elif v[0] == "A4":
            listO.append(value[1])
        elif v[0] == "A5":
            listO.append(value[2])
        
    dictO[b] = listO
    listO = []

newDF = pd.DataFrame(columns = df2.columns.tolist())
    
for key,value in dictO.items():
    
    temp = df2.loc[df2["BedrijfstakkenBranchesSBI2008"] == key]

    temp = temp.assign(wegingB=pd.Series(np.array(value)).values)
        
    newDF = newDF.append(temp)


# In[72]:


dictO ={}
listO = []
branches = df2["BedrijfstakkenBranchesSBI2008"].unique()

for b in branches:
    
    temp = df2.loc[df2["BedrijfstakkenBranchesSBI2008"] == b]
    value = ont_percent[b]
    
    if len(value) == 3:
        grootsteA = 1

        if value[1] < value[2]:
            grootsteA = 2
    else:
        grootsteA = 0

    for v in temp.values: 
        listO.append(grootsteA)
         
    dictO[b] = listO
    listO = []
    
newDF2 = pd.DataFrame(columns = newDF.columns.tolist())

for key,value in dictO.items():
    
    temp = newDF.loc[newDF["BedrijfstakkenBranchesSBI2008"] == key]

    temp = temp.assign(grootsteAfzet=pd.Series(np.array(value)).values)
    newDF2 = newDF2.append(temp)


# In[73]:


# Om alle overkoepelende industrieen samen te nemen.
newDF2['OB'] = 0

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

#overkoepelende lijst die overkoepelende industrie overkoepelt
koepelkoepellijst = ['305700', '346600', '315805', '328110', '341600', '317105', '320005',
                  '312500', '307610', '348000', '342400', '307500']


KoepelLijst = [delftstoffenwinning, energievoorziening, houtbouwindustrie, metalektro,
            papiergrafisch, raffinaderijenchemie, texkleledindustrie, voedinggenotsindustrie, koepelkoepellijst]

i = 1
dictt = {}
for i,ob in enumerate(KoepelLijst):
    dictt[str(koepelkoepellijst[i])] = ob

listt = []
dictOO = {}

for obKey,branches in dictt.items():
    
    percentOB = ont_percent_ob[int(obKey)]
    
    for b in branches:
    
        temp = newDF2.loc[df2["BedrijfstakkenBranchesSBI2008"] == b]
        
        for v in temp.values: 
            listt.append(percentOB)
      
        dictOO[b] = listt
        listt = []

    
newDF3 = pd.DataFrame(columns = newDF.columns.tolist())

for key,values in dictOO.items():
       
    temp = newDF2.loc[newDF2["BedrijfstakkenBranchesSBI2008"] == key]

    temp = temp.assign(pOB=pd.Series(np.array(values)).values)

    newDF3 = newDF3.append(temp)


# In[74]:


newDF3["pTovTotaal"] = newDF3["wegingB"] * newDF3["pOB"]


# In[75]:


newDF3.head()


# In[77]:


newDF3['Afzet'] = newDF3['Afzet'].astype('category')
newDF3['Afzet'] = newDF3['Afzet'].cat.codes
delftDF = newDF3.loc[newDF3["BedrijfstakkenBranchesSBI2008"] == '305700']
delftDF = delftDF.loc[delftDF["Afzet"] == 2]
delftDF.head()


# In[78]:


delftDF1 = delftDF.drop(["OntwikkelingTOV1JaarEerder_2", "OntwikkelingTOV1MaandEerder_3", "Wegingcoefficient_4", "OB", "BedrijfstakkenBranchesSBI2008"], axis=1)
df_x = delftDF1.drop(["Perioden","ProducentenprijsindexPPI_1"], axis=1)
df_y = delftDF1["ProducentenprijsindexPPI_1"]


# In[79]:


df_x.head()


# In[80]:


df_y.head()


# In[81]:


df_x.shape


# In[82]:


names = [i for i in list(df_x)]
names


# In[83]:


regr = linear_model.LinearRegression()


# In[84]:


regr = linear_model.LinearRegression()
x_train, x_test, y_train, y_test = train_test_split(df_x, df_y, test_size=0.2, random_state=4)


# In[85]:


x_train = x_train.fillna(0)
y_train = y_train.fillna(0)
regr.fit(x_train, y_train)


# In[86]:


regr.fit(x_train, y_train)


# In[87]:


regr.intercept_


# In[88]:


print("Coefficients: ", regr.coef_ )
print("Mean squared error: %.2f" 
      % np.mean((regr.predict(x_test) - y_test) ** 2))
#print("Variance score: %.2f" 
#      % regr.score(x_test, y_test))


# In[89]:


style.use("bmh")
plt.scatter(regr.predict(x_test), y_test)
plt.show()


# In[239]:


import statsmodels.api as sm
from statsmodels.sandbox.regression.predstd import wls_prediction_std


# In[240]:


model1 = sm.OLS(y_train, x_train)


# In[241]:


result = model1.fit()


# In[242]:


print(result.summary())

