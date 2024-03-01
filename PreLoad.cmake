# https://stackoverflow.com/a/45247784
# Need python headers and libraries, but msvc not able to find them
# If inside cygwin or msys.

if (WIN32 AND NOT MSVC)
    set (CMAKE_GENERATOR "Unix Makefiles" CACHE INTERNAL "" FORCE)
endif()