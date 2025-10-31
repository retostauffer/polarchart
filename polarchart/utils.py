

import numpy as np


def scale_df(df):
    """scale_df(df)

    Params
    ======
    df : pandas.DataFrame
        An all numeric (!) pandas DataFarame.
    
    Return
    ======
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


def pretty_ticks(xmax, n_ticks=4):
    """Calculate Pretty Ticks

    Args:
        xmax : num
            Positive numeric value.
        n_ticks : int
            Approximate number of ticks to be calculated.

    Returns:
        list : List of numeric values with pretty ticks
        with equal distance between (but excluding) zero
        to about `xmax` (but not above).

    """
    if xmax <= 0: return [0.0]

    # Rough step size
    raw_step = xmax / n_ticks
    exp      = np.floor(np.log10(raw_step))
    base     = 10 ** exp

    # Pick "nice" step SMALLER than raw_step if needed
    nice_multipliers = [1, 2, 2.5, 5, 10]
    for m in nice_multipliers:
        step = m * base
        if step >= raw_step:
            break

    # If too few ticks, go one step smaller
    if (xmax / step) < (n_ticks - 1):
        # find smaller step in the list
        idx = nice_multipliers.index(m)
        if idx > 0:
            step = nice_multipliers[idx - 1] * base / (10 if m == 1 else 1)

    # Build ticks from 0 up to nearest multiple of step <= xmax
    ticks = []
    val   = step
    while val <= xmax + 1e-10:
        ticks.append(val)
        val += step

    # Rounding to match base precision
    decimals = max(0, -int(np.floor(np.log10(step))) )
    ticks    = [float(np.round(t, decimals)) for t in ticks]

    return ticks


