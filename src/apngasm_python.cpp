#include <nanobind/nanobind.h>
#include <apngasm.h>

namespace nb = nanobind;

NB_MODULE(apngasm_python, m) {
    nb::class_<APNGAsm>(m, "APNGAsm")
        .def(nb::init<>())
        .def(nb::init<const std::string &>())
        .def("bark", &Dog::bark)
        .def_rw("name", &Dog::name);
}