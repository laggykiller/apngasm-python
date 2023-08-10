cmake_minimum_required(VERSION 3.17)
cmake_policy(SET CMP0074 NEW)

# Set static linking
set(ZLIB_USE_STATIC_LIBS ON)
set(Boost_USE_STATIC_LIBS ON)
set(BUILD_SHARED_LIBS OFF)
if (WIN32)
    set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>")
    set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} /MT")
    set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} /MTd")
    set(Boost_COMPILER "vc${MSVC_TOOLSET_VERSION}")
elseif (LINUX)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fPIC")
endif()

if (DEFINED VCPKG_INSTALLATION_ROOT)
    if (NOT DEFINED APNGASM_COMPILE_TARGET)
        set(APNGASM_COMPILE_TARGET x64)
    endif()
    if (WIN32)
        set(PLATFORM windows-static)
    elseif (APPLE)
        set(PLATFORM osx-release)
    else()
        set(PLATFORM linux-release)
    endif()
    set(VCPKG_TARGET_TRIPLET ${APNGASM_COMPILE_TARGET}-${PLATFORM})
    set(ZLIB_ROOT ${VCPKG_INSTALLATION_ROOT}/packages/zlib_${VCPKG_TARGET_TRIPLET})
    set(PNG_ROOT ${VCPKG_INSTALLATION_ROOT}/packages/libpng_${VCPKG_TARGET_TRIPLET})
    set(CMAKE_TOOLCHAIN_FILE "${VCPKG_INSTALLATION_ROOT}/scripts/buildsystems/vcpkg.cmake"
    CACHE STRING "Vcpkg toolchain file")
else()
    # Set dependencies root
    if (NOT ZLIB_ROOT)
        set(ZLIB_ROOT ${CMAKE_SOURCE_DIR}/zlib)
    endif()
    if (NOT PNG_ROOT)
        set(PNG_ROOT ${CMAKE_SOURCE_DIR}/libpng)
    endif()
    if (NOT BOOST_ROOT)
        set(BOOST_ROOT ${CMAKE_SOURCE_DIR}/boost)
    endif()
endif()

project(apngasm-python)



# Prepare dependencies
if (WIN32)
    set(PREPARE_CMD "${CMAKE_SOURCE_DIR}/prepare-win.bat")
elseif (APPLE)
    set(PREPARE_CMD "${CMAKE_SOURCE_DIR}/prepare-mac.sh")
else()
    set(PREPARE_CMD "${CMAKE_SOURCE_DIR}/prepare-linux.sh")
endif()

execute_process(
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
    COMMAND ${PREPARE_CMD}
)

add_subdirectory(apngasm)

# Install the module
if (WIN32)
    install(TARGETS apngasm
            EXCLUDE_FROM_ALL
            RUNTIME DESTINATION ${PY_BUILD_CMAKE_MODULE_NAME}
            COMPONENT python_module)
else()
    install(TARGETS apngasm
            EXCLUDE_FROM_ALL
            LIBRARY DESTINATION ${PY_BUILD_CMAKE_MODULE_NAME}
            COMPONENT python_module)
endif()