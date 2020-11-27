# Steps used in making this script:
#   0. Use chocolatey! https://chocolatey.org/
#   1. ps> choco install msys2
#   2. msys2> pacman -S base-devel mingw-w64-i686-toolchain
#

# Update value below to wherever gcc is installed:
Set-Item -Path env:CC -Value C:\tools\msys64\mingw64\bin\gcc.exe
& python -m pip install -U nuitka
& python -m pip install -r .\requirements.txt
# Add the following flags to nuitka for a smaller distribution but longer build:
# --experimental=use_pefile --experimental=use_pefile_recurse
& python -m nuitka `
    --mingw64 `
    --python-flag=no_site `
    --remove-output `
    --show-progress `
    --standalone `
    --windows-dependency-tool=pefile `
    --windows-disable-console `
    --windows-icon=./assets/appicons/app.ico `
    ./src/jute/app.py

Rename-Item -Path ./app.dist/app.exe -NewName jute.exe
Copy-Item -Path ./assets/icons -Destination ./app.dist -Recurse
Copy-Item -Path ./assets/targets -Destination ./app.dist -Recurse