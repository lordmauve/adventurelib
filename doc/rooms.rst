Rooms
=====

Many adventure games - but not all - have a concept of "rooms". A player can
explore rooms with some standard movement commands, perhaps finding interesting
items that they can use or characters they can speak to. Note that despite the
name, a room doesn't have to be a room of a house. You could use rooms to
describe any concept of location, in order to tell your story:

* Drifting in space
* On top of a hill
* Underneath the floorboards
* Nowhere

Adventurelib provides a helper object called ``Room``, that can be used within
your program. You don't have to use this object in order to create the
impression of rooms though. You can do it with creative use of ``@when``
functions.


Creating a room
---------------

Rooms are created by passing a description. Rich descriptions that convey a
story to the user are very important to make your text adventure immersive,
so try to write at least a couple of sentences. ::

    from adventurelib import *

    space = Room("""
    You are drifting in space. It feels very cold.

    A slate-blue spaceship sits completely silently to your left,
    its airlock open and waiting.
    """)

    spaceship = Room("""
    The bridge if the spaceship is shiny and white, with thousands
    of small, red, blinking lights.
    """)


Next you'll want the ability to move between rooms. adventurelib doesn't track
what room the player is in; this is your responsibility!::

    # current_room will be a global variable. Let's start out in
    # space, so assign the 'space' room from above.
    current_room = space


    @when('enter airlock')
    def enter_spaceship():
        # To set a global variable from within a function you have
        # to include the 'global' keyword, to avoid creating a
        # local variable instead.
        global current_room

        # Got to check if this action can be done here
        if current_room is not space:
            print('There is no airlock here.')
            return

        current_room = spaceship

        # You should include some narrative for every action to
        # ensure the transition doesn't feel abrupt.
        print(
            "You heave yourself into the airlock and slam your " +
            "hand on the button to close the outer door."
        )

        # Show the room description to indicate we have arrived.
        print(current_room)


Storing attributes on rooms
---------------------------

Part of the reason for rooms is to have different objects or contexts for the
story. Some actions could only be possible in some rooms. You can assign
arbitrary attribute names to an object in order to track the state of a room
or what actions can be performed there. You can also set attributes on the
``Room`` object, which apply for all rooms::

    Room.can_scream = True  # The default for all rooms
    space.can_scream = False  # Set a value for a specific room.

    @when('scream')
    def scream():
        if current_room.can_scream:
            print(
                "You unleash a piercing shriek that " +
                "reverberates around you."
            )
        else:
            print(
                "You try to yell but there's no sound " +
                "in the vacuum of space."
            )

If you access an attribute that doesn't exist on a room, an ``AttributeError``
will be raised, so ensure that you either set an attribute on every single
room or set a default value on ``Room``.


Directions and exits
--------------------

Many text adventure games let players explore a system of rooms freely, using
common commands such as ``north``, ``south``, ``east`` and ``west``.

``Room`` objects support these compass point directions by default. If you
assign a room as the ``north`` attribute of another room, then you can traverse
this relationship. ::

    space.north = spaceship

Then one could access the room to the north of the current room using normal
attribute access::

    current_room.north

The key feature of the directions system is that these references are
**bi-directional**. adventurelib knows that ``north`` is the opposite of
``south``, so these relationships automatically hold::

    >>> space.north is spaceship
    True
    >>> spaceship.south is space
    True


Exits
-----

Rooms have a couple of methods that allow you to query what exits they have.

These can be useful when writing commands that use the room layout (such as
moving or looking in a direction).


.. function:: room.exit(direction)

    Get the Room that is linked in direction (eg. ``north``). Returns ``None``
    if there is no room in that direction.

.. function:: room.exits()

    Get a list of direction names where a direction is set.


Moving between rooms
--------------------

To follow the links you've defined you could define separate ``north``,
``south``, ``east`` and ``west`` handlers - but the code would be mostly the
same, and this is annoying to type and make changes to.

Instead, we can define one function and use several different ``@when`` lines
to define the directions we will go. Each one will pass a direction in which
to go.::

    @when('north', direction='north')
    @when('south', direction='south')
    @when('east', direction='east')
    @when('west', direction='west')
    def go(direction):
        global current_room
        room = current_room.exit(direction)
        if room:
            current_room = room
            print('You go %s.' % direction)
            look()


Then in game::

    > north
    You go north.
    There is a polar bear here.

    > south
    You go south.
    It is a bright, sunny day.

These can be some of the most heavily used command, so you could also provide
alias commands ``n``, ``s``, ``e`` and ``w`` as a convenience::

    @when('north', direction='north')
    @when('south', direction='south')
    @when('east', direction='east')
    @when('west', direction='west')
    @when('n', direction='south')
    @when('s', direction='south')
    @when('e', direction='east')
    @when('w', direction='west')
    def go(direction):
        ...

Adding more directions
----------------------

While ``north``, ``south``, ``east`` and ``west`` are built into adventurelib,
you don't have to use them. You can also register new directions, so long as
you give an opposite. You would typically do this at the top of the file,
before you define any rooms::

    Room.add_direction('up', 'down')
    Room.add_direction('enter', 'exit')

    tent = Room(...)
    camp = Room(...)
    river = Room(...)
    camp.enter = tent
    camp.down = river
