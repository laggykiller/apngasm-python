#!/bin/sh

brew install cmake boost icu4c

mkdir ./usr

cd zlib
mkdir build
cd build
cmake -DCMAKE_OSX_DEPLOYMENT_TARGET "10.15" ..
make -j
make install
cd ../../

cd libpng
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX:PATH=$(pwd)/../../usr -DCMAKE_OSX_DEPLOYMENT_TARGET "10.15" ..
make -j
make install
cd ../../