

import numpy as np
import pandas as pd
from pandas import DataFrame, Series


class coin_object:
    _ranktests = ["independence_test"]

    def __init__(self, df, x, y, name = "independence_test"):
        # Staying sane
        if not isinstance(df, DataFrame):
            raise TypeError("argument 'df' must be a pandas.DataFrame")
        if not isinstance(x, str):
            raise TypeError("argument 'x' must be str")
        if not isinstance(y, str):
            raise TypeError("argument 'y' must be str")
        if not isinstance(name, str):
            raise TypeError("argument 'name' must be str")

        # Checking values
        if not x in df.columns:
            raise ValueError(f"variable/column {x=} not found in `df`")
        if not y in df.columns:
            raise ValueError(f"variable/column {y=} not found in `df`")
        if not name in self._ranktests:
            raise ValueError(f"argument 'name' must be one of {_ranktests_}")

        self.name    = name
        self.x       = df[x]
        self.y       = df[y]
        self.weights = np.ones(len(x))
        self.block   = np.zeros(len(x))

        # ---------------------------------------------------------------
        if self.get("weights") is not None and not self.is_unity():
            from warnings import warn
            warn("rank transformation doesn't take weights into account")

        # Loading test and execute
        FUN = globals()[name]
        FUN(self)

    # ---------------------------------------------------------------
    # ---------------------------------------------------------------
    def __repr__(self):
        # TODO(R): Develop standard repr
        return "Coin object"

    # ---------------------------------------------------------------
    # ---------------------------------------------------------------
    def get(self, what):
        if not hasattr(self, what):
            raise Exception(f"coin_object has no element \"{what}\"")
        return getattr(self, what)


    # ---------------------------------------------------------------
    # ---------------------------------------------------------------
    def setscores(self, scores):
        # If scores is None, return x untouched
        if scores is not None:
            # Validate scores: must be a dict with names
            if not isinstance(scores, dict) or not scores:
                raise ValueError("'scores' must be a named dict")

            varnames = list(scores.keys())

            # Check variables exist in x.x or x.y
            all_vars = set(x.x.columns).union(x.y.columns)
            missing = [v for v in varnames if v not in all_vars]

            if missing:
                raise ValueError(f"variable(s) {missing} not found in 'x'")

            self.scores = dict()

            # Apply scores to variables in x.x and x.y
            x = self.get("x")
            y = self.get("y")
            for var in varnames:
                # ---- x.x side -------------------------------------------------------
                if var in x.columns:
                    col = x[var]
                    if not pd.api.types.is_categorical_dtype(col):
                        raise TypeError(f"{var!r} is not a factor")
                    if len(col.cat.categories) != len(scores[var]):
                        raise ValueError(f"scores for variable {var!r} don't match")

                    # Re-create ordered categorical
                    x[var] = pd.Categorical(col, categories = col.cat.categories,
                                            ordered = True)

                    # Attach scores attribute
                    self.scores[var] = scores[var]

                # ---- x.y side -------------------------------------------------------
                if var in y.columns:
                    col = y[var]
                    if not pd.api.types.is_categorical_dtype(col):
                        raise TypeError(f"{var!r} is not a factor")

                    if len(col.cat.categories) != len(scores[var]):
                        raise ValueError(f"scores for variable {var!r} don't match")

                    y[var] = pd.Categorical(col, categories = col.cat.categories,
                                            ordered = True)
                    self.scores[var] = scores[var]

            return x


    # ---------------------------------------------------------------
    # ---------------------------------------------------------------
    def is_unity(self):
        return np.all(self.get("weights") == 1)




