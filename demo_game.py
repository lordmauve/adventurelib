from adventurelib import *

Room.items = Bag()

current_room = starting_room = Room("""
You are in a dark room.
""")

valley = starting_room.north = Room("""
You are in a beautiful valley.
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
        print('You go %s.' % direction)
        look()


@when('take ITEM')
def take(item):
    obj = current_room.items.take(item)
    if obj:
        print('You pick up the %s.' % obj)
        inventory.add(obj)
    else:
        print('There is no %s here.' % item)


@when('drop THING')
def drop(thing):
    obj = inventory.take(thing)
    if not obj:
        print('You do not have a %s.' % thing)
    else:
        print('You drop the %s.' % obj)
        current_room.items.add(obj)


@when('look')
def look():
    print(current_room)
    if current_room.items:
        for i in current_room.items:
            print('A %s is here.' % i)


@when('inventory')
def show_inventory():
    print('You have:')
    for thing in inventory:
        print(thing)


look()
start()
