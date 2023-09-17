cmake_minimum_required(VERSION 3.17)
cmake_policy(SET CMP0074 NEW)

find_package(PythonInterp 3 REQUIRED)

set(GET_ARCH_CMD ${PYTHON_EXECUTABLE} "${CMAKE_SOURCE_DIR}/get_arch.py")
set(GET_DEPS_CMD ${PYTHON_EXECUTABLE} "${CMAKE_SOURCE_DIR}/get_deps.py")

message(STATUS "Executing get_arch.py")
execute_process(
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
    COMMAND ${GET_ARCH_CMD}
    OUTPUT_VARIABLE APNGASM_COMPILE_TARGET
)
message(STATUS "Finished get_arch.py")
message(STATUS "APNGASM_COMPILE_TARGET is ${APNGASM_COMPILE_TARGET}")

message(STATUS "Executing get_deps.py")
execute_process(
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
    COMMAND ${GET_DEPS_CMD}
)
message(STATUS "Finished get_deps.py")

if (WIN32)
    set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>")
    set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} /MT")
    set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} /MTd")
elseif (LINUX)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fPIC")
elseif (APPLE)
    if(${APNGASM_COMPILE_TARGET} STREQUAL "x86_64")
        set(CMAKE_OSX_DEPLOYMENT_TARGET "11.0")
    else()
        set(CMAKE_OSX_DEPLOYMENT_TARGET "10.15")
    endif()
endif()

set(ZLIB_USE_STATIC_LIBS ON)
set(PNG_USE_STATIC_LIBS ON)
set(Boost_USE_STATIC_LIBS ON)
if (WIN32)
    set(Boost_USE_MULTITHREADED ON)
    set(Boost_USE_STATIC_RUNTIME ON)
endif()

# Add conan packages
if ("${APNGASM_COMPILE_TARGET}" STREQUAL "universal2")
    # x86_64 Contians static libraries that are universal2
    set(CONAN_TOOLCHAIN ${CMAKE_SOURCE_DIR}/conan_output/x86_64/conan_toolchain.cmake)
else()
    set(CONAN_TOOLCHAIN ${CMAKE_SOURCE_DIR}/conan_output/${APNGASM_COMPILE_TARGET}/conan_toolchain.cmake)
endif()

if (EXISTS ${CONAN_TOOLCHAIN})
    include(${CONAN_TOOLCHAIN})
else()
    message(FATAL_ERROR "The conan_toolchain file could not be found: ${CONAN_TOOLCHAIN}")
endif()

project(apngasm-python VERSION 1.0.9)
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
add_subdirectory(apngasm)
set_target_properties(apngasm-static PROPERTIES BUILD_SHARED_LIBS OFF)

include_directories(${CMAKE_BINARY_DIR}/apngasm/lib/src)
include_directories(${CMAKE_SOURCE_DIR}/apngasm/lib/src)
include_directories(${CMAKE_SOURCE_DIR}/apngasm/lib/src/listener)

target_link_libraries(_apngasm_python PRIVATE apngasm-static)
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