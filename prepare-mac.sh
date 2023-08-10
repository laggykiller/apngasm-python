#!/bin/sh

APNGASM_BUILD_PATH=$PWD

# Cross compiling supported only through vcpkg
if [[ ! -z $VCPKG_INSTALLATION_ROOT ]]; then
    APNGASM_COMPILE_TARGET=$(./get-target-mac.sh)
    
    ${VCPKG_INSTALLATION_ROOT}/vcpkg install zlib:${APNGASM_COMPILE_TARGET}-osx
    ${VCPKG_INSTALLATION_ROOT}/vcpkg install libpng:${APNGASM_COMPILE_TARGET}-osx
    ${VCPKG_INSTALLATION_ROOT}/vcpkg install boost-program-options:${APNGASM_COMPILE_TARGET}-osx
    ${VCPKG_INSTALLATION_ROOT}/vcpkg install boost-regex:${APNGASM_COMPILE_TARGET}-osx
    ${VCPKG_INSTALLATION_ROOT}/vcpkg install boost-system:${APNGASM_COMPILE_TARGET}-osx
    ${VCPKG_INSTALLATION_ROOT}/vcpkg install boost-algorithm:${APNGASM_COMPILE_TARGET}-osx
    ${VCPKG_INSTALLATION_ROOT}/vcpkg install boost-property-tree:${APNGASM_COMPILE_TARGET}-osx
    ${VCPKG_INSTALLATION_ROOT}/vcpkg install boost-foreach:${APNGASM_COMPILE_TARGET}-osx

    exit
fi

which -s brew
if [[ $? != 0 ]] ; then
    ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
fi

which -s cmake
if [[ $? != 0 ]] ; then
    brew install cmake
fi

if [ ! -d /usr/local/opt/icu4c/include ]; then
    brew install icu4c
fi

if [ ! -d ./zlib/build ]; then
    cd ./zlib
    mkdir build
    cd ./build
    cmake -DBUILD_SHARED_LIBS=OFF -DCMAKE_INSTALL_PREFIX:PATH=${APNGASM_BUILD_PATH}/zlib ..
    make install -j
fi

cd $APNGASM_BUILD_PATH
if [ ! -d ./libpng/build ]; then
    cd ./libpng
    mkdir build
    cd ./build
    cmake -DBUILD_SHARED_LIBS=OFF -DCMAKE_INSTALL_PREFIX:PATH=${APNGASM_BUILD_PATH}/libpng -DZLIB_ROOT=${APNGASM_BUILD_PATH}/zlib -DZLIB_USE_STATIC_LIBS=ON -DPNG_SHARED=OFF ..
    make install -j
fi

cd $APNGASM_BUILD_PATH
if [ ! -d ./boost/include ]; then
    cd ./boost
    ./bootstrap.sh
    ./b2 install --build-dir=tmp --prefix=. --build-type=complete --with-program_options --with-regex --with-system -j2 --layout=tagged
    # ./b2 install --build-type=complete --with-program_options --with-regex --with-system -j2 --layout=tagged
fi