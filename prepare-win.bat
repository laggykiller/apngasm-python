@echo off

mkdir C:\opt\zlib
mkdir C:\opt\libpng

cd zlib
mkdir build
cd build
cmake "-DCMAKE_INSTALL_PREFIX:PATH=C:/opt/zlib" ..
cmake --build . --config Release --target INSTALL -j
cd ..\..\

cd libpng
mkdir build
cd build
cmake "-DCMAKE_POLICY_DEFAULT_CMP0074=NEW" "-DCMAKE_INSTALL_PREFIX:PATH=C:/opt/libpng" "-DZLIB_ROOT=C:/opt/zlib" ..
cmake --build . --config Release --target INSTALL -j
cd ..\..\

C:
cd C:\opt
curl -O -L https://boostorg.jfrog.io/artifactory/main/release/1.82.0/source/boost_1_82_0.zip
tar -xf boost_1_82_0.zip
del boost_1_82_0.zip
move boost_1_82_0 boost
cd boost
bootstrap.bat
b2.exe install --build-dir='tmp' --prefix='.' variant='release,debug' address-model='32,64' link='static' --with-program_options --with-regex --with-system -j4 msvc stage
xcopy /E /I include\boost-1_82\boost\ include\boost