# https://stackoverflow.com/a/45247784
# Need python headers and libraries, but msvc not able to find them
# If inside cygwin or msys.

if (WIN32 AND NOT MSVC)
    execute_process(COMMAND uname OUTPUT_VARIABLE uname)
    if (uname MATCHES "^MINGW")
        set (CMAKE_GENERATOR "MinGW Makefiles" CACHE INTERNAL "" FORCE)
    elseif (uname MATCHES "^MSYS")
        set (CMAKE_GENERATOR "MSYS Makefiles" CACHE INTERNAL "" FORCE)
    else ()
        set (CMAKE_GENERATOR "Ninja" CACHE INTERNAL "" FORCE)
    endif()
endif()