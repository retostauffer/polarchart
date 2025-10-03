
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def radar(df, ax = None, scale = True, **kwargs):
    """radar(df, ax = None, scale = True, **kwargs)
    
    TODO(R)
    """

    from pandas import DataFrame
    from matplotlib import axes

    # -----------------------------------------------------------------
    # Sanity checks
    # -----------------------------------------------------------------
    if not isinstance(df, DataFrame):
        raise TypeError("argument 'df' must be a pandas.DataFrame")
    if not isinstance(ax, (axes._axes.Axes, type(None))):
        raise TypeError("argument 'ax' must be None or matplotlib.axes._axes.Axes")
    if not isinstance(scale, bool):
        raise TypeError("argument 'scale' must be boolean True (default) or False")

    if ax is None:
        fig, ax = plt.subplots(figsize = (6, 6))



    # -----------------------------------------------------------------
    # Preparing data
    # -----------------------------------------------------------------
    if scale:
        from radarchart.utils import scale_df
        df = scale_df(df)
    print(df)


    # -----------------------------------------------------------------
    # Plotting
    # -----------------------------------------------------------------

    # Hiding axis, setting (preliminary) limits. We'll draw
    # the * plots at a regular grid with coordinates (1, 1)
    # if we only have one; this way we can keep the scaling
    # to '1.0' to fill one square.
    ax.set_axis_off()
    ax.set_xlim(0, 2)
    ax.set_ylim(0, 2)

    # Ensure x/y aspect is always 1:1
    ax.set_aspect('equal')



    print(kwargs)