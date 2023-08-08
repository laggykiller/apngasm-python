#!/bin/sh

APNGASM_BUILD_PATH=$PWD
rm -rf /tmp/zlib
rm -rf /tmp/libpng

mkdir -p /tmp/zlib
mkdir -p /tmp/libpng

# zlib and libpng usually already exist in Linux system,
# need to isolate own and system build!
cd ./zlib
mkdir build
cd ./build
cmake -DCMAKE_C_FLAGS="${CMAKE_C_FLAGS} -fPIC" -DCMAKE_INSTALL_PREFIX:PATH=/tmp/zlib ..
make install -j

cd $APNGASM_BUILD_PATH
cd ./libpng
mkdir build
cd ./build
cmake -DCMAKE_C_FLAGS="${CMAKE_C_FLAGS} -fPIC" -DCMAKE_POLICY_DEFAULT_CMP0074=NEW -DBUILD_SHARED_LIBS=OFF -DCMAKE_INSTALL_PREFIX:PATH=/tmp/libpng -DPNG_SHARED=OFF -DZLIB_ROOT=/tmp/zlib -DZLIB_USE_STATIC_LIBS=ON ..
make install -j

cd $APNGASM_BUILD_PATH
curl -O -L https://boostorg.jfrog.io/artifactory/main/release/1.82.0/source/boost_1_82_0.tar.gz
tar -xf ./boost_1_82_0.tar.gz -C /tmp
cd /tmp
mv ./boost_1_82_0 ./boost
cd ./boost
./bootstrap.sh
./b2 install --build-dir=tmp --prefix=. --build-type=complete --with-program_options --with-regex --with-system -j16 --layout=tagged