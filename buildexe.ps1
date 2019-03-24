# Steps used in making this script:
#   0. Use chocolatey! https://chocolatey.org/
#   1. ps> choco install msys2
#   2. msys2> pacman -S base-devel mingw-w64-i686-toolchain
#

# Update value below to wherever gcc is installed:
Set-Item -Path env:CC -Value C:\tools\msys64\mingw32\bin\gcc.exe
& python -m pip install -r .\requirements.txt
# Add the following flags to nuitka for a smaller distribution but longer build:
# --experimental=use_pefile --experimental=use_pefile_recurse
& python -m nuitka --standalone --show-progress --show-scons --mingw64 .\jute\app.py
