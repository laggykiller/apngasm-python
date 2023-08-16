cmake_minimum_required(VERSION 3.17)
cmake_policy(SET CMP0074 NEW)

if (WIN32)
    set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>")
    set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} /MT")
    set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} /MTd")
elseif (LINUX)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fPIC")
elseif (APPLE)
    set(CMAKE_OSX_DEPLOYMENT_TARGET "10.15")
endif()

if (WIN32)
    set(GET_TARGET_CMD "cmd" "/c" "${CMAKE_SOURCE_DIR}/get-target-win.bat")
    set(PREPARE_CMD "cmd" "/c" "${CMAKE_SOURCE_DIR}/prepare-win.bat")
elseif (APPLE)
    set(GET_TARGET_CMD "${CMAKE_SOURCE_DIR}/get-target-mac.sh")
    set(PREPARE_CMD "${CMAKE_SOURCE_DIR}/prepare-mac.sh")
else()
    set(GET_TARGET_CMD "${CMAKE_SOURCE_DIR}/get-target-linux.sh")
    set(PREPARE_CMD "${CMAKE_SOURCE_DIR}/prepare-linux.sh")
endif()

execute_process(
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
    COMMAND ${PREPARE_CMD}
)

set(Boost_USE_STATIC_LIBS ON)
if (WIN32)
    set(Boost_USE_MULTITHREADED ON)
    set(Boost_USE_STATIC_RUNTIME ON)
    set(STATIC_LIBRARY_SUFFIX ".lib")
else()
    set(STATIC_LIBRARY_SUFFIX ".a")
endif()

if (DEFINED ENV{VCPKG_INSTALLATION_ROOT})
    set(VCPKG_INSTALLATION_ROOT $ENV{VCPKG_INSTALLATION_ROOT})
endif()

if (DEFINED VCPKG_INSTALLATION_ROOT)
    if (DEFINED ENV{APNGASM_COMPILE_TARGET})
        set(APNGASM_COMPILE_TARGET $ENV{APNGASM_COMPILE_TARGET})
    elseif (NOT DEFINED APNGASM_COMPILE_TARGET)
        execute_process(
            WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
            COMMAND ${GET_TARGET_CMD}
            OUTPUT_VARIABLE APNGASM_COMPILE_TARGET
        )
        if (DEFINED ENV{APNGASM_COMPILE_TARGET})
            set(APNGASM_COMPILE_TARGET $ENV{APNGASM_COMPILE_TARGET})
        endif()
    endif()

    if (DEFINED ENV{PLATFORM})
        set(PLATFORM $ENV{PLATFORM})
    elseif (NOT DEFINED PLATFORM)
        if (WIN32)
            set(PLATFORM windows-static)
        elseif (APPLE)
            set(PLATFORM osx)
        else()
            set(PLATFORM linux)
        endif()
    endif()

    if (WIN32)
        set(LIBZ_NAME zlib)
        set(LIBPNG_NAME libpng16)
    else()
        set(LIBZ_NAME libz)
        set(LIBPNG_NAME libpng16)
    endif()

    set(ZLIB_ROOT ${VCPKG_INSTALLATION_ROOT}/installed)
    set(PNG_ROOT ${VCPKG_INSTALLATION_ROOT}/installed)
    set(Boost_ROOT ${VCPKG_INSTALLATION_ROOT}/installed)
    
    set(VCPKG_TARGET_TRIPLET ${APNGASM_COMPILE_TARGET}-${PLATFORM})

    include_directories(${VCPKG_INSTALLATION_ROOT}/installed/${VCPKG_TARGET_TRIPLET}/include)
    set(LIBZ_PATH ${VCPKG_INSTALLATION_ROOT}/installed/${VCPKG_TARGET_TRIPLET}/lib/${LIBZ_NAME}${STATIC_LIBRARY_SUFFIX})
    set(LIBPNG_PATH ${VCPKG_INSTALLATION_ROOT}/installed/${VCPKG_TARGET_TRIPLET}/lib/${LIBPNG_NAME}${STATIC_LIBRARY_SUFFIX})
    set(CMAKE_TOOLCHAIN_FILE "${VCPKG_INSTALLATION_ROOT}/scripts/buildsystems/vcpkg.cmake"
      CACHE STRING "Vcpkg toolchain file")
