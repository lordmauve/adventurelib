# adventurelib

`adventurelib` provides basic functionality for writing text-based adventure
games, with the aim of making it easy enough for young teenagers to do.

The foundation of adventurelib is the ability to define functions that are
called in response to commands. For example, you could write a function to
be called when the user types commands like "take hat":

    @when('take THING')
    def take(thing):
        print('You take the %s.' % thing)
        inventory.append(thing)

It also includes the foundations needed to write games involving rooms, items,
characters and more... but users will have to implement these features for
themselves as they explore Python programming concepts.

## Installing

adventurelib.py is a single file that can be copied into your project. You can
also install it with pip:

    $ pip install adventurelib


## Documentation

[Comprehensive documentation is on Read The Docs.](http://adventurelib.readthedocs.io/)
