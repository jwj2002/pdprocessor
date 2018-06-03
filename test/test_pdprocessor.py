"""
Tests for `pdprocessor` module.
"""
import os
import pytest
import datetime as dt
from mock import Mock
from pdprocessor.pdprocessor import PDProcessorError, Path, PDProcessor, ExcelPDProcessor


class TestPDProcessorError(object):

    def test_error_message(self):
        error = PDProcessorError("Error!")
        try:
            raise(error)
        except PDProcessorError as e:
            pass
        assert e.message == "Error!"


class TestPath(object):

    def test__init__(self):
        sfile = os.path.join(os.path.dirname(__file__), __file__)
        path = Path(sfile)
        assert path.path == sfile


class TestPDProcessor(object):

    def test__init__(self):
        sfile = os.path.join(os.path.dirname(__file__), __file__)
        processor = PDProcessor(sfile)
        assert processor.path == sfile
        assert processor.data_map == None
        assert processor.date_format == '%m/%d/%Y'

    def test_validate_path_with_valid_file(self):
        sfile = os.path.join(os.path.dirname(__file__), __file__)
        processor = PDProcessor(sfile)
        processor.validate_path()

    def test_validate_path_with_invalid_path(self):
        sfile = 'invalid_path'
        processor = PDProcessor(sfile)
        try:
            processor.validate_path()
        except PDProcessorError as e:
            pass
        assert isinstance(e, PDProcessorError)
        assert e.message == "No file found at 'invalid_path'."

    def test_init_data_map(self, data_map):
        sfile = 'test'
        processor = PDProcessor(sfile)
        processor.data_map = data_map
        processor.init_data_map()
        expected = [
            ('string', 'String', processor.format_uppercase),
            ('float', 'Float', processor._format_none),
            ('integer', 'Integer', processor._format_none),
            ('date', 'Date', processor.format_date),
        ]
        assert processor.data_map == expected
        expected = list(set(['String', 'Float', 'Integer', 'Date']))
        assert processor.source_cols == expected
        assert processor.final_cols == ['string', 'float', 'integer', 'date']

    def test_init_data_map_with_data_map_none(self):
        """Ensure error occurs when data_map is None."""

        processor = PDProcessor('path')
        try:
            processor.init_data_map()
        except PDProcessorError as e:
            pass
        assert isinstance(e, PDProcessorError)
        assert e.message == "data_map is None."

    def test_init_data_map_with_no_formatter(self):
        """Esnure error occurs when formatter is not defined."""

        processor = PDProcessor('path')
        processor.data_map = [
            ('final', 'initial', 'format_uppercase'),
            ('final', 'intial', 'no_formatter'),
        ]
        try:
            processor.init_data_map()
        except PDProcessorError as e:
            pass
        assert isinstance(e, PDProcessorError)
        assert e.message == "Formatter 'no_formatter' is not defined."

    def test_test_dataframe(self, dataframe):
        """Test the test dataframe."""

        columns = ['String', 'Float', 'Integer', 'Date']
        assert dataframe.columns.tolist() == columns
        expected = ['string', 'string']
        assert dataframe['String'].tolist() == expected
        expected = [1.47, 0.0]
        assert dataframe['Float'].tolist() == expected
        expected = ['5/6/1970', '11/18/2017']
        assert dataframe['Date'].tolist() == expected

    def test_validate_dataframe_correct(self, dataframe, data_map):
        processor = PDProcessor('path')
        processor.source_cols = ['String', 'Float', 'Integer', 'Date']
        processor.df = dataframe
        processor.validate_dataframe()

    def test_validate_dateframe_corret2(self, dataframe):
        """Test validate dataframe when dataframe contains more that source_cols."""

        processor = PDProcessor('path')
        processor.source_cols = ['String', 'Float', 'Integer']
        processor.df = dataframe
        processor.validate_dataframe()

    def test_validate_dataframe_incorrect(self, dataframe):
        """Test validate_dataframe with incorrect col in source_cols"""

        processor = PDProcessor('path')
        processor.source_cols = ['String', 'Float', 'Integer', 'Byte']
        processor.df = dataframe
        try:
            processor.validate_dataframe()
        except PDProcessorError as e:
            pass
        expected = "Expected column 'Byte' is not in the source file."
        assert e.message == expected

    def test_format_uppercase(self):
        """Test format none."""

        processor = PDProcessor('path')
        data = processor.format_uppercase('string')
        assert data == 'STRING'

    def test_format_none(self):
        """Test format none."""

        processor = PDProcessor('path')
        data = processor._format_none('string')
        assert data == 'string'

    def test_format_date_with_string(self):
        """Test format_date with string."""

        processor = PDProcessor('path')
        data = processor.format_date('05/06/1970')
        assert data == dt.datetime(1970, 05, 06).date()

    def test_format_date_with_date(self):
        """Test format date with date."""

        processor = PDProcessor('path')
        sdate = dt.datetime(1970, 05, 06).date()
        data = processor.format_date(sdate)
        assert data == dt.datetime(1970, 05, 06).date()

    def test_format_date_with_datetime(self):
        """Test format date with datetime."""

        processor = PDProcessor('path')
        sdate = dt.datetime(1970, 05, 06, 0, 0)
        data = processor.format_date(sdate)
        expected = sdate.date()
        assert data == expected

    def test_format_dataframe(self, dataframe, data_map):
        """Test format_dataframe."""

        processor = PDProcessor('path')
        processor.data_map = data_map
        processor.init_data_map()
        processor.df = dataframe
        processor.format_dataframe()
        expected = set(['string', 'date', 'float', 'integer'])
        actual = set(processor.df.columns.tolist())
        assert actual == expected
        expected = ['STRING', 'STRING']
        assert processor.df['string'].tolist() == expected
        expected = [dt.datetime(1970, 05, 06).date(), dt.datetime(2017, 11, 18).date()]
        assert processor.df['date'].tolist() == expected

    def test_process(self, dataframe, data_map):
        """Test process."""

        sfile = os.path.join(os.path.dirname(__file__), __file__)
        processor = PDProcessor(sfile)
        processor.data_map = data_map
        processor.df = dataframe
        processor.process()
        expected = set(['string', 'date', 'float', 'integer'])
        actual = set(processor.df.columns.tolist())
        assert actual == expected
        expected = ['STRING', 'STRING']
        assert processor.df['string'].tolist() == expected
        expected = [dt.datetime(1970, 05, 06).date(), dt.datetime(2017, 11, 18).date()]
        assert processor.df['date'].tolist() == expected
        expected = [1.47, 0]
        assert processor.df['float'].tolist() == expected
        expected = [1, 2]
        assert processor.df['integer'].tolist() == expected


