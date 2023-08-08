#!/bin/sh

brew install cmake boost icu4c

APNGASM_BUILD_PATH=$PWD
rm -rf /tmp/zlib
rm -rf /tmp/libpng

mkdir -p /tmp/zlib
mkdir -p /tmp/libpng

cd ./zlib
mkdir build
cd ./build
cmake -DBUILD_SHARED_LIBS=OFF -DCMAKE_INSTALL_PREFIX:PATH=/tmp/zlib ..
make install -j

cd ./libpng
mkdir build
cd ./build
cmake -DBUILD_SHARED_LIBS=OFF -DCMAKE_INSTALL_PREFIX:PATH=/tmp/libpng -DZLIB_ROOT=/tmp/zlib -DZLIB_USE_STATIC_LIBS=ON -DPNG_SHARED=OFF ..
make install -j