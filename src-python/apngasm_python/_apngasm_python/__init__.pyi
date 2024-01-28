from __future__ import annotations
import numpy.typing
from typing import Any, Optional, overload, Typing, Sequence
from enum import Enum
from . import _apngasm_python

class APNGAsm:
    """
    Class representing APNG file, storing APNGFrame(s) and other metadata.
    """

    def __init__(self, frames: list[_apngasm_python.APNGFrame]) -> None:
        """
        Construct APNGAsm object from an existing vector of apngasm frames.
        
        :param list[apngasm_python._apngasm_python.APNGFrame] frames: A list of APNGFrame objects.
        """
        ...
    
    @overload
    def __init__(self) -> None:
        """
        Construct an empty APNGAsm object.
        """
        ...
    
    def add_frame(self, frame: _apngasm_python.APNGFrame) -> int:
        """
        Adds an APNGFrame object to the frame vector.
        
        :param frame: The APNGFrame object to be added.
        :type frame: apngasm_python._apngasm_python.APNGFrame
        
        :return: The new number of frames/the number of this frame on the frame vector.
        :rtype: int
        """
        ...
    
    def add_frame_from_file(self, file_path: str, delay_num: int = 100, delay_den: int = 1000) -> int:
        """
        Adds a frame from a PNG file or frames from a APNG file to the frame vector.
        
        :param str file_path: The relative or absolute path to an image file.
        :param int delay_num: The delay numerator for this frame (defaults to DEFAULT_FRAME_NUMERATOR).
        :param int delay_den: The delay denominator for this frame (defaults to DEFAULT_FRAME_DENMINATOR).
        
        :return: The new number of frames/the number of this frame on the frame vector.
        :rtype: int
        """
        ...
    
    def add_frame_from_rgb(self, pixels_rgb: _apngasm_python.rgb, width: int, height: int, trns_color: _apngasm_python.rgb = 0, delay_num: int = 100, delay_den: int = 1000) -> int:
        """
        Adds an APNGFrame object to the vector.
        Not possible to use in Python. As alternative,
        Use create_frame_from_rgb() or create_frame_from_rgba(). Or manually,
        First create an empty APNGFrame with frame = APNGFrame(),
        then set frame.width, frame.height, frame.color_type, frame.pixels,
        frame.palette, frame.delay_num, frame.delay_den manually.
        
        :param apngasm_python._apngasm_python.rgb pixels_rgb: The RGB pixel data.
        :param int width: The width of the pixel data.
        :param int height: The height of the pixel data.
        :param apngasm_python._apngasm_python.rgb trns_color: The color [r, g, b] to be treated as transparent.
        :param int delay_num: The delay numerator for this frame (defaults to DEFAULT_FRAME_NUMERATOR).
        :param int delay_den: The delay denominator for this frame (defaults to DEFAULT_FRAME_DENMINATOR).
        
        :return: The new number of frames/the number of this frame on the frame vector.
        :rtype: int
        """
        ...
    
    def add_frame_from_rgba(self, pixels_rgba: _apngasm_python.rgba, width: int, height: int, delay_num: int = 100, delay_den: int = 1000) -> int:
        """
        Adds an APNGFrame object to the vector.
        Not possible to use in Python. As alternative,
        Use create_frame_from_rgb() or create_frame_from_rgba(). Or manually,
        First create an empty APNGFrame with frame = APNGFrame(),
        then set frame.width, frame.height, frame.color_type, frame.pixels,
        frame.palette, frame.delay_num, frame.delay_den manually.
        
        :param apngasm_python._apngasm_python.rgba pixels_rgba: The RGBA pixel data.
        :param int width: The width of the pixel data.
        :param int height: The height of the pixel data.
        :param int delay_num: The delay numerator for this frame (defaults to DEFAULT_FRAME_NUMERATOR).
        :param int delay_den: The delay denominator for this frame (defaults to DEFAULT_FRAME_DENMINATOR).
        
        :return: The new number of frames/the number of this frame on the frame vector.
        :rtype: int
        """
        ...
    
    def assemble(self, output_path: str) -> bool:
        """
        Assembles and outputs an APNG file.
        
        :param str output_path: The output file path.
        
        :return: true if assemble completed succesfully.
        :rtype: bool
        """
        ...
    
    def disassemble(self, file_path: str) -> list[_apngasm_python.APNGFrame]:
        """
        Disassembles an APNG file.
        
        :param str file_path: The file path to the PNG image to be disassembled.
        
        :return: A vector containing the frames of the disassembled PNG.
        :rtype: list[apngasm_python._apngasm_python.APNGFrame]
        """
        ...
    
    def frame_count(self) -> int:
        """
        Returns the number of frames.
        
        :return: number of frames.
        :rtype: int
        """
        ...
    
    def get_frames(self) -> list[_apngasm_python.APNGFrame]:
        """
        Returns the frame vector.
        
        :return: frame vector.
        :rtype: list[apngasm_python._apngasm_python.APNGFrame]
        """
        ...
    
    def get_loops(self) -> int:
        """
        Returns the loop count.
        
        :return: loop count.
        :rtype: int
        """
        ...
    
    def is_skip_first(self) -> bool:
        """
        Returns the flag of skip first frame.
        
        :return: flag of skip first frame.
        :rtype: bool
        """
        ...
    
    def load_animation_spec(self, file_path: str) -> list[_apngasm_python.APNGFrame]:
        """
        Loads an animation spec from JSON or XML.
        Loaded frames are added to the end of the frame vector.
        For more details on animation specs see:
        https://github.com/Genshin/PhantomStandards
        
        :param str file_path: The path of JSON or XML file.
        
        :return: A vector containing the frames
        :rtype: list[apngasm_python._apngasm_python.APNGFrame]
        """
        ...
    
    def reset(self) -> int:
        """
        Destroy all frames in memory/dispose of the frame vector.
        Leaves the apngasm object in a clean state.
        Returns number of frames disposed of.
        
        :return: number of frames disposed of.
        :rtype: int
        """
        ...
    
    def save_json(self, output_path: str, image_dir: str) -> bool:
        """
        Saves a JSON animation spec file.
        
        :param str output_path: Path to save the file to.
        :param str image_dir: Directory where frame files are to be saved if not the same path as the animation spec.
        
        :return: true if save was successful.
        :rtype: bool
        """
        ...
    
    def save_pngs(self, output_dir: str) -> bool:
        """
        Saves individual PNG files of the frames in the frame vector.
        
        :param str output_dir: The directory where the PNG fils will be saved.
        
        :return: true if all files were saved successfully.
        :rtype: bool
        """
        ...
    
    def save_xml(self, output_path: str, image_dir: str) -> bool:
        """
        Saves an XML animation spec file.
        
        :param str file_path: Path to save the file to.
        :param str image_dir: Directory where frame files are to be saved if not the same path as the animation spec.
        
        :return: true if save was successful.
        :rtype: bool
        """
        ...
    
    def set_apngasm_listener(self, listener: Optional[_apngasm_python.IAPNGAsmListener] = None) -> None:
        """
        Sets a listener.
        
        :param Optional[apngasm_python._apngasm_python.IAPNGAsmListener] listener: A pointer to the listener object. If the argument is NULL a default APNGAsmListener will be created and assigned.
        """
        ...
    
    def set_loops(self, loops: int = 0) -> None:
        """
        Set loop count of animation.
        
        :param int loops: Loop count of animation. If the argument is 0 a loop count is infinity.
        """
        ...
    
    def set_skip_first(self, skip_first: bool) -> None:
        """
        Set flag of skip first frame.
        
        :param int skip_first: Flag of skip first frame.
        """
        ...
    
    def version(self) -> str:
        """
        Returns the version of APNGAsm.
        
        :return: the version of APNGAsm.
        :rtype: str
        """
        ...
    
