#!/usr/bin/env python3
import platform
import os
import subprocess
import platform
import shutil
from get_arch import conan_archs, get_arch

def install_deps(arch=None):
    # Use Conan to install dependencies
    settings = []

    if platform.system() == 'Windows':
        settings.append('os=Windows')
    elif platform.system() == 'Darwin':
        settings.append('os=Macos')
        settings.append('compiler=apple-clang')
        # if arch == 'armv8':s
        settings.append('compiler.version=11.0')
        # else:
        #     settings.append('compiler.version=10.15')
        settings.append('compiler.libcxx=libc++')
    elif platform.system() == 'Linux':
        settings.append('os=Linux')
        settings.append('compiler=gcc')
        settings.append('compiler.version=10')
    if arch:
        settings.append(f'arch={arch}')

    build = ['missing']
    if os.path.isdir('/lib') and len([i for i in os.listdir('/lib') if i.startswith('libc.musl')]) != 0:
        # Need to compile dependencies if musllinux
        build.append('zlib*')
        build.append('libpng*')
        build.append('boost*')
    if platform.architecture()[0] == '32bit' or platform.machine().lower() not in (conan_archs['armv8'] + conan_archs['x86']):
        build.append('cmake*')
    
    subprocess.run(['conan', 'profile', 'detect'])

    conan_output = os.path.join('conan_output', arch)

    subprocess.run([
                    'conan', 'install', 
                    *[x for s in settings for x in ('-s', s)],
                    *[x for b in build for x in ('-b', b)], 
                    '-of', conan_output, '--deployer=full_deploy', '.'
                    ])
    
    return conan_output

def main():
    arch = get_arch()
    conan_output = install_deps(arch)

    if os.getenv('APNGASM_COMPILE_TARGET') == 'universal2':
        # Repeat to install the other architecture version of libwebp
        conan_output_x64 = install_deps('x86_64')
        conan_output_universal2 = 'conan_output/universal2'
        shutil.rmtree(conan_output_universal2, ignore_errors=True)
        os.makedirs(conan_output_universal2)
        subprocess.run([
                        'python3', 'lipo-dir-merge/lipo-dir-merge.py', 
                        conan_output, conan_output_x64, conan_output_universal2
                        ])

        with open(os.path.join(conan_output_universal2, 'CMakePresets.json')) as f:
            cmake_presets = f.read()
        cmake_presets = cmake_presets.replace('armv8', 'universal2')
        with open(os.path.join(conan_output_universal2, 'CMakePresets.json'), 'w+') as f:
            f.write(cmake_presets)

        with open(os.path.join(conan_output_universal2, 'conan_toolchain.cmake')) as f:
            conan_toolchain = f.read()
        conan_toolchain = conan_toolchain.replace('armv8', 'universal2')
        with open(os.path.join(conan_output_universal2, 'conan_toolchain.cmake'), 'w+') as f:
            f.write(conan_toolchain)

if __name__ == '__main__':
    main()