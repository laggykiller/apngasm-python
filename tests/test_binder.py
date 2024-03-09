#!/usr/bin/env python3
import os
from importlib.util import find_spec

import pytest
from _pytest._py.path import LocalPath
from apngasm_python._apngasm_python import APNGFrame
from apngasm_python.apngasm import APNGAsmBinder

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


@pytest.mark.skipif(NUMPY_LOADED is False, reason="Numpy not installed")
@pytest.mark.skipif(PILLOW_LOADED is False, reason="Pillow not installed")
def test_frame_pixels_as_pillow():
    from PIL import Image

    apngasm = APNGAsmBinder()
    apngasm.add_frame_from_file(elephant_frame0_path)
    frame = apngasm.frame_pixels_as_pillow(0)

    assert isinstance(frame, Image.Image)


@pytest.mark.skipif(NUMPY_LOADED is False, reason="Numpy not installed")
def test_frame_pixels_as_numpy():
    import numpy

    apngasm = APNGAsmBinder()
    apngasm.add_frame_from_file(elephant_frame0_path)
    frame = apngasm.frame_pixels_as_numpy(0)

    assert isinstance(frame, numpy.ndarray)


def test_frame_width():
    apngasm = APNGAsmBinder()
    apngasm.add_frame_from_file(elephant_frame0_path)
    width = apngasm.frame_width(0)

    assert width == 480


def test_frame_height():
    apngasm = APNGAsmBinder()
    apngasm.add_frame_from_file(elephant_frame0_path)
    height = apngasm.frame_height(0)

    assert height == 400


def test_frame_color_type():
    apngasm = APNGAsmBinder()
    apngasm.add_frame_from_file(elephant_frame0_path)
    color_type = apngasm.frame_color_type(0)

    assert color_type == 6


@pytest.mark.skipif(NUMPY_LOADED is False, reason="Numpy not installed")
def test_frame_palette():
    import numpy

    apngasm = APNGAsmBinder()
    apngasm.add_frame_from_file(palette_png_path)
    palette = apngasm.frame_palette(0)
    assert isinstance(palette, numpy.ndarray)


@pytest.mark.skipif(NUMPY_LOADED is False, reason="Numpy not installed")
@pytest.mark.skipif(PILLOW_LOADED is False, reason="Pillow not installed")
def test_frame_transparency():
    import numpy
    from PIL import Image

    apngasm = APNGAsmBinder()
    with Image.open(elephant_frame0_path) as im_rgba:
        im_rgb = im_rgba.convert("RGB")
        arr = numpy.asarray(im_rgb, dtype="int32")
        white = numpy.array([255, 255, 255])
        apngasm.add_frame_from_numpy(arr, trns_color=white)
    transparency = apngasm.frame_transparency(0)
    assert isinstance(transparency, numpy.ndarray)


def test_frame_palette_size():
    apngasm = APNGAsmBinder()
    apngasm.add_frame_from_file(palette_png_path)
    palette_size = apngasm.frame_palette_size(0)

    assert palette_size == 0


@pytest.mark.skipif(NUMPY_LOADED is False, reason="Numpy not installed")
@pytest.mark.skipif(PILLOW_LOADED is False, reason="Pillow not installed")
def test_frame_transparency_size():
    import numpy
    from PIL import Image

    apngasm = APNGAsmBinder()
    with Image.open(elephant_frame0_path) as im_rgba:
        im_rgb = im_rgba.convert("RGB")
        arr = numpy.asarray(im_rgb, dtype="int32")
        white = numpy.array([255, 255, 255])
        apngasm.add_frame_from_numpy(arr, trns_color=white)
    transparency_size = apngasm.frame_transparency_size(0)
    assert transparency_size == 6


def test_frame_delay_num():
    apngasm = APNGAsmBinder()
    apngasm.add_frame_from_file(elephant_frame0_path, 50, 250)
    delay_num = apngasm.frame_delay_num(0)
    assert delay_num == 50


def test_frame_delay_den():
    apngasm = APNGAsmBinder()
    apngasm.add_frame_from_file(elephant_frame0_path, 50, 250)
    delay_den = apngasm.frame_delay_den(0)
    assert delay_den == 250


