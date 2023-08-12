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
// apngasmlistener.h not installed by apngasm
// #include "apngasmlistener.h"

namespace nb = nanobind;
using namespace nb::literals;

std::map<int, int> rowbytesMap = {
    { 0, 1 }, // Grayscale
    { 2, 3 }, // RGB
    { 3, 1 }, // Palette
    { 4, 2 }, // Grayscale + A
    { 6, 4 }  // RGBA
};

NB_MODULE(MODULE_NAME, m) {
    m.doc() = "A nanobind API for apngasm, a tool/library for APNG assembly/disassembly";
    m.attr("__version__") = VERSION_INFO;

    nb::class_<apngasm::rgb>(m, "rgb")
        .def(nb::init<>())
        .def(nb::init<unsigned char, unsigned char, unsigned char>())
        .def_rw("r", &apngasm::rgb::r)
        .def_rw("g", &apngasm::rgb::g)
        .def_rw("b", &apngasm::rgb::b);
    
    nb::class_<apngasm::rgba>(m, "rgba")
        .def(nb::init<>())
        .def(nb::init<unsigned char, unsigned char, unsigned char, unsigned char>())
        .def_rw("r", &apngasm::rgba::r)
        .def_rw("g", &apngasm::rgba::g)
        .def_rw("b", &apngasm::rgba::b)
        .def_rw("a", &apngasm::rgba::a);

    nb::class_<apngasm::APNGFrame>(m, "APNGFrame")
        .def(nb::init<>())
        .def(nb::init<const std::string &, unsigned, unsigned>())
        // Exist in apngframe.h but not exist in apngframe.cpp
        // .def(nb::init<apngasm::rgb *, unsigned int, unsigned int, unsigned, unsigned>())
        // Not possible to call with original format, use new_frame_from_rgb
        .def(nb::init<apngasm::rgb *, unsigned int, unsigned int, apngasm::rgb *, unsigned, unsigned>())
        .def(nb::init<apngasm::rgba *, unsigned int, unsigned int, unsigned, unsigned>())
        .def("save", &apngasm::APNGFrame::save)
        .def_prop_rw("pixels", 
                    [](apngasm::APNGFrame &t) {
                        int rowbytes = rowbytesMap[t._colorType];
                        size_t shape[1] = { t._height * t._width * rowbytes };
                        return nb::ndarray<nb::numpy, unsigned char, nb::shape<nb::any>>(t._pixels, 1, shape);
                    },
                    [](apngasm::APNGFrame &t, nb::ndarray<unsigned char, nb::shape<nb::any>> *v) {
                        int rowbytes = rowbytesMap[t._colorType];
                        unsigned char *pixelsNew = new unsigned char[v->shape(0)];
                        unsigned char *v_ptr = v->data();
                        for (int i = 0; i < v->shape(0); ++i) {
                            pixelsNew[i] = *v_ptr;
                            ++v_ptr;
                        }
                        t.pixels(pixelsNew);

                        t._rows = new png_bytep[t._height * sizeof(png_bytep)];
                        for (int j = 0; j < t._height; ++j)
                            t._rows[j] = t._pixels + j * rowbytes;
                    })
        .def_prop_rw("width", 
                    [](apngasm::APNGFrame &t) { return t._width; },
                    [](apngasm::APNGFrame &t, unsigned int v) { t.width(v); })
        .def_prop_rw("height", 
                    [](apngasm::APNGFrame &t) { return t._height; },
                    [](apngasm::APNGFrame &t, unsigned int v) { t.height(v); })
        .def_prop_rw("color_type", 
                    [](apngasm::APNGFrame &t) { return t._colorType; },
                    [](apngasm::APNGFrame &t, unsigned char v) { t.colorType(v); })
        .def_prop_rw("palette", 
                    [](apngasm::APNGFrame &t) {
                        unsigned char paletteView[t._paletteSize][3];
                        for (int i = 0; i < t._paletteSize; ++i) {
                            paletteView[i][0] = t._palette[i].r;
                            paletteView[i][1] = t._palette[i].g;
                            paletteView[i][2] = t._palette[i].b;
                        }
                        size_t shape[2] = { t._paletteSize, 3 };
                        return nb::ndarray<nb::numpy, unsigned char, nb::shape<nb::any, 3>>(paletteView, 2, shape); 
                    },
                    [](apngasm::APNGFrame &t, nb::ndarray<unsigned char, nb::shape<256, 3>> *v) {
                        unsigned char *v_ptr = v->data();
                        for (int i = 0; i < v->shape(0); ++i) {
                            t._palette[i].r = v_ptr[0];
                            t._palette[i].g = v_ptr[1];
                            t._palette[i].b = v_ptr[2];
                            v_ptr += 3;
                        }
                    })
        .def_prop_rw("transparency", 
                    [](apngasm::APNGFrame &t) {
                        size_t shape[1] = { t._transparencySize };
                        return nb::ndarray<nb::numpy, unsigned char, nb::shape<nb::any>>(t._transparency, 1, shape); 
                    },
                    [](apngasm::APNGFrame &t, nb::ndarray<unsigned char, nb::shape<nb::any>> *v) {
                        unsigned char *v_ptr = v->data();
                        for (int i = 0; i < v->shape(0); ++i) {
                            t._transparency[i] = *v_ptr;
                            ++v_ptr;
                        }
                    })
        .def_prop_rw("palette_size", 
                    [](apngasm::APNGFrame &t) { return t._paletteSize; },
                    [](apngasm::APNGFrame &t, unsigned int v) { t.paletteSize(v); })
        .def_prop_rw("transparency_size", 
                    [](apngasm::APNGFrame &t) { return t._transparencySize; },
                    [](apngasm::APNGFrame &t, unsigned int v) { t.transparencySize(v); })
        .def_prop_rw("delay_num", 
                    [](apngasm::APNGFrame &t) { return t._delayNum; },
                    [](apngasm::APNGFrame &t, unsigned int v) { t.delayNum(v); })
        .def_prop_rw("delay_den", 
                    [](apngasm::APNGFrame &t) { return t._delayDen; },
                    [](apngasm::APNGFrame &t, unsigned int v) { t.delayDen(v); });
        // difficult to implement
        // rows is also set when pixels is set
        // .def_prop_rw("rows")

    nb::class_<apngasm::APNGAsm>(m, "APNGAsm")
        .def(nb::init<>())
        .def(nb::init<const std::vector<apngasm::APNGFrame> &>())
        .def("add_frame", nb::overload_cast<const apngasm::APNGFrame &>(&apngasm::APNGAsm::addFrame))
        .def("add_frame_from_file", nb::overload_cast<const std::string &, unsigned, unsigned>(&apngasm::APNGAsm::addFrame))
        .def("add_frame_from_rgb", nb::overload_cast<apngasm::rgb *, unsigned int, unsigned int, apngasm::rgb *, unsigned, unsigned>(&apngasm::APNGAsm::addFrame))
        .def("add_frame_from_rgba", nb::overload_cast<apngasm::rgba *, unsigned int, unsigned int, unsigned, unsigned>(&apngasm::APNGAsm::addFrame))
        .def("assemble", &apngasm::APNGAsm::assemble)
        .def("disassemble", &apngasm::APNGAsm::disassemble)
        .def("save_pngs", &apngasm::APNGAsm::savePNGs)
        .def("load_animation_spec", &apngasm::APNGAsm::loadAnimationSpec)
        .def("save_json", &apngasm::APNGAsm::saveJSON)
        .def("save_xml", &apngasm::APNGAsm::saveXML)
        // Requires apngasmlistener.h
        // .def("set_apng_asm_listener", &apngasm::APNGAsm::setAPNGAsmListener)
        .def("set_loops", &apngasm::APNGAsm::setLoops)
        .def("set_skip_first", &apngasm::APNGAsm::setSkipFirst)
        .def("get_frames", &apngasm::APNGAsm::getFrames)
        .def("get_loops", &apngasm::APNGAsm::getLoops)
        .def("is_skip_first", &apngasm::APNGAsm::isSkipFirst)
        .def("frame_count", &apngasm::APNGAsm::frameCount)
        .def("reset", &apngasm::APNGAsm::reset)
        .def("version", &apngasm::APNGAsm::version);
}