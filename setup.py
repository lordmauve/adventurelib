from os.path import abspath, dirname, join
from setuptools import setup
from adventurelib import __version__


ROOT = abspath(dirname(__file__))


with open(join(ROOT, "README.md")) as fd:
    README = fd.read()

setup(
    name='adventurelib',
    description='Easy text adventures',
    long_description=README,
    long_description_content_type="text/markdown",
    version=__version__,
    author='Daniel Pope',
    author_email='mauve@mauveweb.co.uk',
    url='https://github.com/lordmauve/adventurelib',
    project_urls={
        'Documentation': 'https://adventurelib.readthedocs.io/'
    },
    py_modules=['adventurelib'],
    extras_require={
        ':python_version < "3.3"': [
            'backports.shutil_get_terminal_size>=1.0.0',
        ],
    },
    python_requires='>=3',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Education',
        'Topic :: Games/Entertainment',
    ]
)
