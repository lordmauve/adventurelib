Items
=====

Many games will allow players to pick up objects. Also perhaps some actions in
the game will cause players to receive objects, such as when given them by
a character.

To support this, adventurelib provides two classes that work together: ``Item``
and ``Bag``.

Defining an item
----------------

The ``Item`` class represents an item. The most important feature is that items
can be referred to by a number of names. This means that you can use a
descriptive name for the item in output that you show to the user, but allow
the user to refer to the item by a shorter name. In game, the interaction might
be as follows:

.. code-block:: none

    > look
    You are in a dirt-stained and litter-strewn alley behind
    the cinema.
    There is a broken broom here.

    > take broom
    You take the broom.

    > inventory
    You have:
    a broken broom

To represent an object like this in the game, construct an Item object::

    broom = Item('a broken broom', 'broom')

The first name you give is the default name for the item, which can be inserted
into strings::

    print('You sweep away cobwebs with %s.' % broom)

All the other names you give are *aliases* for the object. See :ref:`bags` for
how to select items based on what the player types.


Item Attributes
'''''''''''''''

Items can be assigned arbitrary attributes, which can be used to set properties
that your ``@when`` handlers can use for game logic.

Like :doc:`Room <rooms>`, you can assign class attributes on ``Item`` in order
to have a default that applies for all items that aren't set specifically.

For example::

    Item.colour = 'grey'

    mug = Item('mug')
    mug.colour = 'red'

    @when('look at ITEM')
    def look(item):
        obj = inventory.find(item)
        if not item:
            print("You do not have a %s." % item)
        else:
            print("It's a sort of %s-ish colour." % obj.colour)


Definite/indefinite articles
''''''''''''''''''''''''''''

In English, we refer to objects using indefinite articles "a", "an" and "some"
when we're talking about some object out of a class of objects, and "the"
when we're talking about a specific one or specific group.

If you're not writing in English, you may have similar grammatical
considerations - genders, word endings etc.

You can store these variations on the name as attributes on the item for use in
constructing grammatical sentences - here we use ``def_name``, but use whatever
attributes you like::

    apples = Item('some apples', 'apples', 'apple')
    apples.def_name = 'the apples'

    @when('take ITEM')
    def take_item(item):
        obj = current_room.items.take(item)
        if not obj:
            print('There is no %s here.' % item)
        else:
            print('You take %s.' % item.def_name)
            inventory.add(obj)

Making your sentences obey correct grammar in all case may not be easy - good
luck!


.. _bags:

Bags of items
-------------

A ``Bag`` is a collection of items. This does not need to be a literal "bag"
that the player is holding - it's a metaphor! You could treat a Room as being
bag of items. Or a group of :ref:`characters` could be held in a Bag.

The point of a Bag is to allow you to look up items by the names that players
have typed for them. For this purpose, they have these methods:

.. class:: Bag([items])

    Construct a bag from a list of items.

.. function:: name in bag

    Test if the name the player entered is an object in the bag.

.. function:: bag.find(name)

    Return the item corresponding to a name the player typed, but don't remove
    it from the bag.

    Returns ``None`` if the name didn't match any object in the bag.

.. function:: bag.take(name)

    Like ``find()``, find the item corresponding to the name the player typed,
    but then remove it from the bag and return it.

    Returns ``None`` if the name didn't match any object in the bag.

But Bags are also sets_ so they **inherit**  various methods for modifying and
iterating over items in the Bag, most usefully:

.. function:: bag.add(item)

    Put `item` into the bag if it isn't already in it.

.. function:: for item in bag

    Loop over the items in the bag.

.. _sets: https://docs.python.org/3/tutorial/datastructures.html#sets


So, you could model the player's inventory as a Bag::

    inventory = Bag()

    @when('eat ITEM')
    def eat(item):
        obj = inventory.take(item)
        if not obj:
            print('You do not have a %s.' % item)
        else:
            print('You eat the %s.' % obj)

    @when('inventory')
    def show_inventory():
        print('You have:')
        if not inventory:
            print('nothing')
            return
        for item in inventory:
            print('* %s' % item)


You could also model the items on the ground in a room as a bag::

    chapel.items = Bag([
        Item('a golden candlestick', 'candlestick'),
    ])

    @when('take ITEM')
    def take(item):
        obj = current_room.take(item)
        if not obj:
            print('There is no %s here.' % item)
        else:
            inventory.add(item)
            print('You take the %s.' % obj)


.. characters:

Characters
----------

You can treat non-player characters as items also.

You might want to store pronouns for the characters as attributes on the Item
object for use in constructing grammatical sentences::

    wizard = Item('a wizard')
    wizard.def_name = 'the wizard'
    wizard.subject_pronoun = 'he'
    wizard.object_pronoun = 'him'

To avoid repeating this for all male and all female characters, consider
creating a small subclass (of course, you could do this for any other group
of Items that share common attributes)::

    class MaleCharacter(Item):
        subject_pronoun = 'he'
        object_pronoun = 'him'

Then the above example can be written just as::

    wizard = MaleCharacter('a wizard')
    wizard.def_name = 'the wizard'
