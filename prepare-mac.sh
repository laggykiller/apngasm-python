#!/bin/sh

SOURCE_PATH=$PWD
FAKEROOT=${SOURCE_PATH}/fakeroot
mkdir ${FAKEROOT}

CORES=$(sysctl -n hw.logicalcpu)
if [[ $? -ne 0 ]]; then
  CORES=2
fi

# Cross compiling supported only through vcpkg
if [[ ! -z $VCPKG_INSTALLATION_ROOT ]]; then
    export VCPKG_OSX_DEPLOYMENT_TARGET=10.15
    export VCPKG_C_FLAGS="-mmacosx-version-min=10.15"
    export VCPKG_CXX_FLAGS="-mmacosx-version-min=10.15"
    export APNGASM_COMPILE_TARGET=$(./get-target-mac.sh)
    
    ${VCPKG_INSTALLATION_ROOT}/vcpkg install zlib:${APNGASM_COMPILE_TARGET}-osx
    ${VCPKG_INSTALLATION_ROOT}/vcpkg install libpng:${APNGASM_COMPILE_TARGET}-osx
    ${VCPKG_INSTALLATION_ROOT}/vcpkg install boost-program-options:${APNGASM_COMPILE_TARGET}-osx
    ${VCPKG_INSTALLATION_ROOT}/vcpkg install boost-regex:${APNGASM_COMPILE_TARGET}-osx
    ${VCPKG_INSTALLATION_ROOT}/vcpkg install boost-system:${APNGASM_COMPILE_TARGET}-osx
    ${VCPKG_INSTALLATION_ROOT}/vcpkg install boost-algorithm:${APNGASM_COMPILE_TARGET}-osx
    ${VCPKG_INSTALLATION_ROOT}/vcpkg install boost-property-tree:${APNGASM_COMPILE_TARGET}-osx
    ${VCPKG_INSTALLATION_ROOT}/vcpkg install boost-foreach:${APNGASM_COMPILE_TARGET}-osx
else
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

    if [ ! -f ${FAKEROOT}/include/zlib.h ]; then
        cd ${SOURCE_PATH}
        git clone https://github.com/madler/zlib.git
        cd ${SOURCE_PATH}/zlib
        git checkout v1.2.13
        mkdir build
        cd ./build
        cmake -DCMAKE_OSX_DEPLOYMENT_TARGET=10.15 -DCMAKE_INSTALL_PREFIX:PATH=${FAKEROOT} ..
        make install -j
    fi

    if [ ! -f ${FAKEROOT}/include/png.h ]; then
        cd ${SOURCE_PATH}
        git clone https://github.com/glennrp/libpng.git
        cd ${SOURCE_PATH}/libpng
        git checkout v1.6.40
        mkdir build
        cd ./build
        cmake -DCMAKE_OSX_DEPLOYMENT_TARGET=10.15 -DCMAKE_POLICY_DEFAULT_CMP0074=NEW -DBUILD_SHARED_LIBS=OFF -DCMAKE_INSTALL_PREFIX:PATH=${FAKEROOT} -DPNG_SHARED=OFF -DZLIB_ROOT=${FAKEROOT} -DZLIB_USE_STATIC_LIBS=ON ..
        make install -j
    fi

    if [ ! -d ${FAKEROOT}/include/boost ]; then
        cd ${SOURCE_PATH}
        git clone --recursive https://github.com/boostorg/boost.git
        cd ${SOURCE_PATH}/boost
        git checkout boost-1.83.0
        ./bootstrap.sh --prefix=.
        ./b2 install link=static macosx-version-min=10.15 --build-dir=tmp --prefix=${FAKEROOT} --with-program_options --with-regex --with-system -j${CORES} --layout=tagged
    fi
fi