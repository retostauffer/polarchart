
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from statsmodels.graphics.mosaicplot import mosaic
from matplotlib import colors as mcolors

def spineplot(df, x, y, labels = None, ax = None, colors = None, *args, **kwargs):
    """Create spine plot

    Args:
        df (pandas.core.frame.DataFrame): A pandas DataFrame.
        x (str): Name of the variable for the first dimension.
        y (str): Name of the variable for the second dimension. Must be
            categorical or easily convertable to categorical (i.e.,
            strings or integers with less than 10 unique values).
        labels (None, str): Either `None` (default) to suppress labels,
            or one of `"absolute"`, `"relative"`, `"percent"`.
        ax (None or matplotlib.axes._axes.Axes): If None, a new figure is
            initialized. Else the existing axis is taken, manipulated, and populated.
        colors (None or list): If `None` (default) a series of grayscale colors
            is used. Can be a list of colors which must match the number of
            categories in y.
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

        Allowed additional arguments via the named **kwargs:
        - "title" (str): Plot title
        - "figsize" (tuple): Custom figure size, ignored if an axis ('ax') is provided.
        - "flipud" (bool): Flip y axis upside down (default is False).

    Examples:

        >>> from numpy import repeat
        >>> from pandas import DataFrame, Series
        >>> from polarchart import spineplot
        >>> import matplotlib.pyplot as plt

        Treatment and improvement of patients with rheumatoid arthritis
        >>> treatment = Series(repeat([1, 2], [43, 41])).map({1: "placebo", 2: "treated"}) 
        >>> improved  = Series(repeat([1, 2, 3, 1, 2, 3], [29, 7, 7, 13, 7, 21])).map({1: "none", 2: "some", 3: "marked"})
        >>>
        >>> df = DataFrame({"treatment": treatment, "improved": improved})
        >>>
        >>> ## Convert to categorial data and manually re-order the levels
        >>> df.improved = df.improved.astype("category")
        >>> df.improved = df.improved.cat.reorder_categories(["marked", "some", "none"])
        >>>
        >>> spineplot(df, x = "treatment", y = "improved",
        >>>           title = "Rheumatoid arthritis treatment")

        NASA space shuttle o-ring failures
        >>> fail = Series([2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 2, 1,
        >>>                2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1])
        >>> fail = fail.map({1: "no", 2: "yes"})
        >>> temperature = [53, 57, 58, 63, 66, 67, 67, 67, 68, 69, 70, 70,
        >>>                70, 70, 72, 73, 75, 75, 76, 76, 78, 79, 81]
        >>> df   = DataFrame({"fail": Series(fail).astype("category"),
        >>>                   "temperature": temperature})
        >>> df.fail = df.fail.cat.reorder_categories(["yes", "no"])
        >>>
        >>> spineplot(df, "temperature", "fail", figsize = (7, 3))
        >>>
        >>> ## Custom figure/axis and customized spine plot
        >>> fig, ax = plt.subplots(figsize = (7, 3))
        >>> spineplot(df, x = "temperature", y = "fail", ax = ax,
        >>>           title = "NASA space shuttle o-ring failures",
        >>>           colors = ["#21CCAD", "#F99BAE"])
        >>> plt.show()


    """

    from pandas import DataFrame, Index, cut
    import numpy as np
    from matplotlib import axes

    from .utils import required_digits

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
    if not isinstance(colors, (type(colors), list)):
        raise TypeError("argument 'colors' must be None or list")

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
    flipud = False if not "flipud" in kwargs else kwargs["flipud"]

    # Convert original data to categorical
    x_cat, x_bins = column_to_category(df[x])
    y_cat, y_bins = column_to_category(df[y], nmax = 10)

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
    cols = get_spineplot_colors(df.y, colors, flipud)

    # Returns properties for facets; scopes 'cols'
    def colors(key):
        return {"facecolor": cols[key[1]],
                "edgecolor": "black",
                "linewidth": 0.5}
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

    # Gap 0.02 to ~0.01
    gap = 0 if x_bins is not None else 0.01 + 0.01 / df.x.nunique()

    # Create main plot
    mosaic(tab.iloc[:,::-1 if flipud else 1].stack(), ax = ax,
           properties = colors, gap = (gap, 0),
           statistic = False, labelizer = labelizer)

    # I updating axis
    if x_bins is not None:
        digits = required_digits(x_bins)
        at = np.concatenate([np.asarray([0]), tab.apply("sum", 1).cumsum().to_numpy()])
        at = at / np.max(at)
        ax.set_xticks(at)
        ax.set_xticklabels([f"{x:.{digits}f}" for x in x_bins])

    if y_bins is not None:
        digits = required_digits(y_bins)
        at = np.concatenate([np.asarray([0]), tab.apply("sum", 0).cumsum().to_numpy()])
        at = at / np.max(at)
        ax.set_yticks(at)
        ax.set_yticklabels([f"{x:.{digits}f}" for x in y_bins])

    # Adding title if requested
    if "title" in kwargs: ax.set_title(kwargs["title"])


    # If 'fig = None' the user provided their own axis ('ax = ...'),
    # in this case we just return the axis. Else we show the plot.
    if fig is None:
        return ax
    else:
        plt.show()
        return df, tab


