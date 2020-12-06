"""
Loads all available locales and stores translation objects in a dictionary of
the same name.
"""

import assets
import gettext
import os
import re


LOCALE_DOMAIN = 'Jute'


def get_locales(locale_dir):
    locales = {}
    locale_expr = r'^[a-z]{2}(?:_[A-Z]{2})?$'

    for path, dirs, files in os.walk(locale_dir):
        for dir in dirs:
            m = re.match(locale_expr, dir)
            if m:
                try:
                    locales[m[0]] = gettext.translation(
                        LOCALE_DOMAIN,
                        locale_dir,
                        languages=[m[0]]
                    )
                except IOError as ex:
                    pass

    return locales


locale_dir = os.path.join(assets.DIRECTORY, 'locales')
locales = get_locales(locale_dir)

if not locales:
    locales = {
        'en_US': gettext.translation(LOCALE_DOMAIN, locale_dir, fallback=True)
    }

locales['en_US'].install()
