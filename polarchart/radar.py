
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Patch
from colorspace import qualitative_hcl

def radar(df, labels = True, ax = None, ncol = None, scale = True, circles = True,
          legend_position = None, color = None, numeric_only = False,
          single_graph = False, *args, **kwargs):
    """Radar (Star/Spider) Plots and Segment Diagrams

    Draw star plots or segment diagrams of a multivariate data set.
    Besides the main function `radar()` additional convenience functions
    (`stars`, `spider`) are available using different defaults for easy
    access to the different visualization types.

    See also [radar](polarchart.radar.radar.qmd),
    [stars](polarchart.plottypes.stars.qmd), and
    [spider](polarchart.plottypes.spider.qmd).

    Args:
        df (pandas.core.frame.DataFrame): A pandas DataFrame with numeric values.
            Must have an index as well as column mames (TODO).
        labels (str, or bool): If `True` (default) the index DataFrame index
            (`df.index`) is used to add labels to each of the plots; `False`
            suppresses these labels. If a string is provided, the corresponding
            column/variable of the DataFrame is used to label the plots.
        ax (None or matplotlib.axes._axes.Axes): If None, a new figure is
            initialized. Else the existing axis is taken, manipulated, and populated.
        ncol (None or int): If `None`, a (near) quadratic grid will be created. Can e
            specified by the user to adjust the gridding. If `single_graph = True`
            this argument controls the number of columns of the color legend
            (defaults to `4` if `None`).
        scale (bool):
            Should the data in 'df' be scaled?
        circles (bool):
            If True, circles are drawn on top of the radar charts.
        legend_position (None, bool, or tuple): If 'None' (or 'True') the
            legend is positioned automatically. A tuple can be provided (x/y
            coordinates) to manually position, where '(x, y)' corresponds to
            '(left, downwards)' with '(0, 0)' corresponding to the position of the
            first radar plot (top left one). If set `False` the legend will not be
            drawn at all. See also argument `single_graph`.
        color (None, bool, list): If `None` (same as `True`) N colors from the
            qualitative palette 'Dynamic' (`colorspace.qualitative_hcl("Dynamic")`)
            will be used. Can be a list of valid colors/hex colors or `False` to
            not fill the polygons (`radar()`, `stars()`). See also argument
            `single_graph`.
        numeric_only (bool): Defaults to `False`, if set `True` all non-numeric
            columns/variables will be excluded.
        single_graph (bool): Defaults to `False`. If set `True` one single
            graph will be drawn with data superimposed on each other. In this
            case no legend is drawn as the labels are drawn on the single graph,
            and `color` is mapped to the rows of the DataFrame, not the columns.
        *args:
            Positional arguments; used by other functions interfacing this main
            function (`stars()`, ...).
        **kwargs:
            Additional keyword arguments, see Details for more information.

    Returns:
        If `ax = None` (no custom axis provided) there is no return but
        the plot created will be shown. If a custom axis is used the
        (modified) axis is returned.

    Details:

        Allowed additional arguments via the named **kwargs:
        - "title" (str): Plot title
        - "angle" (int, float): Rotation angle in degrees.
        - "figsize" (tuple): Custom figure size, ignored if an axis ('ax') is provided.
        - "_type" (str): Controls the plot type (radar, stars, spider).
        - "linewidth" (float): Set the width of the outline. By default, the line width
            is set `0.5` if `single_graph = False`, else `1.0` Can be overwritten.

    Examples:

        >>> from polarchart import get_demodata, radar
        >>> gsa = get_demodata("gsa")
        >>> print(gsa.head())
        >>>
        >>> ## TODO(R): *.iloc[:,1:3] causes erro (only two columns fail?)

        Default options (first three rows, three columns)
        >>> radar(gsa.iloc[:6,:], title = "Default radar chart")

        Customized: No circles, custom legend position, colors, and figure size.
        >>> from colorspace import diverging_hcl
        >>> radar(gsa.iloc[:6,:],
        >>>       title   = "Customized radar chart",
        >>>       circles = False,
        >>>       legend_position = (1.5, 2),
        >>>       color   = diverging_hcl("Green-Orange")(gsa.shape[1]),
        >>>       figsize = (12, 8))

        Single-graph layout:
        >>> radar(gsa, title = "Single-graph layout", single_graph = True)
    """

    from pandas import DataFrame
    from matplotlib import axes
    from .utils import prepare_num_df

    # -----------------------------------------------------------------
    # Sanity checks
    # -----------------------------------------------------------------
    if not isinstance(df, DataFrame):
        raise TypeError("argument 'df' must be a pandas.DataFrame")
    if not isinstance(labels, (bool, str)):
        raise TypeError("argument 'labels' must be bool, or str")
    if not isinstance(ax, (axes._axes.Axes, type(None))):
        raise TypeError("argument 'ax' must be None or matplotlib.axes._axes.Axes")
    if not isinstance(scale, bool):
        raise TypeError("argument 'scale' must be boolean True (default) or False")
    if not isinstance(ncol, (type(None), int)):
        raise TypeError("argument 'nrow' must be None or int")
    if not isinstance(circles, bool):
        raise TypeError("argument 'circles' must be bool")
    if not isinstance(legend_position, (type(None), tuple, bool)):
        raise TypeError("argument 'legend_position' must be None, bool, or a tuple")
    if not isinstance(color, (type(None), bool, list)):
        raise TypeError("argument 'color' must be None or list")
    if not isinstance(numeric_only, bool):
        raise TypeError("argument 'numeric_only' must be bool")
    if not isinstance(single_graph, bool):
        raise TypeError("argument 'single_graph' must be bool")
    if legend_position is None: legend_position = True

    # Value checks
    if isinstance(ncol, int) and ncol <= 0:
        raise ValueError("argument 'nrow' (if set) must be a positive integer")
    if isinstance(legend_position, tuple):
        if not len(legend_position) == 2:
            raise ValueError("if 'legend_position' is a tuple it must be of length 2")
        if not all([isinstance(x, (int, float)) for x in legend_position]):
            raise ValueError("elements in 'legend_position' must be numeric")

    # If single_graph is set we suppress the legend
    if single_graph: legend_position = False

    # Set of colors
    if color is None or color is True:
        color = qualitative_hcl("Dynamic")(df.shape[0 if single_graph else 1])

    # -----------------------------------------------------------------
    # Evaluating some kwargs
    # -----------------------------------------------------------------
    if "_type" in kwargs:
        if not isinstance(kwargs["_type"], str):
            raise TypeError("**kwarg '_type' must be str")
    _type = "radar" if not "_type" in kwargs else kwargs["_type"]
    if not _type in ["radar", "spider", "stars"]:
        raise ValueError("argument _type must be one of \"radar\", \"spider\", or \"stars\"")
    if "title" in kwargs:
        if not isinstance(kwargs["title"], str):
            raise TypeError("**kwarg 'title' must be str")
    title = "Awesome stars plot" if not "title" in kwargs else kwargs["title"]

    # Line width
    if "linewidth" in kwargs:
        if not isinstance(kwargs["linewidth"], (int, float)):
            raise TypeError("**kwarg 'linewidth' must be int or float")
        linewidth = abs(float(kwargs["linewidth"]))
    else:
        linewidth = 0.5 if not single_graph else 2.0


    if "angle" in kwargs:
        if not isinstance(kwargs["angle"], (int, float)):
            raise TypeError("**kwarg 'angle' must be str")
    angle = 0 if not "angle" in kwargs else kwargs["angle"]


    # Default radius used for scaling. 0.5 means that the segments of
    # neighboring radar charts would touch (if x == 1); so we use
    # something < 0.5 to allow all segments to have enough space to 
    # be plotted, at least if the data are scaled (x in [0, 1]).
    radius = 0.4

    # -----------------------------------------------------------------
    # Preparing data
    # -----------------------------------------------------------------

    # [!] First and formost: make a local copy of df to avoid
    # messing with the users object (avoiding scoping and infix operations)
    df = df.copy()

    # Return logical True/False if labels should be drawn later, and the modified
    # data set if everything goes well. Else prepare_data() will throw errors
    # and hints.
    labels, df = prepare_num_df(df, labels, numeric_only)

    # Preparing the data frame
    df = df.astype(float)
    if scale:
        from .utils import scale_df
        df = scale_df(df)
        # After scaling max raduis (normalized) is 1
        df_max = 1
    else:
        # Else we take the overall maximum for scaling the polygons and circles
        df_max = df.max().max()

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
            return nrow, ncol
        # Else we guess based on the aspect ratio of the axis
        asp  = float(axsize[1] / axsize[0])
        nrow = int(np.round(np.sqrt(n / asp)))
        ncol = int(np.ceil(n / nrow))
        return nrow, ncol

    # Has the user set a custom legend position?
    custom_legend_position = True if isinstance(legend_position, tuple) else False

    # The + int(not custom_legend_position) is used to save
    # one grid for the legend if auto-positioned. Else the users
    # has to find a suitable position themselves. Is ignored later
    # if single_graph = True
    nrow, ncol = get_gridsize(axsize, ncol = ncol,
                              n = df.shape[0] + int(not custom_legend_position))

    # Setting automatic legend position (bottom right 'grid cell') if 
    # no custom legend position was specified by the user. This variable
    # is also specified if legend_position = False although never used.
    # If single_graph = True we set the legend position to (0, 0) and will
    # only draw the labels (not the full legend) at the end of this function.
    if single_graph:
        legend_position = (0, 0)
    elif not isinstance(legend_position, tuple) and not legend_position is False:
        legend_position = (ncol - 1, nrow - 1)

    # -----------------------------------------------------------------
    # Plotting
    # -----------------------------------------------------------------

    # Keep aspect ratio 1:1
    ax.set_aspect("equal", adjustable = "box")

    # Hiding axis, setting (preliminary) limits. We'll draw
    # the * plots at a regular grid with coordinates (1, 1)
    # if we only have one; this way we can keep the scaling
    # to '1.0' to fill one square. Accounts for custom and
    # automatic legend positioning.
    ax.set_axis_off()
    if not legend_position is False and not single_graph:
        ax.set_xlim(min(-0.5, legend_position[0] - 0.5),
                    max(ncol - 0.5, legend_position[0] + 0.5))
        ax.set_ylim(min(-0.5, legend_position[1] - 0.5),
                    max(nrow - 0.5, legend_position[1] + 0.5))
    ## If single graph we need space for one plot + legend!
    elif single_graph:
        ax.set_xlim(-0.5, 0.5)
        ax.set_ylim(-0.5, 0.7)
    else:
        ax.set_xlim(-0.5, ncol - 0.5)
        ax.set_ylim(-0.5, nrow - 0.5)

    # Ensure x/y aspect is always 1:1 and invert the y-axis
    # so we draw out grid (0,0), (1,0), (2, 0) "top down"
    ax.invert_yaxis()
    ax.set_aspect('equal')

    # x/y are the positionas as well as the indices!
    col_index = np.reshape(range(ncol * nrow), (nrow, ncol), order = "C")

    ## Transparency; used for _type = "stars" if single_graph = True
    if _type in ["stars", "radar"] and single_graph:
        alpha = float(1 / np.log(df.shape[0]) * np.log(3) * 0.5)
    else:
        alpha = 1.0

    # ---------------------------------------------------------------
    # Adding 'data' (drawing the different radar plots)
    # ---------------------------------------------------------------
    for x in range(ncol):
        for y in range(nrow):
            idx = col_index[y, x]
            ## If 'idx >= df.shape[0]' this is an empty cell (as we
            ## reserve at least one for the legend).
            if idx >= df.shape[0]: continue # Empty grid cell, continue

            ## Calculating polygons for segments as well as label positions
            polygons, polylabels = get_patches(x         = df.iloc[idx, :],
                                               _type     = _type,
                                               center    = (x, y) if not single_graph else (0., 0.),
                                               color     = color if not single_graph else [color[idx]],
                                               radius    = radius,
                                               xmax      = df_max,
                                               angle     = angle,
                                               edgecolor = "gray" if not single_graph else color[idx],
                                               linewidth = linewidth,
                                               alpha     = alpha)
            ## Draw polygons
            for p in polygons.values(): ax.add_patch(p)

            ## Adding labels if requested. Suppressing labels
            ## is not a common usecase but available as an option.
            if labels and not single_graph:
                ax.text(x, y + 0.5, df.index[idx], ha = "center",
                        va = "bottom" if idx % 2 == 0 else "top")

            ## Adding circles if requested. If `single_graph` we only
            ## want to draw one set of circles on index 0, i.e., the
            ## first and only plot drawn.
            if circles and (not single_graph or idx == 0):
                # First we calculate what "useful" circles would be by
                # checking the overall maximum of 'df' and then set up
                # a vector with circles to draw; always on one digit
                # after the decimal sign as the polylabels currently
                # use ".1f" (rounded to closest 0.1).
                from .utils import pretty_ticks
                at = pretty_ticks(4, min_ = 0.0, max_ = df_max)[1:] # Removing zero
                polygons, polylabels = get_circle_coords(center = (x, y),
                                                         radius = radius,
                                                         at     = list(at),
                                                         xmax   = df_max)
                for k,p in polygons.items():
                    ax.add_patch(p)
                    ax.text(x = polylabels[k][0], y = polylabels[k][1], s = k,
                            ha = "center", va = "center",
                            color = "gray" if not single_graph else "dimgray",
                            fontsize = 6)

    # ---------------------------------------------------------------
    # Adding legend
    # ---------------------------------------------------------------
    if not legend_position is False:
        tmp = pd.Series(data = np.repeat(1.0, df.shape[1]),
                        index = df.columns, name = "legend")
        polygons, polylabels = get_patches(x      = tmp,
                                           _type  = _type,
                                           center = legend_position,
                                           color  = color,
                                           radius = 0.25 if not single_graph else 0.35,
                                           xmax   = 1, # fixed size
                                           angle  = angle,
                                           linewidth = linewidth)
        for k in polygons.keys():
            if not single_graph: ax.add_patch(polygons[k])
            ax.text(x = polylabels[k][0], y = polylabels[k][1], s = k,
                    ha = "center", va = "center", fontsize = 7)

        # Adding color legend (single graph only)
        if single_graph:
            leg_ncol = 4 if ncol is None else ncol
            handles = [Patch(color = c, label = l) for c,l in zip(color, df.index)]
            ax.legend(handles        = handles,
                      loc            = "lower center", # Placing legend at the bottom
                      ncol           = df.shape[0] if df.shape[0] <= leg_ncol else leg_ncol,
                      bbox_to_anchor = (0.5, -0.1),
                      fontsize       = "small",
                      frameon        = False)


    # ---------------------------------------------------------------
    # Adjusting axis and show plot (if required)
    # ---------------------------------------------------------------
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.set_title(title)

    # If 'fig = None' the user provided their own axis ('ax = ...'),
    # in this case we just return the axis. Else we show the plot.
    if fig is not None:
        plt.show()
    else:
        return ax


