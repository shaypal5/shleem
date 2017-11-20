"""Core functions for the shleem package."""

import abc


DEFAULT_SOURCE_TYPE = 'unspecified'

class DataSource(object):
    """A base class for shleem data sources.

    Arguments
    ---------
    identifier : str
        An string identifier unique to this data source.
    source_type : str, optional
        A string identifying the type of this data source. If none is given, a
        default value is used.
    """

    def __init__(self, identifier, source_type=None):
        self.identifier = identifier
        if source_type is None:
            source_type = DEFAULT_SOURCE_TYPE
        self.source_type = source_type

    def __repr__(self):
        return "DataSource: {}".format(self.identifier)


class DataTap(DataSource, metaclass=abc.ABCMeta):
    """An abstract base class for tappable shleem data sources.

    Arguments
    ---------
    identifier : str
        An string identifier unique to this data source.
    source_type : str, optional
        A string identifying the type of this data source. If none is given, a
        default value is used.
    """

    @abc.abstractmethod
    def tap(self):
        """Taps this DataTap to produce a raw dataset."""
        pass #pragma: no cover

    @abc.abstractmethod
    def dump(self, file_path, file_format=None):
        """Dumps the raw dataset produced by this tap to a file.

        Arguments
        ---------
        file_path : str
            The full path of the file into which the raw dataset is dumped.
        file_format : str, optional
            A string identifier for the file format the data is serialzed into,
            e.g. 'csv'. Supported formats are dependent on the type of DataTap.
            If not given, a default format, dependent on DataTap type, is used.
        """
        pass

    def __repr__(self):
        return "DataTap: {}".format(self.identifier)
