#!/bin/bash

NAME=wera2netcdf
ORG=axiom-data-science

# Build 2.7
conda build -c ioos -c axiom-data-science --python 2.7 .
PACKAGE_PATH=`conda build --python 2.7 --output .`
conda convert --platform all $PACKAGE_PATH -o ./py27
for f in ./py27/**/$NAME*; do
    anaconda upload -u $ORG --force $f
done
rm -r ./py27

# Build 3.4
conda build -c ioos -c axiom-data-science --python 3.4 .
PACKAGE_PATH=`conda build --python 3.4 --output .`
conda convert --platform all $PACKAGE_PATH -o ./py34
for f in ./py34/**/$NAME*; do
    anaconda upload -u $ORG --force $f
done
rm -r ./py34

# Build 3.5
conda build -c ioos -c axiom-data-science --python 3.5 .
PACKAGE_PATH=`conda build --python 3.5 --output .`
conda convert --platform all $PACKAGE_PATH -o ./py35
for f in ./py35/**/$NAME*; do
    anaconda upload -u $ORG --force $f
done
rm -r ./py35
