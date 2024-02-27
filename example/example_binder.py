#!/usr/bin/env python3
from apngasm_python.apngasm import APNGAsmBinder
import os
import shutil
from PIL import Image
import numpy as np

file_dir = os.path.split(__file__)[0]
samples_dir = os.path.join(file_dir, "../samples")
frames_dir = os.path.join(samples_dir, "frames")
input_dir = os.path.join(samples_dir, "input")
output_dir = os.path.join(samples_dir, "output")
ball_apng_path = os.path.join(input_dir, "ball.apng")
grey_png_path = os.path.join(input_dir, "grey.png")
palette_png_path = os.path.join(input_dir, "palette.png")

# Cleanup
shutil.rmtree(output_dir, ignore_errors=True)
os.mkdir(output_dir)

# Initialize
apngasm = APNGAsmBinder()

# Get libapngasm version
print(f"{apngasm.version() = }")

# Load png from one directory
for file_name in sorted(os.listdir(frames_dir)):
    apngasm.add_frame_from_file(os.path.join(frames_dir, file_name), 100, 1000)

# Getting information about one frame
frame = apngasm.get_frames()[0]

# Saving one frame as file
out = os.path.join(output_dir, "elephant-frame.png")
frame.save(out)

# Getting one frame as Pillow Image
im = apngasm.frame_pixels_as_pillow(0)
out = os.path.join(output_dir, "elephant-frame-pillow.png")
im.save(out) # type: ignore

# Get inforamtion about whole animation
print(f"{apngasm.get_loops() = }")
print(f"{apngasm.is_skip_first() = }")
print(f"{apngasm.frame_count() = }")

# Assemble
out = os.path.join(output_dir, "elephant.apng")
success = apngasm.assemble(out)
print(f"{success = }")

# Clear images loaded in apngasm object
apngasm.reset()

# Disassemble and get pillow image of one frame
frames = apngasm.disassemble_as_pillow(ball_apng_path)
frame = frames[0]
out = os.path.join(output_dir, "ball0.png")
frame.save(out)

# Disassemble all APNG into PNGs
apngasm.save_pngs(output_dir)

# Assemble from pillow images
# Just for fun, let's also make it spin
apngasm.reset()
angle = 0
angle_step = 360 / len(os.listdir(frames_dir))
for file_name in sorted(os.listdir(frames_dir)):
    image = Image.open(os.path.join(frames_dir, file_name))
    image = image.rotate(angle)
    apngasm.add_frame_from_pillow(image)

    angle += angle_step

out = os.path.join(output_dir, "elephant-spinning-pillow.apng")
success = apngasm.assemble(out)
print(f"{success = }")
apngasm.reset()

# Assemble palette and grey PNGs
# You can use with statement to avoid calling reset()
with APNGAsmBinder() as apng:
    apng.add_frame_from_file(palette_png_path, delay_num=1, delay_den=1)
    apng.add_frame_from_file(grey_png_path, delay_num=1, delay_den=1)
    out = os.path.join(output_dir, "birds.apng")
    success = apng.assemble(out)
    print(f"{success = }")

# Assemble palette and grey PNGs, but with Pillow and numpy
image0 = Image.open(grey_png_path)
frame0 = apngasm.add_frame_from_pillow(image0, delay_num=1, delay_den=1)
image1 = Image.open(grey_png_path).convert("RGB")
frame1 = apngasm.add_frame_from_numpy(
    np.array(image1), trns_color=np.array([255, 255, 255]), delay_num=1, delay_den=1
)
image2 = Image.open(palette_png_path)
apngasm.add_frame_from_pillow(image2, delay_num=1, delay_den=1)

out = os.path.join(output_dir, "birds-pillow.apng")
success = apngasm.assemble(out)
print(f"{success = }")
