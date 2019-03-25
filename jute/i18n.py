"""
Imports locale files and defines the standard gettext function.
"""

import config

import gettext
from os import path


locale_dir = path.join(path.abspath(path.dirname(__file__)), "locale")
translation = gettext.translation(config.APP_NAME, locale_dir, fallback=True)
_ = translation.gettext
