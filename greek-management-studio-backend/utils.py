import sys
from typing import Any, Callable, ParamSpec, TypeVar

_T = TypeVar("_T")
_P = ParamSpec("_P")


def export(func: Callable[_P, _T]) -> Callable[_P, _T]:
    """Adds `func` to the list of things imported with `*` for its module.

    Note: using this function or specifying `__all__` overrides the default
    `*` import behavior; if either are used, only things provided using
    this function or `__all__` are used.

    Args:
        func: The function to export.

    Returns:
        The given function, without modification.
    """
    mod = sys.modules[func.__module__]
    if hasattr(mod, "__all__"):
        name = func.__name__
        all_ = mod.__all__
        if name not in all_:
            all_.append(name)
    else:
        mod.__all__ = [func.__name__]
    return func
