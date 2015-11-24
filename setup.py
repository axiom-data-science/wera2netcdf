from setuptools import setup, find_packages

def version():
    with open('VERSION') as f:
        return f.read().strip()

def readme():
    with open('README.md') as f:
        return f.read()

reqs = [line.strip() for line in open('requirements.txt')]

setup(
    name                = "wera2netcdf",
    version             = version(),
    description         = "A utility to convert WERA total ASCII files into CF NetCDF files.",
    long_description    = readme(),
    license             = 'MIT',
    author              = "Kyle Wilcox",
    author_email        = "kyle@axiomdatascience.com",
    url                 = "https://github.com/axiom-data-science/wera2netcdf",
    packages            = find_packages(),
    install_requires    = reqs,
    tests_require       = ['pytest'],
    classifiers         = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering',
    ],
    include_package_data = True,
)