class APNGFrame:
    """
    Class representing a frame in APNG.
    """

    def __init__(self, pixels: _apngasm_python.rgba, width: int, height: int, delay_num: int = 100, delay_den: int = 1000) -> None:
        """
        Creates an APNGFrame from a bitmapped array of RBGA pixel data.
        Not possible to use in Python. To create APNGFrame from pixel data in memory,
        Use create_frame_from_rgb() or create_frame_from_rgba(). Or manually,
        First create an empty APNGFrame with frame = APNGFrame(),
        then set frame.width, frame.height, frame.color_type, frame.pixels,
        frame.palette, frame.delay_num, frame.delay_den manually.
        
        :param apngasm_python._apngasm_python.rgba pixels: The RGBA pixel data.
        :param int width: The width of the pixel data.
        :param int height: The height of the pixel data.
        :param int delay_num: The delay numerator for this frame (defaults to DEFAULT_FRAME_NUMERATOR).
        :param int delay_den: The delay denominator for this frame (defaults to DEFAULT_FRAME_DENMINATOR).
        """
        ...
    
    @overload
    def __init__(self) -> None:
        """
        Creates an empty APNGFrame.
        """
        ...
    
    @overload
    def __init__(self, file_path: str, delay_num: int = 100, delay_den: int = 1000) -> None:
        """
        Creates an APNGFrame from a PNG file.
        
        :param str file_path: The relative or absolute path to an image file.
        :param int delay_num: The delay numerator for this frame (defaults to DEFAULT_FRAME_NUMERATOR).
        :param int delay_den: The delay denominator for this frame (defaults to DEFAULT_FRAME_DENMINATOR).
        """
        ...
    
    @overload
    def __init__(self, pixels: _apngasm_python.rgb, width: int, height: int, trns_color: _apngasm_python.rgb, delay_num: int = 100, delay_den: int = 1000) -> None:
        """
        Creates an APNGFrame from a bitmapped array of RBG pixel data.
        Not possible to use in Python. To create APNGFrame from pixel data in memory,
        Use create_frame_from_rgb() or create_frame_from_rgba(). Or manually,
        First create an empty APNGFrame with frame = APNGFrame(),
        then set frame.width, frame.height, frame.color_type, frame.pixels,
        frame.palette, frame.delay_num, frame.delay_den manually.
        
        :param apngasm_python._apngasm_python.rgb pixels: The RGB pixel data.
        :param int width: The width of the pixel data.
        :param int height: The height of the pixel data.
        :param apngasm_python._apngasm_python.rgb trns_color: The color [r, g, b] to be treated as transparent.
        :param int delay_num: The delay numerator for this frame (defaults to DEFAULT_FRAME_NUMERATOR).
        :param int delay_den: The delay denominator for this frame (defaults to DEFAULT_FRAME_DENMINATOR).
        """
        ...
    
    @property
    def color_type(color_typescolor_typeecolor_typelcolor_typefcolor_type)color_type color_type-color_type>color_type color_typeicolor_typencolor_typetcolor_type:
        """
        The color_type of the frame.
        
        0: Grayscale (Pillow mode='L')
        2: RGB (Pillow mode='RGB')
        3: Palette (Pillow mode='P')
        4: Grayscale + Alpha (Pillow mode='LA')
        6: RGBA (Pillow mode='RGBA')
        """
        ...
    @color_type.setter
    def color_type(color_typescolor_typeecolor_typelcolor_typefcolor_type,color_type color_typeacolor_typercolor_typegcolor_type:color_type color_typeicolor_typencolor_typetcolor_type,color_type color_type/color_type)color_type color_type-color_type>color_type color_typeNcolor_typeocolor_typencolor_typeecolor_type:
        """
        The color_type of the frame.
        
        0: Grayscale (Pillow mode='L')
        2: RGB (Pillow mode='RGB')
        3: Palette (Pillow mode='P')
        4: Grayscale + Alpha (Pillow mode='LA')
        6: RGBA (Pillow mode='RGBA')
        """
        ...
    
    @property
    def delay_den(delay_densdelay_denedelay_denldelay_denfdelay_den)delay_den delay_den-delay_den>delay_den delay_denidelay_denndelay_dentdelay_den:
        """
        The denominator of the duration of frame. Duration of time is delay_num / delay_den seconds.
        """
        ...
    @delay_den.setter
    def delay_den(delay_densdelay_denedelay_denldelay_denfdelay_den,delay_den delay_denadelay_denrdelay_dengdelay_den:delay_den delay_denidelay_denndelay_dentdelay_den,delay_den delay_den/delay_den)delay_den delay_den-delay_den>delay_den delay_denNdelay_denodelay_denndelay_denedelay_den:
        """
        The denominator of the duration of frame. Duration of time is delay_num / delay_den seconds.
        """
        ...
    
    @property
    def delay_num(delay_numsdelay_numedelay_numldelay_numfdelay_num)delay_num delay_num-delay_num>delay_num delay_numidelay_numndelay_numtdelay_num:
        """
        The nominator of the duration of frame. Duration of time is delay_num / delay_den seconds.
        """
        ...
    @delay_num.setter
    def delay_num(delay_numsdelay_numedelay_numldelay_numfdelay_num,delay_num delay_numadelay_numrdelay_numgdelay_num:delay_num delay_numidelay_numndelay_numtdelay_num,delay_num delay_num/delay_num)delay_num delay_num-delay_num>delay_num delay_numNdelay_numodelay_numndelay_numedelay_num:
        """
        The nominator of the duration of frame. Duration of time is delay_num / delay_den seconds.
        """
        ...
    
    @property
    def height(heightsheighteheightlheightfheight)height height-height>height heightiheightnheighttheight:
        """
        The height of frame.
        """
        ...
    @height.setter
    def height(heightsheighteheightlheightfheight,height heightaheightrheightgheight:height heightiheightnheighttheight,height height/height)height height-height>height heightNheightoheightnheighteheight:
        """
        The height of frame.
        """
        ...
    
    @property
    def palette(palettespaletteepalettelpalettefpalette)palette palette-palette>palette palettenpaletteupalettempaletteppaletteypalette.palettetpaletteypaletteppaletteipalettenpalettegpalette.paletteNpaletteDpaletteApaletterpaletterpaletteapaletteypalette:
        """
        The palette data of frame. Only applies to 'P' mode Image (i.e. Not RGB, RGBA).
        Expressed as 2D numpy array in format of [[r0, g0, b0], [r1, g1, b1], ..., [r255, g255, b255]] in Python.
        """
        ...
    @palette.setter
    def palette(palettespaletteepalettelpalettefpalette,palette paletteapaletterpalettegpalette:palette palettenpaletteupalettempaletteppaletteypalette.palettetpaletteypaletteppaletteipalettenpalettegpalette.paletteNpaletteDpaletteApaletterpaletterpaletteapaletteypalette,palette palette/palette)palette palette-palette>palette paletteNpaletteopalettenpaletteepalette:
        """
        The palette data of frame. Only applies to 'P' mode Image (i.e. Not RGB, RGBA).
        Expressed as 2D numpy array in format of [[r0, g0, b0], [r1, g1, b1], ..., [r255, g255, b255]] in Python.
        """
        ...
    
    @property
    def palette_size(palette_sizespalette_sizeepalette_sizelpalette_sizefpalette_size)palette_size palette_size-palette_size>palette_size palette_sizeipalette_sizenpalette_sizetpalette_size:
        """
        The palette data size of frame.
        """
        ...
    @palette_size.setter
    def palette_size(palette_sizespalette_sizeepalette_sizelpalette_sizefpalette_size,palette_size palette_sizeapalette_sizerpalette_sizegpalette_size:palette_size palette_sizeipalette_sizenpalette_sizetpalette_size,palette_size palette_size/palette_size)palette_size palette_size-palette_size>palette_size palette_sizeNpalette_sizeopalette_sizenpalette_sizeepalette_size:
        """
        The palette data size of frame.
        """
        ...
    
    @property
    def pixels(pixelsspixelsepixelslpixelsfpixels)pixels pixels-pixels>pixels pixelsnpixelsupixelsmpixelsppixelsypixels.pixelstpixelsypixelsppixelsipixelsnpixelsgpixels.pixelsNpixelsDpixelsApixelsrpixelsrpixelsapixelsypixels:
        """
        The raw pixel data of frame, expressed as a 3D numpy array in Python.
        Note that setting this value will also set the variable 'rows' internally.
        This should be set AFTER you set the width, height and color_type.
        """
        ...
    @pixels.setter
    def pixels(pixelsspixelsepixelslpixelsfpixels,pixels pixelsapixelsrpixelsgpixels:pixels pixelsnpixelsupixelsmpixelsppixelsypixels.pixelstpixelsypixelsppixelsipixelsnpixelsgpixels.pixelsNpixelsDpixelsApixelsrpixelsrpixelsapixelsypixels,pixels pixels/pixels)pixels pixels-pixels>pixels pixelsNpixelsopixelsnpixelsepixels:
        """
        The raw pixel data of frame, expressed as a 3D numpy array in Python.
        Note that setting this value will also set the variable 'rows' internally.
        This should be set AFTER you set the width, height and color_type.
        """
        ...
    
    def save(self, out_path: str) -> bool:
        """
        Saves this frame as a single PNG file.
        
        :param str out_path: The relative or absolute path to save the image file to.
        
        :return: true if save was successful.
        :rtype: bool
        """
        ...
    
    @property
    def transparency(transparencystransparencyetransparencyltransparencyftransparency)transparency transparency-transparency>transparency transparencyntransparencyutransparencymtransparencyptransparencyytransparency.transparencyttransparencyytransparencyptransparencyitransparencyntransparencygtransparency.transparencyNtransparencyDtransparencyAtransparencyrtransparencyrtransparencyatransparencyytransparency:
        """
        The transparency color of frame that is treated as transparent, expressed as 1D numpy array.
        For more info, refer to 'tRNS Transparency' in http://www.libpng.org/pub/png/spec/1.2/PNG-Chunks.html
        """
        ...
    @transparency.setter
    def transparency(transparencystransparencyetransparencyltransparencyftransparency,transparency transparencyatransparencyrtransparencygtransparency:transparency transparencyntransparencyutransparencymtransparencyptransparencyytransparency.transparencyttransparencyytransparencyptransparencyitransparencyntransparencygtransparency.transparencyNtransparencyDtransparencyAtransparencyrtransparencyrtransparencyatransparencyytransparency,transparency transparency/transparency)transparency transparency-transparency>transparency transparencyNtransparencyotransparencyntransparencyetransparency:
        """
        The transparency color of frame that is treated as transparent, expressed as 1D numpy array.
        For more info, refer to 'tRNS Transparency' in http://www.libpng.org/pub/png/spec/1.2/PNG-Chunks.html
        """
        ...
    
    @property
    def transparency_size(transparency_sizestransparency_sizeetransparency_sizeltransparency_sizeftransparency_size)transparency_size transparency_size-transparency_size>transparency_size transparency_sizeitransparency_sizentransparency_sizettransparency_size:
        """
        The transparency data size of frame.
        """
        ...
    @transparency_size.setter
    def transparency_size(transparency_sizestransparency_sizeetransparency_sizeltransparency_sizeftransparency_size,transparency_size transparency_sizeatransparency_sizertransparency_sizegtransparency_size:transparency_size transparency_sizeitransparency_sizentransparency_sizettransparency_size,transparency_size transparency_size/transparency_size)transparency_size transparency_size-transparency_size>transparency_size transparency_sizeNtransparency_sizeotransparency_sizentransparency_sizeetransparency_size:
        """
        The transparency data size of frame.
        """
        ...
    
    @property
    def width(widthswidthewidthlwidthfwidth)width width-width>width widthiwidthnwidthtwidth:
        """
        The width of frame.
        """
        ...
    @width.setter
    def width(widthswidthewidthlwidthfwidth,width widthawidthrwidthgwidth:width widthiwidthnwidthtwidth,width width/width)width width-width>width widthNwidthowidthnwidthewidth:
        """
        The width of frame.
        """
        ...
    
