"""
Tests for `pdprocessor` module.
"""
import os
import pytest
from pdprocessor.pdprocessor import PDProcessorError, Path, PDProcessor


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



