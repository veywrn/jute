# Jute

Jute is intended to be a save-import and target-export compatible fork of Twine
1.4 with additional features, bugfixes, and as is the nature of developing
software, bugs.

## Usage

### As Source

To build and run this repository requires Python 3.6 or later and the following:

    git clone https://github.com/veywrn/jute.git
    python -m pip install -r ./jute/requirements.txt --user
    python ./jute/app.py

### As Distribution

This project uses [Nuitka](http://nuitka.net/) to make standalone builds. As of
this commit only Windows has been tested. Take a look at `buildexe.ps1` for a 
potential starting point for other systems.
