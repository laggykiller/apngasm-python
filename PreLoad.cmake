# https://stackoverflow.com/a/45247784
# Need python headers and libraries, but msvc not able to find them
# If inside cygwin or msys.

# Use this for MinGW
# set (CMAKE_GENERATOR "MinGW Makefiles" CACHE INTERNAL "" FORCE)

# Use this for MSYS
# set (CMAKE_GENERATOR "MSYS Makefiles" CACHE INTERNAL "" FORCE)

# Use this otherwise
set (CMAKE_GENERATOR "Ninja" CACHE INTERNAL "" FORCE)