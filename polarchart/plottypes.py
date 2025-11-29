

import re
from .radar import radar
from functools import wraps

def copy_doc(from_func):
    """
    Decorator that copies the docstring from `source`.
    """
    def decorator(func):
        func.__doc__ = from_func.__doc__
        return func
    return decorator

def copy_doc_without_examples(source):
    """
    Decorator that copies the docstring from `source` but removes any
    section starting with 'Examples' (case insensitive).
    """
    def decorator(func):
        doc = source.__doc__ or ""
        # Remove "Examples" section until end of docstring
        cleaned = re.sub(
            r"(?is)\nExamples?:.*",   # match "Examples:" and everything after
            "",
            doc
        ).rstrip()

        func.__doc__ = cleaned
        return func
    return decorator


###@copy_doc_without_examples(radar)
@copy_doc(radar)
def stars(*args, **kwargs):
    return radar(*args, _type = "stars", **kwargs)

###stars.__doc__ += """
###Examples
###--------
###
###>>> 1:5
###"""

@copy_doc(radar)
def spider(*args, **kwargs):
    return radar(*args, _type = "spider", **kwargs)

