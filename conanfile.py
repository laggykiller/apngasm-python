from conan import ConanFile
import shutil
from get_arch import get_arch
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout
from conan.tools.apple import is_apple_os

class ApngasmRecipe(ConanFile):
    settings = 'os', 'compiler', 'build_type', 'arch'
    
    def requirements(self):
        self.requires("zlib/1.2.13")
        self.requires("libpng/1.6.40")
        self.requires("boost/1.74.0")

    def build_requirements(self):
        self.build_requires("b2/4.5.0")
        if not shutil.which('cmake'):
            self.tool_requires("cmake/[>=3.27]")
    
    def build(self):
        build_type = 'Release'
    
    def generate(self):
        tc = CMakeToolchain(self)
        cmake = CMakeDeps(self)
        if is_apple_os(self) and get_arch() == 'universal2':
            tc.blocks['apple_system'].values['cmake_osx_architectures'] = 'x86_64; arm64'
        tc.generate()
        cmake.generate()