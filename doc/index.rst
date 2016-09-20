adventurelib - easy text adventures
===================================

adventurelib provides basic functionality for writing text-based adventure
games, with the aim of making it easy enough for young teenagers to do.

The foundation of adventurelib is the ability to define functions that are
called in response to commands. For example, you could write a function to
be called when the user types commands like "take hat"::

    @when('take THING')
    def take(thing):
        print('You take the %s.' % thing)
        inventory.append(thing)

Contents:

.. toctree::
    :maxdepth: 2

    installing
    intro
    commands
    rooms
    items
    customising


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

