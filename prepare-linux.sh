#!/bin/sh

APNGASM_BUILD_PATH=$PWD

if [ ! -d ./zlib/build ]; then
    cd ./zlib
    mkdir build
    cd ./build
    cmake -DCMAKE_C_FLAGS="${CMAKE_C_FLAGS} -O3 -fPIC" -DCMAKE_INSTALL_PREFIX:PATH=${APNGASM_BUILD_PATH}/zlib ..
    make install -j
fi

if [ ! -d ./libpng/build ]; then
    cd $APNGASM_BUILD_PATH
    cd ./libpng
    mkdir build
    cd ./build
    cmake -DCMAKE_C_FLAGS="${CMAKE_C_FLAGS} -O3 -fPIC" -DCMAKE_POLICY_DEFAULT_CMP0074=NEW -DBUILD_SHARED_LIBS=OFF -DCMAKE_INSTALL_PREFIX:PATH=${APNGASM_BUILD_PATH}/libpng -DPNG_SHARED=OFF -DZLIB_ROOT=${APNGASM_BUILD_PATH}/zlib -DZLIB_USE_STATIC_LIBS=ON ..
    make install -j
fi

if [ ! -d ./boost/include ]; then
    cd $APNGASM_BUILD_PATH
    cd ./boost
    ./bootstrap.sh
    ./b2 install --build-dir=tmp --prefix=. --build-type=complete --with-program_options --with-regex --with-system -j2 --layout=tagged
    # ./b2 install --build-type=complete --with-program_options --with-regex --with-system -j2 --layout=tagged
fi