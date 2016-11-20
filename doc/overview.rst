Overview
========

For teachers
------------

Adventurelib was created in response to requests from teachers for more
resources to help teach programming concepts. However, many text-based
adventure game frameworks impose preconceptions about how a text-based
adventure game should work. They often assume items and inventories, rooms and
items, non-player characters (known as NPCs) or more, and producing a game
using these "engines" becomes less a matter of programming and more of
producing the content.

Adventurelib deliberately provides only limited support for rooms, items and so
on, as I believe it is more instructive to learn how to create these structures
oneself.

Programming with adventurelib seems to bring up very different material to
programming graphical games. The challenges are partly in the domain of
computer science - how to model game state and produce business logic - and
partly in the domain of English - such as how to construct grammatical
sentences from fragments.

These topics must be tackled:

* Naming/identity - the difference between an object and a name that may be
  used to refer to that object.
* References - how an object may hold references to other objects, or
  to itself, and how traversal and manipulation of these references is the
  essence of producing game logic.
* Sets - Bags are sets of items, so membership in a set, set intersection,
  union and difference, are very useful.
* Parts of speech such as pronouns and articles; pluralisation; sentence case.
* Writing imaginative, engaging content.

I think of these as somewhat more difficult topics than those that come up in
writing graphical games, and I would therefore suggest teaching `Pygame Zero`_
or some other graphical games library earlier.

If you have feedback to offer having taught with adventurelib, please submit
this using `the Github issues page`__.

.. _`Pygame Zero`: https://pygame-zero.readthedocs.io/
.. __: https://github.com/lordmauve/adventurelib/issues

Non-English speakers
--------------------

Adventurelib was written by an English speaker. One might ask, "Can
adventurelib be used in other languages?"

We need to be careful to distinguish between the language of the API, and the
language of the games created using the API. The API will always be English,
and learners should be encouraged to embrace this; for better or worse, the
vast majority of programming languages, APIs, documentation, and global
conferences are in English.

But for writing games in other languages, some conventions employed by
adventurelib will be anglophone. Here are the issues I can think of:

* ``@when()`` matches on the basis of words - ie. splits on spaces and matches
  word-by-word. This may not work for most ideographic/logographic languages.
* The uppercase/lowercase of ``@when('take ITEM')`` will not be usable in
  languages without a concept of letter case.
* ``north``, ``south``, ``east`` and ``west`` are built into the :doc:`rooms`
  system, though it is possible to add your own directions. Strictly, these
  are identifiers, and could be used with non-English commands, but the results
  of functions like ``room.exits()`` would need translation before display
  to the user.
* No attention has been paid to RTL languages. For example the
  :ref:`say() <say>` function may be broken for RTL languages, and the ``@when``
  pattern matching is left-to-right greedy, so therefore appears ungreedy when
  considered right-to-left.

Under these limitations, adventurelib would be suitable for most European
languages, but perhaps less suitable for languages from the rest of the world.

I would welcome feedback about using adventurelib in other languages; as always
the correct place for this is `the Github issues page`__.

.. __: https://github.com/lordmauve/adventurelib/issues
