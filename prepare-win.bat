@echo off

mkdir deps\lib
mkdir deps\include

cd zlib
mkdir build
cd build
cmake ..
cmake --build . --config Release -j
cd ..\..\
:: For some reason zconf.h disappear after compiling
copy zlib\build\zconf.h zlib
copy zlib\build\zconf.h deps\include
copy zlib\zlib.h deps\include
copy zlib\build\Release\zlib.lib deps\lib

cd libpng
mkdir build
cd build
cmake "-DZLIB_LIBRARY=%cd%\..\..\zlib\build\Release\zlib.lib" "-DZLIB_INCLUDE_DIR=%cd%\..\..\zlib" ..
cmake --build . --config Release -j
cd ..\..\
copy libpng\png.h deps\include
copy libpng\pngconf.h deps\include
copy libpng\build\pnglibconf.h deps\include
copy libpng\build\Release\libpng16.lib deps\lib

mkdir boost
curl -O -L https://sourceforge.net/projects/boost/files/boost-binaries/1.82.0/boost_1_82_0-msvc-14.3-64.exe
start /wait boost_1_82_0-msvc-14.3-64.exe /verysilent /dir=%cd%
del boost_1_82_0-msvc-14.3-64.exe
:: DEBUG
dir
cd ..