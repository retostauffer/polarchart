
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from statsmodels.graphics.mosaicplot import mosaic
from matplotlib import colors as mcolors

def spineplot(df, x, y, labels = None, ax = None, *args, **kwargs):
    """Create spine plot

    Args:
        df (pandas.core.frame.DataFrame): A pandas DataFrame.
        x (str): Name of the variable for the first dimension.
        y (str): Name of the variable for the second dimension.
        labels (None, str): Either `None` (default) to suppress labels,
            or one of `"absolute"`, `"relative"`, `"percent"`.
        ax (None or matplotlib.axes._axes.Axes): If None, a new figure is
            initialized. Else the existing axis is taken, manipulated, and populated.
        *args:
            Positional arguments; used by other functions interfacing this main
            function (`stars()`, ...).
        **kwargs:
            Additional keyword arguments, see Details for more information.

    Returns:
        If `ax = None` (no custom axis provided) a list of length two is
        returned with (i) the data frame with the categorical variables
        used to calculate the spine plot as well as the cross-table
        the plot is based on. If a custom axis was provided, the modified
        axis is returned.

    Details:

        TODO
        Allowed additional arguments via the named **kwargs:
        - "flipud" (bool): Flip y axis upside down (default is True).
        - "title" (str): Plot title
        - "angle" (int, float): Rotation angle in degrees.
        - "figsize" (tuple): Custom figure size, ignored if an axis ('ax') is provided.

    Examples:

    >>> # TODO
    >>> 1 + 5

    """

    from pandas import DataFrame, Index, cut
    import numpy as np
    from matplotlib import axes

    # -----------------------------------------------------------------
    # Sanity checks
    # -----------------------------------------------------------------
    if not isinstance(df, DataFrame):
        raise TypeError("argument 'df' must be a pandas.DataFrame")
    if not isinstance(x, str):
        raise TypeError("argument 'x' must be str")
    if not isinstance(y, str):
        raise TypeError("argument 'y' must be str")
    if not isinstance(labels, (type(None), str)):
        raise TypeError("argument 'labels' must be None or str")
    if not isinstance(ax, (axes._axes.Axes, type(None))):
        raise TypeError("argument 'ax' must be None or matplotlib.axes._axes.Axes")

    if not x in df.columns:
        raise ValueError(f"variable {x=} not found in 'df'")
    if not y in df.columns:
        raise ValueError(f"variable {y=} not found in 'df'")
    if labels is not None:
        labels_allowed = ["absolute", "relative", "percent"]
        if not labels in labels_allowed:
            raise ValueError(f"argument 'labels' must be None or one of {', '.join(labels_allowed)}")

    if ax is None:
        figsize = (6, 6) if not "figsize" in kwargs else kwargs["figsize"]
        fig, ax = plt.subplots(figsize = figsize)
    else:
        fig = None # Dummy which indicates the user provided an axis

    # ---------------------------------------------------------------
    # Evaluating additional kwargs arguments if any
    # ---------------------------------------------------------------
    if "flipud" in kwargs:
        if not isinstance(kwargs["flipud"], bool):
            raise TypeError("**kwarg 'flipud' must be bool")
    flipud = True if not "flipud" in kwargs else kwargs["flipud"]

    # If x/y are integer, check if they are 'continuous'. If so,
    # we handle them as integers. Else we use 'cut'.
    def column_to_category(x):
        # Integer sequence?
        if np.issubdtype(x, int):
            tmp = np.asarray([y for y in range(min(x), max(x) + 1)])
            if np.all(tmp == np.intersect1d(tmp, x)):
                return x.astype("category"), None

        if np.issubdtype(x, float):
            bins = Sturges(x)
            x = pd.cut(x, bins = bins)
        return x, bins

    # Convert original data to categorical
    x_cat, x_bins = column_to_category(df[x])
    y_cat, y_bins = column_to_category(df[y])

    # Create new data.frame with only categorical data
    df = pd.DataFrame(dict(x = x_cat, y = y_cat))

    # ---------------------------------------------------------------
    # Setting up the plot
    # ---------------------------------------------------------------

    # Calculate absolute counts (cross-table)
    tab = pd.crosstab(df.x, df.y)
    tab.index   = tab.index.astype("str")
    tab.columns = tab.columns.astype("str")

    # Drawing color lookup dictionary
    n_cols   = len(df.y.values.categories)
    hex_cols = [mcolors.to_hex(x) for x in plt.cm.gray(np.linspace(0.9, .3, n_cols))]
    cols = dict()
    for i,k in enumerate(df.y.values.categories):
        cols[str(k)] = hex_cols[i]
    del hex_cols, n_cols

    # Color coding
    # Scopes 'cols'
    def colors(key):
        return {"color": cols[key[1]]}
        #return {"color": cols[int(key[1]) - 1]}

    # Scoping 'tab' and 'labels'
    def labelizer(x):
        if not labels: return None
        x = tab.loc[x[0], x[1]]
        n = df.shape[0]
        match labels:
            case "percent":     return(np.round(x / n * 100, 3))
            case "relative":    return(x / n)
            case _:             return(x)

    mosaic(tab.iloc[:,::-1 if flipud else 1].stack(), ax = ax,
           properties = colors, gap = (0.02, 0),
           statistic = False, labelizer = labelizer)

    # I updating axis
    if x_bins is not None:
        ax.set_xticks([0.25, 0.75])
        ax.set_xticklabels(['Left', 'Right'])
    if y_bins is not None:
        at = np.cumsum((tab.iloc[0, :] / sum(tab.iloc[0, :])).values)
        at = np.concatenate([np.asarray([0]), at])
        print(y_bins)
        print(at)
        ax.set_yticks(at)
        ax.set_yticklabels([f"{x:.2f}" for x in y_bins])

    # If 'fig = None' the user provided their own axis ('ax = ...'),
    # in this case we just return the axis. Else we show the plot.
    if fig is None:
        return ax
    else:
        return df, tab


def Sturges(x):
    """Calculates Sturges breaks on a numeric variable

    Args:
        x (pandas.core.series.Series): The data, must be
            a subtype of int or float (numeric).
    """

    if not isinstance(x, pd.core.series.Series):
        raise TypeError("argument 'x' must be a pandas.core.series.Series")
    elif not np.issubdtype(x, "int") and not np.issubdtype(x, "float"):
        raise TypeError("data on 'x' must be numeric (integers or floats)")

    n = int(np.ceil(np.log2(len(x)) + 1))
    return np.linspace(start = np.min(x), stop = np.max(x), num = n)







