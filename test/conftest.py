# -*- coding: utf-8 -*-
"""Defines fixtures available to all tests."""

import pytest
import pandas as pd


@pytest.fixture
def data_map():
    """A data_map for testing PDProcessor."""

    return [
        ('string', 'String', 'format_uppercase'),
        ('float', 'Float', None),
        ('integer', 'Integer', None),
        ('date', 'Date', 'format_date')
    ]

@pytest.fixture
def dataframe():
    data = [
        ('string', 1.47, 1, '5/6/1970'),
        ('string', 0, 2, '11/18/2017')
    ]
    df = pd.DataFrame(data)
    df.columns = ['String', 'Float', 'Integer', 'Date']
    return df

@pytest.fixture
def excel_data_map():
    data_map = [
        ('Date', 'OrderDate', format_date),
        ('Region', 'Region', None),
        ('Qty', 'Units', None),
        ('Cost', 'Unit cost', None),
        ('Ext Cost', 'Total', None)]
    return data_map