class TestExcelPDProcessor(object):

    def test_init(self):
        processor = ExcelPDProcessor('path')
        assert processor.sheet_name == 0
        assert processor.header == 0
        assert processor.skiprows == 0
        assert processor.skipfooter == 0
        assert processor.index_col == None
        assert processor.names == None
        assert processor.usecols == None
        assert processor.parse_dates == False
        assert processor.date_parser == None
        assert processor.na_values == None
        assert processor.thousands == None
        assert processor.convert_float == True
        assert processor.converters == None
        assert processor.dtype == None
        assert processor.true_values == None
        assert processor.false_values == None
        assert processor.engine == None
        assert processor.squeeze == False
        assert processor.encoding == 'iso-8859-1'
        assert processor.data_map == None

    def test_create_dataframe(self, excelpdprocessor, excel_data_map):
        """Test create_dataframe."""

        processor = excelpdprocessor
        processor.create_dataframe()
        expected = ['OrderDate', 'Region', 'Rep', 'Item', 'Units', 'Unit Cost',
                    'Total']
        assert processor.df.columns.tolist() == expected
        assert processor.df.shape == (43, 7)

    def test_validate_dataframe(self, excelpdprocessor, excel_data_map):
        """Test validate_dataframe."""

        processor = excelpdprocessor
        processor.data_map = excel_data_map
        processor.init_data_map()
        processor.create_dataframe()
        processor.validate_dataframe()

    def test_process(self, excelpdprocessor, excel_data_map):
        """Test process."""

        processor = excelpdprocessor
        processor.data_map = excel_data_map
        processor.process()
        expected = ['Date', 'Region', 'Qty', 'Cost', 'Ext Cost']
        assert processor.df.columns.tolist() == expected
        assert processor.df.shape == (43, 5)
        expected = [
            dt.datetime(2016, 1, 6).date(),
            dt.datetime(2016, 1, 23).date(),
        ]
        assert processor.df['Date'].tolist()[:2] == expected
        expected = [95, 50]
        assert processor.df['Qty'].tolist()[:2] == expected
