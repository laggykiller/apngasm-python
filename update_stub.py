#!/usr/bin/env python3
import os
import shutil
import zipfile

def main():
    py_bin = shutil.which('python3')
    if not py_bin:
        py_bin = shutil.which('python')

    shutil.rmtree('./dist', ignore_errors=True)
    os.system(py_bin + ' -m build .')

    for zip_file in os.listdir('dist'):
        if os.path.splitext(zip_file)[1] != '.whl':
            continue
        zip_path = os.path.join('dist', zip_file)
        with zipfile.ZipFile(zip_path, mode="r") as archive:
            for file in archive.namelist():
                if os.path.splitext(file)[1] != '.pyi':
                    continue
                dest_path = os.path.join('src-python', file)
                dest_dir = os.path.split(dest_path)[0]
                if not os.path.isdir(dest_dir):
                    os.makedirs(dest_dir)
                with open(dest_path, 'wb+') as f:
                    f.write(archive.read(file))
    
    with open('src-python/apngasm_python/_apngasm_python/__init__.pyi') as f:
        init_pyi = f.read()
    
    with open('src-python/apngasm_python/_apngasm_python/__init__.pyi', 'w+') as f:
        f.write('from __future__ import annotations\n')
        f.write('import numpy.typing\n')
        f.write(init_pyi)

if __name__ == '__main__':
    main()