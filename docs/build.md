# Build

### Method 1: Without vcpkg
Simply run:
```bash
git clone https://github.com/laggykiller/apngasm-python.git
cd apngasm-python
git submodule update --init --recursive

# To build wheel
python3 -m build .

# To install directly
pip3 install .
```

- Note that you will need CMake.
- If on Windows, you will need Visual Studio installed
- Cross-compilation not supported using this method

### Method 2: With vcpkg
1. Install vcpkg: https://github.com/microsoft/vcpkg
2. Set environment variable that points to the path of vcpkg root
```bash
# On Windows (cmd, not PowerShell)
set VCPKG_INSTALLATION_ROOT=C:/path/to/vcpkg

# On *nix
export VCPKG_INSTALLATION_ROOT=/path/to/vcpkg
```

3. Building
```bash
git clone https://github.com/laggykiller/apngasm-python.git
cd apngasm-python
# --recursive flag not necessary here
git submodule update --init

# To build wheel
python3 -m build .

# To install directly
pip3 install .
```

Note that this method also support cross-compilation,
to do so you will need to set environment variables beforehand:
```bash
# Choose only one

# On Windows (cmd, not PowerShell)
set APNGASM_COMPILE_TARGET=x64
set APNGASM_COMPILE_TARGET=x86
set APNGASM_COMPILE_TARGET=arm64
set APNGASM_COMPILE_TARGET=arm

# On MacOS
export APNGASM_COMPILE_TARGET=x64
export APNGASM_COMPILE_TARGET=x86
export APNGASM_COMPILE_TARGET=arm64

# On *nix
export APNGASM_COMPILE_TARGET=x64
export APNGASM_COMPILE_TARGET=x86
export APNGASM_COMPILE_TARGET=arm64
```