def independence_test(obj,
                      teststat     = "maximum",
                      distribution = "asymptotic",
                      alternative  = "two.sided",
                      xtrafo = None, ytrafo = None, scores = None,
                      check = None, *args, **kwargs):

    if not isinstance(teststat, str):
        raise TypeError("argument 'teststat' must be str")
    if not isinstance(teststat, str):
        raise TypeError("argument 'teststat' must be str")
    if not isinstance(teststat, str):
        raise TypeError("argument 'teststat' must be str")

    from .utils import match_arg

    teststat     = match_arg("teststat",     teststat,     ["maximum", "quadratic", "scalar"])
    alternative  = match_arg("alternative",  alternative,  ["two.sided", "less", "greater"])
    distribution = match_arg("distribution", distribution, ["asymptotic", "approximate", "exact", "none"])

    from .coin import trafo
    if xtrafo is None:   xtrafo = trafo
    if ytrafo is None:   ytrafo = trafo
    print(xtrafo)


    # TODO(R): UNTESTED FUNCTION :)
    if not scores is None:
        import sys; sys.exit("need to call obj.setscores - untested :)")
        obj.setscores(scores)

    # there is id_trafo, f_trafo, ....
    print(xtrafo(obj.get("x")))

    print("foooooooooooooooooooooo independence test")

    ## compute linear statistic, conditional expectation and
    ## conditional covariance
    # R> object <- new("IndependenceLinearStatistic", object)

    ## compute test statistic and corresponding null distribution
    ## return object inheriting from class "IndependenceTest"
    # R> switch(teststat,
    # R>     "scalar" = {
    # R>         object <- new("ScalarIndependenceTestStatistic", object,
    # R>                       alternative = alternative, paired = FALSE)
    # R>         new("ScalarIndependenceTest", statistic = object,
    # R>             distribution = distribution(object), call = match.call())
    # R>     },



def trafo(data, numeric_trafo, factor_trafo, ordered_trafo, surv_trafo,
          var_trafo = None, block = None):

    # --- type checks ---------------------------------------------------------
    if not isinstance(data, (DataFrame, dict)):
        raise TypeError("'data' must be a pandas DataFrame or a dict-like object")

    df = DataFrame(data)

    # --- expensive block handling (two–pass), directly copied logic ----------
    if block is not None:
        if not isinstance(block, Series) or len(block) != len(df):
            raise ValueError("'block' must be a factor-like Series of same length")

        # first pass
        ret = trafo(df, numeric_trafo, factor_trafo, ordered_trafo,
                    surv_trafo, var_trafo = None, block = None)

        # apply transformation per block
        out = ret.copy()
        for lev in block.unique():
            idx = block == lev
            out.loc[idx, :] = trafo(df.loc[idx, :], numeric_trafo,
                                    factor_trafo, ordered_trafo, surv_trafo,
                                    var_trafo = None, block = None)

        return out

    # --- var_trafo consistency check ----------------------------------------
    if var_trafo is not None:
        if not isinstance(var_trafo, dict):
            raise TypeError("'var_trafo' must be a dict")
        missing = [k for k in var_trafo.keys() if k not in df.columns]
        if missing:
            raise ValueError(f"variables {missing} not found in data")

    # --- compute transformations --------------------------------------------
    tr = {}

    for name in df.columns:
        x = df[name]

        if var_trafo and name in var_trafo:
            arr = np.asarray(var_trafo[name](x))
        elif pd.api.types.is_categorical_dtype(x) and x.cat.ordered:
            arr = np.asarray(ordered_trafo(x))
        elif pd.api.types.is_categorical_dtype(x) or x.dtype == bool:
            arr = np.asarray(factor_trafo(x))
        elif (hasattr(x, "dtype") and str(x.dtype).startswith("survival")):
            # you likely need a custom Surv check
            arr = np.asarray(surv_trafo(x))
        elif np.issubdtype(x.dtype, np.number):
            arr = np.asarray(numeric_trafo(x))
        else:
            raise TypeError(f"Unsupported data class for variable '{name}'")

        tr[name] = arr.reshape(len(df), -1)

    # --- build output matrix (slow but faithful to original) -----------------
    ret_list = []
    assignvar = []
    colnames = []

    for i, (name, arr) in enumerate(tr.items(), start=1):
        if arr.shape[0] != len(df):
            raise ValueError(f"transformation for variable {name} has wrong length")

        ret_list.append(arr)
        assignvar.extend([i] * arr.shape[1])

        # build column names
        if arr.ndim == 2 and arr.shape[1] > 1:
            cols = [f"{name}.{j+1}" for j in range(arr.shape[1])]
        else:
            cols = [name]

        colnames.extend(cols)

    ret = np.column_stack(ret_list)

    # return as DataFrame with attributes
    out = DataFrame(ret, columns=colnames)
    out.attrs["assign"] = assignvar

    return out

