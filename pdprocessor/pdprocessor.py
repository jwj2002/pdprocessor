import os
import datetime as dt

class PDProcessorError(Exception):
    """A PDProcessor Error."""

    def __init__(self, message):
        self.message = message

class Path(object):
    """A path class."""

    def __init__(self, path_to_file):
        self.path = path_to_file


class PDProcessor(Path):
    """Base class for a pandas dataframe processor.

    A PDProcessor creates a dataframe from a delimited file such as csv or
    excel. The dataframe is manipulated by adding or formatting columns.
    """

    data_map = None
    date_format = '%m/%d/%Y'

    def process(self):
        """Process the file."""

        self.validate_path()
        self.create_dataframe()
        self.init_data_map()

    def validate_path(self):
        """Validate the path point to a file."""

        if not os.path.isfile(self.path):
            message = "No file found at '{path}'.".format(path=self.path)
            raise PDProcessorError(message)

    def set_date_format(self, format):
        """Set the date format."""

        self.date_format = format

    def create_dataframe(self):
        """Create a dataframe from the source file at self.path."""

        pass

    def init_data_map(self):
        """Intialize the data_map.

        Set source_cols - the expected column names from the source file.
        Set final_cols the final column names.
        """

        if not self.data_map:
            message = 'data_map is None.'
            raise PDProcessorError(message)
        self.source_cols = list(set(
            [source_col for (final_col, source_col, formatter) in self.data_map]))
        self.final_cols = [final_col for (final_col, source_col, formatter) in
                           self.data_map]
        data_map = []
        for final_col, source_col, formatter in self.data_map:
            if not formatter:
                formatter = '_format_none'
            try:
                data_map.append((final_col, source_col, getattr(self, formatter)))
            except AttributeError:
                message = "Formatter '{formatter}' is not defined.".format(formatter = formatter)
                raise PDProcessorError(message)
        self.data_map = data_map

    def _format_none(self, data):
        """Dummy formatter when formatter in self.data_map is None."""

        return data

    def validate_dataframe(self):
        """Validate the dataframe by verifying source_col names against self.data_map."""

        if list(set(self.df.columns.tolist())) == self.source_cols:
            return
        message = 'The source file header does not match the expected header.'
        raise PDProcessorError(message)

    def format_dataframe(self):
        for final_col, source_col, formatter in self.data_map:
            if formatter != self._format_none:
                self.df[final_col] = self.df[source_col].apply(formatter)

    def format_uppercase(self, data):
        return data.upper()

    def format_date(self, data):
        """Format date."""

        if isinstance(data, dt.date) and not isinstance(data, dt.datetime):
            return data
        if isinstance(data, dt.datetime):
            return data.date()
        date = dt.datetime.strptime(data, self.date_format).date()
        return date


