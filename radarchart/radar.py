
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from colorspace import qualitative_hcl

def radar(df, ax = None, ncol = None, scale = True, **kwargs):
    """radar(df, ax = None, scale = True, **kwargs)

    Params
    ======
    df : DataFrame
        A pandas DataFrame with numeric values. Must have an index
        as well as column mames (TODO).
    ax : None or matplotlib.axes._axes.Axes
        If None, a new figure is initialized. Else the existing
        axis is taken, manipulated, and populated.
    ncol : None or int
        If none, a (near) quadratic grid will be created. Can e specified
        by the user to adjust the gridding.
    scale : bool
        Should the data in 'df' be scaled?
    **kwargs : various
        Additional keyword arguments, see Details for more information.

    Details
    =======
    Allowed additional arguments via the named **kwargs:
    - "title" (str): Plot title
    - "angle" (int, float): Rotation angle in degrees.
    """

    from pandas import DataFrame
    from matplotlib import axes

    import matplotlib.colors as mcolors

    if "title" in kwargs:
        if not isinstance(kwargs["title"], str):
            raise TypeError("**kwarg 'title' must be str")
    title = "Awesome stars plot" if not "title" in kwargs else kwargs["title"]

    if "angle" in kwargs:
        if not isinstance(kwargs["angle"], (int, float)):
            raise TypeError("**kwarg 'angle' must be str")
    angle = 0 if not "angle" in kwargs else kwargs["angle"]


    # -----------------------------------------------------------------
    # Sanity checks
    # -----------------------------------------------------------------
    if not isinstance(df, DataFrame):
        raise TypeError("argument 'df' must be a pandas.DataFrame")
    if not isinstance(ax, (axes._axes.Axes, type(None))):
        raise TypeError("argument 'ax' must be None or matplotlib.axes._axes.Axes")
    if not isinstance(scale, bool):
        raise TypeError("argument 'scale' must be boolean True (default) or False")
    if not isinstance(ncol, (type(None), int)):
        raise TypeError("argument 'nrow' must be None or int")
    if isinstance(ncol, int) and ncol <= 0:
        raise ValueError("argument 'nrow' (if set) must be a positive integer")

    if ax is None:
        fig, ax = plt.subplots(figsize = (6, 6))

    figsize = (fig.get_figheight(), fig.get_figwidth())
    print(f"Current figure size: {figsize=}")

    # -----------------------------------------------------------------
    # Preparing data
    # -----------------------------------------------------------------
    if scale:
        from radarchart.utils import scale_df
        df = scale_df(df)

    # -----------------------------------------------------------------
    # Plotting
    # -----------------------------------------------------------------

    # Calculating x/y positions; number of rows + 1 to always have the
    # very last space empty to draw the legend.
    ncharts = df.shape[0] + 1
    if ncol is None: ncol = int(np.floor(np.sqrt(ncharts)))
    nrow = int(np.ceil(ncharts / ncol))
    print(f"Need to draw {ncharts=} with {ncol=}/{nrow=}")

    # Keep aspect ratio 1:1
    ax.set_aspect("equal", adjustable = "box")

    # Hiding axis, setting (preliminary) limits. We'll draw
    # the * plots at a regular grid with coordinates (1, 1)
    # if we only have one; this way we can keep the scaling
    # to '1.0' to fill one square.
    ax.set_axis_off()
    ax.set_xlim(-0.5, ncol - 0.5)
    ax.set_ylim(-0.5, nrow - 0.5)

    # Ensure x/y aspect is always 1:1 and invert the y-axis
    # so we draw out grid (0,0), (1,0), (2, 0) "top down"
    ax.invert_yaxis()
    ax.set_aspect('equal')


    # x/y are the positionas as well as the indices!
    col_index = np.reshape(range(ncol * nrow), (nrow, ncol), order = "C")
    #print(col_index)

    # Set of colors
    color = qualitative_hcl("Dynamic")(df.shape[1])

    print(f"   {ncol=}  {nrow=}")
    print(col_index)
    for x in range(ncol):
        for y in range(nrow):
            idx = col_index[y, x]
            ## If 'idx >= df.shape[0]' this is an empty cell (as we
            ## reserve at least one for the legend).
            if idx >= df.shape[0]: continue # Empty grid

            print(f"Drawing {x=}, {y=}")
            ax.text(x, y, f"x={x},y={y}")

            polygons = calc_radar_coords(df.iloc[idx, :],
                                         center = (x, y), color = color,
                                         angle = angle)
            ###calc_radar?
            for p in polygons.values(): ax.add_patch(p)


    ## Adding legend
    tmp = pd.Series(data = np.repeat(0.8, df.shape[1]),
                    index = df.columns, name = "legend")
    print(tmp)
    print(f"{nrow=}, {ncol=}")
    legend_polygon = calc_radar_coords(tmp,
                                       center = (ncol - 1, nrow - 1),
                                       color = color,
                                       angle = angle)
    ax.text(ncol - 1, nrow - 1, "legend")
    for p in legend_polygon.values(): ax.add_patch(p)


    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.set_title(title)

    plt.show()


def calc_radar_coords(x, center, color, angle = 0):
    ## Additional rotation; angle is in degrees, convert to radiant
    anglerad = angle / 180 * np.pi
    ## Offset of 0.45 ensures that the segments can all be drawn
    ## on a grid of 1 by 1 (x == 1 results in a radius of 'radius'
    radius = 0.45
    ## Rough radius interval (the smaller the 'rounder')
    radi   = 2 * np.pi / 180
    ## Zero ('center') point
    zero   = np.array([0])
    ## Angles for the arc (radiant)
    theta  = np.linspace(0, 2 * np.pi, len(x) + 1) + anglerad

    ## Resulting dictionary
    result = dict()

    ## Create Polygon for each of the segments
    for i in range(len(x)):
        angle = np.hstack([np.linspace(theta[i], theta[i + 1],
                                       int((theta[i + 1] - theta[i]) // radi))])
        # 0.45 so that x[i] = 1 corresponds to a radius of 0.45,
        # allowing all radar plots to exist next to each other
        # on a 1x1 grid.
        arc_x = center[0] + x[i] * radius * np.cos(angle)
        arc_y = center[1] + x[i] * radius * np.sin(angle)
        arc   = np.vstack([center, np.column_stack([arc_x, arc_y])])
        # Setting up matplotlib.patches.Polygon
        result[x.index[i]] = Polygon(arc,
                                     closed = True,
                                     facecolor = color[i])

    return result

