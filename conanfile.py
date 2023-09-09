from conan import ConanFile
import shutil
import platform

class ApngasmRecipe(ConanFile):
    settings = 'os', 'compiler', 'build_type', 'arch'
    
    def requirements(self):
        self.requires("zlib/1.2.13")
        self.requires("libpng/1.6.40")
        self.requires("boost/1.83.0")
        self.generators = ['CMakeToolchain', 'CMakeDeps']

    def build_requirements(self):
        if not shutil.which('cmake'):
            self.tool_requires("cmake/[>=3.5]")
    
    def build(self):
        build_type = 'Release'