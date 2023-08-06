#!/bin/sh

brew install cmake boost icu4c

mkdir ./usr

cd libpng
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX:PATH=$(pwd)/../../usr ..
make -j
make install
cd ../../

cd zlib
mkdir build
cd build
cmake -DZLIB_LIBRARY=$(pwd)/../../usr/lib/zlib.so -DZLIB_INCLUDE_DIR=$(pwd)/../../usr/include -DCMAKE_INSTALL_PREFIX:PATH=$(pwd)/../../usr ..
make -j
make install
cd ../../