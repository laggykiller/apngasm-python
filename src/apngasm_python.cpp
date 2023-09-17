#ifdef _WINDOWS
#  ifdef _apngasm_python_EXPORTS
#    define APNGASM_PY_DECLSPEC __declspec(dllexport)
#  else
#    define APNGASM_PY_DECLSPEC __declspec(dllimport)
#  endif
#else
#  define APNGASM_PY_DECLSPEC __attribute__ ((visibility("default")))
#endif

#include <nanobind/nanobind.h>
#include <nanobind/stl/string.h>
#include <nanobind/stl/vector.h>
#include <nanobind/stl/optional.h>
#include <nanobind/ndarray.h>
#include <nanobind/operators.h>
#include <map>

#include "png.h"
#include "apngframe.h"
#include "apngasm.h"
#include "apngasmlistener.h"

namespace nb = nanobind;
using namespace nb::literals;

std::map<int, int> rowbytesMap = {
    { 0, 1 }, // Grayscale
    { 2, 3 }, // RGB
    { 3, 1 }, // Palette
    { 4, 2 }, // Grayscale + A
    { 6, 4 }  // RGBA
};

nb::object create_frame_from_rgb(nb::ndarray<unsigned char, nb::shape<nb::any>> *pixels,
    unsigned int width, unsigned int height, nb::ndarray<unsigned char, nb::shape<nb::any>> *trns_color = NULL,
    unsigned delayNum = apngasm::DEFAULT_FRAME_NUMERATOR,
    unsigned delayDen = apngasm::DEFAULT_FRAME_DENOMINATOR) {

        apngasm::rgb *pixelsNew = new apngasm::rgb[pixels->shape(0)];
        unsigned char *pixels_ptr = pixels->data();
        for (int i = 0; i < pixels->shape(0) / 3; ++i) {
            pixelsNew[i].r = pixels_ptr[3 * i];
            pixelsNew[i].g = pixels_ptr[3 * i + 1];
            pixelsNew[i].b = pixels_ptr[3 * i + 2];
        }

        apngasm::rgb *trns_colorNew = new apngasm::rgb[trns_color->shape(0)];
        unsigned char *trns_color_ptr = trns_color->data();
        for (int i = 0; i < trns_color->shape(0) / 3; ++i) {
            trns_colorNew[i].r = trns_color_ptr[3 * i];
            trns_colorNew[i].g = trns_color_ptr[3 * i + 1];
            trns_colorNew[i].b = trns_color_ptr[3 * i + 2];
        }

        const apngasm::APNGFrame &frame = apngasm::APNGFrame(pixelsNew, width, height, trns_colorNew, delayNum, delayDen);
        delete[] pixelsNew;
        delete[] trns_colorNew;
        return nb::cast(frame);
}

nb::object create_frame_from_rgba(nb::ndarray<unsigned char, nb::shape<nb::any>> *pixels,
    unsigned int width, unsigned int height,
    unsigned delayNum = apngasm::DEFAULT_FRAME_NUMERATOR,
    unsigned delayDen = apngasm::DEFAULT_FRAME_DENOMINATOR) {

        apngasm::rgba *pixelsNew = new apngasm::rgba[pixels->shape(0)];
        unsigned char *pixels_ptr = pixels->data();

        for (int i = 0; i < pixels->shape(0) / 4; ++i) {
            pixelsNew[i].r = pixels_ptr[4 * i];
            pixelsNew[i].g = pixels_ptr[4 * i + 1];
            pixelsNew[i].b = pixels_ptr[4 * i + 2];
            pixelsNew[i].a = pixels_ptr[4 * i + 3];
        }

        const apngasm::APNGFrame frame(pixelsNew, width, height, delayNum, delayDen);
        delete[] pixelsNew;
        return nb::cast(frame);
}

