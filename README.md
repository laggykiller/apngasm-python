# apngasm-python

A nanobind API for [apngasm](https://github.com/apngasm/apngasm), a tool/library for APNG assembly/disassembly.

apngasm is originally a CLI program for quickly assembling PNG images into animated PNG (APNG). It also supports creating compressed APNG.

apngasm-python is a binding for apngasm using nanobind, allowing you to use apngasm without calling it using commands.

With this module, you can even create APNG using images inside memory (No need to write them out as file and call apngasm!)

A similar python module is https://github.com/eight04/pyAPNG , which handles APNG files with python natively and does not support compression.

For convenience, prebuilt library is packaged with this module, so you need not download apngasm.

## Example usage
For more examples, see [example/example.py](example/example.py)
```
from apngasm_python.apngasm import APNGAsm, APNGFrame, create_frame_from_rgb, create_frame_from_rgba
import os

# From file
for file_name in sorted(os.listdir('frames')):
    apngasm.add_frame_from_file(os.path.join('frames', file_name), 100, 1000)
apng.assemble('result-from-file.apng')

# From Pillow
apngasm.reset()
for file_name in sorted(os.listdir('frames')):
    image = Image.open(os.path.join('frames', file_name)).convert('RGBA')
    frame = create_frame_from_rgba(np.array(image).flatten(), image.width, image.height)
    apngasm.add_frame(frame)
apng.assemble('result-from-pillow.apng')
```

## Building from source
### Method 1: Without vcpkg
Simply run:
```
git clone https://github.com/laggykiller/apngasm-python.git
cd apngasm-python
git submodule update --init --recursive

# To build wheel
python3 -m build .

# To install directly
pip3 install .
```

- Note that you will need CMake.
- If on Windows, you will need Visual Studio installed
- Cross-compilation not supported using this method

### Method 2: With vcpkg
1. Install vcpkg: https://github.com/microsoft/vcpkg
2. Set environment variable that points to the path of vcpkg root
```
# On Windows (cmd, not PowerShell)
set VCPKG_INSTALLATION_ROOT=C:/path/to/vcpkg

# On *nix
export VCPKG_INSTALLATION_ROOT=/path/to/vcpkg
```

3. Building
```
git clone https://github.com/laggykiller/apngasm-python.git
cd apngasm-python
# --recursive flag not necessary here
git submodule update --init

# To build wheel
python3 -m build .

# To install directly
pip3 install .
```

Note that this method also support cross-compilation,
to do so you will need to set environment variables beforehand:
```
# Choose only one

# On Windows (cmd, not PowerShell)
set APNGASM_COMPILE_TARGET=x64
set APNGASM_COMPILE_TARGET=x86
set APNGASM_COMPILE_TARGET=arm64
set APNGASM_COMPILE_TARGET=arm

# On MacOS
export APNGASM_COMPILE_TARGET=x64
export APNGASM_COMPILE_TARGET=x86
export APNGASM_COMPILE_TARGET=arm64

# On *nix
export APNGASM_COMPILE_TARGET=x64
export APNGASM_COMPILE_TARGET=x86
export APNGASM_COMPILE_TARGET=arm64
```

## Credits
- apngasm: https://github.com/apngasm/apngasm
- Packaging: https://github.com/tttapa/py-build-cmake
- Example files:
    - https://apng.onevcat.com/demo/
    - https://commons.wikimedia.org/wiki/File:Animated_PNG_example_bouncing_beach_ball.png
    - https://commons.wikimedia.org/wiki/File:Grayscale_8bits_palette_sample_image.png
    - https://commons.wikimedia.org/wiki/File:RG_16bits_palette_sample_image.png