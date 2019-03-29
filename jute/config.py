"""
Application-wide static settings.
"""

from typing import Tuple
import i18n
import platform


APP_NAME: str = "Jute"
APP_DESCRIPTION: str = _(
    "A save-import and target-export compatible fork of Twine 1.4 with "
    "additional features, bugfixes, and as is the nature of developing "
    "software, bugs."
)
APP_LICENSE: str = "GNU GPLv3"
APP_VERSION: Tuple[int, int, int] = (0, 1, 0)
APP_VERSION_STRING: str = f"{APP_VERSION[0]}.{APP_VERSION[1]}.{APP_VERSION[2]}"
APP_SYSTEM_STRING: str = f"{platform.system()} {platform.release()}"
APP_AUTHORS: str = (
    "tychon <tychon@gmail.com>\n"
)

APP_ORIGIN_NAME: str = "Twine 1.4"
APP_ORIGIN_AUTHORS: str = (
    "Bo Daley <bo@factorypreset.com>\n"
    "Chris Klimas <klimas@gmail.com>\n"
    "Christopher Liu <github@christopherliu.net>\n"
    "HarmlessTrouble <henry.soule@gmail.com>\n"
    "Henry Soule <henry.soule@gmail.com>\n"
    "Lachlan Cooper <lachlancooper@gmail.com>\n"
    "Leon <L_1_L_0@yahoo.com>\n"
    "Maarten ter Huurne <maarten@treewalker.org>\n"
    "Misty De Meo <mistydemeo@gmail.com>\n"
    "Philip-Sutton <Philip.Sutton@green-innovations.asn.au>\n"
    "Richard Lake <richard.lake+git@gmail.com>\n"
    "Stormrose <eturnerx@gmail.com>\n"
    "factorypreset <bo@darkwork.net>\n"
    "greyelf <greyelf@gmail.com>\n"
    "ryan <twine@mesolithicstudios.com>\n"
    "tmedwards <tmedwards@motoslave.net>\n"
)

URL_JUTE_GITHUB: str = "https://github.com/veywrn/jute"
URL_JUTE_GITHUB_AUTHORS: str = "https://github.com/veywrn/jute/graphs/contributors"
URL_JUTE_GITHUB_ISSUES: str = "https://github.com/veywrn/jute/issues/new"

URL_TWINE: str = "http://twinery.org/"
URL_TWINE_FORUM: str = "http://twinery.org/forum/"
URL_TWINE_GITHUB: str = "https://github.com/tweecode/twine"
URL_TWINE_HELP: str = "http://twinery.org/wiki/"
URL_TWINE_HELP_LINKS: str = "http://twinery.org/wiki/link"
URL_TWINE_HELP_MACROS: str = "http://twinery.org/wiki/macro"
URL_TWINE_HELP_PASSAGES: str = "http://twinery.org/wiki/passage"
URL_TWINE_HELP_SCRIPTS: str = "http://twinery.org/wiki/script"
URL_TWINE_HELP_SPECIALS: str = "http://twinery.org/wiki/special_passages"
URL_TWINE_HELP_STORIES: str = "http://twinery.org/wiki/story_format"
URL_TWINE_HELP_STYLESHEETS: str = "http://twinery.org/wiki/stylesheet"
URL_TWINE_HELP_SYNTAX: str = "http://twinery.org/wiki/syntax"
URL_TWINE_HELP_TAGS: str = "http://twinery.org/wiki/tag"