def test_add_frame_from_file_rgba():
    apngasm = APNGAsmBinder()
    frame_count = apngasm.add_frame_from_file(elephant_frame0_path)
    assert frame_count == 1


def test_add_frame_from_file_grey():
    apngasm = APNGAsmBinder()
    frame_count = apngasm.add_frame_from_file(grey_png_path)
    assert frame_count == 1


def test_add_frame_from_file_palette():
    apngasm = APNGAsmBinder()
    frame_count = apngasm.add_frame_from_file(palette_png_path)
    assert frame_count == 1


@pytest.mark.skipif(PILLOW_LOADED is False, reason="Pillow not installed")
def test_add_frame_from_pillow_rgba():
    from PIL import Image

    apngasm = APNGAsmBinder()

    with Image.open(elephant_frame0_path) as im:
        frame_count = apngasm.add_frame_from_pillow(im)
        assert frame_count == 1


@pytest.mark.skipif(PILLOW_LOADED is False, reason="Pillow not installed")
def test_add_frame_from_pillow_grey():
    from PIL import Image

    apngasm = APNGAsmBinder()

    with Image.open(grey_png_path) as im:
        frame_count = apngasm.add_frame_from_pillow(im)
        assert frame_count == 1


@pytest.mark.skipif(PILLOW_LOADED is False, reason="Pillow not installed")
def test_add_frame_from_pillow_palette():
    from PIL import Image

    apngasm = APNGAsmBinder()

    with Image.open(palette_png_path) as im:
        frame_count = apngasm.add_frame_from_pillow(im)
        assert frame_count == 1


@pytest.mark.skipif(PILLOW_LOADED is False, reason="Pillow not installed")
@pytest.mark.skipif(NUMPY_LOADED is False, reason="Numpy not installed")
def test_add_frame_from_numpy_rgba():
    import numpy
    from PIL import Image

    apngasm = APNGAsmBinder()

    with Image.open(elephant_frame0_path) as im:
        arr = numpy.asarray(im, dtype="int32")
        frame_count = apngasm.add_frame_from_numpy(arr)
        assert frame_count == 1


@pytest.mark.skipif(PILLOW_LOADED is False, reason="Pillow not installed")
@pytest.mark.skipif(NUMPY_LOADED is False, reason="Numpy not installed")
def test_add_frame_from_numpy_rgb():
    import numpy
    from PIL import Image

    apngasm = APNGAsmBinder()

    with Image.open(elephant_frame0_path) as im_rgba:
        im_rgb = im_rgba.convert("RGB")
        arr = numpy.asarray(im_rgb, dtype="int32")
        frame_count = apngasm.add_frame_from_numpy(arr)
        assert frame_count == 1


@pytest.mark.skipif(PILLOW_LOADED is False, reason="Pillow not installed")
@pytest.mark.skipif(NUMPY_LOADED is False, reason="Numpy not installed")
def test_add_frame_from_numpy_rgb_trns():
    import numpy
    from PIL import Image

    apngasm = APNGAsmBinder()

    with Image.open(elephant_frame0_path) as im_rgba:
        im_rgb = im_rgba.convert("RGB")
        arr = numpy.asarray(im_rgb, dtype="int32")
        white = numpy.array([255, 255, 255])
        frame_count = apngasm.add_frame_from_numpy(arr, trns_color=white)
        assert frame_count == 1


@pytest.mark.skipif(PILLOW_LOADED is False, reason="Pillow not installed")
@pytest.mark.skipif(NUMPY_LOADED is False, reason="Numpy not installed")
def test_add_frame_from_numpy_non_rgb():
    import numpy
    from PIL import Image

    apngasm = APNGAsmBinder()

    with Image.open(palette_png_path) as im:
        arr = numpy.asarray(im, dtype="int32")
        with pytest.raises(TypeError):
            apngasm.add_frame_from_numpy(arr)


def test_assemble(tmpdir: LocalPath):
    apngasm = APNGAsmBinder()
    apngasm.add_frame_from_file(grey_png_path)
    apngasm.add_frame_from_file(palette_png_path)

    out = os.path.join(tmpdir, "0.apng")
    apngasm.assemble(out)

    assert os.path.isfile(out)


