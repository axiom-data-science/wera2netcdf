import os
import logging
import unittest
from datetime import datetime

import pytz
import netCDF4
import numpy as np
from wera2netcdf.wera import WeraAsciiTotals

logger = logging.getLogger('wera2netcdf')
logger.addHandler(logging.StreamHandler())


class TestConvertTotals(unittest.TestCase):

    def test_import_ascii(self):
        resource = os.path.join(os.path.dirname(__file__), 'resources', 'totals.txt')
        w = WeraAsciiTotals(resource)
        assert not w.data.empty
        assert w.origin_time == datetime(2012, 2, 9, 23, 0, tzinfo=pytz.utc)
        assert w.origin_x == -84.41666
        assert w.origin_y == 28.58333
        assert w.grid_spacing == 1500
        assert w.size_x == 130
        assert w.size_y == 210

    def test_export_netcdf(self):
        resource = os.path.join(os.path.dirname(__file__), 'resources', 'totals.txt')
        output_path = os.path.join(os.path.dirname(__file__), 'resources', 'totals.nc')
        w = WeraAsciiTotals(resource)
        w.export(output_path)
        with netCDF4.Dataset(output_path) as nc:
            assert np.isclose(nc.variables['u'][0, 91, 100], -0.043)
            assert np.isclose(nc.variables['v'][0, 91, 100], -0.047)
            assert np.isclose(nc.variables['uacc'][0, 91, 100], 0.036)
            assert np.isclose(nc.variables['vacc'][0, 91, 100], 0.037)
            assert np.isclose(nc.variables['u'][0, 101, 88], -0.067)
            assert np.isclose(nc.variables['v'][0, 101, 88], -0.058)
            assert np.isclose(nc.variables['uacc'][0, 101, 88], 0.035)
            assert np.isclose(nc.variables['vacc'][0, 101, 88], 0.025)

    def test_empty(self):
        resource = os.path.join(os.path.dirname(__file__), 'resources', 'empty.txt')
        output_path = os.path.join(os.path.dirname(__file__), 'resources', 'empty.nc')
        w = WeraAsciiTotals(resource)
        assert w.data.empty
        with self.assertRaises(ValueError):
            w.export(output_path)

    def test_one_reporting(self):
        resource = os.path.join(os.path.dirname(__file__), 'resources', 'onereporting.txt')
        output_path = os.path.join(os.path.dirname(__file__), 'resources', 'onereporting.nc')
        w = WeraAsciiTotals(resource)
        assert not w.data.empty
        w.export(output_path)
        with netCDF4.Dataset(output_path) as nc:
            assert np.isclose(nc.variables['u'][0, 68, 70], 0)
            assert np.isclose(nc.variables['v'][0, 68, 70], 0.)
            assert np.isclose(nc.variables['uacc'][0, 68, 70], 0.035)
            assert np.isclose(nc.variables['vacc'][0, 68, 70], 0.117)
            assert np.isclose(nc.variables['u'][0, 69, 107], 0.014)
            assert np.isclose(nc.variables['v'][0, 69, 107], -0.103)
            assert np.isclose(nc.variables['uacc'][0, 69, 107], 0.051)
            assert np.isclose(nc.variables['vacc'][0, 69, 107], 0.095)


class TestConvertSkio(unittest.TestCase):

    def setUp(self):
        self.resource    = os.path.join(os.path.dirname(__file__), 'resources', 'skio.cur_asc')
        self.output_path = os.path.join(os.path.dirname(__file__), 'resources', 'skio.nc')

    def test_import_skio_ascii(self):
        w = WeraAsciiTotals(self.resource)
        assert not w.data.empty
        assert w.origin_time == datetime(2015, 10, 15, 16, 53, tzinfo=pytz.utc)
        assert w.origin_x == -81.50
        assert w.origin_y == 33.0
        assert w.grid_spacing == 3000
        assert w.size_x == 100
        assert w.size_y == 170

    def test_export_skio_netcdf(self):
        w = WeraAsciiTotals(self.resource)
        w.export(self.output_path)
