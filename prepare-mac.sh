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
    APNGASM_COMPILE_TARGET=$(./get-target-mac.sh)
    
    ${VCPKG_INSTALLATION_ROOT}/vcpkg install zlib:${APNGASM_COMPILE_TARGET}-osx
    ${VCPKG_INSTALLATION_ROOT}/vcpkg install libpng:${APNGASM_COMPILE_TARGET}-osx
    ${VCPKG_INSTALLATION_ROOT}/vcpkg install boost-program-options:${APNGASM_COMPILE_TARGET}-osx
    ${VCPKG_INSTALLATION_ROOT}/vcpkg install boost-regex:${APNGASM_COMPILE_TARGET}-osx
    ${VCPKG_INSTALLATION_ROOT}/vcpkg install boost-system:${APNGASM_COMPILE_TARGET}-osx
    ${VCPKG_INSTALLATION_ROOT}/vcpkg install boost-algorithm:${APNGASM_COMPILE_TARGET}-osx
    ${VCPKG_INSTALLATION_ROOT}/vcpkg install boost-property-tree:${APNGASM_COMPILE_TARGET}-osx
    ${VCPKG_INSTALLATION_ROOT}/vcpkg install boost-foreach:${APNGASM_COMPILE_TARGET}-osx

    VCPKG_CMAKE_FLAGS="-DCMAKE_TOOLCHAIN_FILE=${VCPKG_INSTALLATION_ROOT}/scripts/buildsystems/vcpkg.cmake -DVCPKG_TARGET_TRIPLET=${APNGASM_COMPILE_TARGET}-osx"
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
        cd ${SOURCE_PATH}/zlib
        mkdir build
        cd ./build
        cmake -DCMAKE_INSTALL_PREFIX:PATH=${FAKEROOT} ..
        make install -j
    fi

    if [ ! -f ${FAKEROOT}/include/png.h ]; then
        cd ${SOURCE_PATH}/libpng
        mkdir build
        cd ./build
        cmake -DCMAKE_POLICY_DEFAULT_CMP0074=NEW -DBUILD_SHARED_LIBS=OFF -DCMAKE_INSTALL_PREFIX:PATH=${FAKEROOT} -DPNG_SHARED=OFF -DZLIB_ROOT=${FAKEROOT} -DZLIB_USE_STATIC_LIBS=ON ..
        make install -j
    fi

    if [ ! -d ${FAKEROOT}/include/boost ]; then
        cd ${SOURCE_PATH}/boost
        ./bootstrap.sh --prefix=.
        ./b2 install link=static --build-dir=tmp --prefix=${FAKEROOT} --with-program_options --with-regex --with-system -j${CORES} --layout=tagged
    fi
fi

if [ ! -d ${FAKEROOT}/lib/libapngasm.a ]; then
    cd ${SOURCE_PATH}/apngasm
    mkdir build
    cd ./build
    cmake -DCMAKE_POLICY_DEFAULT_CMP0074=NEW -DBUILD_SHARED_LIBS=OFF -DCMAKE_INSTALL_PREFIX:PATH=${FAKEROOT} -DZLIB_ROOT=${FAKEROOT} -DPNG_ROOT=${FAKEROOT} -DBoost_ROOT=${FAKEROOT} ${VCPKG_CMAKE_FLAGS} ..
    make install -j
    mkdir ${FAKEROOT}/include/listener
    cp ${SOURCE_PATH}/apngasm/lib/src/listener/apngasmlistener.h ${FAKEROOT}/include/listener
fi