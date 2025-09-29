#!/usr/bin/env python3
from stars import stars
import pandas as pd
import matplotlib.pyplot as plt

# Create a sample DataFrame for demonstration
data = {
    'Speed (km/h)': [80, 55, 95],
    'Efficiency (L/100km)': [6.5, 4.0, 7.8],
    'Durability (Years)': [12, 18, 8],
    'Cost ($1000s)': [30, 15, 45],
    'Aesthetics (Score)': [7, 9, 6]
}
df_widgets = pd.DataFrame(data, index=['Widget A', 'Widget B', 'Widget C'])

# Call the starsplot() function
ax = stars(df_widgets, line_colors=['#007ACC', '#FF4500', '#3CB371'])

# Add a title
ax.set_title('Widget Comparison Across Key Metrics', size=14, y=1.1)

# Display the plot
plt.show()
