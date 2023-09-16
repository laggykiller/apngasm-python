# apngasm-python

A nanobind API for [apngasm](https://github.com/apngasm/apngasm), a tool/library for APNG assembly/disassembly.

apngasm is originally a CLI program for quickly assembling PNG images into animated PNG (APNG). It also supports creating compressed APNG.

apngasm-python is a binding for apngasm using nanobind, allowing you to use apngasm without calling it using commands.

With this module, you can even create APNG using images inside memory (No need to write them out as file and call apngasm! This is about 2 times faster from testing.)

A similar python module is https://github.com/eight04/pyAPNG , which handles APNG files with python natively and does not support compression.

For convenience, prebuilt library is packaged with this module, so you need not download apngasm.

Documentations: https://apngasm-python.readthedocs.io/en/latest/

## Install
```
pip install apngasm-python
```

## Example usage
The recommended usage is to `from apngasm_python import APNGAsmBinder`, see [example/example_binder.py](example/example_binder.py)
```python
from apngasm_python import APNGAsmBinder
import numpy as np
from PIL import Image
import os

apngasm = APNGAsmBinder()

# From file
for file_name in sorted(os.listdir('frames')):
    # To adjust frame duration, set delay_num and delay_den
    # The frame duration will be (delay_num / delay_den) seconds
    apngasm.add_frame_from_file(file_path=os.path.join('frames', file_name), delay_num=100, delay_den=1000)
    
# Default value of loops is 0, which is infinite looping of APNG animation
# This sets the APNG animation to loop for 3 times before stopping
apngasm.set_loops(3)
apng.assemble('result-from-file.apng')
apngasm.reset()

# From Pillow
for file_name in sorted(os.listdir('frames')):
    image = Image.open(os.path.join('frames', file_name)).convert('RGBA')
    frame = apngasm.add_frame_from_pillow(image, delay_num=50, delay_den=1000)
apngasm.assemble('result-from-pillow.apng')
apngasm.reset()

# Disassemble and get pillow image of one frame
# You can use with statement to avoid calling reset()
with APNGAsmBinder() as apng:
    frames = apng.disassemble_as_pillow('input/ball.apng')
    frame = frames[0]
    frame.save('output/ball0.png')

# Disassemble all APNG into PNGs
apngasm.save_pngs('output')
```

Alternatively, you can reduce overhead and do advanced tasks by calling methods directly, see [example/example_direct.py](example/example_direct.py)
```python
from apngasm_python.apngasm import APNGAsm, APNGFrame, create_frame_from_rgb, create_frame_from_rgba
import numpy as np
from PIL import Image
import os

apngasm = APNGAsm()

# From file
for file_name in sorted(os.listdir('frames')):
    # To adjust frame duration, set delay_num and delay_den
    # The frame duration will be (delay_num / delay_den) seconds
    apngasm.add_frame_from_file(file_path=os.path.join('frames', file_name), delay_num=100, delay_den=1000)
    
# Default value of loops is 0, which is infinite looping of APNG animation
# This sets the APNG animation to loop for 3 times before stopping
apngasm.set_loops(3)
apng.assemble('result-from-file.apng')

# From Pillow
apngasm.reset()
for file_name in sorted(os.listdir('frames')):
    image = Image.open(os.path.join('frames', file_name)).convert('RGBA')
    frame = create_frame_from_rgba(np.array(image).flatten(), image.width, image.height)
    frame.delay_num = 50
    frame.delay_den = 1000
    apngasm.add_frame(frame)
apngasm.assemble('result-from-pillow.apng')

# Disassemble and get pillow image of one frame
apngasm.reset()
frames = apngasm.disassemble('input/ball.apng')
frame = frames[0]
im = Image.frombytes(mode, (frame.width, frame.height), frame.pixels)
im.save('output/ball0.png')

# Disassemble all APNG into PNGs
apngasm.save_pngs('output')
```

The methods are based on [apngasm.h](https://github.com/apngasm/apngasm/blob/master/lib/src/apngasm.h) and [apngframe.h](https://github.com/apngasm/apngasm/blob/master/lib/src/apngframe.h)

You can get more info about the binding from [src/apngasm_python.cpp](src/apngasm_python.cpp), or by...

```python
from apngasm_python import _apngasm_python
help(_apngasm_python)
```

## Building from source
```bash
git clone https://github.com/laggykiller/apngasm-python.git
cd apngasm-python
git submodule update --init --recursive

# To build wheel
python3 -m build .

# To install directly
pip3 install .
```

To cross-compile, please set environment variables:
```bash
# Choose only one

# On Windows (cmd, not PowerShell)
set APNGASM_COMPILE_TARGET=x86_64
set APNGASM_COMPILE_TARGET=x86
set APNGASM_COMPILE_TARGET=armv8

# On *nix
export APNGASM_COMPILE_TARGET=x64
export APNGASM_COMPILE_TARGET=x86
export APNGASM_COMPILE_TARGET=armv8
export APNGASM_COMPILE_TARGET=ppc64le
export APNGASM_COMPILE_TARGET=s390x
```

## Credits
- apngasm: https://github.com/apngasm/apngasm
- Packaging: https://github.com/tttapa/py-build-cmake
- Example files:
    - https://apng.onevcat.com/demo/
    - https://commons.wikimedia.org/wiki/File:Animated_PNG_example_bouncing_beach_ball.png
    - https://commons.wikimedia.org/wiki/File:Grayscale_8bits_palette_sample_image.png
    - https://commons.wikimedia.org/wiki/File:RG_16bits_palette_sample_image.png
