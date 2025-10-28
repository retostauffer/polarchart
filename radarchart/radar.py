
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def radar(df, ax = None, ncol = None, scale = True, **kwargs):
    """radar(df, ax = None, scale = True, **kwargs)

    Params
    ======
    ncol : None or int
        None (auto-gridding) or a positive integer.
    TODO(R)
    """

    from pandas import DataFrame
    from matplotlib import axes

    from matplotlib.patches import Polygon
    import matplotlib.colors as mcolors

    from colorspace import qualitative_hcl

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
    if isinstance(ncol, int) and int <= 0:
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
    print(df)

    # -----------------------------------------------------------------
    # Plotting
    # -----------------------------------------------------------------

    # Calculating x/y positions
    ncharts = df.shape[0]
    if ncol is None: ncol = int(np.ceil(np.sqrt(ncharts)))
    nrow = int(np.ceil(ncharts / ncol))
    print(f"Need to draw {ncharts=} with {ncol=}/{nrow=}")

    # Keep aspect ratio 1:1
    ax.set_aspect("equal", adjustable = "box")

    # Calculating center positions; we will center the
    # first circle at (0, 0), (0, 1), ..

    # Hiding axis, setting (preliminary) limits. We'll draw
    # the * plots at a regular grid with coordinates (1, 1)
    # if we only have one; this way we can keep the scaling
    # to '1.0' to fill one square.
    ax.set_axis_off()
    ax.set_xlim(-0.5, ncol + 0.5)
    ax.set_ylim(-0.5, nrow + 0.5)

    def calc_radar_coords(x, center, color, angle = 0):
        # Angles
        radi   = 2 * np.pi / 180 ## rough radius interval (the smaller the 'rounder')
        zero   = np.array([0])
        theta  = np.linspace(0, 2 * np.pi, len(x) + 1)
        result = dict()
        for i in range(len(x)):
            angle = np.hstack([np.linspace(theta[i], theta[i + 1],
                                           int((theta[i + 1] - theta[i]) // radi))])
            # 0.45 so that x[i] = 1 corresponds to a radius of 0.45,
            # allowing all radar plots to exist next to each other
            # on a 1x1 grid.
            arc_x = center[0] + x[i] * 0.45 * np.cos(angle)
            arc_y = center[1] + x[i] * 0.45 * np.sin(angle)
            c = np.vstack([center, np.column_stack([arc_x, arc_y])])
            print(c)
            result[x.index[i]] = Polygon(c, closed = True,
                                         facecolor = color[i])

        return result

    # x/y are the positionas as well as the indices!
    col_index = np.reshape(range(ncol * nrow), (ncol, nrow), order = "C")

    # Set of colors
    color = qualitative_hcl("Dynamic")(df.shape[1])

    print(col_index)
    for x in range(ncol):
        for y in range(nrow):
            print(f"Drawing {x=}, {y=}")
            ax.text(x, y, f"x={x},y={y}")
            polygons = calc_radar_coords(df.iloc[col_index[x, y], :],
                                         center = (x, y), color = color)
            ###calc_radar?
            for p in polygons.values():
                ax.add_patch(p)

    # Ensure x/y aspect is always 1:1
    ax.set_aspect('equal')


    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.set_title("Grid of Circles with Origin Text")

    plt.show()
