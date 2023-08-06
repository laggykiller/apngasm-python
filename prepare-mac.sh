#!/bin/sh

brew install cmake icu4c

curl -O -L https://boostorg.jfrog.io/artifactory/main/release/1.82.0/source/boost_1_82_0.tar.gz
tar -xf boost_1_82_0.tar.gz
rm boost_1_82_0.tar.gz
cd boost_1_82_0
./bootstrap.sh
./b2 install program_options regex system

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