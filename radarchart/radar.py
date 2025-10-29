
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from colorspace import qualitative_hcl

def radar(df, ax = None, ncol = None, scale = True,
          legend_position = None, **kwargs):
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
    legend_position : None or tuple
        If 'None' the legend is positioned automatically. A tuple can
        be provided (x/y coordinates) to manually position, where
        '(x, y)' corresponds to '(left, downwards)' with '(0, 0)' corresponding
        to the position of the first radar plot (top left one).

    **kwargs : various
        Additional keyword arguments, see Details for more information.

    Details
    =======
    Allowed additional arguments via the named **kwargs:
    - "title" (str): Plot title
    - "angle" (int, float): Rotation angle in degrees.
    - "figsize" (tuple): Custom figure size, ignored if an axis ('ax') is provided.
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
    if not isinstance(legend_position, (type(None), tuple)):
        raise TypeError("argument 'legend_position' must be None or a tuple")

    # Value checks
    if isinstance(ncol, int) and ncol <= 0:
        raise ValueError("argument 'nrow' (if set) must be a positive integer")
    if isinstance(legend_position, tuple):
        if not len(legend_position) == 2:
            raise ValueError("if 'legend_position' is a tuple it must be of length 2")
        if not all([isinstance(x, (int, float)) for x in legend_position]):
            raise ValueError("elements in 'legend_position' must be numeric")

    # -----------------------------------------------------------------
    # Preparing data
    # -----------------------------------------------------------------
    if scale:
        from radarchart.utils import scale_df
        df = scale_df(df)

    if ax is None:
        figsize = (6, 6) if not "figsize" in kwargs else kwargs["figsize"]
        fig, ax = plt.subplots(figsize = figsize)
    else:
        fig = None # Dummy which indicates the user provided an axis

    # Determine size of the axis to find the best placement/grid for the plots
    def axis_get_size(ax):
        # Get axis position (relative) and scale it with figure size
        bbox = ax.get_position()
        fig_w, fig_h = ax.figure.get_size_inches()
        ax_h = bbox.height * fig_h
        ax_w = bbox.width  * fig_w
        ##print(f"Current axis size:     height = {ax_h}, width = {ax_w}")
        return((ax_h, ax_w))

    axsize = axis_get_size(ax)

    # Calculating x/y positions; number of df-rows + 1 to always have the
    # very last space empty to draw the legend.
    def get_gridsize(axsize, ncol, n):
        # If 'ncol' is an integer the job is easy
        if ncol is not None:
            nrow = int(np.ceil(n / ncol))
            print(f" --------- {n=}    {nrow=} / {ncol=}")
            return nrow, ncol
        # Else we guess based on the aspect ratio of the axis
        asp  = float(axsize[1] / axsize[0])
        nrow = int(np.round(np.sqrt(n / asp)))
        ncol = int(np.ceil(n / nrow))
        print(f" --------- {asp=}      {n=}    {nrow=} / {ncol=}")
        return nrow, ncol

    # Has the user set a custom legend position?
    custom_legend_position = True if legend_position is not None else False

    # The + int(not custom_legend_position) is used to save
    # one grid for the legend if auto-positioned. Else the users
    # has to find a suitable position themselves.
    nrow, ncol = get_gridsize(axsize, ncol = ncol,
                              n = df.shape[0] + int(not custom_legend_position))

    # Setting automatic legend position (bottom right 'grid cell') if 
    # no custom legend position was specified by the user.
    if legend_position is None:
        legend_position = (ncol - 1, nrow - 1)

    # -----------------------------------------------------------------
    # Plotting
    # -----------------------------------------------------------------

    # Keep aspect ratio 1:1
    ax.set_aspect("equal", adjustable = "box")

    # Hiding axis, setting (preliminary) limits. We'll draw
    # the * plots at a regular grid with coordinates (1, 1)
    # if we only have one; this way we can keep the scaling
    # to '1.0' to fill one square.
    ax.set_axis_off()
    ax.set_xlim(min(-0.5, legend_position[0] - 0.5),
                max(ncol - 0.5, legend_position[0] + 0.5))
    ax.set_ylim(min(-0.5, legend_position[1] - 0.5),
                max(nrow - 0.5, legend_position[1] + 0.5))

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

            polygons = calc_radar_coords(df.iloc[idx, :],
                                         center = (x, y), color = color,
                                         angle = angle)
            ## Draw polygons
            for p in polygons.values(): ax.add_patch(p)
            ## Adding label
            ax.text(x, y + 0.5, df.index[idx],
                    ha = "center",
                    va = "bottom" if idx % 2 == 0 else "top")



    ## Adding legend

    def add_legend(ax, labels, center, color, angle, radius):
        tmp = pd.Series(data = np.repeat(1.0, len(labels)),
                        index = df.columns, name = "legend")
        legend_polygon = calc_radar_coords(tmp,
                                           center = center,
                                           color = color,
                                           angle = angle,
                                           radius = radius)
        for p in legend_polygon.values(): ax.add_patch(p)

        # Labels
        # TODO(R): 'theta' is also calculated in calc_radar_coords,
        #          maybe write a little function for that.
        anglerad = angle / 180 * np.pi
        theta    = np.linspace(0, -2 * np.pi, len(labels) + 1) + anglerad
        theta    = (theta[:-1] + theta[1:]) / 2.0
        for i in range(len(labels)):
            ax.text(x = center[0] + 1.4 * radius * np.cos(theta[i]),
                    y = center[1] + 1.4 * radius * np.sin(theta[i]),
                    s = labels[i],
                    va = "center", ha = "center")

    add_legend(ax, labels = df.columns, center = legend_position,
               color = color, angle = angle, radius = 0.2)

    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.set_title(title)

    plt.show()