# -------------------------------------------------------------------
# -------------------------------------------------------------------
def Sturges(x):
    """Calculates Sturges breaks on a numeric variable

    Args:
        x (pandas.core.series.Series): The data, must be
            a subtype of int or float (numeric).
    """
    from .utils import pretty_ticks

    if not isinstance(x, pd.core.series.Series):
        raise TypeError("argument 'x' must be a pandas.core.series.Series")
    elif not np.issubdtype(x, "int") and not np.issubdtype(x, "float"):
        raise TypeError("data on 'x' must be numeric (integers or floats)")

    n = int(np.ceil(np.log2(len(x)) + 1))
    return pretty_ticks(n, np.min(x), np.max(x))


# -------------------------------------------------------------------
# -------------------------------------------------------------------
# If x/y are integer, check if they are 'continuous'. If so,
# we handle them as integers. Else we use 'cut'.
def column_to_category(x, nmax = None):
    """
    Converting pandas series to categorical.

    Args:
        x (pandas.core.series.Series): Can be of any type, this function tries to convert
            it to categorical used to calculate the crosstable, the main
            object the spine plot is based on.
        nmax (None, int): An integer can be specified to force numeric series with
            many unique values not to be handled as categorical (typically if you
            have integers 1, 2, 3, 4) but to be handled as 'continuous' cut
            into intervals (as is done by default for floats).

    Return:
        pandas.core.series.Series: Returns categorical series.
    """

    from pandas import Series
    if not isinstance(x, Series):
        raise TypeError("argument 'x' must be pandas.core.series.Series")
    if not isinstance(nmax, (type(None), int)):
        raise TypeError("argument 'nmax' must be None or int")
    if isinstance(nmax, int) and nmax < 1:
        raise ValueError("argument 'nmax' (int) cannot be <= 0")

    assert isinstance(nmax, (type(None), int)), "nmax must be None or int"

    # If already categorical, return. If object, convert to category and return.
    if x.dtype.name == "category": return x, None
    if x.dtype.name == "object":   return x.astype("category"), None

    # Integer sequence?
    if np.issubdtype(x, int):
        tmp = np.asarray([y for y in range(min(x), max(x) + 1)])
        ## If all values 'tmp' are in x and the number of unique
        ## integers is < 20 we assume it is 'categorical'.
        if x.nunique() < 20 and np.all(np.isin(tmp, x)):
            return x.astype("category"), None

    # Convert numeric variable (used for x-axis) to categories
    # using pandas.cut() if 'x' is numeric and nmax is None.
    if np.issubdtype(x, (int, float)) and nmax is None:
        bins = Sturges(x)
        x = pd.cut(x, bins = bins)
    # Else we try to take all unique values of the vector
    # as categories, but will throw an error if there are
    # more than 'nmax'.
    else:
        nx = x.nunique()
        if nx > nmax:
            raise ValueError(f"problem converting to categorical variable, more unique values than allowed ({nx} > {nmax}).")
        x = x.astype("category")
        bins = None

    return x, bins

# -------------------------------------------------------------------
# -------------------------------------------------------------------
def get_spineplot_colors(y, colors, flipud):
    """
    Get color vector for spine plot. If `colors` is `None` we pick
    a series of grayscale colors. Else `colors` is a list, we check if
    this has correct length (TODO: Check if valid colors?)

    Args:
        y (pandas.Series): Our categorical variable
        colors (None, list): Colors to be used.
        flipud (bool): Wether or not the colors should be inverted.

    Return:
        list: List of length `n` with the colors used for the facets.
    """
    n = y.nunique()

    if colors is None:
        colors = [mcolors.to_hex(x) for x in plt.cm.gray(np.linspace(0.95, .3, n))]
    else:
        if not len(colors) == n:
            raise ValueError(f"length of 'colors' does not match number of required colors (n = {n}")

    # Prepare dictionary for coloring the facets
    cols = dict()
    if not flipud:
        for i,k in enumerate(reversed(y.values.categories)): cols[str(k)] = colors[i]
    else:
        for i,k in enumerate(y.values.categories): cols[str(k)] = colors[i]

    return cols






