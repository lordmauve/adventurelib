from setuptools import setup

requirements = []


try:
    from shutil import get_terminal_size
except ImportError:
    requirements.append(
        'backports.shutil_get_terminal_size',
    )


setup(
    name='adventurelib',
    description='Easy text adventures',
    version='1.1',
    author='Daniel Pope',
    author_email='mauve@mauveweb.co.uk',
    url='https://adventurelib.readthedocs.io/',
    py_modules=['adventurelib'],
    install_requires=requirements,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Education',
        'Topic :: Games/Entertainment',
    ]
)
