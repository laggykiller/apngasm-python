import platform
import os
import sys
import subprocess
import platform

conan_archs = {
    'x86_64': ['amd64', 'x86_64', 'x64'],
    'x86': ['i386', 'i686', 'x86'],
    'armv8': ['arm64', 'aarch64', 'aarch64_be', 'armv8b', 'armv8l'],
    'ppc64le': ['ppc64le', 'powerpc'],
    's390x': ['s390', 's390x']
}

def install_deps(arch=None):
    # Use Conan to install dependencies

    settings = []

    if platform.system() == 'Windows':
        settings.append('os=Windows')
    elif platform.system() == 'Darwin':
        settings.append('os=Macos')
        settings.append('compiler=apple-clang')
        settings.append('compiler.version=11.0')
        settings.append('compiler.libcxx=libc++')
    elif platform.system() == 'Linux':
        settings.append('os=Linux')

    if arch:
        settings.append(f'arch={arch}')

    build = []
    if os.path.isdir('/lib') and len([i for i in os.listdir('/lib') if i.startswith('libc.musl')]) != 0:
        # Need to compile dependencies if musllinux
        build.append('zlib*')
        build.append('libpng*')
        build.append('boost*')
    if not platform.machine().lower() in conan_archs['armv8'] + conan_archs['x86_64']:
        build.append('cmake*')
    if build == []:
        build.append('missing')
    
    subprocess.run(['conan', 'profile', 'detect'],
                    stdout = subprocess.DEVNULL,
                    stderr = subprocess.DEVNULL)

    conan_output = os.path.join('conan_output', arch)

    subprocess.run([
                    'conan', 'install', 
                    *[x for s in settings for x in ('-s', s)],
                    *[x for b in build for x in ('-b', b)], 
                    '-of', conan_output, '--deployer=full_deploy', '.'
                    ],
                    stdout = subprocess.DEVNULL,
                    stderr = subprocess.DEVNULL)

    return conan_output

arch = None
if os.getenv('APNGASM_COMPILE_TARGET') == 'universal2':
    arch = 'armv8'
elif os.getenv('APNGASM_COMPILE_TARGET'):
    arch = os.getenv('APNGASM_COMPILE_TARGET')
else:
    for k, v in conan_archs.items():
        if platform.machine().lower() in v:
            arch = k
            break

if arch == None:
    arch = platform.machine().lower()

conan_output = install_deps(arch)
if os.getenv('APNGASM_COMPILE_TARGET') == 'universal2':
    # Repeat to install the other architecture version of libwebp
    conan_output_x64 = install_deps('x86_64')
    conan_output_universal2 = 'conan_output/universal2'
    os.makedirs(conan_output_universal2, exist_ok=True)
    subprocess.run([
        'python3', 'lipo-dir-merge/lipo-dir-merge.py', 
        conan_output, conan_output_x64, conan_output_universal2
        ],
        stdout = subprocess.DEVNULL,
        stderr = subprocess.DEVNULL)

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


if os.getenv('APNGASM_COMPILE_TARGET'):
    sys.stdout.write(os.getenv('APNGASM_COMPILE_TARGET'))
else:
    sys.stdout.write(arch)