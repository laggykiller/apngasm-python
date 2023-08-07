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
curl -O -L https://boostorg.jfrog.io/artifactory/main/release/1.82.0/source/boost_1_82_0.zip
tar -xf boost_1_82_0.zip
move boost_1_82_0 boost
cd boost
bootstrap.bat
b2.exe
xcopy stage\lib lib\ /E /H
xcopy boost include\ /E /H