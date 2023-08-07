#!/bin/sh

mkdir ./usr

curl -O -L https://boostorg.jfrog.io/artifactory/main/release/1.82.0/source/boost_1_82_0.tar.gz
tar -xf ./boost_1_82_0.tar.gz
rm ./boost_1_82_0.tar.gz
cd ./boost_1_82_0
./bootstrap.sh
./b2 install
cd ../

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
make install -j
cd ../../