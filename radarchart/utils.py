

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
