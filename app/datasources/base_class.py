"""
Abstract base class for datasource classes.

An abstract base class for child classes to inherit from and extend the
functions as needed.
"""


class DatasourceBaseClass:
    """
    Abstract base class to act as an interface.

    It is meant to define methods that must be present in data sources.
    """

    def new_data_available(self) -> bool:
        """Return true if there are more rows abailable, false if not."""
        pass

    def get_next_row(self) -> dict:
        """
        Return the next data row if one exists.

        Throws an exception if not.
        """
        pass
