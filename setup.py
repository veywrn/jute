import jute.config

from distutils.core import setup

setup(
    name=jute.config.APP_NAME,
    description=jute.config.APP_DESCRIPTION,
    version=jute.config.APP_VERSION_STRING,
    url=jute.config.URL_JUTE_GITHUB,
    license=jute.config.APP_LICENSE,
    packages=["jute",],
)
