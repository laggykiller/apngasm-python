#!/usr/bin/env python3
from apngasm_python.apngasm import APNGAsm, APNGFrame, create_frame_from_rgb, create_frame_from_rgba
import os
import shutil
from PIL import Image
import numpy as np

def frame_info(frame):
    print(f'{frame.pixels = }')
    print(f'{frame.width = }')
    print(f'{frame.height = }')
    print(f'{frame.color_type = }')
    print(f'{frame.palette = }')
    print(f'{frame.transparency = }')
    print(f'{frame.palette_size = }')
    print(f'{frame.transparency_size = }')
    print(f'{frame.delay_num = }')
    print(f'{frame.delay_den = }')

# https://www.w3.org/TR/PNG-Chunks.html
color_type_dict = {
    0: 'L',
    2: 'RGB',
    3: 'P',
    4: 'LA',
    6: 'RGBA'
}

color_type_dict = color_type_dict | dict((v, k) for k, v in color_type_dict.items())

# # Cleanup
shutil.rmtree('output', ignore_errors=True)
os.mkdir('output')

# Initialize
apngasm = APNGAsm()

# Get libapngasm version
print(f'{apngasm.version() = }')

# Load png from one directory
for file_name in sorted(os.listdir('frames')):
    apngasm.add_frame_from_file(os.path.join('frames', file_name), 100, 1000)

# Getting information about one frame
frame = apngasm.get_frames()[0]
frame_info(frame)

# Saving one frame as file
frame.save('output/elephant-frame.png')

# Getting one frame as Pillow Image
mode = color_type_dict[frame.color_type]
im = Image.frombytes(mode, (frame.width, frame.height), frame.pixels)
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

# Load apng for disassemble
frames = apngasm.disassemble('input/ball.apng')
print(f'{len(frames) = }')
frame = frames[0]
frame_info(frame)
apngasm.save_pngs('output')

# Assemble from pillow images
# Just for fun, let's also make it spin
apngasm.reset()
angle = 0
angle_step = 360 / len(os.listdir('frames'))
for file_name in sorted(os.listdir('frames')):
    image = Image.open(os.path.join('frames', file_name))
    image = image.rotate(angle)
    frame = create_frame_from_rgba(np.array(image).flatten(), image.width, image.height)
    apngasm.add_frame(frame)
    
    angle += angle_step

success = apngasm.assemble('output/elephant-spinning-pillow.apng')
print(f'{success = }')

# Assemble palette and grey PNGs
apngasm.reset()
apngasm.add_frame_from_file('input/palette.png', 100, 1000)
apngasm.add_frame_from_file('input/grey.png', 100, 1000)

frame0 = apngasm.get_frames()[0]
frame_info(frame0)

frame1 = apngasm.get_frames()[1]
frame_info(frame1)

success = apngasm.assemble('output/birds.apng')
print(f'{success = }')

del apngasm

# Assemble palette and grey PNGs, but with Pillow
image0 = Image.open('input/grey.png').convert('RGBA')
frame0 = create_frame_from_rgba(np.array(image0).flatten(), image0.width, image0.height)
frame_info(frame0)

# You may even set the variables manually
image1 = Image.open('input/palette.png').convert('RGBA')
frame1 = APNGFrame()
frame1.delay_num = 100
frame1.delay_den = 1000
frame1.color_type = color_type_dict[image1.mode]
frame1.width = image1.width
frame1.height = image1.height
frame1.pixels = np.array(image1).flatten()
frame_info(frame1)

# # Another way of creating APNGAsm object
apngasm = APNGAsm([frame0, frame1])

success = apngasm.assemble('output/birds-pillow.apng')
print(f'{success = }')