.. apngasm-python documentation master file, created by
   sphinx-quickstart on Fri Sep  8 20:36:01 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to apngasm-python's documentation!
==========================================
A nanobind API for apngasm (https://github.com/apngasm/apngasm), a tool/library for APNG assembly/disassembly.

apngasm is originally a CLI program for quickly assembling PNG images into animated PNG (APNG). It also supports creating compressed APNG.

apngasm-python is a binding for apngasm using nanobind, allowing you to use apngasm without calling it using commands.

With this module, you can even create APNG using images inside memory (No need to write them out as file and call apngasm! This is about 2 times faster from testing.)

A similar python module is https://github.com/eight04/pyAPNG , which handles APNG files with python natively and does not support compression.

For convenience, prebuilt library is packaged with this module, so you need not download apngasm.

To install: `pip install apngasm-python`

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   examples
   build
   credits
   modules


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
