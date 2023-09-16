# Build

```bash
git clone https://github.com/laggykiller/apngasm-python.git
cd apngasm-python
git submodule update --init --recursive

# To build wheel
python3 -m build .

# To install directly
pip3 install .
```

To cross-compile, please set environment variables:
```bash
# Choose only one

# On Windows (cmd, not PowerShell)
set APNGASM_COMPILE_TARGET=x86_64
set APNGASM_COMPILE_TARGET=x86
set APNGASM_COMPILE_TARGET=armv8

# On *nix
export APNGASM_COMPILE_TARGET=x64
export APNGASM_COMPILE_TARGET=x86
export APNGASM_COMPILE_TARGET=armv8
export APNGASM_COMPILE_TARGET=ppc64le
export APNGASM_COMPILE_TARGET=s390x
```