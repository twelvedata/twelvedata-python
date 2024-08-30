# -*- coding: utf-8 -*-
import importlib.metadata
from .client import TDClient

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = __name__
    __version__ = importlib.metadata.version(dist_name)
except ImportError as e:
    __version__ = "unknown"
