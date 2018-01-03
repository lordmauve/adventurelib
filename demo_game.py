"""Demonstration game"""
from adventurelib import *

Room.items = Bag()

starting_room = Room("""
You are in a dark room.
""")

valley = starting_room.north = Room("""
You are in a beautiful valley.
""")

mallet = Item('rusty mallet', 'mallet')
valley.items = Bag({mallet, })


@when('north', direction='north')
@when('south', direction='south')
@when('east', direction='east')
@when('west', direction='west')
def go(direction, game):
    room = game.current_room.exit(direction)
    if room:
        game.current_room = room
        game.say('You go %s.' % direction)
        look(game)


@when('take ITEM')
def take(item, game):
    obj = game.current_room.items.take(item)
    if obj:
        game.say('You pick up the %s.' % obj)
        game.inventory.add(obj)
    else:
        game.say('There is no %s here.' % item)


@when('drop THING')
def drop(thing, game):
    obj = game.inventory.take(thing)
    if not obj:
        game.say('You do not have a %s.' % thing)
    else:
        game.say('You drop the %s.' % obj)
        game.current_room.items.add(obj)


@when('look')
def look(game):
    game.say(game.current_room)
    if game.current_room.items:
        for i in game.current_room.items:
            game.say('A %s is here.' % i)


@when('inventory')
def show_inventory(game):
    game.say('You have:')
    for thing in game.inventory:
        game.say(thing)

        
def setup(game):
    """Set up the game world"""
    game.current_room = starting_room
    game.inventory = Bag()
    look(game)


start(setup)
