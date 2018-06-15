import bokeh as bk
from bokeh.io import show
import pandas as pd
import os

for file in os.listdir("../Data/DataFrames/DataFrames_Afzet_Branches"):
    path = os.path.join("../Data/DataFrames/DataFrames_Afzet_Branches", file)
    df = pd.read_csv(path)
show()