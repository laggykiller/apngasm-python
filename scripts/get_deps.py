#!/usr/bin/env python3
import platform
import os
import subprocess
import shutil

from get_arch import conan_archs, get_arch


def install_deps(arch: str):
    # Use Conan to install dependencies
    settings: list[str] = []
    build: list[str] = []
    options: list[str] = []

    if platform.system() == "Windows":
        settings.append("os=Windows")
        settings.append("compiler.runtime=static")
    elif platform.system() == "Darwin":
        settings.append("os=Macos")
        if arch == "armv8":
            settings.append("os.version=11.0")
        else:
            settings.append("os.version=10.15")
        settings.append("compiler=apple-clang")
        settings.append("compiler.libcxx=libc++")
    elif platform.system() == "Linux":
        settings.append("os=Linux")
        settings.append("compiler=gcc")
        settings.append("compiler.version=10")
        settings.append("compiler.libcxx=libstdc++")
    if arch:
        settings.append("arch=" + arch)

    options.append("boost/*:without_atomic=True")
    options.append("boost/*:without_chrono=True")
    options.append("boost/*:without_cobalt=True")
    options.append("boost/*:without_container=True")
    options.append("boost/*:without_context=True")
    options.append("boost/*:without_contract=True")
    options.append("boost/*:without_coroutine=True")
    options.append("boost/*:without_date_time=True")
    options.append("boost/*:without_exception=True")
    options.append("boost/*:without_fiber=True")
    options.append("boost/*:without_filesystem=True")
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


def main():
    arch = get_arch()

    if arch != "universal2":
        install_deps(arch)
    else:
        # Repeat to install the other architecture version of libwebp
        conan_output_x64 = install_deps("x86_64")
        conan_output_arm = install_deps("armv8")
        conan_output_universal2 = conan_output_arm.replace("armv8", "universal2")
        shutil.rmtree(conan_output_universal2, ignore_errors=True)
        subprocess.run(
            [
                "python3",
                "lipo-dir-merge/lipo-dir-merge.py",
                conan_output_x64,
                conan_output_arm,
                conan_output_universal2,
            ]
        )

        shutil.rmtree(conan_output_x64)
        shutil.move(conan_output_universal2, conan_output_x64)


if __name__ == "__main__":
    main()
