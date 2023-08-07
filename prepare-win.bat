@echo off

mkdir usr\lib
mkdir usr\include

cd zlib
mkdir build
cd build
cmake "-DCMAKE_INSTALL_PREFIX:PATH=%cd%/../../usr" ..
cmake --build . --config Release --target INSTALL -j
cd ..\..\

cd libpng
mkdir build
cd build
cmake "-DCMAKE_POLICY_DEFAULT_CMP0074=NEW" "-DCMAKE_INSTALL_PREFIX:PATH=%cd%/../../usr" "-DZLIB_ROOT=%cd%/../../usr" ..
cmake --build . --config Release --target INSTALL -j
cd ..\..\

C:
cd C:\
curl -O -L https://github.com/MarkusJx/prebuilt-boost/releases/download/1.81.0/boost-1.81.0-windows-2022-msvc-static-x86.tar.gz
tar -xf boost-1.81.0-windows-2022-msvc-static-x86.tar.gz
del boost-1.81.0-windows-2022-msvc-static-x86.tar.gz