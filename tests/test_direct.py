#!/usr/bin/env python3
from importlib.util import find_spec
import os

import pytest
from _pytest._py.path import LocalPath

from apngasm_python._apngasm_python import (
    APNGAsm,
    APNGFrame,
    create_frame_from_rgb_trns,
    create_frame_from_rgba,
)

PILLOW_LOADED = True if find_spec("PIL") else False
NUMPY_LOADED = True if find_spec("numpy") else False

file_dir = os.path.split(__file__)[0]
samples_dir = os.path.join(file_dir, "../samples")
frames_dir = os.path.join(samples_dir, "frames")
elephant_frame0_path = os.path.join(frames_dir, "elephant-001.png")
input_dir = os.path.join(samples_dir, "input")
output_dir = os.path.join(samples_dir, "output")
ball_apng_path = os.path.join(input_dir, "ball.apng")
grey_png_path = os.path.join(input_dir, "grey.png")
palette_png_path = os.path.join(input_dir, "palette.png")
animation_spec_0_png_path = os.path.join(input_dir, "0.png")
animation_spec_1_png_path = os.path.join(input_dir, "1.png")
animation_spec_json = os.path.join(input_dir, "animation_spec.json")
animation_spec_xml = os.path.join(input_dir, "animation_spec.xml")


@pytest.mark.skipif(PILLOW_LOADED is False, reason="Pillow not installed")
@pytest.mark.skipif(NUMPY_LOADED is False, reason="Numpy not installed")
def test_frame_pixels():
    from PIL import Image
    import numpy

    image = Image.open(elephant_frame0_path)
    frame = create_frame_from_rgba(numpy.array(image), image.width, image.height)

    assert isinstance(frame.pixels, numpy.ndarray)


@pytest.mark.skipif(PILLOW_LOADED is False, reason="Pillow not installed")
@pytest.mark.skipif(NUMPY_LOADED is False, reason="Numpy not installed")
def test_frame_width():
    from PIL import Image
    import numpy

    image = Image.open(elephant_frame0_path)
    frame = create_frame_from_rgba(numpy.array(image), image.width, image.height)

    assert frame.width == 480


@pytest.mark.skipif(PILLOW_LOADED is False, reason="Pillow not installed")
@pytest.mark.skipif(NUMPY_LOADED is False, reason="Numpy not installed")
def test_frame_height():
    from PIL import Image
    import numpy

    image = Image.open(elephant_frame0_path)
    frame = create_frame_from_rgba(numpy.array(image), image.width, image.height)

    assert frame.height == 400


@pytest.mark.skipif(PILLOW_LOADED is False, reason="Pillow not installed")
@pytest.mark.skipif(NUMPY_LOADED is False, reason="Numpy not installed")
def test_frame_color_type():
    from PIL import Image
    import numpy

    image = Image.open(elephant_frame0_path)
    frame = create_frame_from_rgba(numpy.array(image), image.width, image.height)

    assert frame.color_type == 6


@pytest.mark.skipif(PILLOW_LOADED is False, reason="Pillow not installed")
@pytest.mark.skipif(NUMPY_LOADED is False, reason="Numpy not installed")
def test_frame_palette():
    from PIL import Image
    import numpy

    image = Image.open(elephant_frame0_path)
    frame = create_frame_from_rgba(numpy.array(image), image.width, image.height)
    assert isinstance(frame.palette, numpy.ndarray)


@pytest.mark.skipif(NUMPY_LOADED is False, reason="Numpy not installed")
@pytest.mark.skipif(PILLOW_LOADED is False, reason="Pillow not installed")
def test_frame_transparency():
    from PIL import Image
    import numpy

    image = Image.open(elephant_frame0_path).convert("RGB")
    frame = create_frame_from_rgb_trns(
        numpy.array(image), image.width, image.height, numpy.array([255, 255, 255])
    )

    assert isinstance(frame.transparency, numpy.ndarray)


@pytest.mark.skipif(NUMPY_LOADED is False, reason="Numpy not installed")
@pytest.mark.skipif(PILLOW_LOADED is False, reason="Pillow not installed")
def test_frame_palette_size():
    from PIL import Image
    import numpy

    image = Image.open(elephant_frame0_path)
    frame = create_frame_from_rgba(numpy.array(image), image.width, image.height)

    assert frame.palette_size == 0


@pytest.mark.skipif(NUMPY_LOADED is False, reason="Numpy not installed")
@pytest.mark.skipif(PILLOW_LOADED is False, reason="Pillow not installed")
def test_frame_transparency_size():
    from PIL import Image
    import numpy

    image = Image.open(elephant_frame0_path).convert("RGB")
    frame = create_frame_from_rgb_trns(
        numpy.array(image), image.width, image.height, numpy.array([255, 255, 255])
    )
    assert frame.transparency_size == 6


