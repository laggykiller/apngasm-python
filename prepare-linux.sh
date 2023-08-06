#!/bin/sh

cd libpng
mkdir build
cd build
cmake ..
make
make install
cd ../../

cd zlib
mkdir build
cd build
cmake ..
make
make install
cd ../../