"""MongoDB shleem data sources."""

from .mongodb import (
    server,
)

try:
    del mongodb  # pylint: disable=W0631
except NameError:
    pass
