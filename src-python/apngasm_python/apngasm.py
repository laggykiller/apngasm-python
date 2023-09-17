#!/usr/bin/env python3
from ._apngasm_python import APNGAsm, APNGFrame, IAPNGAsmListener, create_frame_from_rgb, create_frame_from_rgba
from ._apngasm_python import __version__
import numpy as np
from PIL import Image
from typing import Optional

class APNGAsmBinder:
    # https://www.w3.org/TR/PNG-Chunks.html
    color_type_dict = {
        0: 'L',
        2: 'RGB',
        3: 'P',
        4: 'LA',
        6: 'RGBA'
    }

    def __init__(self):
        self.apngasm = APNGAsm()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.apngasm.reset()
    
    def frame_pixels_as_pillow(self, frame: int, new_value: Optional[list] = None) -> Optional[Image.Image]:
        '''
        Get/Set the raw pixel data of frame, expressed as a Pillow object.
        This should be set AFTER you set the width, height and color_type.
        
        :param int frame: Target frame number.
        :param list new_value: (Optional) If set, then the raw pixel data of frame 
            is set with this value.
        
        :return: Pillow image object of the frame (get) or None (set)
        :rtype: PIL.Image.Image or None
        '''
        if new_value:
            self.apngasm.get_frames()[frame].pixels = np.array(new_value).flatten()
        else:
            mode = self.color_type_dict[self.apngasm.get_frames()[frame].color_type]
            return Image.frombytes(mode, (self.apngasm.get_frames()[frame].width, self.apngasm.get_frames()[frame].height), self.apngasm.get_frames()[frame].pixels)
    
    def frame_pixels_as_numpy(self, frame: int, new_value: Optional[list] = None) -> Optional[np.ndarray]:
        '''
        Get/Set the raw pixel data of frame, expressed as a 1D numpy array.
        This should be set AFTER you set the width, height and color_type.

        :param int frame: Target frame number.
        :param list new_value: (Optional) If set, then the raw pixel data of frame 
            is set with this value.

        :return: 1D numpy array representation of raw pixel data of frame (get) or None (set)
        :rtype: numpy.ndarray or None
        '''
        if new_value:
            self.apngasm.get_frames()[frame].pixels = new_value
        else:
            return self.apngasm.get_frames()[frame].pixels
    
    def frame_width(self, frame: int, new_value: Optional[int] = None) -> Optional[int]:
        '''
        Get/Set the width of frame.
        
        :param int frame: Target frame number.
        :param int new_value: (Optional) If set, then the width of frame 
            is set with this value.

        :return: width (get) or None (set)
        :rtype: int or None
        '''
        if new_value:
            self.apngasm.get_frames()[frame].width = new_value
        else:
            return self.apngasm.get_frames()[frame].width
    
    def frame_height(self, frame: int, new_value: Optional[int] = None) -> Optional[int]:
        '''
        Get/Set the height of frame.
        
        :param int frame: Target frame number.
        :param int new_value: (Optional) If set, then the height of frame 
            is set with this value.

        :return: height (get) or None (set)
        :rtype: int or None
        '''
        if new_value:
            self.apngasm.get_frames()[frame].height = new_value
        else:
            return self.apngasm.get_frames()[frame].height
        
    def frame_color_type(self, frame: int, new_value: Optional[int] = None) -> Optional[int]:
        '''
        Get/Set the color_type of frame.

        0: Grayscale (Pillow mode='L')
        2: RGB (Pillow mode='RGB')
        3: Palette (Pillow mode='P')
        4: Grayscale + Alpha (Pillow mode='LA')
        6: RGBA (Pillow mode='RGBA')
        
        :param int frame: Target frame number.
        :param int new_value: (Optional) If set, then the color type of frame 
            is set with this value.
        
        :return: color_type of frame (get) or None (set)
        :rtype: int or None
        '''
        if new_value:
            self.apngasm.get_frames()[frame].color_type = new_value
        else:
            return self.apngasm.get_frames()[frame].color_type
    
    def frame_palette(self, frame: int, new_value: Optional[np.ndarray] = None) -> Optional[np.ndarray]:
        '''
        Get/Set the palette data of frame. Only applies to 'P' mode Image (i.e. Not RGB, RGBA)
        Expressed as 2D numpy array in format of [[r0, g0, b0], [r1, g1, b1], ..., [r255, g255, b255]]
        
        :param int frame: Target frame number.
        :param np.ndarray new_value: (Optional) If set, then the palette data of frame 
            is set with this value.

        :return: 2D numpy array representation of palette data of frame (get) or None (set)
        :rtype: numpy.ndarray or None
        '''
        if new_value:
            self.apngasm.get_frames()[frame].palette = new_value
        else:
            return self.apngasm.get_frames()[frame].palette

    def frame_transparency(self, frame: int, new_value: Optional[int] = None) -> Optional[np.ndarray]:
        '''
        Get/Set the transparency data of frame. Expressed as 1D numpy array.
        
        :param int frame: Target frame number.
        :param int new_value: (Optional) If set, then the transparency of frame 
            is set with this value.

        :return: 1D numpy array representation of transparency data of frame (get) or None (set)
        :rtype: numpy.ndarray or None
        '''
        if new_value:
            self.apngasm.get_frames()[frame].transparency = new_value
        else:
            return self.apngasm.get_frames()[frame].transparency

    def frame_palette_size(self, frame: int, new_value: Optional[int] = None) -> Optional[int]:
        '''
        Get/Set the palette data size of frame.
        
        :param int frame: Target frame number.
        :param int new_value: (Optional) If set, then the palette data size of frame 
            is set with this value.

        :return: Palette data size of frame (get) or None (set)
        :rtype: int or None
        '''
        if new_value:
            self.apngasm.get_frames()[frame].palette_size = new_value
        else:
            return self.apngasm.get_frames()[frame].palette_size
    
    def frame_transparency_size(self, frame: int, new_value: Optional[int] = None) -> Optional[int]:
        '''
        Get/Set the transparency data size of frame.
        
        :param int frame: Target frame number.
        :param int new_value: (Optional) If set, then the transparency data size of frame 
            is set with this value.
        
        :return: Transparency data size of frame (get) or None (set)
        :rtype: int or None
        '''
        if new_value:
            self.apngasm.get_frames()[frame].transparency_size = new_value
        else:
            return self.apngasm.get_frames()[frame].transparency_size
    
    def frame_delay_num(self, frame: int, new_value: Optional[int] = None) -> Optional[int]:
        '''
        Get/Set the nominator of the duration of frame.
        Duration of time is delay_num / delay_den seconds.
        
        :param int frame: Target frame number.
        :param int new_value: (Optional) If set, then the nominator of the duration of frame
            is set with this value.
        
        :return: Nominator of the duration of frame.
        :rtype: int or None
        '''
        if new_value:
            self.apngasm.get_frames()[frame].delay_num = new_value
        else:
            return self.apngasm.get_frames()[frame].delay_num
    
    def frame_delay_den(self, frame: int, new_value: Optional[int] = None) -> Optional[int]:
        '''
        Get/Set the denominator of the duration of frame.
        Duration of time is delay_num / delay_den seconds.
        
        :param int frame: Target frame number.
        :param int new_value: (Optional) If set, then the denominator of the duration of frame
            is set with this value.
        
        :return: Denominator of the duration of frame.
        :rtype: int or None
        '''
        if new_value:
            self.apngasm.get_frames()[frame].delay_den = new_value
        else:
            return self.apngasm.get_frames()[frame].delay_den
    
    def add_frame_from_file(self, file_path: str, delay_num: int = 100, delay_den: int = 1000) -> int:
        '''
        Adds a frame from a PNG file or frames from a APNG file to the frame vector.
        
        :param str file_path: The relative or absolute path to an image file.
        :param int delay_num: The delay numerator for this frame (defaults to 100).
        :param int delay_den: The delay denominator for this frame (defaults to 1000).
        
        :return: The new number of frames.
        :rtype: int
        '''
        return self.apngasm.add_frame_from_file(
            file_path=file_path,
            delay_num=delay_num,
            delay_den=delay_den
        )
    
    def add_frame_from_pillow(self, pillow_image: Image.Image, delay_num: int = 100, delay_den: int = 1000) -> int:
        '''
        Add a frame from Pillow image.
        The frame duration is equal to delay_num / delay_den seconds.
        Default frame duration is 100/1000 second, or 0.1 second.
        
        :param PIL.Image.Image pillow_image: Pillow image object.
        :param int delay_num: The delay numerator for this frame (defaults to 100).
        :param int delay_den: The delay denominator for this frame (defaults to 1000).
        
        :return: The new number of frames.
        :rtype: int
        '''
        if pillow_image.mode not in ('RGB', 'RGBA'):
            pillow_image = pillow_image.convert('RGBA')
        return self.add_frame_from_numpy(
            numpy_data=np.array(pillow_image).flatten(),
            width=pillow_image.width,
            height=pillow_image.height,
            mode=pillow_image.mode,
            delay_num=delay_num,
            delay_den=delay_den
        )
    
    def add_frame_from_numpy(self, numpy_data: int, width: int, height: int, trns_color: int = None, 
                             mode: str = 'RGBA', delay_num: int = 100, delay_den: int = 1000) -> int:
        '''
        Add frame from numpy array.
        The frame duration is equal to delay_num / delay_den seconds.
        Default frame duration is 100/1000 second, or 0.1 second.
        
        :param int numpy_data: The pixel data, expressed as 1D numpy array. 
            For example: [r0, g0, b0, r1, g1, b1, ...]
        :param int width: The width of the pixel data.
        :param int height: The height of the pixel data.
        :param str mode: The color mode of data. Possible values are RGB or RGBA.
        :param int trns_color: An array of transparency data, expressed as 1D numpy array.
            Only use if RGB mode.
        :param int delay_num: The delay numerator for this frame (defaults to 100).
        :param int delay_den: The delay denominator for this frame (defaults to 1000).
        
        :return: The new number of frames.
        :rtype: int
        '''
        if mode == 'RGB':
            frame = create_frame_from_rgb(
                pixels=numpy_data,
                width=width,
                height=height,
                trns_color=trns_color,
                delay_num=delay_num,
                delay_den=delay_den
            )
        elif mode == 'RGBA':
            frame = create_frame_from_rgba(
                pixels=numpy_data,
                width=width,
                height=height,
                delay_num=delay_num,
                delay_den=delay_den
            )
        else:
            raise TypeError(f'Invalid mode: {mode}. Must be RGB or RGBA.')

        return self.apngasm.add_frame(frame)

    def assemble(self, output_path: str) -> bool:
        '''
        Assembles and outputs an APNG file.
        
        :param str output_path: The output file path.
        
        :return: true if assemble completed succesfully.
        :rtype: bool
        '''
        return self.apngasm.assemble(output_path)
    
    def disassemble_as_numpy(self, file_path: str) -> list:
        '''
        Disassembles an APNG file to a list of frames, expressed as 1D numpy array.
        
        :param str file_path: The file path to the PNG image to be disassembled.
        
        :return: A list containing the frames of the disassembled PNG.
        :rtype: list
        '''
        return self.apngasm.disassemble(file_path)

    def disassemble_as_pillow(self, file_path: str) -> list:
        '''
        Disassembles an APNG file to a list of frames, expressed as Pillow images.
        
        :param str file_path: The file path to the PNG image to be disassembled.
        
        :return: A list containing the frames of the disassembled PNG.
        :rtype: list
        '''
        frames_numpy = self.apngasm.disassemble(file_path)
        frames_pillow = []
        for frame in frames_numpy:
            mode = self.color_type_dict[frame.color_type]
            frame_pillow = Image.frombytes(mode, (frame.width, frame.height), frame.pixels)
            frames_pillow.append(frame_pillow)
        
        return frames_pillow
    
    def save_pngs(self, output_dir: str) -> bool:
        '''
        Saves individual PNG files of the frames in the frame vector.
        
        :param str output_dir: The directory where the PNG fils will be saved.
        
        :return: true if all files were saved successfully.
        :rtype: bool
        '''
        return self.apngasm.save_pngs(output_dir)
    
    def load_animation_spec(self, file_path: str) -> list:
        '''
        Loads an animation spec from JSON or XML.
        Loaded frames are added to the end of the frame vector.
        For more details on animation specs see:
        https://github.com/Genshin/PhantomStandards
        You probably won't need to use this function

        :param str file_path: The path of JSON or XML file

        :return: A vector containing the loaded frames
        :rtype: list
        '''
        return self.apngasm.load_animation_spec(file_path)
    
    def save_json(self, output_path: str, image_dir: str) -> bool:
        '''
        Saves a JSON animation spec file.
        You probably won't need to use this function
        
        :param str output_path: Path to save the file to.
        :param str image_dir: Directory where frame files are to be saved
            if not the same path as the animation spec.
        
        :return: true if save was successful.
        :rtype: bool
        '''
        return self.apngasm.save_json(output_path, image_dir)
    
    def save_xml(self, output_path: str, image_dir: str) -> bool:
        '''
        Saves an XML animation spec file.
        
        :param str filePath: Path to save the file to.
        :param str image_dir: Directory where frame files are to be saved
            if not the same path as the animation spec.

        :return: true if save was successful.
        :rtype: bool
        '''
        return self.apngasm.save_xml(output_path, image_dir)

    def set_apng_asm_listener(self, listener: IAPNGAsmListener = None):
        '''
        Sets a listener.
        You probably won't need to use this function
        
        :param apngasm_python.apngasm.IAPNGAsmListener listener: A pointer to the listener object.
            If the argument is None,
            a default APNGAsmListener will be created and assigned.
        '''
        return self.apngasm.set_apng_asm_listener(listener)

    def set_loops(self, loops: int = 0):
        '''
        Set loop count of animation.
        
        :param int loops: Loop count of animation. If the argument is 0 a loop count is infinity.
        '''
        return self.apngasm.set_loops(loops)
    
    def set_skip_first(self, skip_first: int):
        '''
        Set flag of skip first frame.

        :param int skip_first: Flag of skip first frame.
        '''
        return self.apngasm.set_skip_first(skip_first)

    def get_frames(self) -> np.ndarray:
        '''
        Returns the frame vector.

        :return: frame vector
        :rtype: numpy.ndarray
        '''
        return self.apngasm.get_frames()
    
    def get_loops(self) -> int:
        '''
        Returns the loop count.

        :return: loop count
        :rtype: int
        '''
        return self.apngasm.get_loops()
    
    def is_skip_first(self) -> int:
        '''
        Returns the flag of skip first frame.

        :return: flag of skip first frame
        :rtype: int
        '''
        return self.apngasm.get_loops()

    def frame_count(self) -> int:
        '''
        Returns the number of frames.

        :return: number of frames
        :rtype: int
        '''
        return self.apngasm.frame_count()
    
    def reset(self) -> int:
        '''
        Destroy all frames in memory/dispose of the frame vector.
        Leaves the apngasm object in a clean state.
        Returns number of frames disposed of.

        :return: number of frames disposed of
        :rtype: int
        '''
        return self.apngasm.reset()

    def version(self) -> str:
        '''
        Returns the version of APNGAsm.

        :return: version of APNGAsm.
        :rtype: str
        '''
        return self.apngasm.version()

