import re
import sys
import inspect
try:
    import readline  # noqa: adds readline semantics to input()
except ImportError:
    pass
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
            return fallback

__version__ = '1.2.1'
__all__ = (
    'when',
    'start',
    'Room',
    'Item',
    'Bag',
    'say',
    'set_context',
    'get_context',
)


#: The current context.
#:
#: Commands will only be available if their context is "within" the currently
#: active context, a functiondefined by '_match_context()`.
current_context = None


#: The separator that defines the context hierarchy
CONTEXT_SEP = '.'


def set_context(new_context):
    """Set current context.

    Set the context to `None` to clear the context.

    """
    global current_context
    _validate_context(new_context)
    current_context = new_context


def get_context():
    """Get the current command context."""
    return current_context


def _validate_context(context):
    """Raise an exception if the given context is invalid."""
    if context is None:
        return

    err = []
    if not context:
        err.append('be empty')
    if context.startswith(CONTEXT_SEP):
        err.append('start with {sep}')
    if context.endswith(CONTEXT_SEP):
        err.append('end with {sep}')
    if CONTEXT_SEP * 2 in context:
        err.append('contain {sep}{sep}')
    if err:
        if len(err) > 1:
            msg = ' or '.join([', '.join(err[:-1]), err[-1]])
        else:
            msg = err[0]
        msg = 'Context {ctx!r} may not ' + msg
        raise ValueError(msg.format(sep=CONTEXT_SEP, ctx=context))


def _match_context(context, active_context):
    """Return True if `context` is within `active_context`.

    adventurelib offers a hierarchical system of contexts defined with a
    dotted-string notation.

    A context matches if the active context is "within" the pattern's context.

    For example:

    * ``ham.spam`` is within ``ham.spam``
    * ``ham.spam`` is within ``ham``
    * ``ham.spam`` is within ``None``.
    * ``ham.spam`` is not within ``ham.spam.eggs``
    * ``ham.spam`` is not within ``spam`` or ``eggs``
    * ``None`` is within ``None`` and nothing else.

    """
    if context is None:
        # If command has no context, it always matches
        return True

    if active_context is None:
        # If the command has a context, and we don't, no match
        return False

    # The active_context matches if it starts with context and is followed by
    # the end of the string or the separator
    clen = len(context)
    return (
        active_context.startswith(context) and
        active_context[clen:clen + len(CONTEXT_SEP)] in ('', CONTEXT_SEP)
    )


class InvalidCommand(Exception):
    """A command is not defined correctly."""


class InvalidDirection(Exception):
    """The direction specified was not pre-declared."""


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
        for dir in (forward, reverse):
            if not dir.islower():
                raise InvalidCommand(
                    'Invalid direction %r: directions must be all lowercase.'
                )
            if dir in Room._directions:
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._alias_dict = {}
        for item in self:
            self._add_aliases(item)

    #######
    # Convenience functions to update internal alias dict.
    ####### 
    def _add_aliases(self, item):
        """Updates"""
        for alias in item.aliases:
            self._alias_dict.setdefault(alias.lower(), set()).add(item)

    def _discard_aliases(self, item):
        for alias in item.aliases:
            item_set = self._alias_dict.get(alias.lower(), set())
            item_set.discard(item)

            # Avoids memory leaks when many items are added/removed.
            if not item_set and alias in self._alias_dict:
                del self._alias_dict[alias]

    ####### 
    # Implementations of base set interface.
    ####### 
    def add(self, item):
        super().add(item)
        self._add_aliases(item)

    def clear(self):
        super().clear()
        self._alias_dict.clear()

    def copy(self):
        result = super().copy()
        result._alias_dict = self._alias_dict.copy()
        return result

    def difference(self, other_bag):
        return Bag(super().difference(other_bag))

    def difference_update(self, other_bag):
        for element in other_bag:
            self.discard(element)

    def discard(self, item):
        super().discard(item)
        self._discard_aliases(item)

    def intersection(self, other_bag):
        return Bag(super().intersection(other_bag))

    def intersection_update(self, other_bag):
        for element in other_bag:
            self.add(element)

    def pop(self):
        result = super().pop()
        self._discard_aliases(result)
        return result

    def remove(self, item):
        super().remove(item)
        self._discard_aliases(item)

    def symmetric_difference(self, other_bag):
        return Bag(super().symmetric_difference(other_bag))

    def symmetric_difference_update(self, other_bag):
        diff = super().symmetric_difference(other_bag)
        for element in self:
            if element not in diff:
                self.remove(element)
        for element in diff:
            if element not in self:
                self.add(element)

    def union(self, other_bag):
        return Bag(super().union(other_bag))

    def update(self, elements):
        for element in elements:
            self.add(element)

    ####### 
    # Bag interface.
    ####### 
    def find(self, name):
        """Find an object in the bag by name, but do not remove it.

        Return None if the name does not match.
        
        If more than one object with the same name exists, returns one of them.

        """
        name = name.lower()
        for element in self._alias_dict.get(name, []):
            return element

    def __contains__(self, v):
        """Return True if an Item is present in the bag.

        If v is a str, then find the item by name, otherwise find the item by
        identity.

        """
        if isinstance(v, str):
            return bool(self.find(v))
        else:
            return super().__contains__(v)

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


