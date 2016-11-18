import os
from unittest.mock import patch
from contextlib import redirect_stdout
from io import StringIO

import adventurelib
from adventurelib import Pattern, when, _handle_command, say, Room, Item, Bag

orig_commands = adventurelib.commands[:]


def teardown():
    """Reset the commands."""
    adventurelib.commands[:] = orig_commands


def test_match():
    matches = Pattern('apple').match(['apple'])
    assert matches == {}


def test_no_match_different_words():
    matches = Pattern('look').match(['apple'])
    assert matches is None


def test_no_match_extra_words():
    matches = Pattern('look').match(['look', 'at', 'butler'])
    assert matches is None


def test_multiple_words():
    pat = Pattern('take apple')
    matches = pat.match(['take', 'apple'])
    assert matches == {}


def test_multiple_words_mismatch():
    matches = Pattern('take apple').match(['take', 'tortoise'])
    assert matches is None


def test_multiple_words_mismatch_length():
    matches = Pattern('take apple').match(['take', 'golden', 'apple'])
    assert matches is None


def test_capturing_match():
    matches = Pattern('take ITEM').match(['take', 'apple'])
    assert matches == {'item': 'apple'}


def test_multiple_captures():
    pat = Pattern('give ITEM to PERSON')
    matches = pat.match(['give', 'apple', 'to', 'wizard'])
    assert matches == {'item': 'apple', 'person': 'wizard'}


def test_capturing_multiword():
    matches = Pattern('take ITEM').match(['take', 'golden', 'apple'])
    assert matches == {'item': 'golden apple'}


def test_multiple_multiword_captures():
    pat = Pattern('give ITEM to PERSON')
    matches = pat.match(['give', 'golden', 'apple', 'to', 'evil', 'wizard'])
    assert matches == {'item': 'golden apple', 'person': 'evil wizard'}


def test_word_combinations():
    combos = Pattern.word_combinations(have=3, placeholders=2)
    assert list(combos) == [
        (2, 1),
        (1, 2)
    ]


def test_word_combinations_2():
    combos = Pattern.word_combinations(have=4, placeholders=2)
    assert list(combos) == [
        (3, 1),
        (2, 2),
        (1, 3)
    ]


def test_word_combinations_3():
    combos = Pattern.word_combinations(have=4, placeholders=3)
    assert list(combos) == [
        (2, 1, 1),
        (1, 2, 1),
        (1, 1, 2)
    ]


def test_word_combinations_4():
    combos = Pattern.word_combinations(have=5, placeholders=3)
    assert list(combos) == [
        (3, 1, 1),
        (2, 2, 1),
        (2, 1, 2),
        (1, 3, 1),
        (1, 2, 2),
        (1, 1, 3),
    ]


def test_register():
    called = False

    @when('north')
    def func():
        nonlocal called
        called = True

    print(adventurelib.commands)
    _handle_command('north')
    assert called is True


def test_register_args():
    args = None

    @when('north', dir='north')
    def func(dir):
        nonlocal args
        args = [dir]
    _handle_command('north')
    assert args == ['north']


def test_register_match():
    args = None

    @when('hit TARGET with WEAPON', verb='hit')
    def func(target, weapon, verb):
        nonlocal args
        args = [target, weapon, verb]
    _handle_command('hit dragon with glass sword')
    assert args == ['dragon', 'glass sword', 'hit']


def say_at_width(width, msg):
    buf = StringIO()
    with patch('adventurelib.get_terminal_size', return_value=(width, 24)):
        with redirect_stdout(buf):
            say(msg)
    return buf.getvalue()


def test_say_room():
    """saw() will format input as strings."""
    r = Room('You are standing in a hallway.')

    buf = StringIO()
    with redirect_stdout(buf):
        say(r)
    assert buf.getvalue() == 'You are standing in a hallway.\n'


def test_say_wrap():
    """The say() function will print output wrapped to the terminal width."""
    out = say_at_width(40, """
    This is a long sentence that the say command will wrap.
    """)

    assert out == (
        "This is a long sentence that the say\n"
        "command will wrap.\n"
    )


def test_say_wrap2():
    """The say() function will print output wrapped to the terminal width."""
    out = say_at_width(20, """
    This is a long sentence that the say command will wrap.
    """)

    assert out == (
        "This is a long\n"
        "sentence that the\n"
        "say command will\n"
        "wrap.\n"
    )


def test_say_paragraph():
    out = say_at_width(40, """
    This is a long sentence that the say command will wrap.

    And this is a second paragraph that is separately wrapped.
    """)

    assert out == (
        "This is a long sentence that the say\n"
        "command will wrap.\n"
        "\n"
        "And this is a second paragraph that is\n"
        "separately wrapped.\n"
    )


@patch('random.randrange', return_value=0)
def test_bag_get_random(randrange):
    """We can select an item from a bag at random."""
    bag = Bag(['a', 'b', 'c'])
    assert bag.get_random() == list(bag)[0]
    randrange.assert_called_once_with(3)


@patch('random.randrange', return_value=1)
def test_bag_get_random2(randrange):
    """We can select an item from a bag at random."""
    bag = Bag(['a', 'b', 'c'])
    assert bag.get_random() == list(bag)[1]
    randrange.assert_called_once_with(3)


def test_empty_bag_get_random():
    """Choosing from an empty bag returns None."""
    bag = Bag()
    assert bag.get_random() is None


@patch('random.randrange', return_value=0)
def test_bag_take_random(randrange):
    """We can select and remove an item from a bag at random."""
    bag = Bag(['a', 'b', 'c'])
    items = list(bag)
    assert bag.take_random() == items[0]
    assert bag == Bag(items[1:])
    randrange.assert_called_once_with(3)


def test_bag_find():
    name, *aliases = ['Name', 'UPPER ALIAS', 'lower alias']
    bag = Bag({
        Item(name, *aliases)
    })

    assert bag.find('name')
    assert bag.find('Name')
    assert bag.find('NAME')
    assert bag.find('upper alias')
    assert bag.find('LOWER ALIAS')
    assert not bag.find('other')
