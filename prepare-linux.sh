#!/bin/sh

yum update -y
yum install -y boost-devel

cd zlib
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