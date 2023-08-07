#!/bin/sh

yum update -y
yum install -y boost-devel

mkdir ./usr

# zlib and libpng usually already exist in Linux system,
# need to isolate own and system build!
cd ./zlib
mkdir build
cd ./build
cmake -DCMAKE_INSTALL_PREFIX:PATH=$(pwd)/../../usr ..
make install -j
cd ../../

cd ./libpng
mkdir build
cd ./build
cmake -DCMAKE_INSTALL_PREFIX:PATH=$(pwd)/../../usr -DZLIB_ROOT=$(pwd)/../../usr ..
cmake -DCMAKE_INSTALL_PREFIX:PATH=$(pwd)/../../usr ..
make install -j
cd ../../