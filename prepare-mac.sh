#!/bin/sh

brew install cmake boost icu4c

cd ./zlib
mkdir build
cd ./build
cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr/local ..
make install -j
cd ../../
rm -rf ./zlib/build # https://github.com/pypa/cibuildwheel/issues/139#issuecomment-495984087

cd ./libpng
mkdir build
cd ./build
cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr/local -DZLIB_ROOT=/usr/local ..
make install -j
cd ../../
rm -rf ./libpng/build # https://github.com/pypa/cibuildwheel/issues/139#issuecomment-495984087