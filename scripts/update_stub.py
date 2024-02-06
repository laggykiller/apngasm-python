#!/usr/bin/env python3
import os
from pathlib import Path
import shutil
import zipfile


def main():
    py_bin = shutil.which("python3")
    if not py_bin:
        py_bin = shutil.which("python")
    if not py_bin:
        raise RuntimeError("Cannot find path for python")

    proj_dir = Path(Path(__file__).parent, "../").resolve()
    dist_dir = Path(proj_dir, "dist")

    shutil.rmtree(dist_dir, ignore_errors=True)
    os.chdir(proj_dir)
    os.system(py_bin + " -m build .")

    for zip_file in os.listdir(dist_dir):
        if os.path.splitext(zip_file)[1] != ".whl":
            continue
        zip_path = os.path.join(dist_dir, zip_file)
        with zipfile.ZipFile(zip_path, mode="r") as archive:
            for file in archive.namelist():
                if os.path.splitext(file)[1] != ".pyi":
                    continue
                dest_path = os.path.join("src-python", file)
                dest_dir = os.path.split(dest_path)[0]
                if not os.path.isdir(dest_dir):
                    os.makedirs(dest_dir)
                with open(dest_path, "wb+") as f:
                    f.write(archive.read(file))


if __name__ == "__main__":
    main()
