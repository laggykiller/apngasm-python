#!/usr/bin/env python3
import sys


def main():
    init_pyi_path = sys.argv[1]
    with open(init_pyi_path) as f:
        init_pyi = f.read()

    with open(init_pyi_path, "w+") as f:
        init_pyi = init_pyi.replace("List[", "list[")
        if "from __future__ import annotations" not in init_pyi:
            f.write("from __future__ import annotations\n")
        if "import numpy.typing" not in init_pyi:
            f.write("import numpy.typing\n")
        if "from . import _apngasm_python" not in init_pyi:
            init_pyi = init_pyi.replace(
                "import _apngasm_python", "from . import _apngasm_python"
            )
        f.write(init_pyi)


if __name__ == "__main__":
    main()
