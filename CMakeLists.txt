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
    if (DEFINED ENV{MSVC_TOOLSET_VERSION})
        set(Boost_COMPILER "vc${MSVC_TOOLSET_VERSION}")
    endif()
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