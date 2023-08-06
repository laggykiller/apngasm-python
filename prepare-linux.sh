#!/bin/sh

git clone https://github.com/boostorg/boost
cd boost
git submodule update --init
mkdir build
cd build
cmake ..
make -j
make install
cd ../../

cd libpng
mkdir build
cd build
cmake ..
make -j
make install
cd ../../

cd zlib
mkdir build
cd build
cmake ..
make -j
make install
cd ../../