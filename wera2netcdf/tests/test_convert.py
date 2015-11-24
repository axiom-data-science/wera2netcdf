import os
import logging
import unittest
from datetime import datetime

import pytz
import netCDF4
from wera2netcdf.wera import WeraAsciiTotals

logger = logging.getLogger('wera2netcdf')
logger.addHandler(logging.StreamHandler())


class TestConvertTotals(unittest.TestCase):

    def setUp(self):
        self.resource    = os.path.join(os.path.dirname(__file__), 'resources', 'totals.txt')
        self.output_path = os.path.join(os.path.dirname(__file__), 'resources', 'totals.nc')

    def test_import_ascii(self):
        w = WeraAsciiTotals(self.resource)
        assert not w.data.empty
        assert w.origin_time == datetime(2012, 2, 9, 23, 0, tzinfo=pytz.utc)
        assert w.origin_x == -84.41666
        assert w.origin_y == 28.58333
        assert w.grid_spacing == 1500
        assert w.size_x == 130
        assert w.size_y == 210

    def test_export_netcdf(self):
        w = WeraAsciiTotals(self.resource)
        w.export(self.output_path)


class TestConvertSkio(unittest.TestCase):

    def setUp(self):
        self.resource    = os.path.join(os.path.dirname(__file__), 'resources', '20152881653_pri.cur_asc')
        self.output_path = os.path.join(os.path.dirname(__file__), 'resources', '20152881653_pri.nc')

    def test_import_ascii(self):
        w = WeraAsciiTotals(self.resource)
        assert not w.data.empty
        assert w.origin_time == datetime(2015, 10, 15, 16, 53, tzinfo=pytz.utc)
        assert w.origin_x == -81.50
        assert w.origin_y == 33.0
        assert w.grid_spacing == 3000
        assert w.size_x == 100
        assert w.size_y == 170

    def test_export_netcdf(self):
        w = WeraAsciiTotals(self.resource)
        w.export(self.output_path)
