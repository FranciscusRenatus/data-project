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
from bokeh.plotting import (figure,output_file)
import nationalaverage as avg
import graphgenerator as graph
import os

def main():
    impact = {}
    for file in os.listdir("../Data/DataFrames/DataFrames_Afzet_Branches"):
        path = os.path.join("../Data/DataFrames/DataFrames_Afzet_Branches", file)
        df = pd.read_csv(path)
        perioden = df["Perioden"].tolist()
        prijzen = df["ProducentenprijsindexPPI_1"].tolist()
        if prijzen != []:
            dips = []
            peak = (prijzen[0],perioden[0])
            verschil = prijzen[1] - prijzen[0]
            for i in range(2,len(prijzen)):
                newverschil = prijzen[i] - prijzen[i-1]
                if prijzen[i] > peak[0]:
                    peak = (prijzen[i],perioden[i])
                if newverschil >= 0 and verschil < 0:
                    dal = (prijzen[i],perioden[i])
                    dips.append((peak[0]-dal[0],avg.month(peak[1]),avg.month(dal[1])))
                    peak = dal
                verschil = newverschil
        impact[file] = max(dips)
    return impact

if __name__ == "__main__":
    impact = main()
    # graph.generate([x[1] for x in impact.values()],[x[2] for x in impact.values()])
    dfdict = {
        "branch":[avg.titel(x[:6]) for x in impact.keys()],
        "afzet":[avg.titel(x[-2:]) for x in impact.keys()],
        "dip":[x[0] for x in impact.values()],
        "start":[x[1] for x in impact.values()],
        "eind":[x[2] for x in impact.values()],
        "tijd":[x[2]-x[1] for x in impact.values()],
        "imgs":["dipfigures/" + x + ".png" for x in impact.keys()]
    }
    
    source = ColumnDataSource(dfdict)
    TOOLTIPS = """
        <div>
            <div>
                <img
                    src="@imgs" height="200" alt="@imgs" width="300"
                    style="float: left; margin: 0px 15px 15px 0px"
                ></img>
            </div>
            <div>
                <span style="font-size: 17px; font-weight: bold;">@branch</span>
            </div>
        </div>
    """
                    # afzet:@afzet
                    # dip:@dip
                    # tijd:@tijd
                    # start:@start
                    # eind:@eind
    p = figure(title = "dip", tools = "pan,hover,save,box_zoom,reset,wheel_zoom")
    p.scatter(size = 'dip', y = "tijd", x = "start", source = source, alpha = 0.3)
    p.select_one(HoverTool).tooltips = TOOLTIPS
    #     ('branch', '@branch'),
    #     ('afzet','@afzet'),
    #     ('dip', '@dip'),
    #     ('tijd', '@tijd'),
    #     ('start','avg.unmonth(@start)'),
    #     ('eind','avg.unmonth(@eind)'),
    # ]
    p.xaxis.axis_label = "starting year of the dip"
    p.yaxis.axis_label = "duration of the dip"
    show(p)