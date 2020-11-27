from jute import config

from typing import List
import os
import py2exe
import shutil
import sys


def is_data_path(path: str) -> bool:
    return not path.endswith(("__pycache__", ".py", ".pyc", ".pyd"))


def get_data_files(source: str, message: str = None) -> List[str]:
    data_files = []

    for path, dirs, files in os.walk(source):
        rel_path = os.path.relpath(path)
        if is_data_path(rel_path):
            if message:
                print(message.format(rel_path))
            data_files.append(
                (
                    rel_path,
                    [
                        os.path.join(rel_path, file)
                        for file in files
                        if is_data_path(file)
                    ],
                )
            )

    return data_files


build_manifest = """
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
    <assemblyIdentity name="{name}"
        type="win32"
        version="{version}"
        />
    <description>{description}</description>
    <dependency>
        <dependentAssembly>
            <assemblyIdentity name="Microsoft.VC90.CRT"
                language="*"
                processorArchitecture="x86"
                publicKeyToken="1fc8b3b9a1e18e3b"
                type="win32"
                version="9.0.30729.6161"
                />
        </dependentAssembly>
    </dependency>
</assembly>
"""

build_path = os.path.realpath(os.path.dirname(__file__))
build_dest_path = os.path.join(build_path, "bin", "win32")
build_data_path = os.path.join(build_path, "assets", "targets")
build_icon_path = os.path.join(build_path, "assets", "icons")

print("Removing old build at {} ... ".format(build_dest_path), end="")
shutil.rmtree(build_dest_path, ignore_errors=True)
os.makedirs(build_dest_path)
print("done.", flush=True)

print("Collecting data files:")
target_files = get_data_files(build_data_path, "  adding files from {} ...")
icon_files = get_data_files(build_icon_path, "  adding files from {} ...")
build_data_files = target_files + icon_files
print("... done.", flush=True)

sys.argv.append(py2exe.__name__)

setup_args = dict(
    name=config.APP_NAME,
    description=config.APP_DESCRIPTION,
    version=config.APP_VERSION_STRING,
    windows=[
        {
            "dest_base": config.APP_NAME,
            "script": os.path.join(build_path, "jute", "app.py"),
            "icon_resources": [
                (4, os.path.join(build_path, "assets", "appicons", "app.ico")),
                (5, os.path.join(build_path, "assets", "appicons", "doc.ico")),
            ],
            "other_resources": [
                (
                    24,
                    1,
                    build_manifest.format(
                        name=config.APP_NAME,
                        description=config.APP_DESCRIPTION,
                        version=config.APP_VERSION_STRING,
                    ),
                )
            ],
        }
    ],
    options={
        "py2exe": {
            "bundle_files": 3,
            "compressed": True,
            "dist_dir": build_dest_path,
            "dll_excludes": ["w9xpopen.exe", "MSVCP90.dll"],
            "ignores": ["_scproxy"],
            "optimize": 2,
        }
    },
    data_files=build_data_files,
    zipfile="library.zip",
)
