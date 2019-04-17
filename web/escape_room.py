from adventurelib import *

Room.items = Bag()
Room.add_direction('examine', 'reverse')
Room.add_direction('examine2', 'reverse2') 
print ( "Ah...what the heck. Where am I?")
print ( "It looks like I'm in  a bedroom of a cruise ship.")
print ( "Ugh, it seems I'm trap in here what should I do?")
print ( "I know I can type 'help' for help but what else can I do?...")

currentRoom = starting_room = Room("""
I'm in the middle of the room
""")

northside = starting_room.north = Room("""
You see a broken window with water gushing from it. "I'll be dead soon
if I just stand here."
To the left of the of the window you see bulletin board with a note.
A shelf with a photo in a picture frame and a sink.
""")

southside = starting_room.south = Room("""
Theres nothing but a wall there
""")


westside = starting_room.west = Room("""
You see a bunk bed with blue suitcase on it. By the bunk bed you see
a small stove with a teapot on top of it. 
"I should examine these things."
""")
eastside = starting_room.east = Room("""
You see a door.
"There's a weird keypad next to it."
""")

stovearea = westside.examine = Room("""
 There is a screwdriver on attached to the stove
""")

teaarea = westside.examine2 = Room("""
  In the teapot there is a blue key
""")


screwdriver = Item('screwdriver')
picture = Item('picture')
note = Item('note')
bluekey = Item('blue key')
suitcase = Item ('blue suitcase')
northside.items = Bag({picture, note})
stovearea.items = Bag({screwdriver})
westside.items = Bag({suitcase})
teaarea.items = Bag({bluekey})
inventory = Bag()


@when('north', direction='north')
@when('south', direction='south')
@when('east', direction='east')
@when('west', direction='west')
@when('examine stove', direction='examine')
@when('examine teapot', direction='examine2')
@when('exit stove area', direction='reverse')
@when('exit teapot area', direction='reverse2')


def go(direction):
    global currentRoom
    room = currentRoom.exit(direction)
    if room:
        currentRoom = room
        say('You go %s.' % direction)
        look()
        if room == northside:
            set_context('o')
        elif room == westside:
            set_context('o')
        elif room == southside:
            set_context('o')
        elif room == eastside:
            set_context('o')
        elif room == stovearea:
            set_context('o')
        elif room == teaarea:
            set_context('o')
        else:
            set_context('o')

@when('take ITEM')
def take(item):
    obj = currentRoom.items.take(item)
    if obj:
        say('You pick up the %s.' % obj)
        inventory.add(obj)
    
    else:
        say('There is no %s here.' % item)




@when('drop THING')
def drop(thing):
    obj = inventory.take(thing)
    if not obj:
        say('You do not have a %s.' % thing)
    else:
        say('You drop the %s.' % obj)
        currentRoom.items.add(obj)


@when('look')
def look():
    say(currentRoom)
    if currentRoom.items:
        for i in currentRoom.items:
            say('A %s is here.' % i)


@when('examine door')    
def door():
    global currentRoom
    room = currentRoom
    if room == eastside:
        print("It's locked")
    else:
        print("What door is there too look at")
   
    
   

@when('examine keypad')    
def keypad():
    global currentRoom
    room = currentRoom
    if room == eastside:
        print("It's says enter key. Guess it needs some kinda code")
    else:
        print("There is no keypad here")

clue = "01010100 01101000 01100101 00100000 01100011 01101111 01101101 01110000 01101100 01100101 01101101 01100101 01101110 01110100 01100001 01110010 01111001 00100000 01100011 01101111 01101100 01101111 01110010 00100000 01101111 01100110 00100000 01100111 01110010 01100101 01100101 01101110 00100000 01101001 01110011 00100000 01110100 01101000 01100101 00100000 01100011 01101111 01100100 01100101 00100000 01110100 01101111 00100000 01110100 01101000 01100101 00100000 01101011 01100101 01111001 01110000 01100001 01100100"


@when('examine ITEM')    
def examine(item):
    obj = inventory.find(item)
    if not obj:
        print(f'You do not have a {item}.')

    elif item == "picture with message":
        print("you see behind the picture is colored blue. There is text saying the color is the code")
    elif item == "screwdriver":
        print("I wonder if I can use this on something")
    elif item == "blue key":
        print("Hmmm what else in this room is blue...")
    elif item == "picture":
        print("It's a framed photo screwed shut. There's a family in the photo they look depressed")
    elif item == "note":
        print("The note says")
        print("An image leads you to the end.")
    elif item == "blue suitcase":
        print("The blue suit case needs is locked") 
    elif item == "second note":
        print("The note says")
        print(clue)
        print("what the heck does that mean?!")
        
@when('inventory')
def show_inventory():
    say('You have:')
    for thing in inventory:
        say(thing)



@when('use ITEM on blue suitcase')
def use(item):
    obj = inventory.find(item)
    if not obj:
        print(f'You do not have a {item}.')
    elif obj is not bluekey:
        print("That's not a blue key")
    else:
        print(f"You used the {obj} on the blue suitcase. Its still locked . What the heck. Looks like it needs a code too.")


@when('unscrew CONTAINER')
def unlock(container):
    obj = inventory.find(container)
    if not obj:
        say(f"You don't have a {container}.")
        return

    if obj is not picture:
        say("I don't know how to unscrew that.")
        return

    if not inventory.take('screwdriver'):
        say("You don't have the screwdriver.")
        return

    inventory.discard(obj)
    inventory.add(Item('picture with message'))
    say(f"You unscrewed the {obj.name} - somethings off about it I should examine it")


@when('enter NUM on CONTAINER')
def code(num, container):
    obj = inventory.find(container)
    if not obj:
       say(f"You don't have a {container}.")
    if num == "212215":
        print("Code matched!")
        inventory.discard(obj)
        inventory.add(Item('second note'))
        print(f"You opened the {obj.name} - There was note with code on it ")

    elif num == "blue":
        print("Invalid code please enter numbers")
    else:
        print("Invalid code try again")
    

@when('enter KEY')
def pad(key):
    global currentRoom
    room = currentRoom
    if room == eastside:
        if key == "1854":
           print("Code matched!")
           print("You have unlocked the door beside the keypad! Congratulations you you're free to go. Type 'exit out of door'")
           @when('exit out of door')
           def gameover():
               print("I'm free I'm getting the hell outta here!")
               print("You have exited the now flooded room")
               print("Game over")
               print("Type 'quit' to end the game")
        elif key == "red":
            print("Invalid code please enter numbers")
        elif key == "blue":
            print("Invalid code please enter numbers")
        else:
            print("Invalid code try again")
    else:
        print("I'm not near the keypad")


@when('jump', context='o', jump=None)
def yahoo(jump):
    if  jump == None:
        say("What the hell am I doing? Now isn't the time for jumping.")
  
look()
start()
