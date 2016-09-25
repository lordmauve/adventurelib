Binding commands
================

Text adventure games respond to commands entered by the player. Some typical
commands might be:

* ``north``
* ``take wand``
* ``give wand to wizard``

adventurelib lets the programmer write code that will run when a command is
entered. This means you can decide what happens in response to a command. Your
code might decide whether the wizard wants the wand and print what the wizard
says when he gets it.

Note that you also needs to check that the wizard is here and you have the
wand to give to him!


@when decorator
---------------

The ``@when`` decorator is written on the line above a function. The function
will then be called when a player types a matching command.

This code will be called when the player types "scream"::

    @when("scream")
    def scream():
        print("You unleash a piercing shriek that reverberates around you.")

Note that this is case-insensitive, so it will also be called when the player
types "SCREAM" or "sCrEAM"::

    > scream
    You unleash a piercing shriek that reverberates around you.

    > SCREAM
    You unleash a piercing shriek that reverberates around you.

You can put multiple words into the command. You can also write more than
one ``@when`` line, which means the function will be called if any of the
commands match. This can make it easier for the player to work out what to
type::

    @when("shout loudly")
    @when("shout")
    @when("yell")
    def yell():
        print("You bellow at the top of your lungs.")

And then in game::

    > yell
    You bellow at the top of your lungs.

    > shout loudly
    You bellow at the top of your lungs.


As with the case of what a player types, so too the spacing of what a player
types doesn't matter::

    >   shout        loudly
    You bellow at the top of your lungs.

All the words you want the player to type have to be in lower case letters.


Capturing values
----------------

While you could write separate functions for "take wand" and "take hat", it's
more normal to write a single function that will be called when the player
types "take *anything*".

This code will be called when the player types "take *anything*", and the words
that match the *anything* will be passed into the function so that you can
react to what it was they tried to take::

    @when("take THING")
    def take(thing):
        print("You take the %s." % thing)

So, in a game::

    > take hat
    You take the hat.

    > take horse
    You take the horse.

    > take cheeseburger
    You take the cheeseburger.

Of course, this isn't a very useful function, because it does not check that
there is a thing to take! You will have to write the code that does these
checks.

Here's another example, where we capture two words::

    @when("give ITEM to RECIPIENT")
    def give(item, recipient):
        print("You give the %s to the %s." % (item, recipient))

Here are the rules for what you can write:

* All the words you want the player to type have to be in lower case letters.
* Words that you write in CAPITAL LETTERS will match any word the player types.
* For each word you write in CAPITAL LETTERS, the function has to take a
  parameter with the same name in lowercase letters.
* The function will be called with the names the player typed - but they will
  be converted to lower case.


Capturing multi-word names
--------------------------

An UPPERCASE name can match multiple words. If your code contains the above
example::

    @when("give ITEM to RECIPIENT")

Then a player can type:

.. code-block:: none

    > give poison apple to evil godmother

And your code will receive the values::

    item = "poison apple"
    recipient = "evil godmother"

As long as you require players to type some command words between ``ITEM`` and
``RECIPIENT`` (``to`` in this case), this will do what you expect.  But beware
of providing a shorter alias::

    @when("give ITEM RECIPIENT")

Adventurelib uses what's called a **greedy algorithm** - "greedy", because the
first group will hungrily "eat" as many words as it can. If a player typed:

.. code-block:: none

    > give poison apple evil godmother

Then ``ITEM`` will "eat" the first three words, and your code will receive the
values::

    item = "poison apple evil"
    recipient = "godmother"

Which is probably not what you expect!

However, each CAPITALISED word will match at least one word. So ``give apple
godmother`` will do what you expect. Therefore one solution is to make sure
every object in the game can be referred to by a single-word name like
``apple``. This can work well in simple games, but the drawback is that you
would struggle to create puzzles that involve multiple variations on an object:

.. code-block:: none

    > inventory
    You have:
    a red apple
    a blue apple

    > feed red apple to water nymph
    The nymph sticks out her tongue and shivers unenthusiastically.

    > feed blue apple to water nymph
    The nymph's eyes widen as you take out the blue apple. She dashes
    towards you and snatches it from your hands, and then immediately
    turns and runs towards the small door.

    Glancing back towards you momentarily, she wordlessly tosses you
    a slender, silver-blue key, and a moment later is gone.

It is probably best to require words like ``to``, ``with`` and ``on``, so that
adventurelib knows how to split up a phrase::

   @when('give ITEM to RECIPIENT')

   @when('use ITEM on TARGET')

   @when('hit TARGET with WEAPON')


Additional parameters to commands
---------------------------------

In some cases, you might like to use a function to handle a number of similar
commands.

You can pass additional keyword arguments to the ``@when`` decorator which will
be passed into the handler function whenever that version of the command line
matched.

For example::

    @when('shout', action='bellow')
    @when('yell', action='holler')
    @when('scream', action='shriek')
    def shout(action):
        print('You %s loudly.' % action)


Calling @when functions yourself
--------------------------------

Even though you've written a ``@when`` function and it will be called
automatically when the player enters that command, you can still call the
function yourself normally.

For example, if you write a ``look`` command, you can call this from other
commands, such as when you enter a room:

.. code-block:: python
    :emphasize-lines: 11

    @when('look'):
    def look():
        print(current_room)


    @when('go north'):
    def go_north():
        global current_room
        current_room = current_room.north
        print('You go north.')
        look()
