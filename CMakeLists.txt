cmake_minimum_required(VERSION 3.17)
project(apngasm-python)

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