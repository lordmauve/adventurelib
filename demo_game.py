#from adventurelib import *
import adventurelib as a

a.Room.items = a.Bag()

current_room = starting_room = a.Room("""
You are in a dark room.
""")

valley = starting_room.north = a.Room("""
You are in a beautiful valley.
""")

magic_forest = valley.north = a.Room("""
You are in a enchanted forest where magic grows wildly.
""")

mallet = a.Item('rusty mallet', 'mallet')
valley.items = a.Bag({mallet,})

inventory = a.Bag()


@a.when('north', direction='north')
@a.when('south', direction='south')
@a.when('east', direction='east')
@a.when('west', direction='west')
def go(direction):
    global current_room
    room = current_room.exit(direction)
    if room:
        current_room = room
        a.say('You go %s.' % direction)
        look()
        if room == magic_forest:
            a.set_context('magic_aura')
        else:
            a.set_context('default')


@a.when('take ITEM')
def take(item):
    obj = current_room.items.take(item)
    if obj:
        a.say('You pick up the %s.' % obj)
        inventory.add(obj)
    else:
        a.say('There is no %s here.' % item)


@a.when('drop THING')
def drop(thing):
    obj = inventory.take(thing)
    if not obj:
        a.say('You do not have a %s.' % thing)
    else:
        a.say('You drop the %s.' % obj)
        current_room.items.add(obj)


@a.when('look')
def look():
    a.say(current_room)
    if current_room.items:
        for i in current_room.items:
            a.say('A %s is here.' % i)


@a.when('inventory')
def show_inventory():
    a.say('You have:')
    for thing in inventory:
        a.say(thing)

@a.when('cast', magic=None, context='magic_aura')
@a.when("cast MAGIC", context='magic_aura')
def cast(magic):
    if magic == None:
        a.say("Which magic you would like to spell?")
    elif magic == "fireball":
        a.say("you cast a flaming Fireball! Woooosh....")




look()
a.start()
