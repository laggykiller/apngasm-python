#!/usr/bin/env python3
import os
import platform
import shutil
import subprocess
import sys

from get_arch import conan_archs, get_arch  # type: ignore


def install_deps(arch: str):
    # Use Conan to install dependencies
    settings: list[str] = []
    build: list[str] = []
    options: list[str] = []

    if platform.system() == "Windows":
        settings.append("os=Windows")
        if sys.platform.startswith(("cygwin", "msys")):
            # Need python headers and libraries, but msvc not able to find them
            # If inside cygwin or msys.
            settings.append("compiler=gcc")
            settings.append("compiler.version=10")
            settings.append("compiler.libcxx=libstdc++")
        else:
            settings.append("compiler.runtime=static")
    elif platform.system() == "Darwin":
        settings.append("os=Macos")
        if arch == "armv8":
            settings.append("os.version=11.0")
        else:
            settings.append("os.version=10.9")
        settings.append("compiler=apple-clang")
        settings.append("compiler.libcxx=libc++")
    elif platform.system() == "Linux":
        settings.append("os=Linux")
        settings.append("compiler=gcc")
        settings.append("compiler.version=10")
        settings.append("compiler.libcxx=libstdc++")
    if arch:
        settings.append("arch=" + arch)

    options.append("boost/*:without_atomic=False")  # Depedency for filesystem
    options.append("boost/*:without_chrono=True")
    options.append("boost/*:without_cobalt=True")
    options.append("boost/*:without_container=True")
    options.append("boost/*:without_context=True")
    options.append("boost/*:without_contract=True")
    options.append("boost/*:without_coroutine=True")
    options.append("boost/*:without_date_time=True")
    options.append("boost/*:without_exception=True")
    options.append("boost/*:without_fiber=True")
    options.append("boost/*:without_filesystem=False")  # Required by osx 10.9 fork
    options.append("boost/*:without_graph=True")
    options.append("boost/*:without_graph_parallel=True")
    options.append("boost/*:without_iostreams=True")
    options.append("boost/*:without_json=True")
    options.append("boost/*:without_locale=True")
    options.append("boost/*:without_log=True")
    options.append("boost/*:without_math=True")
    options.append("boost/*:without_mpi=True")
    options.append("boost/*:without_nowide=True")
    options.append("boost/*:without_program_options=False")
    options.append("boost/*:without_python=True")
    options.append("boost/*:without_random=True")
    options.append("boost/*:without_regex=False")
    options.append("boost/*:without_serialization=True")
    options.append("boost/*:without_stacktrace=True")
    options.append("boost/*:without_system=False")
    options.append("boost/*:without_test=True")
    options.append("boost/*:without_thread=True")
    options.append("boost/*:without_timer=True")
    options.append("boost/*:without_type_erasure=True")
    options.append("boost/*:without_url=True")
    options.append("boost/*:without_wave=True")

    if platform.system() == "Linux":
        # Need to compile dependencies if Linux
        build.append("*")
    elif not shutil.which("cmake") and (
        platform.architecture()[0] == "32bit"
        or platform.machine().lower() not in (conan_archs["armv8"] + conan_archs["x86"])
    ):
        build.append("cmake*")

    if build == []:
        build.append("missing")

    print("conan cli settings:")
    print("settings: " + str(settings))
    print("build: " + str(build))
    print("options: " + str(options))

    subprocess.run(["conan", "profile", "detect", "-f"])

    conan_output = os.path.join("conan_output", arch)

    subprocess.run(
        [
            "conan",
            "install",
            *[x for s in settings for x in ("-s", s)],
            *[x for b in build for x in ("-b", b)],
            *[x for o in options for x in ("-o", o)],
            "-of",
            conan_output,
            "--deployer=direct_deploy",
            ".",
        ]
    )

    return conan_output


def patch_conan_toolchain_universal2(lipo_dir_merge_src: str):
    conan_toolchain_path = os.path.join(lipo_dir_merge_src, "conan_toolchain.cmake")

    result = ""
    with open(conan_toolchain_path) as f:
        for line in f:
            if line.startswith("set(CMAKE_OSX_ARCHITECTURES"):
                result += "# " + line
            else:
                result += line

    with open(conan_toolchain_path, "w+") as f:
        f.write(result)


def main():
    arch = get_arch()

    if not arch.startswith("universal2"):
        install_deps(arch)
    else:
        # Repeat to install the other architecture version of libwebp
        conan_output_x64 = install_deps("x86_64")
        conan_output_arm = install_deps("armv8")

        if arch.endswith("x86_64"):
            lipo_dir_merge_src = conan_output_x64
            lipo_dir_merge_dst = conan_output_arm
        elif arch.endswith("armv8"):
            lipo_dir_merge_src = conan_output_arm
            lipo_dir_merge_dst = conan_output_x64
        else:
            raise RuntimeError("Invalid arch: " + arch)

        lipo_dir_merge_result = conan_output_arm.replace("armv8", "universal2")
        shutil.rmtree(lipo_dir_merge_result, ignore_errors=True)

        subprocess.run(
            [
                "python3",
                "lipo-dir-merge/lipo-dir-merge.py",
                lipo_dir_merge_src,
                lipo_dir_merge_dst,
                lipo_dir_merge_result,
            ]
        )

        shutil.rmtree(lipo_dir_merge_src)
        shutil.move(lipo_dir_merge_result, lipo_dir_merge_src)

        patch_conan_toolchain_universal2(lipo_dir_merge_src)


if __name__ == "__main__":
    main()
