Customisations
==============

Of course, your game will have a unique story, but you can also change
adventurelib's behaviour to suit your game.

Below we will discuss some of the possible customisations and why you might
want to use them in a game.


Input Prompt
------------

Some games display status information in the prompt, such as health. For
example::

    10HP > attack grue
    You flail wildly at the grue, but it neatly side-steps you and
    kicks you in the ribs, for 1HP damage.

    9HP >

'HP' is an abbreviation for 'health points' that comes from classic computer
games. But you could use a Unicode heart symbol for this!

Alternatively, you might want to display some status at intervals in the game,
unrelated to the actions a player has taken, such as the footsteps in this
example::

    > north
    You enter a long, rocky passage dimly lit with flickering torches.
    The corridor curves to the east.

    You hear footsteps to the east.

    > east
    There's a small nook here. Sitting on a plinth is a crude idol of
    a beat with horns.

    You hear footsteps to the north.
    >

To customise the prompt, write a function that returns what the prompt string
should be. Usually it should end with a space. Then assign this function as
``adventurelib.prompt`` like this::

    import adventurelib  # Put this at the top of the file

    def prompt():
        return '{hp}HP > '.format(hp=player_hp)

    adventurelib.prompt = prompt


Disabling the help command
--------------------------

In some games, forcing the player to work out what to type is half the fun.

To make this kind of game work, it's important to respond to things that the
player types with custom responses, so be prepared to write a lot of ``@when``
functions that respond to many varieties of input.

However, the built-in ``help``/``?`` commands would spoil this kind of game by
giving all the answers.

You can disable the help by setting ``help=False`` when calling ``start()``::

    start(help=False)


Customising the "I don't understand" message
--------------------------------------------

When the player types a command that doesn't match any existing ``@when``
function, adventurelib responds with a basic "I don't understand" message::

    > jump up and down
    I don't understand 'jump up and down'.

This could get very boring if users see it a lot!

To customise this, write a function and assign it as
``adventurelib.no_command_matches``. This function should accept the input the
player typed as its argument, and print any responses::

    import adventurelib  # Put this at the top of the file

    def no_command_matches(command):
        print(random.choice([
            'Huh?',
            'Sorry?',
            'I beg your pardon?'
        ]))

    adventurelib.no_command_matches = no_command_matches