NB_MODULE(MODULE_NAME, m) {
    m.doc() = "A nanobind API for apngasm, a tool/library for APNG assembly/disassembly";
    m.attr("__version__") = VERSION_INFO;

    m.def("create_frame_from_rgb", &create_frame_from_rgb,
        "pixels"_a, "width"_a, "height"_a, "trns_color"_a = NULL, "delay_num"_a = apngasm::DEFAULT_FRAME_NUMERATOR, "delay_den"_a = apngasm::DEFAULT_FRAME_DENOMINATOR,
        R"pbdoc(
            Creates an APNGFrame from a bitmapped array of RBG pixel data.
            
            :param int pixels: The RGB pixel data, expressed as 1D numpy array.
            :param int width: The width of the pixel data.
            :param int height: The height of the pixel data.
            :param numpy.ndarray trns_color: An array of transparency data, expressed as 1D numpy array.
            :param int delay_num: The delay numerator for this frame (defaults to DEFAULT_FRAME_NUMERATOR).
            :param int delay_den: The delay denominator for this frame (defaults to DEFAULT_FRAME_DENMINATOR).
            
            :return: A APNGFrame object.
            :rtype: apngasm_python._apngasm_python.APNGFrame
        )pbdoc");
    
    m.def("create_frame_from_rgba", &create_frame_from_rgba,
        "pixels"_a, "width"_a, "height"_a, "delay_num"_a = apngasm::DEFAULT_FRAME_NUMERATOR, "delay_den"_a = apngasm::DEFAULT_FRAME_DENOMINATOR,
        R"pbdoc(
            Creates an APNGFrame from a bitmapped array of RBGA pixel data.
            
            :param pixels: The RGBA pixel data, expressed as 1D numpy array.
            :param width: The width of the pixel data.
            :param height: The height of the pixel data.
            :param delay_num: The delay numerator for this frame (defaults to DEFAULT_FRAME_NUMERATOR)
            :param delay_den: The delay denominator for this frame (defaults to DEFAULT_FRAME_DENMINATOR)

            :return: A APNGFrame object.
            :rtype: apngasm_python._apngasm_python.APNGFrame
        )pbdoc");
    
    nb::class_<apngasm::listener::IAPNGAsmListener>(m, "IAPNGAsmListener");

    nb::class_<apngasm::rgb>(m, "rgb")
        .def(nb::init<>(),
            R"pbdoc(
                Create an empty RGB object. Meant to be used internally.
            )pbdoc")

        .def(nb::init<unsigned char, unsigned char, unsigned char>(), 
            R"pbdoc(
                Create a RGB object. Meant to be used internally.
            )pbdoc")

        .def_rw("r", &apngasm::rgb::r)
        .def_rw("g", &apngasm::rgb::g)
        .def_rw("b", &apngasm::rgb::b);
    
    nb::class_<apngasm::rgba>(m, "rgba")
        .def(nb::init<>(),
            R"pbdoc(
                Create an empty RGBA object. Meant to be used internally.
            )pbdoc")
        .def(nb::init<unsigned char, unsigned char, unsigned char, unsigned char>(),
            R"pbdoc(
                Create a RGBA object. Meant to be used internally.
            )pbdoc")

        .def_rw("r", &apngasm::rgba::r)
        .def_rw("g", &apngasm::rgba::g)
        .def_rw("b", &apngasm::rgba::b)
        .def_rw("a", &apngasm::rgba::a);

    nb::class_<apngasm::APNGFrame>(m, "APNGFrame")
        .def(nb::init<>(),
            R"pbdoc(
                Creates an empty APNGFrame.
            )pbdoc")

        .def(nb::init<const std::string &, unsigned, unsigned>(),
            "file_path"_a, "delay_num"_a = apngasm::DEFAULT_FRAME_NUMERATOR, "delay_den"_a = apngasm::DEFAULT_FRAME_DENOMINATOR,
            R"pbdoc(
                Creates an APNGFrame from a PNG file.
                
                :param str file_path: The relative or absolute path to an image file.
                :param int delay_num: The delay numerator for this frame (defaults to DEFAULT_FRAME_NUMERATOR).
                :param int delay_den: The delay denominator for this frame (defaults to DEFAULT_FRAME_DENMINATOR).
            )pbdoc")

        // Exist in apngframe.h but not exist in apngframe.cpp
        // .def(nb::init<apngasm::rgb *, unsigned int, unsigned int, unsigned, unsigned>())

        .def(nb::init<apngasm::rgb *, unsigned int, unsigned int, apngasm::rgb *, unsigned, unsigned>(),
            "pixels"_a, "width"_a, "height"_a, "trns_color"_a, "delay_num"_a = apngasm::DEFAULT_FRAME_NUMERATOR, "delay_den"_a = apngasm::DEFAULT_FRAME_DENOMINATOR,
            R"pbdoc(
                Creates an APNGFrame from a bitmapped array of RBG pixel data.
                Not possible to use in Python. To create APNGFrame from pixel data in memory,
                Use create_frame_from_rgb() or create_frame_from_rgba(). Or manually,
                First create an empty APNGFrame with frame = APNGFrame(),
                then set frame.width, frame.height, frame.color_type, frame.pixels,
                frame.palette, frame.delay_num, frame.delay_den manually.
                
                :param pixels: The RGB pixel data.
                :param int width: The width of the pixel data.
                :param int height: The height of the pixel data.
                :param trns_color: An array of transparency data.
                :param int delay_num: The delay numerator for this frame (defaults to DEFAULT_FRAME_NUMERATOR).
                :param int delay_den: The delay denominator for this frame (defaults to DEFAULT_FRAME_DENMINATOR).
            )pbdoc")

        .def(nb::init<apngasm::rgba *, unsigned int, unsigned int, unsigned, unsigned>(),
            "pixels"_a, "width"_a, "height"_a, "delay_num"_a = apngasm::DEFAULT_FRAME_NUMERATOR, "delay_den"_a = apngasm::DEFAULT_FRAME_DENOMINATOR,
            R"pbdoc(
                Creates an APNGFrame from a bitmapped array of RBGA pixel data.
                Not possible to use in Python. To create APNGFrame from pixel data in memory,
                Use create_frame_from_rgb() or create_frame_from_rgba(). Or manually,
                First create an empty APNGFrame with frame = APNGFrame(),
                then set frame.width, frame.height, frame.color_type, frame.pixels,
                frame.palette, frame.delay_num, frame.delay_den manually.
                
                :param pixels: The RGBA pixel data.
                :param int width: The width of the pixel data.
                :param int height: The height of the pixel data.
                :param int delay_num: The delay numerator for this frame (defaults to DEFAULT_FRAME_NUMERATOR).
                :param int delay_den: The delay denominator for this frame (defaults to DEFAULT_FRAME_DENMINATOR).
            )pbdoc")

        .def("save", &apngasm::APNGFrame::save,
            "out_path"_a,
            R"pbdoc(
                Saves this frame as a single PNG file.
                
                :param str out_path: The relative or absolute path to save the image file to.
                
                :return: true if save was successful.
                :rtype: bool
            )pbdoc")

        .def_prop_rw("pixels", 
                    [](apngasm::APNGFrame &t) APNGASM_PY_DECLSPEC {
                        int rowbytes = rowbytesMap[t._colorType];
                        size_t shape[1] = { t._height * t._width * rowbytes };
                        return nb::cast(nb::ndarray<nb::numpy, unsigned char, nb::shape<nb::any>>(t._pixels, 1, shape));
                    },
                    [](apngasm::APNGFrame &t, nb::ndarray<unsigned char, nb::shape<nb::any>> *v) APNGASM_PY_DECLSPEC {
                        int rowbytes = rowbytesMap[t._colorType];
                        unsigned char *pixelsNew = new unsigned char[v->shape(0)];
                        unsigned char *v_ptr = v->data();
                        for (int i = 0; i < v->shape(0); ++i) {
                            pixelsNew[i] = *v_ptr;
                            ++v_ptr;
                        }
                        t._pixels = pixelsNew;

                        t._rows = new png_bytep[t._height * sizeof(png_bytep)];
                        for (int j = 0; j < t._height; ++j)
                            t._rows[j] = t._pixels + j * rowbytes;
                    },
                    R"pbdoc(
                        The raw pixel data of frame, expressed as a 1D numpy array in Python.
                        Note that setting this value will also set the variable 'rows' internally.
                        This should be set AFTER you set the width, height and color_type.
                    )pbdoc")

        .def_prop_rw("width", 
                    [](apngasm::APNGFrame &t) APNGASM_PY_DECLSPEC { return t._width; },
                    [](apngasm::APNGFrame &t, unsigned int v) APNGASM_PY_DECLSPEC { t.width(v); },
                    R"pbdoc(
                        The width of frame.
                    )pbdoc")

        .def_prop_rw("height", 
                    [](apngasm::APNGFrame &t) APNGASM_PY_DECLSPEC { return t._height; },
                    [](apngasm::APNGFrame &t, unsigned int v) APNGASM_PY_DECLSPEC { t.height(v); },
                    R"pbdoc(
                        The height of frame.
                    )pbdoc")

        .def_prop_rw("color_type", 
                    [](apngasm::APNGFrame &t) APNGASM_PY_DECLSPEC { return t._colorType; },
                    [](apngasm::APNGFrame &t, unsigned char v) APNGASM_PY_DECLSPEC { t.colorType(v); },
                    R"pbdoc(
                        The color_type of the frame.
                        
                        0: Grayscale (Pillow mode='L')
                        2: RGB (Pillow mode='RGB')
                        3: Palette (Pillow mode='P')
                        4: Grayscale + Alpha (Pillow mode='LA')
                        6: RGBA (Pillow mode='RGBA')
                    )pbdoc")

        .def_prop_rw("palette", 
                    [](apngasm::APNGFrame &t) APNGASM_PY_DECLSPEC {
                        unsigned char paletteView[256][3];
                        for (int i = 0; i < 256; ++i) {
                            paletteView[i][0] = t._palette[i].r;
                            paletteView[i][1] = t._palette[i].g;
                            paletteView[i][2] = t._palette[i].b;
                        }
                        size_t shape[2] = { 256, 3 };
                        return nb::cast(nb::ndarray<nb::numpy, unsigned char, nb::shape<256, 3>>(paletteView, 2, shape)); 
                    },
                    [](apngasm::APNGFrame &t, nb::ndarray<unsigned char, nb::shape<256, 3>> *v) APNGASM_PY_DECLSPEC {
                        unsigned char *v_ptr = v->data();
                        for (int i = 0; i < 256; ++i) {
                            t._palette[i].r = v_ptr[0];
                            t._palette[i].g = v_ptr[1];
                            t._palette[i].b = v_ptr[2];
                            v_ptr += 3;
                        }
                    },
                    R"pbdoc(
                        The palette data of frame. Only applies to 'P' mode Image (i.e. Not RGB, RGBA)
                        Expressed as 2D numpy array in format of [[r0, g0, b0], [r1, g1, b1], ..., [r255, g255, b255]] in Python
                    )pbdoc")

        .def_prop_rw("transparency", 
                    [](apngasm::APNGFrame &t) APNGASM_PY_DECLSPEC {
                        size_t shape[1] = { static_cast<size_t>(t._transparencySize) };
                        return nb::cast(nb::ndarray<nb::numpy, unsigned char, nb::shape<nb::any>>(t._transparency, 1, shape)); 
                    },
                    [](apngasm::APNGFrame &t, nb::ndarray<unsigned char, nb::shape<nb::any>> *v) APNGASM_PY_DECLSPEC {
                        unsigned char *v_ptr = v->data();
                        for (int i = 0; i < v->shape(0); ++i) {
                            t._transparency[i] = *v_ptr;
                            ++v_ptr;
                        }
                    },
                    R"pbdoc(
                        The transparency data of frame. Expressed as 1D numpy array.
                    )pbdoc")

        .def_prop_rw("palette_size", 
                    [](apngasm::APNGFrame &t) APNGASM_PY_DECLSPEC { return t._paletteSize; },
                    [](apngasm::APNGFrame &t, unsigned int v) APNGASM_PY_DECLSPEC { t.paletteSize(v); },
                    R"pbdoc(
                        The palette data size of frame.
                    )pbdoc")

        .def_prop_rw("transparency_size", 
                    [](apngasm::APNGFrame &t) APNGASM_PY_DECLSPEC { return t._transparencySize; },
                    [](apngasm::APNGFrame &t, unsigned int v) APNGASM_PY_DECLSPEC { t.transparencySize(v); },
                    R"pbdoc(
                        The transparency data size of frame.
                    )pbdoc")

        .def_prop_rw("delay_num", 
                    [](apngasm::APNGFrame &t) APNGASM_PY_DECLSPEC { return t._delayNum; },
                    [](apngasm::APNGFrame &t, unsigned int v) APNGASM_PY_DECLSPEC { t.delayNum(v); },
                    R"pbdoc(
                        The nominator of the duration of frame. Duration of time is delay_num / delay_den seconds.
                    )pbdoc")
        .def_prop_rw("delay_den", 
                    [](apngasm::APNGFrame &t) APNGASM_PY_DECLSPEC { return t._delayDen; },
                    [](apngasm::APNGFrame &t, unsigned int v) APNGASM_PY_DECLSPEC { t.delayDen(v); },
                    R"pbdoc(
                        The denominator of the duration of frame. Duration of time is delay_num / delay_den seconds.
                    )pbdoc");

        // difficult to implement
        // rows is also set when pixels is set
        // .def_prop_rw("rows")

    nb::class_<apngasm::APNGAsm>(m, "APNGAsm")
        .def(nb::init<>(),
        R"pbdoc(
            Construct an empty APNGAsm object.
        )pbdoc")

        .def(nb::init<const std::vector<apngasm::APNGFrame> &>(),
        "frames"_a,
        R"pbdoc(
            Construct APNGAsm object from an existing vector of apngasm frames.
        
            :param list frames: A list of APNGFrame objects.
        )pbdoc")

        .def("add_frame", nb::overload_cast<const apngasm::APNGFrame &>(&apngasm::APNGAsm::addFrame),
        "frame"_a,
        R"pbdoc(
            Adds an APNGFrame object to the frame vector.
        
            :param frame: The APNGFrame object to be added
            :type frame: apngasm_python._apngasm_python.APNGFrame

            :return: The new number of frames/the number of this frame on the frame vector.
            :rtype: int
        )pbdoc")

        .def("add_frame_from_file", nb::overload_cast<const std::string &, unsigned, unsigned>(&apngasm::APNGAsm::addFrame),
        "file_path"_a, "delay_num"_a = apngasm::DEFAULT_FRAME_NUMERATOR, "delay_den"_a = apngasm::DEFAULT_FRAME_DENOMINATOR,
        R"pbdoc(
            Adds a frame from a PNG file or frames from a APNG file to the frame vector.
        
            :param str file_path: The relative or absolute path to an image file.
            :param int delay_num: The delay numerator for this frame (defaults to DEFAULT_FRAME_NUMERATOR).
            :param int delay_den: The delay denominator for this frame (defaults to DEFAULT_FRAME_DENMINATOR).

            :return: The new number of frames/the number of this frame on the frame vector.
            :rtype: int
        )pbdoc")

        .def("add_frame_from_rgb", nb::overload_cast<apngasm::rgb *, unsigned int, unsigned int, apngasm::rgb *, unsigned, unsigned>(&apngasm::APNGAsm::addFrame),
        "pixels_rgb"_a, "width"_a, "height"_a, "trns_color"_a = NULL, "delay_num"_a = apngasm::DEFAULT_FRAME_NUMERATOR, "delay_den"_a = apngasm::DEFAULT_FRAME_DENOMINATOR,
        R"pbdoc(
            Adds an APNGFrame object to the vector.
            Not possible to use in Python. As alternative,
            Use create_frame_from_rgb() or create_frame_from_rgba(). Or manually,
            First create an empty APNGFrame with frame = APNGFrame(),
            then set frame.width, frame.height, frame.color_type, frame.pixels,
            frame.palette, frame.delay_num, frame.delay_den manually.
            
            :param pixels_rgb: The RGB pixel data.
            :param int width: The width of the pixel data.
            :param int height: The height of the pixel data.
            :param trns_color: An array of transparency data.
            :param int delay_num: The delay numerator for this frame (defaults to DEFAULT_FRAME_NUMERATOR).
            :param int delay_den: The delay denominator for this frame (defaults to DEFAULT_FRAME_DENMINATOR).

            :return: The new number of frames/the number of this frame on the frame vector.
            :rtype: int
        )pbdoc")

        .def("add_frame_from_rgba", nb::overload_cast<apngasm::rgba *, unsigned int, unsigned int, unsigned, unsigned>(&apngasm::APNGAsm::addFrame),
        "pixels_rgba"_a, "width"_a, "height"_a, "delay_num"_a = apngasm::DEFAULT_FRAME_NUMERATOR, "delay_den"_a = apngasm::DEFAULT_FRAME_DENOMINATOR,
        R"pbdoc(
            Adds an APNGFrame object to the vector.
            Not possible to use in Python. As alternative,
            Use create_frame_from_rgb() or create_frame_from_rgba(). Or manually,
            First create an empty APNGFrame with frame = APNGFrame(),
            then set frame.width, frame.height, frame.color_type, frame.pixels,
            frame.palette, frame.delay_num, frame.delay_den manually.
            
            :param pixels_rgba: The RGBA pixel data.
            :param int width: The width of the pixel data.
            :param int height: The height of the pixel data.
            :param int delay_num: The delay numerator for this frame (defaults to DEFAULT_FRAME_NUMERATOR).
            :param int delay_den: The delay denominator for this frame (defaults to DEFAULT_FRAME_DENMINATOR).
            
            :return: The new number of frames/the number of this frame on the frame vector.
            :rtype: int
        )pbdoc")
        
        .def("assemble", &apngasm::APNGAsm::assemble,
        "output_path"_a,
        R"pbdoc(
            Assembles and outputs an APNG file.
            
            :param str output_path: The output file path.
            
            :return: true if assemble completed succesfully.
            :rtype: bool
        )pbdoc")

        .def("disassemble", &apngasm::APNGAsm::disassemble,
        "file_path"_a,
        R"pbdoc(
            Disassembles an APNG file.
            
            :param str file_path: The file path to the PNG image to be disassembled.

            :return: A vector containing the frames of the disassembled PNG.
            :rtype: list
        )pbdoc")

        .def("save_pngs", &apngasm::APNGAsm::savePNGs,
        "output_dir"_a,
        R"pbdoc(
            Saves individual PNG files of the frames in the frame vector.
            
            :param str output_dir: The directory where the PNG fils will be saved.
            
            :return: true if all files were saved successfully.
            :rtype: bool
        )pbdoc")

        .def("load_animation_spec", &apngasm::APNGAsm::loadAnimationSpec,
        "file_path"_a,
        R"pbdoc(
            Loads an animation spec from JSON or XML.
            Loaded frames are added to the end of the frame vector.
            For more details on animation specs see:
            https://github.com/Genshin/PhantomStandards
            
            :param str file_path: The path of JSON or XML file

            :return: A vector containing the frames
            :rtype: list
        )pbdoc")

        .def("save_json", &apngasm::APNGAsm::saveJSON,
        "output_path"_a, "image_dir"_a,
        R"pbdoc(
            Saves a JSON animation spec file.
            
            :param str output_path: Path to save the file to.
            :param str image_dir: Directory where frame files are to be saved if not the same path as the animation spec.

            :return: true if save was successful.
            :rtype: bool
        )pbdoc")

        .def("save_xml", &apngasm::APNGAsm::saveXML,
        "output_path"_a, "image_dir"_a,
        R"pbdoc(
            Saves an XML animation spec file.
            
            :param str file_path: Path to save the file to.
            :param str image_dir: Directory where frame files are to be saved if not the same path as the animation spec.
            
            :return: true if save was successful.
            :rtype: bool
        )pbdoc")

        .def("set_apng_asm_listener", &apngasm::APNGAsm::setAPNGAsmListener,
        "listener"_a = NULL,
        R"pbdoc(
            Sets a listener.
            
            :param listener: A pointer to the listener object. If the argument is NULL a default APNGAsmListener will be created and assigned.8
        )pbdoc")

        .def("set_loops", &apngasm::APNGAsm::setLoops,
        "loops"_a = 0,
        R"pbdoc(
            Set loop count of animation.
            
            :param int loops: Loop count of animation. If the argument is 0 a loop count is infinity.
        )pbdoc")

        .def("set_skip_first", &apngasm::APNGAsm::setSkipFirst,
        "skip_first"_a,
        R"pbdoc(
            Set flag of skip first frame.
            
            :param int skip_first: Flag of skip first frame.
        )pbdoc")

        .def("get_frames", &apngasm::APNGAsm::getFrames,
        R"pbdoc(
            Returns the frame vector.

            :return: frame vector
            :rtype: numpy.ndarray
        )pbdoc")

        .def("get_loops", &apngasm::APNGAsm::getLoops,
        R"pbdoc(
            Returns the loop count.
            
            :return: loop count
            :rtype: int
        )pbdoc")

        .def("is_skip_first", &apngasm::APNGAsm::isSkipFirst,
        R"pbdoc(
            Returns the flag of skip first frame.
            
            :return: flag of skip first frame
            :rtype: bool
        )pbdoc")

        .def("frame_count", &apngasm::APNGAsm::frameCount,
        R"pbdoc(
            Returns the number of frames.
            
            :return: number of frames
            :rtype: int
        )pbdoc")

        .def("reset", &apngasm::APNGAsm::reset,
        R"pbdoc(
            Destroy all frames in memory/dispose of the frame vector.
            Leaves the apngasm object in a clean state.
            Returns number of frames disposed of.
            
            :return: number of frames disposed of
            :rtype: int
        )pbdoc")

        .def("version", &apngasm::APNGAsm::version,
        R"pbdoc(
            Returns the version of APNGAsm.
            
            :return: the version of APNGAsm
            :rtype: str
        )pbdoc");
}