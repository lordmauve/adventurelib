from setuptools import setup
from adventurelib import __version__

requirements = []
extras_require = {
    'prompt_toolkit':  ["prompt_toolkit >= 2.0.0"]
}

try:
    from shutil import get_terminal_size  # noqa
except ImportError:
    requirements.append(
        'backports.shutil_get_terminal_size',
    )


setup(
    name='adventurelib',
    description='Easy text adventures',
    version=__version__,
    author='Daniel Pope',
    author_email='mauve@mauveweb.co.uk',
    url='https://adventurelib.readthedocs.io/',
    py_modules=['adventurelib'],
    install_requires=requirements,
    extras_require=extras_require,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Education',
        'Topic :: Games/Entertainment',
    ]
)
