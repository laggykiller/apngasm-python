#!/usr/bin/env python3
import sys
import os
import platform

conan_archs = {
    'x86_64': ['amd64', 'x86_64', 'x64'],
    'x86': ['i386', 'i686', 'x86'],
    'armv8': ['arm64', 'aarch64', 'aarch64_be', 'armv8b', 'armv8l'],
    'ppc64le': ['ppc64le', 'powerpc'],
    's390x': ['s390', 's390x']
}

def get_arch():
    arch = None
    if os.getenv('APNGASM_COMPILE_TARGET'):
        arch = os.getenv('APNGASM_COMPILE_TARGET')
    else:
        for k, v in conan_archs.items():
            if platform.machine().lower() in v:
                arch = k
                break

    if arch == None:
        arch = platform.machine().lower()
    
    return arch

def main():
    arch = get_arch()
    if os.getenv('APNGASM_COMPILE_TARGET'):
        sys.stdout.write(os.getenv('APNGASM_COMPILE_TARGET'))
    else:
        sys.stdout.write(arch)

if __name__ == '__main__':
    main()