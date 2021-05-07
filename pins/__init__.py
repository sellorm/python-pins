"""
A simple package to be able to "pin" data to an RStudio Connect instance
"""


from .board_parent import Board
from .board_rstudio_connect import BoardRsconnect


try:
    from importlib import metadata
except ImportError:
    # Running on pre-3.8 Python; use importlib-metadata package
    import importlib_metadata as metadata

__version__ = metadata.version("pins")
