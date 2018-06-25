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
    impact = []
    for file in os.listdir("../Data/DataFrames/DataFrames_Afzet_Branches"):
        path = os.path.join("../Data/DataFrames/DataFrames_Afzet_Branches", file)
        df = pd.read_csv(path)
        perioden = df["Perioden"].tolist()
        prijzen = df["ProducentenprijsindexPPI_1"].tolist()
        if prijzen != []:
            peak = dal = (prijzen[0],perioden[0])
            for i in range(len(prijzen)):
                if prijzen[i] > peak[0]:
                    peak = (prijzen[i],perioden[i])
                elif prijzen[i] <= dal[0]:
                    dal = (prijzen[i],perioden[i])
                else:
                    impact.append(((peak[0]-dal[0])/peak[0],avg.month(peak[1]),avg.month(dal[1]),file))
                    peak = dal = (prijzen[i],perioden[i])
    return impact

if __name__ == "__main__":
    impact = main()
    impact = [x for x in impact if (x[0] > 1/16) and (x[3][:6] in ['305700', '346600', '315805', '328110', '341600', '317105', '320005', '312500', '307610', '348000', '342400', '307500'])]
    print(len(impact))
    graph.generate([x[1] for x in impact],[x[2] for x in impact],[x[3] for x in impact])
    print("done graphing")
    output_file("../Data/HTML/industrychange.html")
    dfdict = {
        "branch":[avg.titel(x[3][:6]) for x in impact],
        "afzet":[avg.titel(x[3][-2:]) for x in impact],
        "dip":[x[0] for x in impact],
        "start":[x[1] for x in impact],
        "eind":[x[2] for x in impact],
        "tijd":[abs(x[2]-x[1]) for x in impact],
        "color":["lime" if x[1] > x[2] else "red" for x in impact],
        "imgs":["../../Docs/relativedipfigures/" + x[3] + " " + "".join(ch if ch != "." else "," for ch in str(x[1])) + ".png" for x in impact]
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
    p.scatter(y = "dip", x = "start", source = source, fill_color = "color")
    p.select_one(HoverTool).tooltips = TOOLTIPS
    #     ('branch', '@branch'),
    #     ('afzet','@afzet'),
    #     ('dip', '@dip'),
    #     ('tijd', '@tijd'),
    #     ('start','avg.unmonth(@start)'),
    #     ('eind','avg.unmonth(@eind)'),
    # ]
    p.xaxis.axis_label = "starting year of the change"
    p.yaxis.axis_label = "relative size of the change"
    show(p)