class IAPNGAsmListener:
    """
    Class for APNGAsmListener. Meant to be used internally.
    """

    def __init__(*args, **kwargs):
        """
        Initialize self.  See help(type(self)) for accurate signature.
        """
        ...
    
def create_frame_from_rgb(pixels: numpy.typing.NDArray, width: int, height: int, delay_num: int = 100, delay_den: int = 1000) -> _apngasm_python.APNGFrame:
    """
    Creates an APNGFrame from a bitmapped array of RBG pixel data.
    
    :param numpy.typing.NDArray pixels: The RGB pixel data, expressed as 3D numpy array.
    :param int width: The width of the pixel data.
    :param int height: The height of the pixel data.
    :param int delay_num: The delay numerator for this frame (defaults to DEFAULT_FRAME_NUMERATOR).
    :param int delay_den: The delay denominator for this frame (defaults to DEFAULT_FRAME_DENMINATOR).
    
    :return: A APNGFrame object.
    :rtype: apngasm_python._apngasm_python.APNGFrame
    """
    ...

def create_frame_from_rgb_trns(pixels: numpy.typing.NDArray, width: int, height: int, trns_color: numpy.typing.NDArray, delay_num: int = 100, delay_den: int = 1000) -> _apngasm_python.APNGFrame:
    """
    Creates an APNGFrame from a bitmapped array of RBG pixel data, with one color treated as transparent.
    
    :param numpy.typing.NDArray pixels: The RGB pixel data, expressed as 3D numpy array.
    :param int width: The width of the pixel data.
    :param int height: The height of the pixel data.
    :param numpy.typing.NDArray trns_color: The color [r, g, b] to be treated as transparent, expressed as 1D numpy array.
    :param int delay_num: The delay numerator for this frame (defaults to DEFAULT_FRAME_NUMERATOR).
    :param int delay_den: The delay denominator for this frame (defaults to DEFAULT_FRAME_DENMINATOR).
    
    :return: A APNGFrame object.
    :rtype: apngasm_python._apngasm_python.APNGFrame
    """
    ...

