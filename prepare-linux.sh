#!/bin/sh

APNGASM_BUILD_PATH=$PWD

# Cross compiling supported only through vcpkg
if [[ ! -z $VCPKG_INSTALLATION_ROOT ]]; then
    if [[ -z $APNGASM_COMPILE_TARGET ]]; then
        arch=$(uname --machine)
        if [[ $arch == x86_64* ]]; then
            APNGASM_COMPILE_TARGET=x64
        elif [[ $arch == i*86 ]]; then
            APNGASM_COMPILE_TARGET=x86
        elif [[ $arch == aarch64 ]]; then
            APNGASM_COMPILE_TARGET=arm64
        elif [[ $arch == '' ]]; then
            APNGASM_COMPILE_TARGET=x64
        else
            APNGASM_COMPILE_TARGET=$arch
        fi
    fi
    
    $VCPKG_INSTALLATION_ROOT/vcpkg install zlib:${APNGASM_COMPILE_TARGET}-linux-release
    $VCPKG_INSTALLATION_ROOT/vcpkg install libpng:${APNGASM_COMPILE_TARGET}-linux-release
    $VCPKG_INSTALLATION_ROOT/vcpkg install boost-program-options:${APNGASM_COMPILE_TARGET}-linux-release
    $VCPKG_INSTALLATION_ROOT/vcpkg install boost-regex:${APNGASM_COMPILE_TARGET}-linux-release
    $VCPKG_INSTALLATION_ROOT/vcpkg install boost-system:${APNGASM_COMPILE_TARGET}-linux-release

    exit
fi

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