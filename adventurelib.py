"""Simple library for writing Text Adventures in Python"""
import re
import sys
import inspect
import textwrap
import random
from copy import deepcopy
try:
    from shutil import get_terminal_size
except ImportError:
    try:
        from backports.shutil_get_terminal_size import get_terminal_size
    except ImportError:
        def get_terminal_size(fallback=(80, 24)):
            """Fallback definition for terminal size getting"""
            return fallback


__all__ = (
    'when',
    'start',
    'Room',
    'Pattern',
    '_handle_command',
    'Item',
    'Bag',
    'say',
)


class InvalidCommand(Exception):
    """A command is not defined correctly."""


class InvalidDirection(Exception):
    """User attempts to travel in an invalid direction."""


class Placeholder:
    """Match a word in a command string."""
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name.upper()


class Room:
    """A generic room object that can be used by game code."""

    _directions = {}

    @staticmethod
    def add_direction(forward, reverse):
        """Add a direction."""
        for direc in (forward, reverse):
            if not direc.islower():
                raise InvalidCommand(
                    'Invalid direction %r: directions must be all lowercase.'
                )
            if direc in Room._directions:
                raise KeyError('%r is already a direction!' % dir)
        Room._directions[forward] = reverse
        Room._directions[reverse] = forward

        # Set class attributes to None to act as defaults
        setattr(Room, forward, None)
        setattr(Room, reverse, None)

    def __init__(self, description):
        self.description = description.strip()

        # Copy class Bags to instance variables
        for k, v in vars(type(self)).items():
            if isinstance(v, Bag):
                setattr(self, k, deepcopy(v))

    def __str__(self):
        return self.description

    def exit(self, direction):
        """Get the exit of a room in a given direction.

        Return None if the room has no exit in a direction.

        """
        if direction not in self._directions:
            raise KeyError('%r is not a direction' % direction)
        return getattr(self, direction, None)

    def exits(self):
        """Get a list of directions to exit the room."""
        return sorted(d for d in self._directions if getattr(self, d))

    def __setattr__(self, name, value):
        if isinstance(value, Room):
            if name not in self._directions:
                raise InvalidDirection(
                    '%r is not a direction you have declared.\n\n' +
                    'Try calling Room.add_direction(%r, <opposite>) ' % name +
                    ' where <opposite> is the return direction.'
                )
            reverse = self._directions[name]
            object.__setattr__(self, name, value)
            object.__setattr__(value, reverse, self)
        else:
            object.__setattr__(self, name, value)


Room.add_direction('north', 'south')
Room.add_direction('east', 'west')


class Item:
    """A generic item object that can be referred to by a number of names."""

    def __init__(self, name, *aliases):
        self.name = name
        self.aliases = tuple(
            label.lower()
            for label in (name,) + aliases
        )

    def __repr__(self):
        return '%s(%s)' % (
            type(self).__name__,
            ', '.join(repr(n) for n in self.aliases)
        )

    def __str__(self):
        return self.name


class Bag(set):
    """A collection of Items, such as in an inventory.

    Behaves very much like a set, but the 'in' operation is overloaded to
    accept a str item name, and there is a ``take()`` method to remove an item
    by name.

    """
    def find(self, name):
        """Find an object in the bag by name, but do not remove it.

        Return None if the name does not match.

        """
        for item in self:
            if name.lower() in item.aliases:
                return item
        return None

    def __contains__(self, v):
        """Return True if an Item is present in the bag.

        If v is a str, then find the item by name, otherwise find the item by
        identity.

        """
        if isinstance(v, str):
            return bool(self.find(v))
        else:
            return set.__contains__(self, v)

    def take(self, name):
        """Remove an Item from the bag if it is present.

        If multiple names match, then return one of them.

        Return None if no item matches the name.

        """
        obj = self.find(name)
        if obj is not None:
            self.remove(obj)
        return obj

    def get_random(self):
        """Choose an Item from the bag at random, but don't remove it.

        Return None if the bag is empty.

        """
        if not self:
            return None
        which = random.randrange(len(self))
        for index, obj in enumerate(self):
            if index == which:
                return obj

    def take_random(self):
        """Remove an Item from the bag at random, and return it.

        Return None if the bag is empty.

        """
        obj = self.get_random()
        if obj is not None:
            self.remove(obj)
        return obj


def _register(command, func, kwargs=None):
    """Register func as a handler for the given command."""
    if kwargs is None:
        kwargs = {}
    pattern = Pattern(command)
    sig = inspect.signature(func)
    func_argnames = set(sig.parameters)
    when_argnames = set(pattern.argnames) | set(kwargs.keys()) | {'game'}
    if func_argnames != when_argnames:
        raise InvalidCommand(
            'The function %s%s has the wrong signature for @when(%r)' % (
                func.__name__, sig, command
            ) + '\n\nThe function arguments should be (%s)' % (
                ', '.join(pattern.argnames + list(kwargs.keys()))
            )
        )

    commands.append((pattern, func, kwargs))


