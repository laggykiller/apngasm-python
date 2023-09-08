# Examples

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