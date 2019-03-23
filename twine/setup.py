from setuptools import setup, find_packages
import jute.config

setup(
    name=jute.config.APP_NAME,
    description=jute.config.APP_DESCRIPTION,
    version=jute.config.APP_VERSION,
    license=jute.config.APP_LICENSE,

    packages=find_packages(exclude=['tests']),

    install_requires=[
        'py2app==0.6.*',
        'py2exe_py2==0.6.*',
        'pywin32>=214',
        'wxPython==4.0.*',
    ]
)