def create_frame_from_rgba(pixels: numpy.typing.NDArray, width: int, height: int, delay_num: int = 100, delay_den: int = 1000) -> _apngasm_python.APNGFrame:
    """
    Creates an APNGFrame from a bitmapped array of RBGA pixel data.
    
    :param numpy.typing.NDArray pixels: The RGBA pixel data, expressed as 3D numpy array.
    :param int width: The width of the pixel data.
    :param int height: The height of the pixel data.
    :param int delay_num: The delay numerator for this frame (defaults to DEFAULT_FRAME_NUMERATOR)
    :param int delay_den: The delay denominator for this frame (defaults to DEFAULT_FRAME_DENMINATOR)
    
    :return: A APNGFrame object.
    :rtype: apngasm_python._apngasm_python.APNGFrame
    """
    ...

class rgb:
    """
    Class for RGB object. Meant to be used internally.
    """

    def __init__(self, arg0: int, arg1: int, arg2: int, /) -> None:
        """
        Create a RGB object. Meant to be used internally.
        """
        ...
    
    @overload
    def __init__(self) -> None:
        """
        Create an empty RGB object. Meant to be used internally.
        """
        ...
    
    @property
    def b(bsbeblbfb)b b-b>b bibnbtb:
        ...
    @b.setter
    def b(bsbeblbfb,b babrbgb:b bibnbtb,b b/b)b b-b>b bNbobnbeb:
        ...
    
    @property
    def g(gsgeglgfg)g g-g>g gigngtg:
        ...
    @g.setter
    def g(gsgeglgfg,g gagrggg:g gigngtg,g g/g)g g-g>g gNgogngeg:
        ...
    
    @property
    def r(rsrerlrfr)r r-r>r rirnrtr:
        ...
    @r.setter
    def r(rsrerlrfr,r rarrrgr:r rirnrtr,r r/r)r r-r>r rNrornrer:
        ...
    
