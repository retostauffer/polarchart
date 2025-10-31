#!/usr/bin/env python3

import os, sys
from polarchart import radar, get_demodata
import pandas as pd
import matplotlib.pyplot as plt

############ Only num
gsa4 = get_demodata("gsa4")

print(gsa4.head())
radar(gsa4, labels = "ISO3", numeric_only = True,
      angle = 45, title = "Testing angle argument")
radar(gsa4, labels = "ISO3", numeric_only = True,
      angle = 45, title = "Testing angle argument")
radar(gsa4, labels = "ISO3", numeric_only = True,
      scale = False)

##
import sys; sys.exit(" -- psa4 -- ")
gsa3 = get_demodata("gsa3")



gsa_x = gsa3.iloc[:, :6]
print(gsa_x.head())
radar(gsa_x, labels = "ISO3", numeric_only = True,
      angle = 45, title = "Testing angle argument")
radar(gsa_x, labels = "ISO3", numeric_only = True)

radar(gsa_x, labels = "ISO3", numeric_only = True,
      scale = True,
      angle = 45, title = "Testing angle argument")

sys.exit(" -- end of the gsa -- ")


#radar(gsa3, scale = True)
#radar(gsa3, labels = 'ISO3', scale = True)
radar(gsa3, labels = 'ISO3', numeric_only = True, scale = True)


sys.exit(" -- end of the gsa -- ")

############ One char col
gsa2 = get_demodata("gsa2")
try:
    # Expected to fail as we have non-numeric columns
    radar(gsa2, scale = True)
except:
    pass
radar(gsa2, labels = "Country", scale = True)

############ Only num
gsa = get_demodata("gsa")
radar(gsa, labels = False, scale = True)
radar(gsa, labels = True, scale = True)


sys.exit(" -- end of the gsa -- ")


#ice = pd.read_csv("Ice.csv")
#ice["foo"] = list(ice.index)
#print(ice)

#radar(ice * 100, scale = False)
radar(ice * 100, scale = True)

sys.exit(" -- end of the ice -- ")


radar(ice, scale = True,
      circles = False,
      labels = True,
      legend_position = False)

sys.exit(" -- end of the ice f -- ")

#radar(mtcars, scale = True, figsize = (5, 10))
radar(mtcars, scale = True, figsize = (5, 10),
      legend_position = (-1, -1))
radar(mtcars, scale = True, figsize = (5, 10),
      legend_position = None)

sys.exit(" -- dev stop test.py -- ")

reto =  dict(a = [0.499, 0.167, 0.134, 3.53],
             b = [0.403, 0.365, 0.114, 3.23],
             c = [0.184, 0.407, 0.334, 2.53],
             d = [0.519, 0.077, 0.234, 3.13])
reto = pd.DataFrame(reto, index = ["foo", "bar", "three", "four"])             


#radar(reto, ncol = 2, angle = 0)
#radar(reto, angle = 0, figsize = (5, 10))

sys.exit(" -- dev stop test.py -- ")

fix, ax = plt.subplots(figsize = (12, 5))
ax = radar(reto, ax = ax, ncol = None, angle = 0)
plt.show()

#ax = radar(reto, ncol = None, angle = 0)

sys.exit(" -- dev stop test.py -- ")

# # Create a sample DataFrame for demonstration
# data = {
#     'Speed (km/h)': [80, 55, 95],
#     'Efficiency (L/100km)': [6.5, 4.0, 7.8],
#     'Durability (Years)': [12, 18, 8],
#     'Cost ($1000s)': [30, 15, 45],
#     'Aesthetics (Score)': [700, 900, 600]
# }
# df_widgets = pd.DataFrame(data, index=['Widget A', 'Widget B', 'Widget C'])

# Call the radar() function
ax = radar(reto, line_colors=['#007ACC', '#FF4500', '#3CB371'])

### Add a title
##ax.set_title('Widget Comparison Across Key Metrics', size=14, y=1.1)

# Display the plot
plt.show()