@pytest.mark.skipif(NUMPY_LOADED is False, reason="Numpy not installed")
def test_disassemble_as_numpy():
    import numpy

    apngasm = APNGAsmBinder()
    arrs = apngasm.disassemble_as_numpy(ball_apng_path)

    assert len(arrs) == 20
    for arr in arrs:
        assert isinstance(arr, numpy.ndarray)


@pytest.mark.skipif(PILLOW_LOADED is False, reason="Pillow not installed")
def test_disassemble_as_pillow():
    from PIL import Image

    apngasm = APNGAsmBinder()
    ims = apngasm.disassemble_as_pillow(ball_apng_path)

    assert len(ims) == 20
    for im in ims:
        assert isinstance(im, Image.Image)


def test_save_pngs(tmpdir: LocalPath):
    apngasm = APNGAsmBinder()
    apngasm.add_frame_from_file(elephant_frame0_path)
    apngasm.save_pngs(str(tmpdir))

    assert len(os.listdir(tmpdir)) == 1


def test_load_animation_spec_xml():
    apngasm = APNGAsmBinder()
    frames = apngasm.load_animation_spec(animation_spec_xml)

    assert len(frames) == 2


def test_load_animation_spec_json():
    apngasm = APNGAsmBinder()
    frames = apngasm.load_animation_spec(animation_spec_json)

    assert len(frames) == 2


def test_save_json(tmpdir: LocalPath):
    apngasm = APNGAsmBinder()
    apngasm.add_frame_from_file(animation_spec_0_png_path)
    apngasm.add_frame_from_file(animation_spec_1_png_path)
    out = os.path.join(tmpdir, "animation_spec.json")

    apngasm.save_json(out, str(tmpdir))

    with open(out) as f, open(animation_spec_json) as g:
        assert f.read() == g.read()


def test_save_xml(tmpdir: LocalPath):
    apngasm = APNGAsmBinder()
    apngasm.add_frame_from_file(animation_spec_0_png_path)
    apngasm.add_frame_from_file(animation_spec_1_png_path)
    out = os.path.join(tmpdir, "animation_spec.xml")

    apngasm.save_xml(out, str(tmpdir))

    with open(out) as f, open(animation_spec_xml) as g:
        assert f.read() == g.read()


def test_set_apngasm_listener():
    apngasm = APNGAsmBinder()
    with pytest.raises(NotImplementedError):
        apngasm.set_apngasm_listener()


def test_get_set_loops():
    apngasm = APNGAsmBinder()
    apngasm.add_frame_from_file(elephant_frame0_path)
    apngasm.set_loops(5)
    assert apngasm.get_loops() == 5


def test_skip_first():
    apngasm = APNGAsmBinder()
    apngasm.add_frame_from_file(elephant_frame0_path)
    apngasm.set_skip_first(True)
    assert apngasm.is_skip_first() is True
    apngasm.set_skip_first(False)
    assert apngasm.is_skip_first() is False


def test_get_frames():
    apngasm = APNGAsmBinder()
    apngasm.add_frame_from_file(grey_png_path)
    apngasm.add_frame_from_file(palette_png_path)
    frames = apngasm.get_frames()

    assert len(frames) == 2
    for frame in frames:
        assert isinstance(frame, APNGFrame)


def test_frame_count():
    apngasm = APNGAsmBinder()
    apngasm.add_frame_from_file(grey_png_path)
    apngasm.add_frame_from_file(palette_png_path)
    frame_count = apngasm.frame_count()

    assert frame_count == 2


def test_reset():
    apngasm = APNGAsmBinder()
    assert apngasm.frame_count() == 0
    apngasm.add_frame_from_file(grey_png_path)
    assert apngasm.frame_count() == 1
    apngasm.reset()
    assert apngasm.frame_count() == 0
    apngasm.add_frame_from_file(palette_png_path)
    assert apngasm.frame_count() == 1


def test_version():
    apngasm = APNGAsmBinder()
    assert isinstance(apngasm.version(), str)


def test_with():
    with APNGAsmBinder() as apngasm:
        assert isinstance(apngasm.version(), str)
