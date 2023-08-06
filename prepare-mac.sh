#!/bin/sh

brew install cmake boost icu4c

mkdir ./deps

cd libpng
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX:PATH=$(pwd)/../../deps ..
make -j
make install
cd ../../

cd zlib
mkdir build
cd build
cmake -DZLIB_LIBRARY=$(pwd)/../../deps/lib/zlib.so -DZLIB_INCLUDE_DIR=$(pwd)/../../deps/include -DCMAKE_INSTALL_PREFIX:PATH=$(pwd)/../../deps ..
make -j
make install
cd ../../