def get_patches(x, _type, center, color, radius, xmax, angle = 0,
                edgecolor = "gray", linewidth = 0.5, alpha = 1.0):
    """get_patches(x, _type, center, color, radius, angle = 0, edgecolor = "gray", linewidth = 0.5)

    Args:
        x (pandas.core.series.Series): A pandas series with numeric values for
            which the radar plot segments need to be created.
        _type (str): Plot type, defines how the patches (geometries) are
            calculated.
        center (tuple): Tuple with two numeric values defining the center of
            the radar plot used for positioning.
        color (False, list): False suppresses facecolor. A list of valid colors
            used as facecolor of the segments.
        radius (float): Radius of the
            segments, defaults to '0.43'. The plotting function uses a "1 by 1"
            grid, i.e., two neighboring radar plots are distanced by "1.0" on the
            x/y coordinates. 'radius = 0.43' means that a segment where 'x = 1.0'
            will have a radius of '0.43' which gives us enough space to draw the
            radar plots side-by-side without overlap. If `x` is not scaled the
            picture looks different, though.
        xmax (num): Additional scaling factor. When plotting standardized data
            `xmax = 1.0` so that the max radius is equal to `radius`. All
            coordinates will be scaled with this factor.
        angle (float or int): Rotation angle (in degrees), defaults to '0'.
            When '0' the first segments starts "to the right" of the center.
        edgecolor (str, int, None): Edge color used to draw polygon outlines.
        linewidth (float): Width of the line for the polygon outlines.
        alpha (float): A value between `0` (completely transparent) and `1`
            (completely opaque). Used for `single_graph` displays.

    Returns:
        list of dicts : Returns two dictionaries. The first one contains
        a series of 'matplotlib.patches.Polygons' which define the segments
        to be drawn, the second one (same length) a series of tuples corresponding
        to the '(x, y)' coordinates to position the labels. The dict keys correspond
        to the labels (properties) of the different segments.
    """

    ## Angle in radiant
    anglerad = angle / 180 * np.pi
    ## Rough radius interval (the smaller the 'rounder')
    radi   = 2 * np.pi / 180
    ## Angles for the arc (radiant)
    theta  = np.linspace(0, -2 * np.pi, len(x) + 1) + anglerad

    ## For '_type == "radar" we use the center of the two 
    ## neighboring thetas, else theta
    label_angle = (theta[:-1] + theta[1:]) / 2.0 if _type == "radar" else theta[:-1]

    ## IF 'color' is a list of length 1, recycle
    if isinstance(color, list) and len(color) == 1:
        color = [color[0] for x in range(len(x))]

    ## Resulting dictionary
    result = dict()
    labels = dict()

    ## Create Polygon for each of the segments
    for i in range(len(x)):
        num = int(abs(theta[i + 1] - theta[i]) // radi) if _type == "radar" else 2
        angle = np.hstack([np.linspace(theta[i], theta[i + 1], num)])

        # Calculate geometry of the polygon
        if _type == "radar":
            poly_x = center[0] + x.iloc[i] * radius * np.cos(angle) / xmax
            poly_y = center[1] + x.iloc[i] * radius * np.sin(angle) / xmax
        else:
            ii = [i, i + 1] if i < (len(x) - 1) else [i, 0]
            poly_x = center[0] + x.iloc[ii] * radius * np.cos(angle) / xmax
            poly_y = center[1] + x.iloc[ii] * radius * np.sin(angle) / xmax

        if _type == "radar" or _type == "stars":
            arc   = np.vstack([center, np.column_stack([poly_x, poly_y])])
        else:
            arc   = np.column_stack([poly_x, poly_y])
        # Setting up matplotlib.patches.Polygon
        result[x.index[i]] = Polygon(arc,
                                     closed    = not _type == "spider",
                                     facecolor = "none" if not color else color[i],
                                     edgecolor = edgecolor,
                                     linewidth = linewidth,
                                     alpha     = alpha)

        # Calculating label position
        labels[x.index[i]] = (center[0] + 1.4 * radius * np.cos(label_angle[i]),
                              center[1] + 1.4 * radius * np.sin(label_angle[i]))

    return result, labels


def get_circle_coords(center, radius, at, xmax):
    """Calculate Circle Polygons

    Args:
        center : tuple
            Tuple of two numeric values defining the center of the
            stars plot/center of the grid box.
        radius : num
            Positive numeric, maximum radius (if 0.5 neighboring
            plots would touch as we are on a one-by-one grid).
        at : list
            List of numeric values for which a circle should be
            drawn (calculated).
        xmax : num
            Additional scaling factor. When plotting standardized
            data `xmax = 1.0` so that the max radius is equal to
            `radius`. All coordinates will be scaled with this factor.

    Returns:
        A dictionary of polygons (`matplotlib.patches.Polygon`s),
        each of which defines one circle. The dict keys are used
        as labels when drawn.
    """

    n        = 180 # Number of points along the polygon
    theta    = np.linspace(0, -2 * np.pi, 180) # Calculating angles
    anglerad = -45 / 180 * np.pi

    # Number of significant digits needed
    from .utils import required_digits
    digits = required_digits(at)

    labels = dict()
    result = dict()
    for a in at:
        hash = f"{a:.{digits}f}"
        # Multiply by radius for proper scaling
        arc_x  = center[0] + a * radius * np.cos(theta) / xmax
        arc_y  = center[1] + a * radius * np.sin(theta) / xmax
        circle = np.column_stack([arc_x, arc_y])

        # Setting up matplotlib.patches.Polygon
        result[hash] = (Polygon(circle,
                                closed    = True,
                                fill      = False,
                                edgecolor = "gray",
                                linestyle = (0, (6, 7)), # loosely dashed
                                linewidth = 0.5))
        labels[hash] = (center[0] + a * radius * np.cos(anglerad) / xmax,
                        center[1] + a * radius * np.sin(anglerad) / xmax)

    return result, labels