def calc_radar_coords(x, center, color, angle = 0, radius = 0.40,
                      edgecolor = "gray", linewidth = 0.5):
    """calc_radar_coords(x, center, color, angle = 0, radius = 0.40)

    Params
    ======
    x : pandas.core.series.Series
        A pandas series with numeric values for which the radar plot
        segments need to be created.
    center : tuple
        Tuple with two numeric values defining the center of the radar
        plot used for positioning.
    color : list
        List of valid colors used as facecolor of the segments.
    angle : float or int
        Rotation angle (in degrees), defaults to '0'. When '0'
        the first segments starts "to the right" of the center.
    radius : float
        Radius of the segments, defaults to '0.43'.
        The plotting function uses a "1 by 1" grid, i.e., two
        neighboring radar plots are distanced by "1.0" on the x/y
        coordinates. 'radius = 0.43' means that a segment
        where 'x = 1.0' will have a radius of '0.43' which gives
        us enough space to draw the radar plots side-by-side without
        overlap. If `x` is not scaled the picture looks different, though.
    edgecolor : str, int, None
        Edge color used to draw polygon outlines.
    linewidth : float
        Width of the line for the polygon outlines.

    Return
    ======
    dict : A dictionary with a series of 'matplotlib.patches.Polygons'
    which represent the segments to be drawn. The dict keys correspond
    to the index of the pandas series ('x').
    """
    ## Offset of 0.45 ensures that the segments can all be drawn
    ## on a grid of 1 by 1 (x == 1 results in a radius of 'radius'
    ## Additional rotation; angle is in degrees, convert to radiant
    anglerad = angle / 180 * np.pi
    ## Rough radius interval (the smaller the 'rounder')
    radi   = 2 * np.pi / 180
    ## Zero coordinate point
    zero   = np.array([0])
    ## Angles for the arc (radiant)
    theta  = np.linspace(0, -2 * np.pi, len(x) + 1) + anglerad

    ## Resulting dictionary
    result = dict()

    ## Create Polygon for each of the segments
    for i in range(len(x)):
        angle = np.hstack([np.linspace(theta[i], theta[i + 1],
                                       int(abs(theta[i + 1] - theta[i]) // radi))])
        # 0.45 so that x[i] = 1 corresponds to a radius of 0.45,
        # allowing all radar plots to exist next to each other
        # on a 1x1 grid.
        arc_x = center[0] + x[i] * radius * np.cos(angle)
        arc_y = center[1] + x[i] * radius * np.sin(angle)
        arc   = np.vstack([center, np.column_stack([arc_x, arc_y])])
        # Setting up matplotlib.patches.Polygon
        result[x.index[i]] = Polygon(arc,
                                     closed = True,
                                     facecolor = color[i],
                                     edgecolor = edgecolor,
                                     linewidth = linewidth)

    return result

