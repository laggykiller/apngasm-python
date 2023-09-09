from conan import ConanFile

class ApngasmRecipe(ConanFile):
    settings = 'os', 'compiler', 'build_type', 'arch'
    
    def requirements(self):
        self.requires("zlib/1.2.13")
        self.requires("libpng/1.6.40")
        self.requires("boost/1.73.0")
        self.generators = ['CMakeToolchain', 'CMakeDeps']

    def build_requirements(self):
        # https://stackoverflow.com/questions/42123509/cmake-finds-boost-but-the-imported-targets-not-available-for-boost-version
        self.tool_requires("cmake/[>=3.27]")
    
    def build(self):
        build_type = 'Release'