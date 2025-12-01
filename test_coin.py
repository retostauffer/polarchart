#!/usr/bin/env python3

import pandas as pd
from pandas import Categorical
import numpy as np

import statsmodels.api as sm
import statsmodels.formula.api as smf
from polarchart import coin_object


group = Categorical(np.repeat(["Control", "Compound"], [19, 15]),
                categories = ["Control", "Compound"])
asat  = ["1.33", "1.78", "1.53", "1.95", "1.83", "1.47", "1.87", "1.55",
         "2.58", "2.17", "1.97", "1.62", "2.25", "3.53", "2.92", "1.78",
         "2.22", "2.55", "2.75", "1.53", "1.75", "2.12", "2.83", "2.58",
         "2.37", "2.92", "2.08", "3.01", "2.67", "2.08", "2.25", "3.08",
         "2.01", "1.58"]

df = pd.DataFrame({"asat": asat, "group": group})
print(df.head())
print("\n ---------------- \n")

coin_object(df, x = "group", y = "asat")
