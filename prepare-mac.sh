#!/bin/sh

brew install cmake boost icu4c

cd ./zlib
mkdir build
cd ./build
cmake -DCMAKE_INSTALL_PREFIX:PATH=../../usr ..
make install -j
cd ../../

cd ./libpng
mkdir build
cd ./build
cmake -DCMAKE_INSTALL_PREFIX:PATH=../../usr ..
make install -j
cd ../../