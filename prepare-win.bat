@echo off

set SOURCE_PATH=%cd%
set FAKEROOT=%SOURCE_PATH%\fakeroot
mkdir %FAKEROOT%

if defined NUMBER_OF_PROCESSORS (
    set CORES=%NUMBER_OF_PROCESSORS%
) else (
    set CORES=4
)

:: Cross compiling supported only through vcpkg
if defined VCPKG_INSTALLATION_ROOT (
    call get-target-win.bat
    
    %VCPKG_INSTALLATION_ROOT%\vcpkg.exe install zlib:%APNGASM_COMPILE_TARGET%-windows-static
    %VCPKG_INSTALLATION_ROOT%\vcpkg.exe install libpng:%APNGASM_COMPILE_TARGET%-windows-static
    %VCPKG_INSTALLATION_ROOT%\vcpkg.exe install boost-program-options:%APNGASM_COMPILE_TARGET%-windows-static
    %VCPKG_INSTALLATION_ROOT%\vcpkg.exe install boost-regex:%APNGASM_COMPILE_TARGET%-windows-static
    %VCPKG_INSTALLATION_ROOT%\vcpkg.exe install boost-system:%APNGASM_COMPILE_TARGET%-windows-static
    %VCPKG_INSTALLATION_ROOT%\vcpkg.exe install boost-algorithm:%APNGASM_COMPILE_TARGET%-windows-static
    %VCPKG_INSTALLATION_ROOT%\vcpkg.exe install boost-property-tree:%APNGASM_COMPILE_TARGET%-windows-static
    %VCPKG_INSTALLATION_ROOT%\vcpkg.exe install boost-foreach:%APNGASM_COMPILE_TARGET%-windows-static

    set VCPKG_CMAKE_FLAGS="-DCMAKE_TOOLCHAIN_FILE=${VCPKG_INSTALLATION_ROOT}/scripts/buildsystems/vcpkg.cmake -DVCPKG_TARGET_TRIPLET=${APNGASM_COMPILE_TARGET}-windows-static"
) else (
    if not exist %FAKEROOT%\include\zlib.h (
        cd %SOURCE_PATH%\zlib
        mkdir build
        cd build
        cmake -DCMAKE_C_FLAGS_RELEASE="/MT" -DBUILD_SHARED_LIBS=OFF -DCMAKE_INSTALL_PREFIX:PATH=%FAKEROOT% ..
        cmake --build . --target INSTALL --config Release
    )

    if not exist %FAKEROOT%\include\png.h (
        cd %SOURCE_PATH%\libpng
        mkdir build
        cd build
        cmake -DCMAKE_C_FLAGS_RELEASE="/MT" -DBUILD_SHARED_LIBS=OFF -DCMAKE_POLICY_DEFAULT_CMP0074=NEW -DCMAKE_INSTALL_PREFIX:PATH=%FAKEROOT% -DZLIB_ROOT=%FAKEROOT% -DZLIB_USE_STATIC_LIBS=ON -DPNG_SHARED=OFF ..
        cmake --build . --target INSTALL --config Release
    )

    if not exist %FAKEROOT%\include\boost (
        cd %SOURCE_PATH%\boost
        call bootstrap.bat
        b2.exe install --link=static --runtime-link=static --threading=multi --prefix=%FAKEROOT% --build-dir=tmp --with-program_options --with-regex --with-system -j%CORES% msvc stage
        robocopy %FAKEROOT%\include\boost-1_82\boost %FAKEROOT%\include\boost /E
    )
)

if not exist %SOURCE_PATH%\apngasm\build (
    cd %SOURCE_PATH%\apngasm
    mkdir build
    cd build
    cmake -DBUILD_SHARED_LIBS=OFF -DZLIB_ROOT=%FAKEROOT% -DPNG_ROOT=%FAKEROOT% -DBoost_ROOT=%FAKEROOT% -DCMAKE_INSTALL_PREFIX:PATH=%FAKEROOT% %VCPKG_CMAKE_FLAGS% ..
    cmake --build . --target INSTALL --config Release
)

exit 0