from adventurelib import *

Room.items = Bag()

current_room = starting_room = Room("""
You are in a dark room.
""")

valley = starting_room.north = Room("""
You are in a beautiful valley.
""")

magic_forest = valley.north = Room("""
You are in a enchanted forest where magic grows wildly.
""")

mallet = Item('rusty mallet', 'mallet')
valley.items = Bag({mallet,})

inventory = Bag()


@when('north', direction='north')
@when('south', direction='south')
@when('east', direction='east')
@when('west', direction='west')
def go(direction):
    global current_room
    room = current_room.exit(direction)
    if room:
        current_room = room
        say(f'You go {direction}.')
        look()
        if room == magic_forest:
            set_context('magic_aura')
        else:
            set_context('default')


@when('take ITEM')
def take(item):
    obj = current_room.items.take(item)
    if obj:
        say(f'You pick up the {obj}.')
        inventory.add(obj)
    else:
        say(f'There is no {item} here.')


@when('drop THING')
def drop(thing):
    obj = inventory.take(thing)
    if not obj:
        say(f'You do not have a {thing}.')
    else:
        say(f'You drop the {obj}.')
        current_room.items.add(obj)


@when('look')
def look():
    say(current_room)
    if current_room.items:
        for item in current_room.items:
            say(f'A {item} is here.')


@when('inventory')
def show_inventory():
    say('You have:')
    for thing in inventory:
        say(thing)

@when('cast', context='magic_aura', magic=None)
@when('cast MAGIC', context='magic_aura')
def cast(magic):
    if magic == None:
        say("Which magic you would like to spell?")
    elif magic == 'fireball':
        say("A flaming Fireball shoots form your hands!")

look()
start()
