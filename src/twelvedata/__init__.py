# -*- coding: utf-8 -*-
from .client import TDClient

try:
    from ._version import version as __version__
except ImportError:
    try:
        import importlib.metadata
        __version__ = importlib.metadata.version(__name__)
    except Exception:
        __version__ = "unknown"
