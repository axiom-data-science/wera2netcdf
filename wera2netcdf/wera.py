import os
from datetime import datetime

import pytz
import netCDF4
import numpy as np
import pandas as pd
from dateutil.parser import parse
from pygc import great_distance, great_circle

import logging
logger = logging.getLogger('wera2netcdf')
logger.addHandler(logging.NullHandler())


class WeraAsciiTotals(object):

    def __init__(self, ascii_file):

        # Extract current data
        self.data = pd.read_csv(ascii_file, skiprows=[0, 1, 2, 3, 4, 5, 6, 7, 8, 10], sep=' ', skipinitialspace=True, header=0)

        # Extract origin metadata
        ogm = pd.read_csv(ascii_file, skiprows=[0, 1, 2, 3, 5], sep=' ', skipinitialspace=True, header=0, nrows=1)
        self.origin_x = ogm['LON(1,1)'][0]
        self.origin_y = ogm['LAT(1,1)'][0]
        self.grid_spacing = ogm['DGT[km]'][0] * 1000.
        self.size_x = ogm['NX'][0]
        self.size_y = ogm['NY'][0]

        # Extract time metadata
        tm = pd.read_csv(ascii_file, skiprows=[0], sep=' ', skipinitialspace=True, nrows=2, names=['date', 'time', 'timezone', 'loc', 'lat', 'lat_dir', 'lon', 'lon_dir', 'type', 'at', 'num', 'unit'])
        self.origin_time = parse('{} {} {}'.format(tm['date'][0], tm['time'][0], tm['timezone'][0]))

    def export(self, output_file):
        if os.path.isfile(output_file):
            os.remove(output_file)
        with netCDF4.Dataset(output_file, 'w', clobber=True) as nc:

            # Compute lat/lon values
            """
            Iterates over the first row or points and calculates each column
            of lon, lat values. This matches the numpy axis order.

            upper_row (basis)
            o  o  o  o  o  o
            .  .  .  .  .  .
            .  .  .  .  .  .
            .  .  .  .  .  .
            .  .  .  .  .  .
            . .  .  .  .  .

            column (first iteration)
            o  .  .  .  .  .
            o  .  .  .  .  .
            o  .  .  .  .  .
            o  .  .  .  .  .
            o  .  .  .  .  .
            o  .  .  .  .  .

            column (second iteration)
            .  o  .  .  .  .
            .  o  .  .  .  .
            .  o  .  .  .  .
            .  o  .  .  .  .
            .  o  .  .  .  .
            .  o  .  .  .  .
            """
            xs = np.ndarray(0)
            ys = np.ndarray(0)
            upper_row = great_circle(distance=[x*self.grid_spacing for x in range(self.size_x)], azimuth=90., longitude=self.origin_x, latitude=self.origin_y)
            for i, (upper_x, upper_y) in enumerate(zip(upper_row['longitude'], upper_row['latitude'])):
                column = great_circle(distance=[x*self.grid_spacing for x in range(self.size_y)], azimuth=180., longitude=upper_x, latitude=upper_y)
                xs = np.append(xs, column['longitude'])
                ys = np.append(ys, column['latitude'])
            
            lon_values = xs.reshape(self.size_x, self.size_y)
            lat_values = ys.reshape(self.size_x, self.size_y)

            fillvalue = -999.9
            nc.createDimension('time', 1)
            time = nc.createVariable('time', int, ('time',), fill_value=int(fillvalue))
            time.setncatts({
                'units' : 'seconds since 1970-01-01 00:00:00',
                'standard_name' : 'time',
                'long_name': 'time',
                'calendar': 'gregorian'
            })
            time[:] = netCDF4.date2num(self.origin_time.astimezone(pytz.utc).replace(tzinfo=None), units=time.units, calendar=time.calendar)

            nc.createDimension('x', self.size_x)
            nc.createDimension('y', self.size_y)
            lat = nc.createVariable('lat', 'f8', ('x', 'y',), fill_value=fillvalue)
            lat.setncatts({
                'units' : 'degrees_north',
                'standard_name' : 'latitude',
                'long_name' : 'latitude',
                'axis': 'Y'
            })
            lat[:] = lat_values

            lon = nc.createVariable('lon', 'f8', ('x', 'y',), fill_value=fillvalue)
            lon.setncatts({
                'units' : 'degrees_east',
                'standard_name' : 'longitude',
                'long_name' : 'longitude',
                'axis': 'X'
            })
            lon[:] = lon_values

            nc.createDimension('z', 1)
            z = nc.createVariable('z', int, ('z',), fill_value=int(fillvalue))
            z.setncatts({
                'units' : 'm',
                'standard_name' : 'depth',
                'long_name' : 'depth',
                'positive': 'down',
                'axis': 'Z'
            })
            z[:] = 0

            u_values = np.ma.masked_all((self.size_x, self.size_y))
            uc_values = np.ma.masked_all((self.size_x, self.size_y))
            v_values = np.ma.masked_all((self.size_x, self.size_y))
            vc_values = np.ma.masked_all((self.size_x, self.size_y))
            for i, r in self.data.iterrows():
                u_values[r['IX'], r['IY']] = r['U[m/s]']
                uc_values[r['IX'], r['IY']] = r['Acc_U[m/s]']
                v_values[r['IX'], r['IY']] = r['V[m/s]']
                vc_values[r['IX'], r['IY']] = r['Acc_V[m/s]']

            # U
            u = nc.createVariable('u', 'f8', ('time', 'x', 'y'), fill_value=fillvalue)
            u[:] = u_values
            u.setncatts({
                'long_name': 'Eastward Surface Current (m/s)',
                'standard_name': 'eastward_sea_water_velocity',
                'coordinates': 'time lon lat',
                'units': "m/s",
            })

            # UC
            uc = nc.createVariable('uacc', 'f8', ('time', 'x', 'y'), fill_value=fillvalue)
            uc[:] = uc_values
            uc.setncatts({
                'long_name': 'Eastward Surface Current Accuracy (m/s)',
                'standard_name': 'eastward_sea_water_velocity_accuracy',
                'coordinates': 'time lon lat',
                'units': "m/s",
            })

            # V
            v = nc.createVariable('v', 'f8', ('time', 'x', 'y'), fill_value=fillvalue)
            v[:] = v_values
            v.setncatts({
                'long_name': 'Northward Surface Current (m/s)',
                'standard_name': 'northward_sea_water_velocity',
                'coordinates': 'time lon lat',
                'units': "m/s",
            })

            # VC
            vc = nc.createVariable('vacc', 'f8', ('time', 'x', 'y'), fill_value=fillvalue)
            vc[:] = vc_values
            vc.setncatts({
                'long_name': 'Northward Surface Current Accuracy (m/s)',
                'standard_name': 'northward_sea_water_velocity_accuracy',
                'coordinates': 'time lon lat',
                'units': "m/s",
            })

            crs = nc.createVariable('crs', 'i4')
            crs.setncatts({
                'long_name' : 'http://www.opengis.net/def/crs/EPSG/0/4326',
                'grid_mapping_name' : 'latitude_longitude',
                'epsg_code' : 'EPSG:4326',
                'semi_major_axis' : float(6378137.0),
                'inverse_flattening' : float(298.257223563)
            })

            gas = {
                'time_coverage_start': self.origin_time.strftime("%Y-%m-%dT%H:%M:00Z"),
                'time_coverage_end': self.origin_time.strftime("%Y-%m-%dT%H:%M:00Z"),
                'date_created': datetime.utcnow().strftime("%Y-%m-%dT%H:%M:00Z"),
                'Conventions': 'CF-1.6',
                'Metadata_conventions': 'Unidata Dataset Discovery v1.0',
                'cdm_data_type': 'Grid',
                'geospatial_vertical_min': 0,
                'geospatial_vertical_max': 0,
                'geospatial_vertical_positive': 'down',
                'geospatial_lat_min': lat_values.min(),
                'geospatial_lat_max': lat_values.max(),
                'geospatial_lon_min': lon_values.min(),
                'geospatial_lon_max': lon_values.max(),
            }
            nc.setncatts(gas)
