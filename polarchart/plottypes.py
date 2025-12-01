

import re
from .radar import radar
from functools import wraps

def copy_doc(from_func, new_examples = None):
    """
    Decorator that copies the docstring from `source`.
    """
    if new_examples is None:
        def decorator(func):
            func.__doc__ = from_func.__doc__
            return func
    else:
        def decorator(func):
            doc = from_func.__doc__ or ""
            # Remove everything after the "Examples" section until end of docstring
            func.__doc__ = re.sub(r"(?is)(?is)\n\s+?Example(s)?:.*", "", doc)
            func.__doc__ += f"\n{new_examples}"
            return func

    return decorator

#def copy_doc_without_examples(from_func):
#    """
#    Decorator that copies the docstring from `source` but removes any
#    section starting with 'Examples' (case insensitive).
#    """
#    def decorator(func):
#        doc = from_func.__doc__ or ""
#        # Remove everything after the "Examples" section until end of docstring
#        func.__doc__ = re.sub(r"(?is)(?is)\n\s+?Example(s)?:.*", "", doc)
#        return func
#
#    return decorator


ex = """
    Examples:

        >>> from polarchart import get_demodata, stars
        >>> gsa = get_demodata("gsa")
        >>> print(gsa.head())

        Default options (first three rows, three columns)
        >>> stars(gsa.iloc[:6,:], title = "Default stars chart")

        Customized: No circles, custom legend position, colors, and figure size.
        >>> from colorspace import diverging_hcl
        >>> stars(gsa.iloc[:6,:],
        >>>       title   = "Customized stars chart",
        >>>       circles = False,
        >>>       legend_position = (1.5, 2),
        >>>       color   = diverging_hcl("Green-Orange")(gsa.shape[1]),
        >>>       figsize = (12, 8))

        Single-graph layout:
        >>> stars(gsa, title = "Single-graph layout", single_graph = True)
"""
@copy_doc(radar, ex)
def stars(*args, **kwargs):
    return radar(*args, _type = "stars", **kwargs)


ex = """
    Examples:

        >>> from polarchart import get_demodata, spider
        >>> gsa = get_demodata("gsa")
        >>> print(gsa.head())

        Default options (first three rows, three columns)
        >>> spider(gsa.iloc[:6,:], title = "Default spider chart")

        Customized: No circles, custom legend position, colors, and figure size.
        >>> from colorspace import diverging_hcl
        >>>
        >>> spider(gsa.iloc[:6,:],
        >>>        title   = "Customized spider chart",
        >>>        circles = False,
        >>>        legend_position = (1.5, 2),
        >>>        color   = diverging_hcl("Green-Orange")(gsa.shape[1]),
        >>>        figsize = (12, 8))

        Single-graph layout:
        >>> spider(gsa, title = "Single-graph layout", single_graph = True, ncol = 3)
"""
@copy_doc(radar, ex)
def spider(*args, **kwargs):
    return radar(*args, _type = "spider", **kwargs)

