#!/usr/bin/env python3
from apngasm_python import APNGAsmBinder
import os
import shutil
from PIL import Image

# Cleanup
shutil.rmtree('output', ignore_errors=True)
os.mkdir('output')

# Initialize
apngasm = APNGAsmBinder()

# Get libapngasm version
print(f'{apngasm.version() = }')

# Load png from one directory
for file_name in sorted(os.listdir('frames')):
    apngasm.add_frame_from_file(os.path.join('frames', file_name), 100, 1000)

# Getting information about one frame
frame = apngasm.get_frames()[0]

# Saving one frame as file
frame.save('output/elephant-frame.png')

# Getting one frame as Pillow Image
im = apngasm.frame_pixels_as_pillow(0)
im.save('output/elephant-frame-pillow.png')

# Get inforamtion about whole animation
print(f'{apngasm.get_loops() = }')
print(f'{apngasm.is_skip_first() = }')
print(f'{apngasm.frame_count() = }')

# Assemble
success = apngasm.assemble('output/elephant.apng')
print(f'{success = }')

# Clear images loaded in apngasm object
apngasm.reset()

# Disassemble and get pillow image of one frame
frames = apngasm.disassemble_as_pillow('input/ball.apng')
frame = frames[0]
frame.save('output/ball0.png')

# Disassemble all APNG into PNGs
apngasm.save_pngs('output')

# Assemble from pillow images
# Just for fun, let's also make it spin
apngasm.reset()
angle = 0
angle_step = 360 / len(os.listdir('frames'))
for file_name in sorted(os.listdir('frames')):
    image = Image.open(os.path.join('frames', file_name))
    image = image.rotate(angle)
    apngasm.add_frame_from_pillow(image)
    
    angle += angle_step

success = apngasm.assemble('output/elephant-spinning-pillow.apng')
print(f'{success = }')
apngasm.reset()

# Assemble palette and grey PNGs
# You can use with statement to avoid calling reset()
with APNGAsmBinder() as apng:
    apng.add_frame_from_file('input/palette.png')
    apng.add_frame_from_file('input/grey.png')
    success = apng.assemble('output/birds.apng')
    print(f'{success = }')

# Assemble palette and grey PNGs, but with Pillow
image0 = Image.open('input/grey.png')
frame0 = apngasm.add_frame_from_pillow(image0)
image1 = Image.open('input/palette.png')
apngasm.add_frame_from_pillow(image1)

success = apngasm.assemble('output/birds-pillow.apng')
print(f'{success = }')