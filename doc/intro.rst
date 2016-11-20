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
        print("You brush your teeth. They feel clean.")

If you start the game again you can try out the new command::

    > brush teeth
    You brush your teeth. They feel clean.


.. _say:

Using long text
---------------

Writing rich, descriptive text is your main tool for getting a player to feel
immersed in your game.

While Python's built-in ``print()`` function is useful for displaying output
to a user, it is a bit unwieldy when you want to write several lines of text
at once. You could write your descriptions like this, using ``+`` to glue
together individual strings::

    @when("brush teeth")
    def brush_teeth():
        print(
            "You squirt a bit too much toothpaste onto your " +
            "brush and dozily jiggle it round your mouth."
        )

This can be inconvenient and harder to make changes to. Adventurelib provides a
convenience function called ``say()`` that you can use instead to show longer
strings of text to the player. It's intended to be used with triple-quoted
strings like this::

    @when("brush teeth")
    def brush_teeth():
        say("""
            You squirt a bit too much toothpaste onto your
            brush and dozily jiggle it round your mouth.
        """)

This will clean up the spacing of the string, then wrap the output to the width
of the player's screen.

.. code-block:: none

    > brush teeth
    You squirt a bit too much toothpaste onto
    your brush and dozily jiggle it round
    your mouth.

It also supports multiple paragraphs of text, separated by blank lines::

    @when("brush teeth")
    def brush_teeth():
        say("""
            You squirt a bit too much toothpaste onto your
            brush and dozily jiggle it round your mouth.

            Your teeth feel clean and shiny now, as you
            run your tongue over them.
        """)

.. code-block:: none

    > brush teeth
    You squirt a bit too much toothpaste onto
    your brush and dozily jiggle it round
    your mouth.

    Your teeth feel clean and shiny now, as
    you run your tongue over them.

You do not have to use ``say()`` over ``print()``:

* ``print()`` will preserve the formatting of the strings you give it. This is
  sometimes needed; for example, to show a pre-formatted poem, or to display
  `ASCII art`_.
* Use ``say()`` to make it easier to output prose, in a way that will be
  easier for the player to read.

.. _`ASCII art`: https://en.wikipedia.org/wiki/ASCII_art

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
