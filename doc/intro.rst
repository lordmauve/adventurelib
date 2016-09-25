Introduction
============

In this section we'll look at how to get started writing a game with
adventurelib.

Starting a project
------------------

The first thing you'll need to do is import the good stuff from adventurelib::

    from adventurelib import *

Then, at the bottom of the file, call the ``start()`` function, which begins
the game::

    start()

Save the file.

Because we haven't added any behaviours, this game won't do very much, but we
should run it at this point as a "sanity check" that everything is installed.
If you're using IDLE, the game should just run, or you can run it at a command
prompt using the ``python`` or ``python3`` binary.

.. code-block:: bash

    python3 my_game.py

You should be able to get results like the following::

    > go north
    I don't understand 'go north'.

    > help
    Here is a list of the commands you can give:
    ?
    help
    quit

Pressing Ctrl+D will quit the game, or you can type the built-in ``quit``
command.


Adding a command
----------------

All of the rest of your code should go in between the ``from adventurelib
import *`` and the ``start()`` lines.

We can use the :doc:`@when <commands>` syntax to create a command that player
can type in order to interact with your game. Let's add a ``brush teeth``
command::

    @when("brush teeth")
    def brush_teeth():
        print(
            "You squirt a bit too much toothpaste onto your " +
            "brush and dozily jiggle it round your mouth a bit."
        )

If you start the game again you can try out the new command::

    > brush teeth
    You squirt a bit too much toothpaste onto your brush and dozily jiggle it
    round your mouth a bit.

Be creative
-----------

That's more or less all there is to it. Now you need to think up a good story
for your game.

Adventurelib can help with:

* :doc:`Calling your code in response to player commands <commands>`
* :doc:`Moving through interconnected locations <rooms>`
* :doc:`Referring to items and characters by name <items>`

...but you're going to need to use those features to tell a story that players
can interact with and get drawn into. You're going to have to write the Python
code that enforces the game's rules and lets you tell that story.

Think about:

* Characters
* Locations
* Emotions
* Detailed descriptions
* Expressive language
* How players will experience your game

Good luck and have fun!
