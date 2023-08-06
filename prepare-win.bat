@echo off

mkdir deps
mkdir deps\lib
mkdir deps\include

cd zlib
mkdir build
cd build
cmake  -G "Visual Studio 17 2022" ..
cmake --build . --config Release
cd ..\..\
:: For some reason zconf.h disappear after compiling
copy zlib\build\zconf.h zlib
copy zlib\build\zconf.h deps\include
copy zlib\zlib.h deps\include
copy zlib\build\Release\zlib.lib deps\lib

cd libpng
mkdir build
cd build
cmake -G "Visual Studio 17 2022" "-DZLIB_LIBRARY=%cd%\..\..\zlib\build\Release\zlib.lib" "-DZLIB_INCLUDE_DIR=%cd%\..\..\zlib" ..
cmake --build . --config Release
cd ..\..\
copy libpng\png.h deps\include
copy libpng\pngconf.h deps\include
copy libpng\build\pnglibconf.h deps\include
copy libpng\build\Release\libpng16.lib deps\lib

curl -O -L https://sourceforge.net/projects/boost/files/boost-binaries/1.82.0/boost_1_82_0-msvc-14.3-64.exe
start /wait boost_1_82_0-msvc-14.3-64.exe /verysilent
del boost_1_82_0-msvc-14.3-64.exe

cmd /V /C "set LIB=%cd%\deps\lib;C:\local\boost_1_82_0\lib64-msvc-14.3 && set INCLUDE=%cd%\deps\include && cmake -G "Visual Studio 17 2022" .. && cmake --build . --config Release"