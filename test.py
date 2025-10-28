#!/usr/bin/env python3

import os, sys
from radarchart import radar, load_mtcars
import pandas as pd
import matplotlib.pyplot as plt

mtcars = load_mtcars()


reto =  dict(a = [0.499, 0.167, 0.134, 3.53],
             b = [0.403, 0.365, 0.114, 3.23],
             c = [0.184, 0.407, 0.334, 2.53],
             d = [0.519, 0.077, 0.234, 3.13])
reto = pd.DataFrame(reto, index = ["foo", "bar", "three", "four"])             
ax = radar(reto)

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