def _register(command, func, context=None, kwargs=None):
    """Register func as a handler for the given command."""
    if kwargs is None:
        kwargs = {}
    pattern = Pattern(command, context)
    sig = inspect.signature(func)
    func_argnames = set(sig.parameters)
    when_argnames = set(pattern.argnames) | set(kwargs.keys())
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
    """A pattern for matching a command.

    Patterns are defined with a string like 'take ITEM' which corresponds to
    matching 'take' exactly followed by capturing one or more words as the
    group named 'item'.
    """

    def __init__(self, pattern, context=None):
        self.orig_pattern = pattern
        _validate_context(context)
        self.pattern_context = context
        words = pattern.split()
        match = []
        argnames = []
        self.placeholders = 0
        for w in words:
            if not w.isalpha():
                raise InvalidCommand(
                    'Invalid command %r' % pattern +
                    'Commands may consist of letters only.'
                )
            if w.isupper():
                arg = w.lower()
                if arg in argnames:
                    raise InvalidCommand(
                            'Invalid command %r' % pattern +
                            ' Identifiers may only be used once'
                            )
                argnames.append(arg)
                match.append(Placeholder(arg))
                self.placeholders += 1
            elif w.islower():
                match.append(w)
            else:
                raise InvalidCommand(
                    'Invalid command %r' % pattern +
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
        ctx = ''
        if self.pattern_context:
            ctx = ', context=%r' % self.pattern_context
        return '%s(%r%s)' % (
            type(self).__name__,
            self.orig_pattern,
            ctx
        )

    @staticmethod
    def word_combinations(have, placeholders):
        """Iterate over possible assignments of words in have to placeholders.

        `have` is the number of words to allocate and `placeholders` is the
        number of placeholders that those could be distributed to.

        Return an iterable of tuples of integers; the length of each tuple
        will match `placeholders`.

        """
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

    def is_active(self):
        """Return True if a command is active in the current context."""
        return _match_context(self.pattern_context, current_context)

    def ctx_order(self):
        """Return an integer indicating how nested the context is."""
        if not self.pattern_context:
            return 0
        return self.pattern_context.count(CONTEXT_SEP) + 1

    def match(self, input_words):
        """Match a given list of input words against this pattern.

        Return a dict of captured groups if the pattern matches, or None if
        the pattern does not match.

        """
        global current_context

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


def when(command, context=None, **kwargs):
    """Decorator for command functions."""
    def dec(func):
        _register(command, func, context, kwargs)
        return func
    return dec


def help():
    """Print a list of the commands you can give."""
    print('Here is a list of the commands you can give:')
    cmds = sorted(c.orig_pattern for c, _, _ in commands if c.is_active())
    for c in cmds:
        print(c)


def _available_commands():
    """Return the list of available commands in the current context.

    The order will be the order in which they should be considered, which
    corresponds to how deeply nested the context is.

    """
    available_commands = []
    for c in commands:
        pattern = c[0]
        if pattern.is_active():
            available_commands.append(c)
    available_commands.sort(
        key=lambda c: c[0].ctx_order(),
        reverse=True,
    )
    return available_commands


def _handle_command(cmd):
    """Handle a command typed by the user."""
    ws = cmd.lower().split()

    for pattern, func, kwargs in _available_commands():
        args = kwargs.copy()
        matches = pattern.match(ws)
        if matches is not None:
            args.update(matches)
            func(**args)
            break
    else:
        no_command_matches(cmd)
    print()


def start(help=True):
    """Run the game."""
    if help:
        # Ugly, but we want to keep the arguments consistent
        help = globals()['help']
        qmark = Pattern('help')
        qmark.prefix = ['?']
        qmark.orig_pattern = '?'
        commands.insert(0, (Pattern('help'), help, {}))
        commands.insert(0, (qmark, help, {}))
    while True:
        try:
            cmd = input(prompt()).strip()
        except EOFError:
            print()
            break

        if not cmd:
            continue

        _handle_command(cmd)


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
