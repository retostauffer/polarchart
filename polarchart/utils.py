

import numpy as np


def scale_df(df):
    """scale_df(df)

    Args:
        df : pandas.DataFrame
            An all numeric (!) pandas DataFarame.

    Returns:
        pandas.DataFrame : Returns an object of the same dimension as the
        input argument 'df' scaled rowwise. I.e., the highest value per row
        is scaled to '1.0', the lowest to '0.0'.
    """

    def fn(x):
        mn = np.min(x)
        mx = np.max(x)
        return (x - mn) / (mx - mn)

    for j in range(df.shape[1]):
        df.iloc[:, j] = fn(df.iloc[:, j])

    return df


def pretty_ticks(n, min_, max_):
    """Calculate Pretty Ticks

    Args:
        n (int): Approximate number of ticks.
        min_ (float, int): Lowest value.
        max_ (float, int): Highest value.

    Returns:
        list : List of numeric values with pretty ticks
        with equal distance between (but excluding) zero
        to about `xmax` (but not above).

    """
    from matplotlib.ticker import MaxNLocator
    return MaxNLocator(nbins = n).tick_values(min_, max_)


def prepare_num_df(x, labels = True, numeric_only = False):
    """Prepare DataFrame for Plotting

    Polar charts work only with numeric data. The users have a series
    of options to chose, this function prepares data DataFrame for
    drawing the result.

    Args:
        x (pandas.core.frame.DataFrame): Data set.
        labels (bool, str): If string, the index (row names) the index
            of `x` is replaced by the corresponding column of `x` (if found).
            Else this argument is untouched but returned.
        numeric_only (bool): If `False` (default) the function will throw
            an exception if it finds any non-numeric columns/variables after
            updating the index (see argument `labels`). If `True`
            all non-numeric columns will be thrown away. If nothing is left
            afterwards, an error will be thrown.

    Returns:
        list: If no exeption is thrown, a list of length two is returned
        where the first element ('labels') is either `True` or `False`,
        and the second is a (potentially modified) version of the original
        data DataFrame `x`.
    """
    from pandas.api.types import is_numeric_dtype

    # Evaluating 'labels'. If 'labels' is string we re-write the index of
    # the data frame and delete the corresponding column from 'x'.
    if isinstance(labels, str):
        if not labels in x.columns:
            raise ValueError(f"labels = \"{labels}\" invalid, not a column of `x`")
        # Set new index (overwrites existing index and removes column from the data).
        x.set_index(labels, inplace = True)

    # Check all columns/variables: numeric?
    isnum = x.apply(is_numeric_dtype).values
    if not numeric_only and not isnum.all():
        # Very verbal exception to support our students
        if not isinstance(labels, str):
            msg_idx       = ""
            msg_set_idx   = "\n        * Specify which column to use for the labels by setting labels = \"<column name>\""
            msg_both      = "\n        * Or a combination of both options"
        else:
            msg_idx       = f"\n        after replacing the index with '{labels}'"
            msg_set_idx   = ""
            msg_both      = ""

        # List non-numeric columns
        non_num_cols = ", ".join(x.columns[~isnum])

        # Gluing together the message
        msg = f"""
        Non-numeric columns/variables found in the DataFrame{msg_idx}.

        Namely: {non_num_cols}

        Consider the following options:{msg_set_idx}
        * Use `numeric_only = True` to remove all non-numeric columns{msg_both}
        """
        raise Exception(msg)
    elif numeric_only:
        # There will be nothing left after subsetting as all is non-numeric? Well ...
        if not isnum.any():
            raise Exception("No numeric columns/variables found in the DataFrame")

        # Subsetting the data.frame
        x = x.iloc[:, isnum]


    # Converting labels to True in case it was str
    labels = True if isinstance(labels, str) else labels
    return labels, x


def required_digits(x):
    from re import compile
    from numpy import asarray

    if isinstance(x, (int, float)): x = [x]
    x = asarray(x)

    # Number of digits
    pat = compile("\\.([0-9]+)$")
    def fn(k):
        k = pat.search(k)
        return 0 if not k else len(k.group(1))

    res = np.zeros(len(x))
    for i in range(len(x)):
        res[i] = fn(format(x[i], "g"))
    return int(max(res))

