from setuptools import setup
import platform
if platform.system() is 'Windows':
    from buildexe import setup_args
elif platform.system() is 'Darwin':
    from buildapp import setup_args

setup(**setup_args)
