from adventurelib import *

current_room = starting_room = Room("""
You are in a dark room.
""")

starting_room.north = Room("""
You are in a beautiful valley.
""")


inventory = []


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


@when('take THING')
def take(thing):
    print('You take the %s.' % thing)
    inventory.append(thing)


@when('look')
def look():
    print(current_room)


@when('inventory')
def show_inventory():
    print('You have:')
    for thing in inventory:
        print(thing)


look()
start()
