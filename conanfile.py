from conan import ConanFile
import os
import shutil
import platform
import subprocess

class ApngasmRecipe(ConanFile):
    settings = 'os', 'compiler', 'build_type', 'arch'

    zlib_libs = [
        'libz.a'
    ]

    zlib_headers = [
        'zlib.h',
        'zconf.h',
    ]

    libpng_libs = [
        'libpng.a'
    ]

    libpng_headers = [
        'png.h',
        'pngconf.h',
        'pnglibconf.h'
    ]

    boost_libs = [
        'libboost_program_options.a',
        'libboost_regex.a',
        'libboost_system.a'
    ]

    boost_headers = [
        'algorithm',
        'property_tree',
        'foreach.hpp'
    ]

    def check_file_present(self, target, search_path):        
        if target in os.listdir(search_path):
            return True
        
        return False
    
    def requirements(self):
        self.generators = ['CMakeToolchain', 'CMakeDeps']

        if not (platform.system() == 'Linux' and 
                all([self.check_file_present(i, '/usr/lib') for i in self.zlib_libs]) and
                all([self.check_file_present(i, '/usr/include') for i in self.zlib_headers])):
            
            self.requires("zlib/1.2.13")
        
        if not (platform.system() == 'Linux' and 
                all([self.check_file_present(i, '/usr/lib') for i in self.libpng_libs]) and
                all([self.check_file_present(i, '/usr/include') for i in self.libpng_headers])):
            
            self.requires("libpng/1.6.40")

        if not (platform.system() == 'Linux' and
            all([self.check_file_present(i, '/usr/lib') for i in self.boost_libs]) and
            all([self.check_file_present(i, '/usr/include/boost') for i in self.boost_headers])):

            self.requires("boost/1.82.0")

    def build_requirements(self):
        self.build_requires("b2/[>4.10]")
        if not shutil.which('cmake'):
            self.tool_requires("cmake/[>=3.27]")
    
    def build(self):
        build_type = 'Release'