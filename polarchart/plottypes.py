

from .radar import radar
from functools import wraps

def copy_doc(from_func):
    def decorator(func):
        func.__doc__ = from_func.__doc__
        return func
    return decorator

@copy_doc(radar)
def stars(*args, **kwargs):
    return radar(*args, _type = "stars", **kwargs)

@copy_doc(radar)
def spider(*args, **kwargs):
    return radar(*args, _type = "spider", **kwargs)