else()
    if (WIN32)
        set(LIBZ_NAME zlibstatic)
        set(LIBPNG_NAME libpng16_static)
    else()
        set(LIBZ_NAME libz)
        set(LIBPNG_NAME libpng16)
    endif()

    set(ZLIB_ROOT ${CMAKE_SOURCE_DIR}/fakeroot)
    set(PNG_ROOT ${CMAKE_SOURCE_DIR}/fakeroot)
    set(Boost_ROOT ${CMAKE_SOURCE_DIR}/fakeroot)

    set(LIBZ_PATH ${CMAKE_SOURCE_DIR}/fakeroot/lib/${LIBZ_NAME}${STATIC_LIBRARY_SUFFIX})
    if(NOT EXISTS ${LIBZ_PATH})
        set(LIBZ_PATH ${CMAKE_SOURCE_DIR}/fakeroot/lib64/${LIBZ_NAME}${STATIC_LIBRARY_SUFFIX})
    endif()

    set(LIBPNG_PATH ${CMAKE_SOURCE_DIR}/fakeroot/lib/${LIBPNG_NAME}${STATIC_LIBRARY_SUFFIX})
    if(NOT EXISTS ${LIBPNG_PATH})
        set(LIBPNG_PATH ${CMAKE_SOURCE_DIR}/fakeroot/lib64/${LIBPNG_NAME}${STATIC_LIBRARY_SUFFIX})
    endif()
endif()

project(apngasm-python VERSION 1.0.1)
set(PY_VERSION_SUFFIX "")
set(PY_FULL_VERSION ${PROJECT_VERSION}${PY_VERSION_SUFFIX})

# Make sure that the Python and CMake versions match
if (DEFINED PY_BUILD_CMAKE_PACKAGE_VERSION)
    if (NOT "${PY_BUILD_CMAKE_PACKAGE_VERSION}" MATCHES "^${PY_FULL_VERSION}$")
        message(FATAL_ERROR "Version number does not match "
                             "(${PY_BUILD_CMAKE_PACKAGE_VERSION} - ${PY_FULL_VERSION}).")
    endif()
endif()

# Find the nanobind package
include(cmake/QueryPythonForNanobind.cmake)
find_nanobind_python_first()

# Compile the Python module
nanobind_add_module(_apngasm_python "src/apngasm_python.cpp" NB_STATIC STABLE_ABI)
if (WIN32)
    nanobind_compile_options(_apngasm_python "/MT /MP /bigobj")
endif()
target_compile_definitions(_apngasm_python PRIVATE _apngasm_python_EXPORTS)
target_compile_definitions(_apngasm_python PRIVATE apngasm_EXPORTS)

# Static linking
add_library(zlibstatic STATIC IMPORTED)
add_library(png_static STATIC IMPORTED)

add_subdirectory(apngasm)
set_target_properties(apngasm-static PROPERTIES BUILD_SHARED_LIBS OFF)

include_directories(${CMAKE_SOURCE_DIR}/fakeroot/include)
include_directories(${CMAKE_BINARY_DIR}/apngasm/lib/src)
include_directories(${CMAKE_SOURCE_DIR}/apngasm/lib/src)
include_directories(${CMAKE_SOURCE_DIR}/apngasm/lib/src/listener)

set_target_properties(zlibstatic PROPERTIES IMPORTED_LOCATION ${LIBZ_PATH})
set_target_properties(png_static PROPERTIES IMPORTED_LOCATION ${LIBPNG_PATH})

target_link_libraries(_apngasm_python PRIVATE apngasm-static png_static zlibstatic)

target_compile_definitions(_apngasm_python PRIVATE
    MODULE_NAME=$<TARGET_FILE_BASE_NAME:_apngasm_python>
    VERSION_INFO="${PY_FULL_VERSION}"
)

# Hide all symbols by default (including external libraries on Linux)
set_target_properties(_apngasm_python PROPERTIES
    CXX_VISIBILITY_PRESET "hidden"
    VISIBILITY_INLINES_HIDDEN true
    POSITION_INDEPENDENT_CODE true)
if (WIN32)
    set_target_properties(_apngasm_python PROPERTIES LINK_FALGS_RELEASE "/WHOLEARCHIVE:MNN")
elseif (LINUX)
    target_link_options(_apngasm_python PRIVATE "LINKER:--exclude-libs,ALL")
endif()

# Install the module
install(TARGETS _apngasm_python
    EXCLUDE_FROM_ALL
    DESTINATION ${PY_BUILD_CMAKE_MODULE_NAME}
    COMPONENT python_module)

# Generate stubs for the Python module
option(WITH_PY_STUBS
    "Generate Python stub files (.pyi) for the Python module." On)
if (WITH_PY_STUBS AND NOT CMAKE_CROSSCOMPILING)
    include(cmake/NanobindStubgen.cmake)
    nanobind_stubgen(_apngasm_python)
    nanobind_stubgen_install(_apngasm_python ${PY_BUILD_CMAKE_MODULE_NAME})
endif()