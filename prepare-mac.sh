#!/bin/sh

brew install cmake boost icu4c

mkdir /opt/zlib
mkdir /opt/libpng

cd ./zlib
mkdir build
cd ./build
cmake -DCMAKE_INSTALL_PREFIX:PATH=/opt/zlib ..
make install -j
cd ../../

cd ./libpng
mkdir build
cd ./build
cmake -DCMAKE_INSTALL_PREFIX:PATH=/opt/libpng -DZLIB_ROOT=/opt/zlib ..
make install -j
cd ../../