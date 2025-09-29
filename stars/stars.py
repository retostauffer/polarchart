

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def stars(df, ax=None, line_colors=None, fill=True, alpha=0.25, line_width=1.5, **kwargs):
    """
    Plots a Star Plot (Radar Chart) for each row in a DataFrame.

    Parameters:
    - df (pd.DataFrame): Data where rows are observations/items and columns are variables/axes.
    - ax (plt.Axes): Existing axes to plot on. If None, creates a new polar subplot.
    - line_colors (list): List of colors for the lines.
    - fill (bool): Whether to fill the polygons.
    - alpha (float): Transparency for the polygon fill.
    - line_width (float): Thickness of the line boundaries.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    # --- 1. Data Preparation and Normalization ---
    # Normalize data (0 to 1) for consistent radial scaling
    df_norm = df.apply(lambda x: (x - x.min()) / (x.max() - x.min()), axis=0)

    # Number of variables (axes)
    N = df.shape[1]

    # --- 2. Calculate Angles ---
    # Create an array of angles (in radians) for each variable, closing the circle
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    angles += angles[:1] # Repeat the first angle to close the plot

    # --- 3. Plotting Loop ---
    # Prepare colors if not provided
    if line_colors is None:
        # Use a Matplotlib colormap (e.g., 'viridis')
        cmap = plt.cm.get_cmap('viridis', len(df))
        line_colors = [cmap(i) for i in range(len(df))]

    # Iterate over each row (observation/item)
    for i, (index, row) in enumerate(df_norm.iterrows()):
        values = row.tolist()
        values += values[:1] # Repeat the first value to close the polygon

        color = line_colors[i % len(line_colors)]
        label = index # Use the row index as the label

        # Plot the line (the boundary of the star)
        ax.plot(angles, values, color=color, linewidth=line_width, label=label, **kwargs)

        # Fill the polygon
        if fill:
            ax.fill(angles, values, color=color, alpha=alpha)

    # --- 4. Axis Customization ---

    # Set the label position to the angles
    ax.set_xticks(angles[:-1])

    # Set the variable names as the labels for the axes
    ax.set_xticklabels(df.columns)

    # Set radial limits and ticks (0 to 1 for normalized data)
    ax.set_yticks(np.linspace(0, 1, 5)) # Show 5 radial grid lines
    return ax
