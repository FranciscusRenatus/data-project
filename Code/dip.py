import pandas as pd
import matplotlib.pyplot as plt
from bokeh.io import show
from bokeh.models import (
    ColumnDataSource,
    HoverTool,
    LinearColorMapper,
    BasicTicker,
    PrintfTickFormatter,
    ColorBar,
)
from bokeh.plotting import figure
import nationalaverage as avg
import os

def main():
    impact = {}
    for file in os.listdir("../Data/DataFrames/DataFrames_Afzet_Branches"):
        path = os.path.join("../Data/DataFrames/DataFrames_Afzet_Branches", file)
        df = pd.read_csv(path)
        perioden = df["Perioden"].tolist()
        prijzen = df["ProducentenprijsindexPPI_1"].tolist()
        if prijzen != []:
            dalen = []
            peak = (prijzen[0],perioden[0])
            verschil = prijzen[0] - prijzen[1]
            for i in range(2,len(prijzen)):
                newverschil = prijzen[i-1] - prijzen[i]
                if prijzen[i] > peak[0]:
                    peak = (prijzen[i],perioden[i])
                if newverschil >= 0 and verschil < 0:
                    dal = (prijzen[i],perioden[i])
                    # print(peak,dal,i)
                    dalen.append((peak[0]-dal[0],peak[1],dal[1]))
                    peak = dal
                verschil = newverschil
        return dalen
                    

        # if "2008MM01" in df["Perioden"].tolist():
        #     prijsvoor = df.loc[df["Perioden"] == "2008MM01"]["ProducentenprijsindexPPI_1"].tolist()[0]
        #     prijsna = df.loc[df["Perioden"] == "2010MM01"]["ProducentenprijsindexPPI_1"].tolist()[0]
        #     impact[file[:6]] = (prijsna/100)/(prijsvoor/100)
            # print(avg.titel(file[:6])," = ", impact[file[:6]])
    # return impact

    # source = ColumnDataSource({'bedrijf':list(impact.keys()),'verschil':list(impact.values())})
    # print(source.to_df())
    # X = [avg.titel(b) for b in impact.keys()]
    # Y = list(impact.values())
    # p = figure(x_range = X, tools = "hover,save,box_zoom,reset,wheel_zoom")
    # p.vbar(x = 'bedrijf', top = 'verschil', source = source, width = 1)
    # p.select_one(HoverTool).tooltips = [
    #     ('bedrijf', '@bedrijf'),
    #     ('verschil', '@verschil'),
    # ]
    # show(p)
    # # X = impact.keys()
    # # Y = impact.values()
    # # print(X)
    # # print(Y)
    # # plt.bar(X,Y)
    # # plt.show()

if __name__ == "__main__":
    print(max(main()))
    # for key in main():
        # print(avg.titel(key),":",main()[key])