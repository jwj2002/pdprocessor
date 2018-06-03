import os
import pandas as pd
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
        self.init_data_map()
        self.create_dataframe()
        self.validate_dataframe()
        self.preprocess()
        self.format_dataframe()
        self.postprocess()


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

    def validate_dataframe(self):
        """Validate the dataframe by verifying source_col are in df.columns."""

        source_cols = set(self.source_cols)
        actual_cols = set(self.df.columns.tolist())
        if source_cols <= actual_cols:
            return
        for col in source_cols:
            if col not in actual_cols:
                message = "Expected column '{col}' is not in the source file.".format(col=col)
                raise PDProcessorError(message)

    def preprocess(self):
        """Provide preprocess steps."""
        pass

    def format_dataframe(self):
        for final_col, source_col, formatter in self.data_map:
            self.df[final_col] = self.df[source_col].apply(formatter)
        self.df = self.df[self.final_cols]

    def postprocess(self):
        """Provide post process steps."""
        pass

    def set_final_cols(self):
        self.df = self.df[self.final_cols]


    def _format_none(self, data):
        """Dummy formatter when formatter in self.data_map is None."""

        return data

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

class ExcelPDProcessor(PDProcessor):
    """An Excel PDProcessor

    sheet_name: integer or string used to determine sheet index or name (default=0)
    encoding: sets the encoding of the file (default='iso-8859-1')
    skiprows: number of rows to skip (zero based) (default=0)
    usecols:
      if None then parse all columns
      if integer then indicates last column to be parsed
      if list of ints then indicates list of column numbers to be parsed
      If string then indicates comma separated list of Excel column letters and
      column ranges (e.g. "A:E" or "A,C,E:F"). Ranges are inclusive of both sides.
    """

    sheet_name = 0
    header = 0
    skiprows = 0
    skipfooter = 0
    index_col = None
    names = None
    usecols = None
    parse_dates = False
    date_parser = None
    na_values = None
    thousands = None
    convert_float = True
    converters = None
    dtype = None
    true_values = None
    false_values = None
    engine = None
    squeeze = False
    encoding = 'iso-8859-1'

    data_map = None

    def create_dataframe(self):
        """Create the dataframe."""
        df = pd.read_excel(self.path, sheet_name=self.sheet_name,
                           header=self.header, skiprows=self.skiprows, 
                           skipfooter=self.skipfooter, index_col=self.index_col,
                           names=self.names, usecols=self.usecols,
                           parse_dates=self.parse_dates, date_parser=self.date_parser,
                           na_values=self.na_values, thousands=self.thousands,
                           convert_float=self.convert_float, converters=self.converters,
                           dtype=self.dtype, true_values=self.true_values,
                           false_values=self.false_values, engine=self.engine,
                           squeeze=self.squeeze, encoding=self.encoding)
        self.df = df