class rgba:
    """
    Class for RGBA object. Meant to be used internally.
    """

    def __init__(self, arg0: int, arg1: int, arg2: int, arg3: int, /) -> None:
        """
        Create a RGBA object. Meant to be used internally.
        """
        ...
    
    @overload
    def __init__(self) -> None:
        """
        Create an empty RGBA object. Meant to be used internally.
        """
        ...
    
    @property
    def a(asaealafa)a a-a>a aianata:
        ...
    @a.setter
    def a(asaealafa,a aaaraga:a aianata,a a/a)a a-a>a aNaoanaea:
        ...
    
    @property
    def b(bsbeblbfb)b b-b>b bibnbtb:
        ...
    @b.setter
    def b(bsbeblbfb,b babrbgb:b bibnbtb,b b/b)b b-b>b bNbobnbeb:
        ...
    
    @property
    def g(gsgeglgfg)g g-g>g gigngtg:
        ...
    @g.setter
    def g(gsgeglgfg,g gagrggg:g gigngtg,g g/g)g g-g>g gNgogngeg:
        ...
    
    @property
    def r(rsrerlrfr)r r-r>r rirnrtr:
        ...
    @r.setter
    def r(rsrerlrfr,r rarrrgr:r rirnrtr,r r/r)r r-r>r rNrornrer:
        ...
    
