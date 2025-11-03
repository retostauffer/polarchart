

from .radar import radar
from functools import wraps

def copy_doc(from_func):
    def decorator(func):
        func.__doc__ = from_func.__doc__
        return func
    return decorator

@copy_doc(radar)
def stars(*args, **kwargs):
    """Create radar charts.

    Args:
        *args:
            Positional arguments, see `help(radar)` for details.
        **kwargs:
            Additional keyword arguments, see `help(radar)` for details.

    Returns:
        If `ax = None` (no custom axis provided) there is no return but
        the plot created will be shown. If a custom axis is used the
        (modified) axis is returned.

    Details:

        Allowed additional arguments via the named **kwargs:
        - "title" (str): Plot title
        - "angle" (int, float): Rotation angle in degrees.
        - "figsize" (tuple): Custom figure size, ignored if an axis ('ax') is provided.

    Examples:

        >>> from polarchart import get_demodata, stars
        >>> gsa = get_demodata("gsa")
        >>> print(gsa.head())
        >>>
        >>> ## Default options
        >>> stars(gsa, title = "Default stars chart")
        >>>
        >>> ## Customized: No circles, custom legend position, colors,
        >>> ##             and figure size.
        >>> from colorspace import diverging_hcl
        >>>
        >>> stars(gsa,
        >>>       title   = "Customized stars chart",
        >>>       circles = False,
        >>>       legend_position = (1.5, 2),
        >>>       color   = diverging_hcl("Green-Orange")(gsa.shape[1]),
        >>>       figsize = (12, 8))
    """

    return radar(*args, _type = "stars", **kwargs)
