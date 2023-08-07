#!/bin/sh

mkdir ./usr

# zlib and libpng usually already exist in Linux system,
# need to isolate own and system build!
cd ./zlib
mkdir build
cd ./build
cmake -DCMAKE_POLICY_DEFAULT_CMP0074=NEW -DCMAKE_INSTALL_PREFIX:PATH=../../usr ..
make install -j
cd ../../

cd ./libpng
mkdir build
cd ./build
cmake -DCMAKE_POLICY_DEFAULT_CMP0074=NEW -DCMAKE_INSTALL_PREFIX:PATH=../../usr -DZLIB_ROOT=../../usr ..
make install -j
cd ../../

curl -O -L https://boostorg.jfrog.io/artifactory/main/release/1.82.0/source/boost_1_82_0.tar.gz
tar -xf ./boost_1_82_0.tar.gz
rm ./boost_1_82_0.tar.gz
cd ./boost_1_82_0
./bootstrap.sh
./b2 install
cd ../