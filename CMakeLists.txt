cmake_minimum_required(VERSION 3.17)
project(apngasm-python)

include_directories(zlib)
include_directories(libpng)

add_subdirectory(zlib)
add_subdirectory(libpng)
add_subdirectory(apngasm)

# Install the module
if (WIN32)
    install(TARGETS zlib png_shared apngasm
            EXCLUDE_FROM_ALL
            RUNTIME DESTINATION ${PY_BUILD_CMAKE_MODULE_NAME}
            COMPONENT python_module)
else()
    install(TARGETS zlib png_shared apngasm-dynamic
            EXCLUDE_FROM_ALL
            LIBRARY DESTINATION ${PY_BUILD_CMAKE_MODULE_NAME}
            COMPONENT python_module)
endif()