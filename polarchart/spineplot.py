
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def spineplot(df, x, y, *args, **kwargs):
    """Create spine plot

    Args:
        df (pandas.core.frame.DataFrame): A pandas DataFrame.
        x (str): Name of the variable for the first dimension.
        y (str): Name of the variable for the second dimension.
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

        TODO
        Allowed additional arguments via the named **kwargs:
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

    if not x in df.columns:
        raise ValueError(f"variable {x=} not found in 'df'")
    if not y in df.columns:
        raise ValueError(f"variable {y=} not found in 'df'")


    df = df[[x, y]]
    df.columns = Index(["x", "y"])

    # If x/y are integer, check if they are 'continuous'. If so,
    # we handle them as integers. Else we use 'cut'.
    def int_to_category(x):
        print(x)
        print(np.min(x))
        print(np.max(x))
        if np.issubdtype(type(x), int):
            tmp = np.asarray([y for y in range(min(x), max(x) - 1)])
            print(tmp)
            if np.all(tmp == np.intersect1d(tmp, x)):
                x = x.astype("category")
        return x

    df.loc[:, "x"] = int_to_category(df.x.values)
    df.loc[:, "y"] = int_to_category(df.y.values)


    return df


