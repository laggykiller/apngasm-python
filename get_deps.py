#!/usr/bin/env python3
import platform
import os
import subprocess
import platform
import shutil
from get_arch import conan_archs, get_arch

def install_deps(arch):
    # Use Conan to install dependencies
    settings = []

    if platform.system() == 'Windows':
        settings.append('os=Windows')
    elif platform.system() == 'Darwin':
        settings.append('os=Macos')
        if arch == 'x86_64':
            settings.append('os.version=10.15')
        else:
            settings.append('os.version=11.0')
        settings.append('compiler=apple-clang')
        settings.append('compiler.libcxx=libc++')
    elif platform.system() == 'Linux':
        settings.append('os=Linux')
        settings.append('compiler=gcc')
        settings.append('compiler.version=10')
        settings.append('compiler.libcxx=libstdc++')
    if arch:
        settings.append('arch=' + arch)

    build = []
    if platform.system() == 'Linux':
        # Need to compile dependencies if Linux
        build.append('*')
    elif (not shutil.which('cmake') and 
        (platform.architecture()[0] == '32bit' or 
        platform.machine().lower() not in (conan_archs['armv8'] + conan_archs['x86']))):
        build.append('cmake*')
    
    if build == []:
        build.append('missing')
    
    print('conan cli settings:')
    print('settings: ' + str(settings))
    print('build: ' + str(build))
    
    subprocess.run(['conan', 'profile', 'detect'])

    conan_output = os.path.join('conan_output', arch)

    subprocess.run([
                    'conan', 'install', 
                    *[x for s in settings for x in ('-s', s)],
                    *[x for b in build for x in ('-b', b)], 
                    '-of', conan_output, '--deployer=direct_deploy', '.'
                    ])
    
    return conan_output

def main():
    arch = get_arch()
    if arch == 'universal2':
        conan_output = 'conan_output/x86_64'
    else:
        conan_output = 'conan_output/' + arch
    if os.path.isdir(conan_output):
        print('Dependencies found at:' + conan_output)
        print('Skip conan install...')
        return

    if arch != 'universal2':
        conan_output = install_deps(arch)
    else:
        # Repeat to install the other architecture version of libwebp
        conan_output_x64 = install_deps('x86_64')
        conan_output_arm = install_deps('armv8')
        conan_output_universal2 = conan_output_arm.replace('armv8', 'universal2')
        shutil.rmtree(conan_output_universal2, ignore_errors=True)
        subprocess.run([
                        'python3', 'lipo-dir-merge/lipo-dir-merge.py', 
                        conan_output_x64, conan_output_arm, conan_output_universal2
                        ])

        shutil.rmtree(conan_output_x64)
        shutil.move(conan_output_universal2, conan_output_x64)

if __name__ == '__main__':
    main()