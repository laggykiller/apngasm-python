from ._apngasm_python import APNGAsm, APNGFrame, create_frame_from_rgb, create_frame_from_rgba
from ._apngasm_python import __version__
import numpy as np
from PIL import Image

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

    def __del__(self):
        self.apngasm.reset()
        del self.apngasm
    
    def frame_pixels_as_pillow(self, frame, new_value=None):
        '''
        Get/Set the raw pixel data of frame, expressed as a Pillow object.
        This should be set AFTER you set the width, height and color_type.
        ===
        frame: Target frame number.
        new_value: If set, then the raw pixel data of frame is set with this value.
        '''
        if new_value:
            self.apngasm.get_frames()[frame].pixels = np.array(new_value).flatten()
        else:
            mode = self.color_type_dict[self.apngasm.get_frames()[frame].color_type]
            return Image.frombytes(mode, (self.apngasm.get_frames()[frame].width, self.apngasm.get_frames()[frame].height), self.apngasm.get_frames()[frame].pixels)
    
    def frame_pixels_as_numpy(self, frame, new_value=None):
        '''
        Get/Set the raw pixel data of frame, expressed as a 1D numpy array.
        This should be set AFTER you set the width, height and color_type.
        ===
        frame: Target frame number.
        new_value: If set, then the raw pixel data of frame is set with this value.
        '''
        if new_value:
            self.apngasm.get_frames()[frame].pixels = new_value
        else:
            return self.apngasm.get_frames()[frame].pixels
    
    def frame_width(self, frame, new_value=None):
        '''
        Get/Set the width of frame.
        ===
        frame: Target frame number.
        new_value: If set, then the width of frame is set with this value.
        '''
        if new_value:
            self.apngasm.get_frames()[frame].width = new_value
        else:
            return self.apngasm.get_frames()[frame].width
    
    def frame_height(self, frame, new_value=None):
        '''
        Get/Set the height of frame.
        ===
        frame: Target frame number.
        new_value: If set, then the height of frame is set with this value.
        '''
        if new_value:
            self.apngasm.get_frames()[frame].height = new_value
        else:
            return self.apngasm.get_frames()[frame].height
        
    def frame_color_type(self, frame, new_value=None):
        '''
        Get/Set the color_type of frame.
        ===
        frame: Target frame number.
        new_value: If set, then the color type of frame is set with this value.
        ===
        0: Grayscale (Pillow mode='L')
        2: RGB (Pillow mode='RGB')
        3: Palette (Pillow mode='P')
        4: Grayscale + Alpha (Pillow mode='LA')
        6: RGBA (Pillow mode='RGBA')
        '''
        if new_value:
            self.apngasm.get_frames()[frame].color_type = new_value
        else:
            return self.apngasm.get_frames()[frame].color_type
    
    def frame_palette(self, frame, new_value=None):
        '''
        Get/Set the palette data of frame. Only applies to 'P' mode Image (i.e. Not RGB, RGBA)
        Expressed as 2D numpy array in format of [[r0, g0, b0], [r1, g1, b1], ..., [r255, g255, b255]]
        ===
        frame: Target frame number.
        new_value: If set, then the palette data of frame is set with this value.
        '''
        if new_value:
            self.apngasm.get_frames()[frame].palette = new_value
        else:
            return self.apngasm.get_frames()[frame].palette

    def frame_transparency(self, frame, new_value=None):
        '''
        Get/Set the transparency data of frame. Expressed as 1D numpy array.
        ===
        frame: Target frame number.
        new_value: If set, then the transparency of frame is set with this value.
        '''
        if new_value:
            self.apngasm.get_frames()[frame].transparency = new_value
        else:
            return self.apngasm.get_frames()[frame].transparency

    def frame_palette_size(self, frame, new_value=None):
        '''
        Get/Set the palette data size of frame.
        ===
        frame: Target frame number.
        new_value: If set, then the palette data size of frame is set with this value.
        '''
        if new_value:
            self.apngasm.get_frames()[frame].palette_size = new_value
        else:
            return self.apngasm.get_frames()[frame].palette_size
    
    def frame_transparency_size(self, frame, new_value=None):
        '''
        Get/Set the transparency data size of frame.
        ===
        frame: Target frame number.
        new_value: If set, then the transparency data size of frame is set with this value.
        '''
        if new_value:
            self.apngasm.get_frames()[frame].transparency_size = new_value
        else:
            return self.apngasm.get_frames()[frame].transparency_size
    
    def frame_delay_num(self, frame, new_value=None):
        '''
        Get/Set the nominator of the duration of frame. Duration of time is delay_num / delay_den seconds.
        ===
        frame: Target frame number.
        new_value: If set, then the nominator of the duration of frame is set with this value.
        '''
        if new_value:
            self.apngasm.get_frames()[frame].delay_num = new_value
        else:
            return self.apngasm.get_frames()[frame].delay_num
    
    def frame_delay_den(self, frame, new_value=None):
        '''
        Get/Set the denominator of the duration of frame. Duration of time is delay_num / delay_den seconds.
        ===
        frame: Target frame number.
        new_value: If set, then the denominator of the duration of frame is set with this value.
        '''
        if new_value:
            self.apngasm.get_frames()[frame].delay_den = new_value
        else:
            return self.apngasm.get_frames()[frame].delay_den
    
    def add_frame_from_file(self, file_path, delay_num=100, delay_den=1000):
        '''
        Adds a frame from a PNG file or frames from a APNG file to the frame vector.
        ===
        file_path: The relative or absolute path to an image file.
        delay_num: The delay numerator for this frame (defaults to 100).
        delay_den: The delay denominator for this frame (defaults to 1000).
        Returns: The [new] number of frames.
        '''
        return self.apngasm.add_frame_from_file(
            file_path=file_path,
            delay_num=delay_num,
            delay_den=delay_den
        )
    
    def add_frame_from_pillow(self, pillow_image, delay_num=100, delay_den=1000):
        '''
        Add a frame from Pillow image.
        The frame duration is equal to delay_num / delay_den seconds.
        Default frame duration is 100/1000 second, or 0.1 second.
        ===
        pillow_image: Pillow image object.
        delay_num: The delay numerator for this frame (defaults to 100).
        delay_den: The delay denominator for this frame (defaults to 1000).
        Returns: The [new] number of frames.
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
    
    def add_frame_from_numpy(self, numpy_data, width, height, trns_color=None, 
                             mode='RGBA', delay_num=100, delay_den=1000):
        '''
        Add frame from numpy array.
        The frame duration is equal to delay_num / delay_den seconds.
        Default frame duration is 100/1000 second, or 0.1 second.
        ===
        numpy_data: The pixel data, expressed as 1D numpy array.
                    For example: [r0, g0, b0, r1, g1, b1, ...]
        width: The width of the pixel data.
        height: The height of the pixel data.
        mode: The color mode of data. Possible values are RGB or RGBA.
        trns_color: An array of transparency data, expressed as 1D numpy array.
                    Only use if RGB mode.
        delay_num: The delay numerator for this frame (defaults to 100).
        delay_den: The delay denominator for this frame (defaults to 1000).
        Returns: The [new] number of frames.
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

    def assemble(self, output_path):
        '''
        Assembles and outputs an APNG file.
        ===
        output_path: The output file path.
        Returns: true if assemble completed succesfully.
        '''
        return self.apngasm.assemble(output_path)
    
    def disassemble_as_numpy(self, file_path):
        '''
        Disassembles an APNG file to a list of frames, expressed as 1D numpy array.
        ===
        file_path: The file path to the PNG image to be disassembled.
        Returns: A list containing the frames of the disassembled PNG.
        '''
        return self.apngasm.disassemble(file_path)

    def disassemble_as_pillow(self, file_path):
        '''
        Disassembles an APNG file to a list of frames, expressed as Pillow images.
        ===
        file_path: The file path to the PNG image to be disassembled.
        Returns: A list containing the frames of the disassembled PNG.
        '''
        frames_numpy = self.apngasm.disassemble(file_path)
        frames_pillow = []
        for frame in frames_numpy:
            mode = self.color_type_dict[frame.color_type]
            frame_pillow = Image.frombytes(mode, (frame.width, frame.height), frame.pixels)
            frames_pillow.append(frame_pillow)
        
        return frames_pillow
    
    def save_pngs(self, output_dir):
        '''
        Saves individual PNG files of the frames in the frame vector.
        ===
        output_dir: The directory where the PNG fils will be saved.
        Returns: true if all files were saved successfully.
        '''
        return self.apngasm.save_pngs(output_dir)
    
    def load_animation_spec(self, file_path):
        '''
        Loads an animation spec from JSON or XML.
        Loaded frames are added to the end of the frame vector.
        For more details on animation specs see:
        https://github.com/Genshin/PhantomStandards
        You probably won't need to use this function
        '''
        return self.apngasm.load_animation_spec(file_path)
    
    def save_json(self, output_path, image_dir):
        '''
        Saves a JSON animation spec file.
        You probably won't need to use this function
        ===
        output_path: Path to save the file to.
        image_dir: Directory where frame files are to be saved
                   if not the same path as the animation spec.
        Returns: true if save was successful.
        '''
        return self.apngasm.save_json(output_path, image_dir)
    
    def save_xml(self, output_path, image_dir):
        '''
        Saves an XML animation spec file.
        ===
        filePath: Path to save the file to.
        imageDir: Directory where frame files are to be saved
                  if not the same path as the animation spec.
        Returns: true if save was successful.
        '''
        return self.apngasm.save_xml(output_path, image_dir)

    def set_apng_asm_listener(self, listener=None):
        '''
        Sets a listener.
        You probably won't need to use this function
        ===
        listener: A pointer to the listener object.
        If the argument is None,
        a default APNGAsmListener will be created and assigned.
        '''
        return self.apngasm.set_apng_asm_listener(listener)

    def set_loops(self, loops=0):
        '''
        Set loop count of animation.
        loops: Loop count of animation. If the argument is 0 a loop count is infinity.
        '''
        return self.apngasm.set_loops(loops)
    
    def set_skip_first(self, skip_first):
        '''
        Set flag of skip first frame.
        skip_first: Flag of skip first frame.
        '''
        return self.apngasm.set_skip_first(skip_first)

    def get_frames(self):
        '''
        Returns the frame vector.
        '''
        return self.apngasm.get_frames()
    
    def get_loops(self):
        '''
        Returns the loop count.
        '''
        return self.apngasm.get_loops()
    
    def is_skip_first(self):
        '''
        Returns the flag of skip first frame.
        '''
        return self.apngasm.get_loops()

    def frame_count(self):
        '''
        Returns the number of frames.
        '''
        return self.apngasm.frame_count()
    
    def reset(self):
        '''
        Destroy all frames in memory/dispose of the frame vector.
        Leaves the apngasm object in a clean state.
        Retruns number of frames disposed of.
        '''
        return self.apngasm.reset()

    def version(self):
        '''
        Returns the version of APNGAsm.
        '''
        return self.apngasm.version()

