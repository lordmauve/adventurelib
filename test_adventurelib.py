import adventurelib
from adventurelib import Pattern, when, _handle_command

orig_commands = adventurelib.commands[:]


def teardown():
    """Reset the commands."""
    adventurelib.commands[:] = orig_commands


def test_match():
    matches = Pattern('apple').match(['apple'])
    assert matches == {}


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
