#!/bin/sh

yum install -y boost-devel

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