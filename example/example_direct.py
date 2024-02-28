#!/usr/bin/env python3
from apngasm_python._apngasm_python import (
    APNGAsm,
    APNGFrame,
    create_frame_from_rgb,
    create_frame_from_rgb_trns,
    create_frame_from_rgba,
)
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


def frame_info(frame: APNGFrame):
    print(f"{frame.pixels = }")
    print(f"{frame.width = }")
    print(f"{frame.height = }")
    print(f"{frame.color_type = }")
    print(f"{frame.palette = }")
    print(f"{frame.transparency = }")
    print(f"{frame.palette_size = }")
    print(f"{frame.transparency_size = }")
    print(f"{frame.delay_num = }")
    print(f"{frame.delay_den = }")


# https://www.w3.org/TR/PNG-Chunks.html
color_type_dict = {0: "L", 2: "RGB", 3: "P", 4: "LA", 6: "RGBA"}

color_type_dict.update(dict((v, k) for k, v in color_type_dict.items()))  # type: ignore

# Cleanup
shutil.rmtree(output_dir, ignore_errors=True)
os.mkdir(output_dir)

# Initialize
apngasm = APNGAsm()

# Get libapngasm version
print(f"{apngasm.version() = }")

# Load png from one directory
for file_name in sorted(os.listdir(frames_dir)):
    apngasm.add_frame_from_file(os.path.join(frames_dir, file_name), 100, 1000)

# Getting information about one frame
frame = apngasm.get_frames()[0]
frame_info(frame)

# Saving one frame as file
out = os.path.join(output_dir, "elephant-frame.png")
frame.save(out)

# Getting one frame as Pillow Image
mode = color_type_dict[frame.color_type]
im = Image.frombytes(mode, (frame.width, frame.height), frame.pixels)  # type: ignore
out = os.path.join(output_dir, "elephant-frame-pillow.png")
im.save(out)

# Get inforamtion about whole animation
print(f"{apngasm.get_loops() = }")
print(f"{apngasm.is_skip_first() = }")
print(f"{apngasm.frame_count() = }")

# Assemble
out = os.path.join(output_dir, "elephant.png")
success = apngasm.assemble(out)
print(f"{success = }")

# Clear images loaded in apngasm object
apngasm.reset()

# Disassemble and get pillow image of one frame
frames = apngasm.disassemble(ball_apng_path)
print(f"{len(frames) = }")
frame = frames[0]
frame_info(frame)
mode = color_type_dict[frame.color_type]
im = Image.frombytes(mode, (frame.width, frame.height), frame.pixels)  # type: ignore
out = os.path.join(output_dir, "ball0.png")
im.save(out)

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
    frame = create_frame_from_rgba(np.array(image), image.width, image.height)
    apngasm.add_frame(frame)

    angle += angle_step

out = os.path.join(output_dir, "elephant-spinning-pillow.apng")
success = apngasm.assemble(out)
print(f"{success = }")

# Assemble palette and grey PNGs
apngasm.reset()
apngasm.add_frame_from_file(palette_png_path, 100, 1000)
apngasm.add_frame_from_file(grey_png_path, 100, 1000)

frame0 = apngasm.get_frames()[0]
frame_info(frame0)

frame1 = apngasm.get_frames()[1]
frame_info(frame1)

out = os.path.join(output_dir, "birds.apng")
success = apngasm.assemble(out)
print(f"{success = }")

del apngasm

# Assemble palette and grey PNGs, but with Pillow
image0 = Image.open(grey_png_path).convert("RGB")
frame0 = create_frame_from_rgb(np.array(image0), image0.width, image0.height, 1, 1)
frame_info(frame0)

image1 = Image.open(grey_png_path).convert("RGB")
frame1 = create_frame_from_rgb_trns(
    np.array(image1), image0.width, image0.height, np.array([255, 255, 255]), 1, 1
)
frame_info(frame1)

# You may even set the variables manually
image2 = Image.open(palette_png_path).convert("RGBA")
frame2 = APNGFrame()
frame2.delay_num = 1
frame2.delay_den = 1
frame2.color_type = color_type_dict[image2.mode]  # type: ignore
frame2.width = image2.width
frame2.height = image2.height
frame2.pixels = np.array(image2)
frame_info(frame2)

# Another way of creating APNGAsm object
apngasm = APNGAsm([frame0, frame1, frame2])  # type: ignore

out = os.path.join(output_dir, "birds-pillow.apng")
success = apngasm.assemble(out)
print(f"{success = }")