@pytest.mark.skipif(NUMPY_LOADED is False, reason="Numpy not installed")
@pytest.mark.skipif(PILLOW_LOADED is False, reason="Pillow not installed")
def test_frame_delay_num():
    from PIL import Image
    import numpy

    image = Image.open(elephant_frame0_path)
    frame = create_frame_from_rgba(
        numpy.array(image), image.width, image.height, 50, 250
    )
    assert frame.delay_num == 50


@pytest.mark.skipif(NUMPY_LOADED is False, reason="Numpy not installed")
@pytest.mark.skipif(PILLOW_LOADED is False, reason="Pillow not installed")
def test_frame_delay_den():
    from PIL import Image
    import numpy

    image = Image.open(elephant_frame0_path)
    frame = create_frame_from_rgba(
        numpy.array(image), image.width, image.height, 50, 250
    )
    assert frame.delay_den == 250


def test_add_frame_from_file_rgba():
    apngasm = APNGAsm()
    frame_count = apngasm.add_frame_from_file(elephant_frame0_path)
    assert frame_count == 1


def test_add_frame_from_file_grey():
    apngasm = APNGAsm()
    frame_count = apngasm.add_frame_from_file(grey_png_path)
    assert frame_count == 1


def test_add_frame_from_file_palette():
    apngasm = APNGAsm()
    frame_count = apngasm.add_frame_from_file(palette_png_path)
    assert frame_count == 1


def test_assemble(tmpdir: LocalPath):
    apngasm = APNGAsm()
    apngasm.add_frame_from_file(grey_png_path)
    apngasm.add_frame_from_file(palette_png_path)

    out = os.path.join(tmpdir, "0.apng")
    apngasm.assemble(out)

    assert os.path.isfile(out)


def test_disassemble():
    apngasm = APNGAsm()
    frames = apngasm.disassemble(ball_apng_path)

    assert len(frames) == 20
    for frame in frames:
        assert isinstance(frame, APNGFrame)


def test_save_pngs(tmpdir: LocalPath):
    apngasm = APNGAsm()
    apngasm.add_frame_from_file(elephant_frame0_path)
    apngasm.save_pngs(str(tmpdir))

    assert len(os.listdir(tmpdir)) == 1


def test_load_animation_spec_xml():
    apngasm = APNGAsm()
    frames = apngasm.load_animation_spec(animation_spec_xml)

    assert len(frames) == 2


def test_load_animation_spec_json():
    apngasm = APNGAsm()
    frames = apngasm.load_animation_spec(animation_spec_json)

    assert len(frames) == 2


def test_save_json(tmpdir: LocalPath):
    apngasm = APNGAsm()
    apngasm.add_frame_from_file(animation_spec_0_png_path)
    apngasm.add_frame_from_file(animation_spec_1_png_path)
    out = os.path.join(tmpdir, "animation_spec.json")

    apngasm.save_json(out, str(tmpdir))

    with open(out) as f, open(animation_spec_json) as g:
        assert f.read() == g.read()


def test_save_xml(tmpdir: LocalPath):
    apngasm = APNGAsm()
    apngasm.add_frame_from_file(animation_spec_0_png_path)
    apngasm.add_frame_from_file(animation_spec_1_png_path)
    out = os.path.join(tmpdir, "animation_spec.xml")

    apngasm.save_xml(out, str(tmpdir))

    with open(out) as f, open(animation_spec_xml) as g:
        assert f.read() == g.read()


def test_get_set_loops():
    apngasm = APNGAsm()
    apngasm.add_frame_from_file(elephant_frame0_path)
    apngasm.set_loops(5)
    assert apngasm.get_loops() == 5


def test_skip_first():
    apngasm = APNGAsm()
    apngasm.add_frame_from_file(elephant_frame0_path)
    apngasm.set_skip_first(True)
    assert apngasm.is_skip_first() is True
    apngasm.set_skip_first(False)
    assert apngasm.is_skip_first() is False


def test_get_frames():
    apngasm = APNGAsm()
    apngasm.add_frame_from_file(grey_png_path)
    apngasm.add_frame_from_file(palette_png_path)
    frames = apngasm.get_frames()

    assert len(frames) == 2
    for frame in frames:
        assert isinstance(frame, APNGFrame)


def test_frame_count():
    apngasm = APNGAsm()
    apngasm.add_frame_from_file(grey_png_path)
    apngasm.add_frame_from_file(palette_png_path)
    frame_count = apngasm.frame_count()

    assert frame_count == 2


def test_reset():
    apngasm = APNGAsm()
    assert apngasm.frame_count() == 0
    apngasm.add_frame_from_file(grey_png_path)
    assert apngasm.frame_count() == 1
    apngasm.reset()
    assert apngasm.frame_count() == 0
    apngasm.add_frame_from_file(palette_png_path)
    assert apngasm.frame_count() == 1


def test_version():
    apngasm = APNGAsm()
    assert isinstance(apngasm.version(), str)
