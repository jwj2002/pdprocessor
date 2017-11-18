"""
Tests for `pdprocessor` module.
"""
import pytest
from pdprocessor.pdprocessor import PDProcessorError


class TestPDProcessorError(object):

    error = PDProcessorError("Error!")
    try:
        raise(error)
    except PDProcessorError as e:
        pass
    assert e.message == "Error!"
        



class TestPdprocessor(object):

    @classmethod
    def setup_class(cls):
        pass

    def test_something(self):
        pass

    @classmethod
    def teardown_class(cls):
        pass
