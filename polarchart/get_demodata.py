

def get_demodata(name):
    """Return Demo Data

    The package is shipped with one/few (TODO(R)) demo data
    sets used for the examples as well as the documentation.

    Params:
        x : str or None
            If `None` a pandas DataFrame with all available data sets
            is returned. If string, the corresponding data set is loaded
            and returned (pandas DataFrame).

    Source:
        TODO(R)

    Return:
        pandas.DataFrame : Setting `name = None` allows to retrieve
        a list of all available data sets. If `name` is a string,
        the corresponding data set is loaded and returned.

    Examples:
    >>> ## Get a DataFrame with all available demo data sets
    >>> datasets = get_demodata(None)
    >>> print(datasets)
    >>>
    >>> ## Load specific demo data set
    >>> gsa = get_demodata("gsa")
    >>> print(gsa)
    """
    from importlib.resources import files
    from pandas import read_csv, DataFrame
    from numpy import isnan

    # Staying sane
    if not isinstance(name, (type(None), str)):
        raise TypeError("argument 'name' must be str or None")

    # Loading available data sets
    csv = files("polarchart.data").joinpath("available_demodata.csv")
    datasets = read_csv(csv, index_col = 0,
                        na_values = "None",  skipinitialspace = True)
    datasets = datasets.rename_axis(None, axis = 0)

    # Return list of all available data sets
    if name is None:
        return datasets[["description"]]

    # Else trying to find the corresponding data set
    if not name in datasets.index:
        tmp = ", ".join([f"\"{x}\"" for x in datasets.index])
        raise ValueError(f"dataset 'name' must be one of {tmp} (see 'get_demodata(None)')")

    index_col = datasets.index_col[name]
    index_col = None if bool(isnan(index_col)) else int(index_col)

    # Read and return data set
    csv = files("polarchart.data").joinpath(datasets.file[name])
    try:
        res = read_csv(csv, index_col = index_col)
    except Exception as e:
        raise Exception("problems loading data set (\"{csv}\"): {e}")
    finally:
        return res


