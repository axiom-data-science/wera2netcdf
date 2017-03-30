# wera2netcdf  [![Build Status](https://travis-ci.org/axiom-data-science/wera2netcdf.svg?branch=master)](https://travis-ci.org/axiom-data-science/wera2netcdf)

Converting WERA Total ASCII files (the final total current speed and direction
of the combined radial data) into CF NetCDF files.

## Installation

```
$ conda install -c ioos wera2netcdf
```

## Usage

```python
In [1]: from wera2netcdf import WeraAsciiTotals
In [2]: w = WeraAsciiTotals('totals.txt')
In [3]: w.is_valid()
Out[3]: True

# Pandas dataframe of the data
In [4]: w.data.head()
Out[4]:
   IX   IY  U[m/s]  V[m/s]  KL  Acc_U[m/s]  Acc_V[m/s]
0  68   70   0.000   0.000   0       0.035       0.117
1  69  107   0.014  -0.103   0       0.051       0.095
2  69  108   0.012  -0.097   0       0.050       0.098
3  69  109   0.009  -0.104   0       0.051       0.102
4  70  102   0.035  -0.093   0       0.048       0.087

# Export to netCDF file
In [5]: w.export('out.nc')

In [6]: import netCDF4
In [7]: netCDF4.Dataset('out.nc').variables
Out[7]:
OrderedDict([('time', <class 'netCDF4._netCDF4.Variable'>
              int64 time(time)
                  _FillValue: -999
                  units: seconds since 1970-01-01 00:00:00
                  standard_name: time
                  calendar: gregorian
                  long_name: time
              unlimited dimensions:
              current shape = (1,)
              filling on),

              ('lat', <class 'netCDF4._netCDF4.Variable'>
              float64 lat(x, y)
                  _FillValue: -999.9
                  units: degrees_north
                  standard_name: latitude
                  axis: Y
                  long_name: latitude
              unlimited dimensions:
              current shape = (130, 210)
              filling on),

              ('lon', <class 'netCDF4._netCDF4.Variable'>
              float64 lon(x, y)
                  _FillValue: -999.9
                  units: degrees_east
                  standard_name: longitude
                  axis: X
                  long_name: longitude
              unlimited dimensions:
              current shape = (130, 210)
              filling on),

              ('z', <class 'netCDF4._netCDF4.Variable'>
              int64 z(z)
                  _FillValue: -999
                  units: m
                  standard_name: depth
                  positive: down
                  axis: Z
                  long_name: depth
              unlimited dimensions:
              current shape = (1,)
              filling on),

              ('u', <class 'netCDF4._netCDF4.Variable'>
              float64 u(time, x, y)
                  _FillValue: -999.9
                  standard_name: eastward_sea_water_velocity
                  long_name: Eastward Surface Current (m/s)
                  units: m/s
                  coordinates: time lon lat
              unlimited dimensions:
              current shape = (1, 130, 210)
              filling on),

              ('uacc', <class 'netCDF4._netCDF4.Variable'>
              float64 uacc(time, x, y)
                  _FillValue: -999.9
                  standard_name: eastward_sea_water_velocity_accuracy
                  long_name: Eastward Surface Current Accuracy (m/s)
                  units: m/s
                  coordinates: time lon lat
              unlimited dimensions:
              current shape = (1, 130, 210)
              filling on),

              ('v', <class 'netCDF4._netCDF4.Variable'>
              float64 v(time, x, y)
                  _FillValue: -999.9
                  standard_name: northward_sea_water_velocity
                  long_name: Northward Surface Current (m/s)
                  units: m/s
                  coordinates: time lon lat
              unlimited dimensions:
              current shape = (1, 130, 210)
              filling on),

              ('vacc', <class 'netCDF4._netCDF4.Variable'>
              float64 vacc(time, x, y)
                  _FillValue: -999.9
                  standard_name: northward_sea_water_velocity_accuracy
                  long_name: Northward Surface Current Accuracy (m/s)
                  units: m/s
                  coordinates: time lon lat
              unlimited dimensions:
              current shape = (1, 130, 210)
              filling on),

              ('crs', <class 'netCDF4._netCDF4.Variable'>
              int32 crs()
                  long_name: http://www.opengis.net/def/crs/EPSG/0/4326
                  grid_mapping_name: latitude_longitude
                  epsg_code: EPSG:4326
                  inverse_flattening: 298.257223563
                  semi_major_axis: 6378137.0
              unlimited dimensions:
              current shape = ()
              filling on, default _FillValue of -2147483647 used)
])
```
