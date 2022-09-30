import os
import platform
import subprocess
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
from pathlib import Path


PACKAGE_NAME = "clustalo"

CLUSTAL_OMEGA_BASE_DIR = "external/clustal-omega-1.2.4"
CLUSTAL_OMEGA_INCLUDE_DIR = "external/clustal-omega-1.2.4/src"
CLUSTAL_OMEGA_FINAL_LIB_DIR = str(Path(CLUSTAL_OMEGA_BASE_DIR)/"src/.libs")

ARGTABLE2_BASE_DIR = "external/argtable2-13"
ARGTABLE2_INCLUDE_DIR = "external/argtable2-13/src"
ARGTABLE2_FINAL_LIB_DIR = str(Path(ARGTABLE2_BASE_DIR)/"src/.libs")

def get_version():
    with open("VERSION") as versionfile:
        return versionfile.read().strip()

class BuildFlags:
    _args = {
        "Darwin": {"compiler": ["-Xpreprocessor", "-fopenmp"], "linker": ["-lomp"]},
        "Default": {"compiler": ["-fopenmp"], "linker": ["-fopenmp", "-fPIC"]},
    }
    compiler: list
    linker: list

    def __init__(self):
        _system = platform.system()
        args = self._args.get(_system, self._args["Default"])
        for key, val in args.items():
            self.__setattr__(key, val)


# TODO: This should copy 'external' to the build directory, then run these commands so we don't pollute
#       the git library dir.
class CustomBuildExt(build_ext):
    def build_libargtable(self):
        if not list(Path(ARGTABLE2_FINAL_LIB_DIR).glob("*")):
            subprocess.check_call(["autoreconf", "-f", "-i"], cwd=ARGTABLE2_BASE_DIR)
            subprocess.check_call(["./configure"], cwd=ARGTABLE2_BASE_DIR)
            subprocess.check_call(["make"], cwd=ARGTABLE2_BASE_DIR)

    def build_libclustalo(self):
        if not list(Path(CLUSTAL_OMEGA_FINAL_LIB_DIR).glob("*")):
            subprocess.check_call(["autoreconf", "-f", "-i"], cwd=CLUSTAL_OMEGA_BASE_DIR)
            subprocess.check_call(
                [
                    "./configure",
                    f"LDFLAGS=-L{os.getcwd()}/{ARGTABLE2_FINAL_LIB_DIR}",
                    f"CFLAGS=-I{os.getcwd()}/{ARGTABLE2_INCLUDE_DIR} -fPIC",
                ],
                cwd=CLUSTAL_OMEGA_BASE_DIR,
            )
            subprocess.check_call(["make"], cwd=CLUSTAL_OMEGA_BASE_DIR)

    def run(self):
        self.build_libargtable()
        self.build_libclustalo()
        super().run()


flags = BuildFlags()

module = Extension(
    "_clustalo",
    sources=["clustalo.c"],
    include_dirs=[CLUSTAL_OMEGA_INCLUDE_DIR, ARGTABLE2_INCLUDE_DIR],
    library_dirs=[CLUSTAL_OMEGA_FINAL_LIB_DIR, "/usr/local/lib"],
    libraries=["stdc++"],
    extra_objects=[CLUSTAL_OMEGA_FINAL_LIB_DIR + "/libclustalo.a"],
    extra_compile_args=flags.compiler,
    extra_link_args=flags.linker,
)

setup(
    name="cyrus-clustalo-py",
    version=get_version(),
    description="Python wrapper around libclustalo",
    packages=[PACKAGE_NAME],
    author="Danny Farrell",
    author_email="danpf@uw.edu",
    url="https://github.com/danpf/clustalo-python",
    ext_modules=[module],
    ext_package=PACKAGE_NAME,
    cmdclass={"build_ext": CustomBuildExt},
)
