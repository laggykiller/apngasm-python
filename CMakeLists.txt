cmake_minimum_required(VERSION 3.17)
cmake_policy(SET CMP0074 NEW)

project(apngasm-python)

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

# Set static linking
set(ZLIB_USE_STATIC_LIBS ON)
set(Boost_USE_STATIC_LIBS ON)
set(BUILD_SHARED_LIBS OFF)
if (WIN32)
    set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>")
    set(Boost_COMPILER "vc${MSVC_TOOLSET_VERSION}")
elseif (LINUX)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fPIC")
endif()

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
    install(TARGETS apngasm-dynamic
            EXCLUDE_FROM_ALL
            LIBRARY DESTINATION ${PY_BUILD_CMAKE_MODULE_NAME}
            COMPONENT python_module)
endif()