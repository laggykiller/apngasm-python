@echo off

set APNGASM_BUILD_PATH=%cd%

:: Cross compiling supported only through vcpkg
if defined VCPKG_INSTALLATION_ROOT (
    if defined APNGASM_CROSSCOMPILE_TARGET (
        set VCPKG_DOWNLOAD_PLATFORM=%APNGASM_CROSSCOMPILE_TARGET%
    ) else if %PROCESSOR_ARCHITECTURE%==AMD64 (
        set VCPKG_DOWNLOAD_PLATFORM=x64
    ) else if %PROCESSOR_ARCHITECTURE%==X86 (
        set VCPKG_DOWNLOAD_PLATFORM=x86
    ) else if %PROCESSOR_ARCHITECTURE%==ARM64 (
        set VCPKG_DOWNLOAD_PLATFORM=arm64
    ) else if %PROCESSOR_ARCHITECTURE%==ARM (
        set VCPKG_DOWNLOAD_PLATFORM=arm
    ) else (
        set VCPKG_DOWNLOAD_PLATFORM=%PROCESSOR_ARCHITECTURE%
    )
    
    %VCPKG_INSTALLATION_ROOT%\vcpkg.exe install zlib:%VCPKG_DOWNLOAD_PLATFORM%-windows-static
    %VCPKG_INSTALLATION_ROOT%\vcpkg.exe install libpng:%VCPKG_DOWNLOAD_PLATFORM%-windows-static
    %VCPKG_INSTALLATION_ROOT%\vcpkg.exe install boost-program-options:%VCPKG_DOWNLOAD_PLATFORM%-windows-static
    %VCPKG_INSTALLATION_ROOT%\vcpkg.exe install boost-regex:%VCPKG_DOWNLOAD_PLATFORM%-windows-static
    %VCPKG_INSTALLATION_ROOT%\vcpkg.exe install boost-system:%VCPKG_DOWNLOAD_PLATFORM%-windows-static

    exit 0
)

if not exist zlib\build (
    cd zlib
    mkdir build
    cd build
    cmake -DCMAKE_C_FLAGS_RELEASE="/MT" -DBUILD_SHARED_LIBS=OFF -DCMAKE_INSTALL_PREFIX:PATH=%APNGASM_BUILD_PATH%\zlib ..
    cmake --build . --target INSTALL --config Release
)

cd %APNGASM_BUILD_PATH%
if not exist libpng\build (
    cd libpng
    mkdir build
    cd build
    cmake -DCMAKE_C_FLAGS_RELEASE="/MT" -DBUILD_SHARED_LIBS=OFF -DCMAKE_POLICY_DEFAULT_CMP0074=NEW -DCMAKE_INSTALL_PREFIX:PATH=%APNGASM_BUILD_PATH%\libpng -DZLIB_ROOT=%APNGASM_BUILD_PATH%\zlib -DZLIB_USE_STATIC_LIBS=ON -DPNG_SHARED=OFF ..
    cmake --build . --target INSTALL --config Release
)

cd %APNGASM_BUILD_PATH%
if not exist boost\include (
    cd boost
    call bootstrap.bat --prefix=.
    b2.exe install --prefix=. --build-dir=tmp --build-type=complete --with-program_options --with-regex --with-system -j4 msvc stage
    robocopy include\boost-1_82\boost include\boost /E
)

exit 0