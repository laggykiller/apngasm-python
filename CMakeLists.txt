cmake_minimum_required(VERSION 3.17)
cmake_policy(SET CMP0074 NEW)

if (WIN32)
    set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>")
    set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} /MT")
    set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} /MTd")
elseif (LINUX)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fPIC")
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

project(apngasm-python VERSION 1.0.0)
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

# Somehow GitHub runner cannot find nanobind-config.cmake / nanobindConfig.cmake with this
# include(cmake/QueryPythonForNanobind.cmake)
# find_nanobind_python_first()

find_package(Python COMPONENTS Interpreter Development.Module REQUIRED)
add_subdirectory(nanobind)

# Compile the example Python module
nanobind_add_module(_apngasm_python "src/apngasm_python.cpp" NB_STATIC STABLE_ABI)
if (WIN32)
    nanobind_compile_options(_apngasm_python "/MT /MP /bigobj")
endif()
target_compile_definitions(_apngasm_python PRIVATE APNGASM_PY_BUILD)
target_compile_definitions(_apngasm_python PRIVATE apngasm_EXPORTS)

# Static linking
add_library(zlibstatic STATIC IMPORTED)
add_library(png_static STATIC IMPORTED)
add_library(apngasm-static STATIC IMPORTED)

if (DEFINED ENV{VCPKG_INSTALLATION_ROOT})
    set(VCPKG_INSTALLATION_ROOT $ENV{VCPKG_INSTALLATION_ROOT})
endif()

if (WIN32)
    set(LIBZ_NAME zlibstatic)
    set(LIBPNG_NAME libpng16_static)
    set(LIBAPNGASM_NAME apngasm)
else()
    set(LIBZ_NAME libz)
    set(LIBPNG_NAME libpng16)
    set(LIBAPNGASM_NAME libapngasm)
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
    
    set(VCPKG_TARGET_TRIPLET ${APNGASM_COMPILE_TARGET}-${PLATFORM})

    include_directories(${VCPKG_INSTALLATION_ROOT}/installed/${VCPKG_TARGET_TRIPLET}/include)
    set(LIBZ_PATH ${VCPKG_INSTALLATION_ROOT}/installed/${VCPKG_TARGET_TRIPLET}/lib/${LIBZ_NAME}${CMAKE_STATIC_LIBRARY_SUFFIX})
    set(LIBPNG_PATH ${VCPKG_INSTALLATION_ROOT}/installed/${VCPKG_TARGET_TRIPLET}/lib/${LIBPNG_NAME}${CMAKE_STATIC_LIBRARY_SUFFIX})
    set(LIBAPNGASM_PATH ${VCPKG_INSTALLATION_ROOT}/installed/${VCPKG_TARGET_TRIPLET}/lib/${LIBAPNGASM_NAME}${CMAKE_STATIC_LIBRARY_SUFFIX})
else()
    set(LIBZ_PATH ${CMAKE_SOURCE_DIR}/fakeroot/lib/${LIBZ_NAME}${CMAKE_STATIC_LIBRARY_SUFFIX})
    set(LIBPNG_PATH ${CMAKE_SOURCE_DIR}/fakeroot/lib/${LIBPNG_NAME}${CMAKE_STATIC_LIBRARY_SUFFIX})
    set(LIBAPNGASM_PATH ${CMAKE_SOURCE_DIR}/fakeroot/lib/${LIBAPNGASM_NAME}${CMAKE_STATIC_LIBRARY_SUFFIX})
endif()

include_directories(${CMAKE_SOURCE_DIR}/fakeroot/include)
include_directories(${CMAKE_SOURCE_DIR}/fakeroot/include/listener)

set_target_properties(zlibstatic PROPERTIES IMPORTED_LOCATION ${LIBZ_PATH})
set_target_properties(png_static PROPERTIES IMPORTED_LOCATION ${LIBPNG_PATH})
set_target_properties(apngasm-static PROPERTIES IMPORTED_LOCATION ${LIBAPNGASM_PATH})

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