from conan import ConanFile
import os
import shutil

class ApngasmRecipe(ConanFile):
    settings = 'os', 'compiler', 'build_type', 'arch'

    def check_file_present(self, target, search_path):        
        if target in os.listdir(search_path):
            return True
        
        return False
    
    def requirements(self):
        self.requires("zlib/1.2.13")
        self.requires("libpng/1.6.40")
        self.requires("boost/1.82.0")

        self.generators = ['CMakeToolchain', 'CMakeDeps']

    def build_requirements(self):
        self.build_requires("b2/[>4.10]")
        if not shutil.which('cmake'):
            self.tool_requires("cmake/[>=3.27]")
    
    def build(self):
        build_type = 'Release'