class Pattern:
    """Command-matching pattern"""
    def __init__(self, pattern):
        self.orig_pattern = pattern
        words = pattern.split()
        match = []
        argnames = []
        self.placeholders = 0
        for w in words:
            if not w.isalpha():
                raise InvalidCommand(
                    'Invalid command %r' % w +
                    'Commands may consist of letters only.'
                )
            if w.isupper():
                arg = w.lower()
                argnames.append(arg)
                match.append(Placeholder(arg))
                self.placeholders += 1
            elif w.islower():
                match.append(w)
            else:
                raise InvalidCommand(
                    'Invalid command %r' % w +
                    '\n\nWords in commands must either be in lowercase or ' +
                    'capitals, not a mix.'
                )
        self.argnames = argnames
        self.prefix = []
        for w in match:
            if isinstance(w, Placeholder):
                break
            self.prefix.append(w)
        self.pattern = match[len(self.prefix):]
        self.fixed = len(self.pattern) - self.placeholders

    def __repr__(self):
        return '%s(%r)' % (
            type(self).__name__,
            self.orig_pattern
        )

    @staticmethod
    def word_combinations(have, placeholders):
        """??? (not sure what this does)"""
        if have < placeholders:
            return
        if have == placeholders:
            yield (1,) * placeholders
            return
        if placeholders == 1:
            yield (have,)
            return

        # Greedy - start by taking everything
        other_groups = placeholders - 1
        take = have - other_groups
        while take > 0:
            remain = have - take
            if have >= placeholders - 1:
                combos = Pattern.word_combinations(remain, other_groups)
                for buckets in combos:
                    yield (take,) + tuple(buckets)
            take -= 1  # backtrack

    def match(self, input_words):
        """Attempt to match a command against the pattern"""
        if len(input_words) < len(self.argnames):
            return None

        if input_words[:len(self.prefix)] != self.prefix:
            return None

        input_words = input_words[len(self.prefix):]

        if not input_words and not self.pattern:
            return {}
        if bool(input_words) != bool(self.pattern):
            return None

        have = len(input_words) - self.fixed

        for combo in self.word_combinations(have, self.placeholders):
            matches = {}
            take = iter(combo)
            inp = iter(input_words)
            try:
                for cword in self.pattern:
                    if isinstance(cword, Placeholder):
                        count = next(take)
                        ws = []
                        for _ in range(count):
                            ws.append(next(inp))
                        matches[cword.name] = ws
                    else:
                        word = next(inp)
                        if cword != word:
                            break
                else:
                    return {k: ' '.join(v) for k, v in matches.items()}
            except StopIteration:
                continue
        return None


def prompt():
    """Called to get the prompt text."""
    return '> '


def no_command_matches(command):
    """Called when a command is not understood."""
    print("I don't understand '%s'." % command)


def when(command, **kwargs):
    """Decorator for command functions."""
    def dec(func):
        """decorator"""
        _register(command, func, kwargs)
        return func
    return dec


def cmd_help():
    """Print a list of the commands you can give."""
    print('Here is a list of the commands you can give:')
    cmds = sorted(c.orig_pattern for c, _, _ in commands)
    for c in cmds:
        print(c)


def _handle_command(cmd, game=None):
    """Handle a command typed by the user."""
    ws = cmd.lower().split()
    for pattern, func, kwargs in commands:
        args = kwargs.copy()
        matches = pattern.match(ws)
        if matches is not None:
            args.update(matches)
            func(**args, game=game)
            break
    else:
        no_command_matches(cmd)
    print()


class Interface:
    """Superclass for all interfaces (ways of interacting with the game)"""
    def __init__(self):
        pass
    
    def get_command(self, prompt):
        """Get a command"""
        return ''
    
    def say(self, msg):
        """Send output to the user"""
        pass

        
class TerminalInterface(Interface):
    """Interface for basic terminal I/O (the default)"""
    def get_command(self, prompt):
        """Get a command"""
        return input(prompt).strip()
    
    def say(self, msg):
        """Print a message.

        Unlike print(), this deals with de-denting and wrapping of text to fit
        within the width of the terminal.

        Paragraphs separated by blank lines in the input will be wrapped
        separately.

        """
        msg = str(msg)
        msg = re.sub(r'^[ \t]*(.*?)[ \t]*$', r'\1', msg, flags=re.M)
        width = get_terminal_size()[0]
        paragraphs = re.split(r'\n(?:[ \t]*\n)', msg)
        formatted = (textwrap.fill(p.strip(), width=width) for p in paragraphs)
        print('\n\n'.join(formatted))

        
class Game:
    """Game World Environment"""
    def __init__(self, interface: Interface):
        self.worldvars = {}
        self.interface = interface
        self.say = self.interface.say
    
    def __getattr__(self, item):
        try:
            return self.worldvars[item]
        except KeyError:
            raise AttributeError()
    
    def __setattr__(self, attr, val):
        if attr in {'worldvars', 'interface', 'say'}:
            print('  in dict')
            self.__dict__[attr] = val
        else:
            self.worldvars[attr] = val


def start(setup=None, interface: Interface=TerminalInterface(), help=True):
    """Run the game."""
    if help:
        qmark = Pattern('help')
        qmark.prefix = ['?']
        qmark.orig_pattern = '?'
        commands.insert(0, (Pattern('help'), cmd_help, {}))
        commands.insert(0, (qmark, cmd_help, {}))
    
    game = Game(interface)
    
    if setup is not None:
        setup(game)
    
    while True:
        try:
            cmd = interface.get_command(prompt())
        except EOFError:
            print()
            break

        if not cmd:
            continue

        _handle_command(cmd, game)


def say(msg):
    """Print a message.

    Unlike print(), this deals with de-denting and wrapping of text to fit
    within the width of the terminal.

    Paragraphs separated by blank lines in the input will be wrapped
    separately.

    """
    msg = str(msg)
    msg = re.sub(r'^[ \t]*(.*?)[ \t]*$', r'\1', msg, flags=re.M)
    width = get_terminal_size()[0]
    paragraphs = re.split(r'\n(?:[ \t]*\n)', msg)
    formatted = (textwrap.fill(p.strip(), width=width) for p in paragraphs)
    print('\n\n'.join(formatted))


commands = [
    (Pattern('quit'), sys.exit, {}),  # quit command is built-in
]
